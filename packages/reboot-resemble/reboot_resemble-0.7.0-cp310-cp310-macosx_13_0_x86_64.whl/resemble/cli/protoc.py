import aiofiles.os
import argparse
import asyncio
import glob
import os
from collections import defaultdict
from grpc_tools import protoc as grpc_tools_protoc
from importlib import resources
from pathlib import Path
from resemble.cli import terminal
from resemble.cli.directories import (
    add_working_directory_options,
    chdir,
    compute_working_directory,
    dot_rsm_directory,
    is_on_path,
    use_working_directory,
)
from resemble.cli.rc import ArgumentParser
from resemble.cli.subprocesses import Subprocesses
from resemble.cli.terminal import error, fail, info
from resemble.settings import DOCS_BASE_URL

RESEMBLE_SPECIFIC_PLUGINS = ['python', 'react', 'nodejs']
RESEMBLE_EXPERIMENTAL_PLUGINS = ['nodejs']

# Dictionary from out path to list of sufficient plugins (it's a list
# since in some cases more than one plugin may be sufficient).
PLUGINS_SUFFICIENT_FOR_EXPLICIT_OUT_FLAGS = {
    '--python_out': ['python'],
    '--grpc_python_out': ['python'],
    '--resemble_python_out': ['python'],
    '--mypy_out': ['python'],
    '--es_out': ['react', 'nodejs'],
    '--resemble_react_out': ['react'],
    '--resemble_nodejs_out': ['nodejs'],
}

# Specify all possible flags for supported languages, in a priority order.
OUTPUT_FLAGS_BY_LANGUAGE = {
    "python":
        [
            "--resemble_python_out",
            "--python_out",
            "--grpc_python_out",
            "--mypy_out",
        ],
    "react": [
        "--resemble_react_out",
        "--es_out",
    ],
    "nodejs": [
        "--resemble_nodejs_out",
        "--es_out",
    ],
}

PROTOC_PLUGIN_BY_LANGUAGE = {
    "python": "protoc-gen-resemble_python",
    "react": "protoc-gen-resemble_react",
    "nodejs": "protoc-gen-resemble_nodejs",
}

BOILERPLATE_SUPPORTED_LANGUAGES = ['python']

BOILERPLATE_PLUGIN_BY_LANGUAGE = {
    "python": "protoc-gen-resemble_python_boilerplate",
}

OUTPUT_BOILERPLATE_FLAG_BY_LANGUAGE = {
    "python": "--resemble_python_boilerplate_out",
}


def register_protoc(parser: ArgumentParser):
    add_working_directory_options(parser.subcommand('protoc'))

    parser.subcommand('protoc').add_argument(
        '--python',
        type=str,
        default=None,
        help="output directory in which `protoc` will generate Python files"
    )

    parser.subcommand('protoc').add_argument(
        '--react',
        type=str,
        default=None,
        help="output directory in which `protoc` will generate React files"
    )

    parser.subcommand('protoc').add_argument(
        '--nodejs',
        type=str,
        default=None,
        # Don't output the '--nodejs' flag in the help message, as we don't
        # officially support it yet.
        help=argparse.SUPPRESS,
    )

    parser.subcommand('protoc').add_argument(
        '--boilerplate',
        type=str,
        help="generate a fill-in-the-blanks boilerplate at the specified path.",
    )

    parser.subcommand('protoc').add_argument(
        'proto_directories',
        type=str,
        help="proto directory(s) which will (1) be included as import paths "
        "and (2) be recursively searched for '.proto' files to compile",
        repeatable=True,
        required=True,
    )


