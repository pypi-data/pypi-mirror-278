import asyncio
import os
import resemble.cli.terminal as terminal
import sys
from resemble.cli.cloud import cloud_down, cloud_up, register_cloud
from resemble.cli.dev import dev_expunge, dev_run, register_dev
from resemble.cli.init.init import init_run, register_init
from resemble.cli.protoc import protoc, register_protoc
from resemble.cli.rc import ArgumentParser
from resemble.cli.secret import register_secret, secret_delete, secret_write
from resemble.cli.subprocesses import Subprocesses
from typing import Optional


def create_parser(
    *,
    rc_file: Optional[str] = None,
    argv: Optional[list[str]] = None,
) -> ArgumentParser:
    parser = ArgumentParser(
        program='rsm',
        filename='.rsmrc',
        subcommands=[
            'dev run',
            'dev expunge',
            'protoc',
            'secret write',
            'secret delete',
            'cloud up',
            'cloud down',
            'init',
        ],
        rc_file=rc_file,
        argv=argv,
    )

    register_dev(parser)
    register_protoc(parser)
    register_secret(parser)
    register_cloud(parser)
    register_init(parser)

    return parser


async def rsm() -> int:
    # Sets up the terminal for logging.
    verbose, argv = ArgumentParser.strip_any_arg(sys.argv, '-v', '--verbose')
    terminal.init(verbose=verbose)

    # Install signal handlers to help ensure that Subprocesses get cleaned up.
    Subprocesses.install_terminal_app_signal_handlers()

    parser = create_parser(argv=argv)

    args, argv_after_dash_dash = parser.parse_args()

    if args.subcommand == 'dev run':
        return await dev_run(
            args,
            parser=parser,
            parser_factory=lambda argv: create_parser(argv=argv),
        )
    elif args.subcommand == 'dev expunge':
        await dev_expunge(args)
        return 0
    elif args.subcommand == 'protoc':
        return await protoc(args, argv_after_dash_dash, parser=parser)
    elif args.subcommand == 'secret write':
        await secret_write(args)
        return 0
    elif args.subcommand == 'secret delete':
        await secret_delete(args)
        return 0
    elif args.subcommand == 'cloud up':
        await cloud_up(args)
        return 0
    elif args.subcommand == 'cloud down':
        await cloud_down(args)
        return 0
    elif args.subcommand == 'init':
        await init_run(args)
        return 0

    raise NotImplementedError(
        f"Subcommand '{args.subcommand}' is not implemented"
    )


# This is a separate function (rather than just being in `__main__`) so that we
# can refer to it as a `script` in our `pyproject.rsm.toml` file.
def main():
    # We ignore _known_ warnings from
    # `multiprocessing.resource_tracker` that we know are harmless so
    # that we don't spam stdout. See #2793.
    #
    # We do this via an environment variable instead of using
    # `warnings.filterwarnings()` because we fork/exec multiple
    # processes and need to make sure all of those processes ignore
    # these warnings.
    warnings = os.environ.get('PYTHONWARNINGS')
    if warnings is not None:
        warnings += ','
    else:
        warnings = ''

    warnings += (
        'ignore:resource_tracker:UserWarning:multiprocessing.resource_tracker'
    )

    os.environ['PYTHONWARNINGS'] = warnings

    try:
        returncode = asyncio.run(rsm())
        sys.exit(returncode)
    except KeyboardInterrupt:
        # Don't print an exception and stack trace if the user does a
        # Ctrl-C.
        pass


if __name__ == '__main__':
    main()