async def _check_or_install_npm_packages(
    subprocesses: Subprocesses, package_names: list[str]
):
    # Check and see if we've already installed a package and if not install it.
    # We redirect stdout/stderr to a pipe and only print it out if any of our
    # commands fail.
    for package_name in package_names:
        async with subprocesses.shell(
            f'npm list {package_name}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        ) as process:
            stdout, _ = await process.communicate()

            if process.returncode != 0:
                info(f"Installing '{package_name}' ...")

                async with subprocesses.shell(
                    f'npm install {package_name}',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                ) as process:
                    stdout, _ = await process.communicate()

                    if process.returncode != 0:
                        fail(
                            "\n"
                            f"Failed to install '{package_name}':\n"
                            f"{stdout.decode() if stdout is not None else '<no output>'}"
                            "\n"
                            "Please report this bug to the maintainers."
                        )


async def ensure_protoc_gen_es(subprocesses: Subprocesses):
    """Helper to ensure we have 'protoc-gen-es' and its dependencies
    installed.

    We install these in the '.rsm' directory, by placing an empty
    'package.json' file and then running 'npm install' as
    necessary. This approach makes it so that we don't have to bundle
    'protoc-gen-es' as part of our pip package.
    """
    if not is_on_path('npm'):
        fail(
            "We require 'npm' and couldn't find it on your PATH. "
            "Is it installed?"
        )

    if not is_on_path('node'):
        fail(
            "We require 'node' and couldn't find it on your PATH. "
            "Is it installed?"
        )

    await aiofiles.os.makedirs(dot_rsm_directory(), exist_ok=True)

    with chdir(dot_rsm_directory()):
        if (
            not await aiofiles.os.path.isfile('package.json') or
            await aiofiles.os.path.getsize('package.json') == 0
        ):
            with open('package.json', 'w') as file:
                file.write('{ "type": "module" }')

        await _check_or_install_npm_packages(
            subprocesses,
            ['@bufbuild/protobuf', '@bufbuild/protoc-gen-es'],
        )


async def _transpile_typescript(
    subprocesses: Subprocesses,
    output_directory: str,
    protos_by_directory: defaultdict[str, list[str]],
):
    """Convert the generated `*_rsm*.ts` files into `.js` and
    `.d.ts` files, so that both TypeScript and JavaScript users
    can use them. We do this by running `tsc` on those `.ts`
    files, and then removing them.
    We run `tsc` from the '.rsm' directory; that's where we
    have our `node_modules` with all the tools we need.

    'protos_by_directory' is a dictionary where key is a proto directory and
    values are proto files in that directory, we need that since we do 'glob' in
    a user specified path and we need to know which proto files are in which
    directory."""

    with chdir(dot_rsm_directory()):
        await _check_or_install_npm_packages(
            subprocesses,
            [
                '@reboot-dev/resemble',
                '@reboot-dev/resemble-react',
                'typescript@4.9.5',
            ],
        )

        RSM_OUTPUT_SYMLINK = 'resemble_protoc_output_directory_symlink'

        # We need to invoke `tsc` from the '.rsm' directory, where we
        # have its dependencies installed. We must create
        # a symlink to the protoc 'output_directory' inside `.rsm`, since tsc
        # cannot compile files outside the current working directory.
        await aiofiles.os.symlink(output_directory, RSM_OUTPUT_SYMLINK)

        # Wrap the code in a try/finally block to make sure we
        # remove the symlink even if something goes wrong.
        try:
            # Not all `.proto` files contain 'resemble' services and we only
            # generate `*_rsm*.ts` for the files that do. Thus, we create a
            # list of possible files that we'll need to transpile.
            maybe_generated_files: list[str] = []
            for directory, protos in protos_by_directory.items():
                for proto in protos:
                    proto = os.path.join(
                        RSM_OUTPUT_SYMLINK,
                        proto.removeprefix(directory),
                    )

                    # NOTE: we currently only transpile nodejs code.
                    maybe_generated_files.append(
                        proto.replace('.proto', '_rsm.ts')
                    )

            for file in maybe_generated_files:
                if not await aiofiles.os.path.isfile(file):
                    continue

                assert file.endswith('_rsm.ts')

                command = (
                    'npx tsc '
                    '--module "esnext" '
                    '--moduleResolution "node" '
                    '--target "es2015" '
                    '--declaration '
                    f'{file}'
                )

                async with subprocesses.shell(command) as process:
                    stdout, _ = await process.communicate()
                    if process.returncode != 0:
                        fail(
                            "\n"
                            f"Failed to run '{command}':\n"
                            f"{stdout.decode() if stdout is not None else '<no output>'}"
                            "\n"
                            "Please report this bug to the maintainers."
                        )

                # The produced `.d.ts` and `.js` files together provide
                # everything both JavaScript and TypeScript callers need,
                # making the original `.ts` file redundant. Remove it, to avoid
                # any confusion.
                await aiofiles.os.remove(file)

        finally:
            await aiofiles.os.unlink(RSM_OUTPUT_SYMLINK)


LanguageName = str
OutputPath = str
FlagName = str


async def get_output_paths_and_languages(
    args,
) -> dict[LanguageName, OutputPath]:
    """Get the output paths for each language that we are generating code for.
    We'll return a dictionary where the key is the language and the value is
    an output path.
    """

    output_by_language: dict[LanguageName, OutputPath] = {}

    if args.python is not None:
        output_by_language['python'] = args.python
    if args.react is not None:
        output_by_language['react'] = args.react
    if args.nodejs is not None:
        output_by_language['nodejs'] = args.nodejs

    return output_by_language


async def protoc(
    args,
    argv_after_dash_dash: list[str],
    parser: ArgumentParser,
) -> int:
    """Invokes `protoc` with the arguments passed to 'rsm protoc'."""
    # Determine the working directory and move into it.
    with use_working_directory(args, parser):
        return await protoc_direct(args, argv_after_dash_dash, parser)


async def protoc_direct(
    args,
    argv_after_dash_dash: list[str],
    parser: ArgumentParser,
) -> int:
    """Invokes `protoc` with the arguments passed to 'rsm protoc', while asserting that
    the working directory is already correct."""

    if Path(os.getcwd()).resolve() != compute_working_directory(args, parser):
        # TODO: This should really be a global flag somehow.
        fail(
            "The `--working-directory` for `protoc` must match the "
            "`--working-directory` for the current command."
        )

    # Use `Subprocesses` to manage all of our subprocesses for us.
    subprocesses = Subprocesses()

    # Fill in `protoc` args based on our args.
    protoc_args: list[str] = ["grpc_tool.protoc"]

    # We want to find the Python `site-packages`/`dist-packages` directories
    # that contain a 'resemble/v1alpha1' directory, which is where we'll
    # find our protos. We can look for the 'resemble' folder via the
    # `resources` module; the resulting path is a `MultiplexedPath`, since
    # there may be multiple. Such a path doesn't contain a `parent`
    # attribute, since there isn't one answer. Instead we use `iterdir()` to
    # get all of the children of all 'resemble' folders, and then
    # deduplicate the parents-of-the-parents-of-those-children (via the
    # `set`), which gives us the `resemble` folders' parents' paths.
    resemble_parent_paths: set[str] = set()
    for resource in resources.files('resemble').iterdir():
        with resources.as_file(resource) as path:
            resemble_parent_paths.add(str(path.parent.parent))

    if len(resemble_parent_paths) == 0:
        raise FileNotFoundError(
            "Failed to find 'resemble' resource path. "
            "Please report this bug to the maintainers."
        )

    # Now add these to '--proto_path', so that users don't need to provide
    # their own Resemble protos.
    for resemble_parent_path in resemble_parent_paths:
        protoc_args.append(f"--proto_path={resemble_parent_path}")

    # User protos may rely on `google.protobuf.*` protos. We
    # conveniently have those files packaged in our Python
    # package; make them available to users, so that users don't
    # need to provide them.
    protoc_args.append(
        f"--proto_path={resources.files('grpc_tools').joinpath('_proto')}"
    )

    for flag, languages in PLUGINS_SUFFICIENT_FOR_EXPLICIT_OUT_FLAGS.items():
        if any(arg.startswith(flag) for arg in argv_after_dash_dash):
            suggestions = ' or '.join(
                [
                    f"'--{language}'" for language in languages
                    if language not in RESEMBLE_EXPERIMENTAL_PLUGINS
                ]
            )
            fail(
                f"{flag} was specified after '--'. Instead, use {suggestions} "
                "to specify the output directory."
            )

    output_path_by_language = await get_output_paths_and_languages(args)

    if len(output_path_by_language) == 0:
        official_supported_plugins = [
            plugin for plugin in RESEMBLE_SPECIFIC_PLUGINS
            if plugin not in RESEMBLE_EXPERIMENTAL_PLUGINS
        ]

        fail(
            f"At least one of '{', '.join(official_supported_plugins)}' must be specified."
        )

    languages_to_generate = list(output_path_by_language.keys())

    protoc_plugin_out_flags: dict[FlagName, OutputPath] = {}

    skip_next: bool = False
    for i, arg in enumerate(argv_after_dash_dash):
        if skip_next is True:
            skip_next = False
            continue
        if '=' in arg:
            protoc_plugin_out_flags[arg.split('=')[0]] = arg.split('=')[1]
        else:
            if len(argv_after_dash_dash) - 1 == i:
                fail(f'Missing value for {arg}, try {arg}=VALUE')
            protoc_plugin_out_flags[arg] = argv_after_dash_dash[i + 1]
            skip_next = True

    for language in languages_to_generate:
        if language in BOILERPLATE_SUPPORTED_LANGUAGES and args.boilerplate is not None:
            if await aiofiles.os.path.isfile(args.boilerplate):
                fail(
                    f"Expecting a directory for '--boilerplate={args.boilerplate}'"
                )
            if not await aiofiles.os.path.isdir(args.boilerplate):
                await aiofiles.os.makedirs(
                    args.boilerplate,
                )
            if not is_on_path(BOILERPLATE_PLUGIN_BY_LANGUAGE[language]):
                raise FileNotFoundError(
                    f"Failed to find '{BOILERPLATE_PLUGIN_BY_LANGUAGE[language]}'. "
                    "Please report this bug to the maintainers."
                )

            protoc_args.append(
                f"{OUTPUT_BOILERPLATE_FLAG_BY_LANGUAGE[language]}={args.boilerplate}"
            )

        if not is_on_path(PROTOC_PLUGIN_BY_LANGUAGE[language]):
            raise FileNotFoundError(
                f"Failed to find '{PROTOC_PLUGIN_BY_LANGUAGE[language]}'. "
                "Please report this bug to the maintainers."
            )

        # If the directory doesn't exist create it (we checked in
        # `_check_explicitly_specified_out_paths()` that none of
        # the specified out paths were files).
        #
        # This is a _much_ better experience than the error message
        # that `protoc` gives if the directory does not exist.
        if not await aiofiles.os.path.isdir(output_path_by_language[language]):
            await aiofiles.os.makedirs(
                output_path_by_language[language],
                exist_ok=True,
            )

        # This is safe even when multiple languages share one protoc plugin,
        # because in those cases their output path is guaranteed to be the
        # same.
        for flag_name in OUTPUT_FLAGS_BY_LANGUAGE[language]:
            protoc_plugin_out_flags[flag_name] = output_path_by_language[
                language]

    for flag_name, out in protoc_plugin_out_flags.items():
        protoc_args.append(f"{flag_name}={out}")

    if args.react is not None or args.nodejs is not None:
        await ensure_protoc_gen_es(subprocesses)

        protoc_args.append(
            f"--plugin={os.path.join(dot_rsm_directory(), 'node_modules', '.bin', 'protoc-gen-es')}"
        )

    # The `mypy` plugin is by default being a little loud for our liking.
    # This can be suppressed by passing the parameter `quite` to the plugin.
    # https://github.com/nipunn1313/mypy-protobuf/blob/7f4a558c00faf8fac0cd6d7a6d1332d1643cc08c/mypy_protobuf/main.py#L1082
    # Check if we are going to invoke `mypy` and if so, make sure we are
    # also passing `quite`,
    using_mypy = any(['--mypy' in arg for arg in protoc_args])
    if using_mypy:
        quite_arg = '--mypy_opt=quiet'
        if quite_arg not in protoc_args:
            protoc_args.append(quite_arg)

    # Grab all of the positional '.proto' arguments.
    proto_directories: list[str] = args.proto_directories or []

    protos_by_directory: defaultdict[str, list[str]] = defaultdict(list)

    for proto_directory in proto_directories:
        # Since we rely on a 'proto_directory' during the 'tsc' processing, we
        # need the same schema of 'proto_directory' to be able to compute the
        # generated file names, but users can provide it in different forms,
        # e.g. 'directory', 'directory/'.
        if not proto_directory.endswith(os.path.sep):
            proto_directory += os.path.sep
        # Expand any directories to be short-form for 'directory/**/*.proto'.
        if not await aiofiles.os.path.isdir(proto_directory):
            fail(f"Failed to find directory '{proto_directory}'")
        else:
            # Also add any directories given to us as part of the import path.
            protoc_args.append(f'--proto_path={proto_directory}')
            found_protos = False
            for file in glob.iglob(
                os.path.join(proto_directory, '**', '*.proto'),
                recursive=True,
            ):
                _, extension = os.path.splitext(file)
                if extension == '.proto':
                    found_protos = True
                    protos_by_directory[proto_directory].append(file)

            if not found_protos:
                fail(f"'{proto_directory}' did not match any '.proto' files")

    for protos in protos_by_directory.values():
        for file in protos:
            if os.stat(file).st_size == 0:
                error(
                    f"'{file}' is empty. "
                    f"See {DOCS_BASE_URL}/docs/model/overview for "
                    "more information on filling out your proto file."
                )
                # Return an error code here to not break the 'rsm dev' loop.
                return 1
        protoc_args.extend(protos)

    while True:
        if not terminal.is_verbose():
            info(
                'Running `protoc ...` (use --verbose to see full command)'
                '\n'
            )
        else:
            terminal.verbose('protoc')
            for arg in protoc_args[1:]:
                terminal.verbose(f'  {arg}')

        returncode = grpc_tools_protoc.main(protoc_args)

        if returncode == 0 and args.react is not None:
            await _transpile_typescript(
                subprocesses,
                os.path.abspath(output_path_by_language['react']),
                protos_by_directory,
            )

        # Print if we failed.
        if returncode != 0:
            error(f'`protoc` failed with return code {returncode}'
                  '\n')

        return returncode
