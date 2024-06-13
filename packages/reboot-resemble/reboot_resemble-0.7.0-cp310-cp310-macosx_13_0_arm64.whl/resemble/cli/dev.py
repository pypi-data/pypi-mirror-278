import aiofiles.os
import argparse
import asyncio
import functools
import grpc
import os
import random
import shutil
import sys
import termios
import tty
from backoff import Backoff
from colorama import Fore
from contextlib import asynccontextmanager
from grpc_health.v1 import health_pb2, health_pb2_grpc
from pathlib import Path
from resemble.aio.contexts import EffectValidation
# We import the whole `terminal` module (as opposed to the methods it contains)
# to allow us to mock these methods out in tests.
from resemble.cli import terminal
from resemble.cli.cloud import add_cloud_options
from resemble.cli.directories import (
    add_working_directory_options,
    dot_rsm_dev_directory,
    use_working_directory,
)
from resemble.cli.monkeys import monkeys, no_chaos_monkeys
from resemble.cli.protoc import protoc_direct
# We won't mock the classes in `rc`, so it's safe to import those directly.
from resemble.cli.rc import (
    ArgumentParser,
    ArgumentParserFactory,
    BaseTransformer,
    TransformerError,
)
from resemble.cli.subprocesses import Subprocesses
from resemble.cli.watch import watch
from resemble.settings import (
    DEFAULT_SECURE_PORT,
    DOCS_BASE_URL,
    ENVOY_PROXY_IMAGE,
    ENVVAR_RSM_CLOUD_API_KEY,
    ENVVAR_RSM_CLOUD_GATEWAY_ADDRESS,
    ENVVAR_RSM_CLOUD_GATEWAY_SECURE_CHANNEL,
    ENVVAR_RSM_DEV,
    ENVVAR_RSM_DEV_EFFECT_VALIDATION,
    ENVVAR_RSM_DEV_INSPECT_PORT,
    ENVVAR_RSM_DEV_LOCAL_ENVOY,
    ENVVAR_RSM_DEV_LOCAL_ENVOY_PORT,
    ENVVAR_RSM_DEV_NAME,
    ENVVAR_RSM_DEV_SECRETS_DIRECTORY,
    ENVVAR_RSM_DOT_RSM_DEV_DIRECTORY,
    SIDECAR_SUFFIX,
)
from typing import Any, Awaitable, Callable, Optional


class EnvTransformer(BaseTransformer):

    def transform(self, value: str):
        if '=' not in value:
            raise TransformerError(
                f"Invalid flag '--env={value}': must be in the form "
                "'--env=KEY=VALUE'"
            )
        return value.split('=', 1)


def register_dev(parser: ArgumentParser):
    _register_dev_run(parser)
    _register_dev_expunge(parser)


def _register_dev_run(parser: ArgumentParser):
    add_working_directory_options(parser.subcommand('dev run'))

    parser.subcommand('dev run').add_argument(
        '--name',
        type=str,
        help="name of application; state will be persisted using this name in "
        f"'{dot_rsm_dev_directory()}'",
    )

    parser.subcommand('dev run').add_argument(
        '--background-command',
        type=str,
        repeatable=True,
        help=
        'command(s) to execute in the background (multiple instances of this '
        'flag are supported)',
    )

    parser.subcommand('dev run').add_argument(
        '--local-envoy',
        type=bool,
        default=True,
        help='whether or not to bring up a local Envoy'
    )

    parser.subcommand('dev run').add_argument(
        '--local-envoy-port',
        type=int,
        help=f'port for local Envoy; defaults to {DEFAULT_LOCAL_ENVOY_PORT}',
    )

    parser.subcommand('dev run').add_argument(
        '--inspect-port',
        type=int,
        help=f'port for inspecting state; defaults to {DEFAULT_INSPECT_PORT}',
    )

    parser.subcommand('dev run').add_argument(
        '--python',
        type=bool,
        default=False,
        help="whether or not to launch the application by "
        "passing it as an argument to 'python'",
    )

    parser.subcommand('dev run').add_argument(
        '--watch',
        type=str,
        repeatable=True,
        help=
        'path to watch; multiple instances are allowed; globbing is supported',
    )

    parser.subcommand('dev run').add_argument(
        '--chaos',
        type=bool,
        default=True,
        help='whether or not to randomly induce failures',
    )

    parser.subcommand('dev run').add_argument(
        '--effect-validation',
        type=str,
        default="quiet",
        help=(
            'Whether to validate effects in development mode. '
            f'See {DOCS_BASE_URL}/docs/model/side_effects for more '
            'information.'
        ),
    )

    parser.subcommand('dev run').add_argument(
        "--env",
        type=str,
        repeatable=True,
        transformer=EnvTransformer(),
        help=
        "sets any specified environment variables before running the application; "
        "'ENV' should be of the form 'KEY=VALUE'",
    )

    parser.subcommand('dev run').add_argument(
        "--protoc-watch",
        type=bool,
        default=True,
        help="also run `rsm protoc --watch` in the background if true, taking "
        "'protoc' arguments from the '.rsmrc' file, which must be present"
    )

    parser.subcommand('dev run').add_argument(
        'application',
        type=str,  # TODO: consider argparse.FileType('e')
        help='path to application to execute',
    )

    parser.subcommand('dev run').add_argument(
        "--secrets-directory",
        type=Path,
        default=None,
        help=(
            "A directory to use to override the default source of Secrets. "
            "By default, Secrets are read from the Resemble Cloud API, and are written using "
            "`rsm secret write`."
        )
    )

    parser.subcommand('dev run').add_argument(
        "--terminate-after-health-check",
        type=bool,
        default=False,
        help=argparse.SUPPRESS,
    )

    # The `dev` command does not require an API key, since not everyone will
    # have access to secrets on day one.
    add_cloud_options(parser.subcommand('dev run'), api_key_required=False)


def _register_dev_expunge(parser: ArgumentParser):
    parser.subcommand('dev expunge').add_argument(
        '--name',
        type=str,
        help="name of the application to expunge; will remove this "
        f"application's state from '{dot_rsm_dev_directory()}'",
        required=True,
    )


async def _run_background_command(
    background_command: str,
    *,
    verbose: bool,
    print_as: Optional[str] = None,
    subprocesses: Subprocesses,
):
    # TODO: Align this with the global `terminal.is_verbose` boolean. We always
    # want error output in case of failure, but we might only want streamed output
    # if `is_verbose`.
    if verbose:
        terminal.info(
            f"Running background command '{print_as or background_command}'"
        )

    async with subprocesses.shell(background_command) as process:
        await process.wait()

        if process.returncode != 0:
            terminal.fail(
                f"Failed to run background command '{background_command}', "
                f"exited with {process.returncode}"
            )
        elif verbose:
            terminal.warn(
                f"Background command '{background_command}' exited without errors"
            )


@asynccontextmanager
async def _run(
    application,
    *,
    env: dict[str, str],
    launcher: Optional[str],
    subprocesses: Subprocesses,
    application_started_event: asyncio.Event,
):
    """Helper for running the application with an optional launcher."""
    args = [application] if launcher is None else [launcher, application]

    async with subprocesses.exec(*args, env=env) as process:
        application_started_event.set()
        yield process

    # As control is returned back to us, it means the application is no longer
    # running. We clear the event in preparation for the next run.
    application_started_event.clear()


async def _check_docker_status(subprocesses: Subprocesses):
    """Checks if Docker is running and can use the Envoy proxy image. Downloads
    that image if necessary."""
    async with subprocesses.exec(
        'docker',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    ) as process:
        stdout, _ = await process.communicate()
        if process.returncode != 0:
            terminal.fail(
                f"Could not use Docker:\n"
                "\n"
                f"{stdout.decode() if stdout is not None else '<no output>'}"
            )

    # The '-q' flag returns only the image ID, so if stdout is empty
    # then the image is not downloaded.
    async with subprocesses.exec(
        'docker',
        'images',
        '-q',
        ENVOY_PROXY_IMAGE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    ) as process:
        stdout, _ = await process.communicate()

        if process.returncode != 0:
            terminal.fail(
                f"Could not use Docker; 'docker images -q {ENVOY_PROXY_IMAGE}' failed with output:\n"
                "\n"
                f"{stdout.decode() if stdout is not None else '<no output>'}"
            )
        elif stdout is None or stdout == b'':
            # Empty output means the image is not downloaded because
            # 'docker' didn't find a match for the image name.
            terminal.info(
                f"Pulling Envoy proxy image '{ENVOY_PROXY_IMAGE}'..."
            )
            async with subprocesses.exec(
                'docker',
                'pull',
                ENVOY_PROXY_IMAGE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            ) as process:
                stdout, _ = await process.communicate()
                if process.returncode != 0:
                    terminal.fail(
                        f"Could not use Docker; 'docker pull {ENVOY_PROXY_IMAGE}' failed with output:\n"
                        "\n"
                        f"{stdout.decode() if stdout is not None else '<no output>'}"
                    )


async def _check_local_envoy_status(
    *,
    port: int,
    terminate_after_health_check: bool,
    application_started_event: asyncio.Event,
) -> None:
    """Checks if the application is up and running.
    Optionally exits as soon as the health check has passed.
    """
    # Wait until application is running with starting health check.
    await application_started_event.wait()

    # Using 'dev' subdomain of 'localhost.direct' as a workaround on a
    # gRPC bug that produces log message error about not matching the
    # entry (*.localhost.direct) in the certificate.  See
    # https://github.com/reboot-dev/respect/issues/2305
    #
    # We also want to print out 'dev.localhost.direct' so that our
    # users copy that to also avoid getting the log message error from
    # their gRPC or Resemble calls.
    address = f'dev.localhost.direct:{port}'

    backoff = Backoff(
        initial_backoff_seconds=0.01,
        max_backoff_seconds=1,
        backoff_multiplier=1.01,
    )
    was_application_serving = False
    while True:
        try:
            async with grpc.aio.secure_channel(
                address,
                grpc.ssl_channel_credentials(),
            ) as channel:
                response = await health_pb2_grpc.HealthStub(channel).Check(
                    health_pb2.HealthCheckRequest()
                )

                is_application_serving = (
                    response.status == health_pb2.HealthCheckResponse.SERVING
                )

        except grpc.aio.AioRpcError:
            is_application_serving = False

        if is_application_serving:
            backoff.clear()

        if (
            is_application_serving != was_application_serving and
            application_started_event.is_set()
        ):
            was_application_serving = is_application_serving

            if is_application_serving:
                terminal.info("Application is serving traffic ...\n")
                terminal.info(
                    f"  Your API is available at https://{address}\n"
                    "\n"
                    f"  You can use '{address}' as the `gateway` for a `Workflow`\n"
                    "\n"
                    "  You can inspect your state at http://localhost:9992\n",
                    color=Fore.WHITE,
                )
                if terminate_after_health_check is True:
                    return
            else:
                terminal.warn("Application stopped serving traffic\n")

        if is_application_serving:
            # Once an application is known to be serving traffic, we can take it
            # a little easier on the health checks. That saves us from spamming
            # Envoy logs, if nothing else.
            await asyncio.sleep(1)
        else:
            await backoff()


async def _cancel_all(tasks: list[asyncio.Task]) -> None:
    if not tasks:
        return

    for task in tasks:
        task.cancel()

    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)


async def _wait_for_first_completed(
    arg0: asyncio.Task[Any], *args: asyncio.Task[Any] | None
) -> set[asyncio.Task[Any]]:
    """Return the first of the given tasks to complete."""
    completed, _ = await asyncio.wait(
        [arg0, *(arg for arg in args if arg is not None)],
        return_when=asyncio.FIRST_COMPLETED
    )
    return completed


def protoc_parser_if_protoc_watch(
    dev_args,
    dev_parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
) -> Optional[ArgumentParser]:
    """Check whether we can run `rsm protoc --watch` without further
    user-specified arguments. That depends on whether the user has
    specified the necessary arguments in an `.rsmrc`.

    If so, returns the `rsm protoc` ArgumentParser to use.
    """
    if not dev_args.protoc_watch:
        return None
    if dev_parser.dot_rc is None:
        terminal.fail(
            "The '--protoc-watch' flag was specified, but no '.rsmrc' file was found. "
            "Add an '.rsmrc' file containing the necessary arguments to run 'rsm protoc' "
            "to use 'rsm dev run --protoc-watch'"
        )

    return parser_factory(['rsm', 'protoc'])


async def induce_chaos() -> Optional[int]:
    """Helper that allows inducing chaos via pressing keys 0-9."""

    def read(future: asyncio.Future[Optional[int]]):
        value = sys.stdin.read(1)
        if value == '0':
            # No delay, restart app immediately.
            future.set_result(None)
        elif value in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            # Delay restarting app by the 2 raised to the power of the
            # key pressed, e.g., if '3' was pressed we'll wait 8
            # seconds, if '4' is pressed we'll wait 16 seconds, if '9'
            # was pressed we'll wait 512 seconds (almost 10 minutes).
            future.set_result(2**int(value))

    future: asyncio.Future[Optional[int]] = asyncio.Future()

    # Add an async file descriptor reader to our running event
    # loop so that we know when a key has been pressed.
    loop = asyncio.get_running_loop()

    sys_stdin_fd = sys.stdin.fileno()

    loop.add_reader(sys_stdin_fd, read, future)

    try:
        return await future
    finally:
        loop.remove_reader(sys_stdin_fd)


DEFAULT_LOCAL_ENVOY_PORT: int = DEFAULT_SECURE_PORT
DEFAULT_INSPECT_PORT: int = 9992


async def dev_run(
    args,
    *,
    parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
) -> int:
    """Implementation of the 'dev run' subcommand."""

    if parser.dot_rc is not None:
        while True:
            async with watch([parser.dot_rc]) as rc_file_event_task:
                return_code = await _dev_run(
                    args,
                    parser=parser,
                    parser_factory=parser_factory,
                    rc_file_event_task=rc_file_event_task,
                )
            if return_code is not None:
                return return_code

            terminal.info(
                '\n'
                f'{parser.dot_rc_filename} modified; restarting ... '
                '\n'
            )
            args, _ = parser.parse_args()
    else:
        return_code = await _dev_run(
            args,
            parser=parser,
            parser_factory=parser_factory,
            rc_file_event_task=None,
        )
        assert return_code is not None, "Should not have requested re-running: no `rc_file_event_task` was set."
        return return_code


async def _dev_run(
    args,
    *,
    parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
    rc_file_event_task: Optional[asyncio.Task],
) -> Optional[int]:
    """Changes the working directory, and executes other preparation that needs
    cleanup when the dev loop exits.

    Has the same return semantics as `__dev_run`.
    """

    # Determine the working directory and move into it.
    with use_working_directory(args, parser, verbose=True):

        # If on Linux try and become a child subreaper so that we can
        # properly clean up all processes descendant from us!
        if sys.platform == 'linux':
            # The 'pyprctl' module is available on Linux only.
            import pyprctl
            try:
                pyprctl.set_child_subreaper(True)
            except:
                terminal.warn(
                    "Failed to become child subreaper, we'll do our "
                    "best to ensure all created processes are terminated"
                )
                pass

        # Prepare to run background tasks and to potentially adjust terminal
        # settings, both of which need cleanup on exit.
        background_command_tasks: list[asyncio.Task] = []

        # In some environments, e.g., CI, we don't have a tty, nor do
        # we need one as we're not expecting to read from stdin.
        # 'sys.stdin.isatty()' returns True even if it is called from a
        # '.sh' script, which blocks the execution of
        # 'rsm dev run --terminate-after-health-check'.
        use_tty = sys.stdin.isatty() and not args.terminate_after_health_check

        # Save the old tty settings so we can set them back to that
        # when exiting.
        sys_stdin_fd = sys.stdin.fileno()
        old_tty_settings = termios.tcgetattr(sys_stdin_fd) if use_tty else None
        try:
            # Set the tty to not echo key strokes back to the terminal
            # and also remove buffering so we can read a single key
            # stroke at a time (yes, `tty.setcbreak()` does all that!)
            if use_tty:
                tty.setcbreak(sys_stdin_fd)

            # Then execute the dev loop.
            return await __dev_run(
                args,
                parser=parser,
                parser_factory=parser_factory,
                rc_file_event_task=rc_file_event_task,
                background_command_tasks=background_command_tasks,
            )
        finally:
            await _cancel_all(background_command_tasks)
            # Reset the terminal to old settings, i.e., make key
            # strokes be echoed, etc.
            if old_tty_settings is not None:
                termios.tcsetattr(
                    sys_stdin_fd, termios.TCSADRAIN, old_tty_settings
                )


async def __dev_run(
    args,
    *,
    parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
    rc_file_event_task: Optional[asyncio.Task],
    background_command_tasks: list[asyncio.Task],
) -> Optional[int]:
    """Runs until:
      * the given `rc_file_event_task` triggers (returns None)
      * the health check passes, and `--terminate-on-health-check` is set (returns 0)
      * an exception is raised
    """
    # Use `Subprocesses` to manage all of our subprocesses for us.
    subprocesses = Subprocesses()

    application = os.path.abspath(args.application)
    application_started_event = asyncio.Event()

    # Run background tasks.
    for background_command in args.background_command or []:
        background_command_tasks.append(
            asyncio.create_task(
                _run_background_command(
                    background_command,
                    verbose=True,
                    subprocesses=subprocesses,
                )
            )
        )

    # If `--protoc-watch` is enabled, prepare to invoke protoc as part of our loop.
    proto_globs = []
    needs_proto_compile = False
    proto_compile: Optional[Callable[[], Awaitable[int]]] = None
    protoc_parser = protoc_parser_if_protoc_watch(args, parser, parser_factory)
    if protoc_parser:
        protoc_args, protoc_argv_after_dash_dash = protoc_parser.parse_args()
        proto_globs = [
            f"{pd}/**/*.proto" for pd in protoc_args.proto_directories
        ]
        needs_proto_compile = True
        proto_compile = functools.partial(
            protoc_direct,
            protoc_args,
            protoc_argv_after_dash_dash,
            protoc_parser,
        )

    # Set all the environment variables that
    # 'resemble.aio.Application' will be looking for.
    #
    # We make a copy of the environment so that we don't change
    # our environment variables which might cause an issue.
    env = os.environ.copy()

    env[ENVVAR_RSM_DEV] = 'true'

    if args.name is not None:
        env[ENVVAR_RSM_DEV_NAME] = args.name
        env[ENVVAR_RSM_DOT_RSM_DEV_DIRECTORY] = dot_rsm_dev_directory()

    if args.secrets_directory is not None:
        env[ENVVAR_RSM_DEV_SECRETS_DIRECTORY] = args.secrets_directory

    health_check_task: Optional[asyncio.Task] = None
    if args.local_envoy:
        # Check if Docker is running and can access the Envoy proxy image.
        # Fail otherwise.
        await _check_docker_status(subprocesses)
        env[ENVVAR_RSM_DEV_LOCAL_ENVOY] = 'true'

        health_check_task = asyncio.create_task(
            _check_local_envoy_status(
                port=args.local_envoy_port or DEFAULT_LOCAL_ENVOY_PORT,
                terminate_after_health_check=args.terminate_after_health_check
                or False,
                application_started_event=application_started_event,
            )
        )
        background_command_tasks.append(health_check_task)
    else:
        env[ENVVAR_RSM_DEV_LOCAL_ENVOY] = 'false'

    env[ENVVAR_RSM_DEV_LOCAL_ENVOY_PORT] = str(
        args.local_envoy_port or DEFAULT_LOCAL_ENVOY_PORT
    )

    try:
        # TODO: In Python 3.12, can use `choice in Enum`.
        EffectValidation[args.effect_validation.upper()]
    except KeyError:
        options = ', '.join(e.name.lower() for e in EffectValidation)
        terminal.fail(
            f"Unexpected value for --effect-validation: `{args.effect_validation}`. "
            f"Legal values are: {options}"
        )
    env[ENVVAR_RSM_DEV_EFFECT_VALIDATION] = args.effect_validation.upper()

    env[ENVVAR_RSM_DEV_INSPECT_PORT] = str(
        args.inspect_port or DEFAULT_INSPECT_PORT
    )

    if args.api_key is not None:
        env[ENVVAR_RSM_CLOUD_API_KEY] = args.api_key
    env[ENVVAR_RSM_CLOUD_GATEWAY_ADDRESS] = args.cloud_cell_address
    env[ENVVAR_RSM_CLOUD_GATEWAY_SECURE_CHANNEL
       ] = 'true' if args.cloud_secure_channel else 'false'

    # Also include all environment variables from '--env='.
    for (key, value) in args.env or []:
        env[key] = value

    if not args.chaos:
        # When running with '--terminate-after-health-check', we
        # would love to be consistent in the output we produce to be able to
        # test it.
        no_chaos_monkey = no_chaos_monkeys[
            0] if args.terminate_after_health_check is True else random.choice(
                no_chaos_monkeys
            )
        terminal.warn(
            '\n' + no_chaos_monkey + '\n'
            'You Have Disabled Chaos Monkey! (see --chaos)\n'
            '\n'
            'Only You (And Chaos Monkey) Can Prevent Bugs!'
            '\n'
        )

    # Bool used to steer the printing. i.e., are we starting or restarting
    # the application?
    first_start = True

    # Optional delay, used for inducing chaos with a delay.
    delay: Optional[int] = None

    while True:
        if delay is not None:
            await asyncio.sleep(delay)
            delay = None

        # Determine the appropriate verb.
        start_verb = "Starting" if first_start else "Restarting"
        if args.name is None:
            terminal.warn(
                f'{start_verb} an ANONYMOUS application; to reuse state '
                'across application restarts use --name'
                '\n'
            )
        else:
            terminal.info(
                f'{start_verb} application with name "{args.name}"...'
                '\n'
            )
        first_start = False

        # It's possible that the application may get deleted
        # and then (re)created by a build system so rather
        # than fail if we can't find it we'll retry but print
        # out a warning every ~10 seconds (which corresponds
        # to ~20 retries since we sleep for 0.5 seconds
        # between each retry).
        retries = 0
        while not await aiofiles.os.path.isfile(application):
            if retries != 0 and retries % 20 == 0:
                terminal.warn(
                    f"Missing application at '{application}' "
                    "(is it being rebuilt?)"
                )
            retries += 1
            await asyncio.sleep(0.5)

        # Expect an executable if we haven't been asked to use
        # `python`.
        if (
            args.python is None and
            not await aiofiles.os.access(application, os.X_OK)
        ):
            terminal.fail(
                f"Expecting executable application at '{application}'. "
                "Specify '--python' if you want to run a Python application."
            )

        async with watch(proto_globs) as protos_event_task:

            if needs_proto_compile:
                assert proto_compile is not None
                if await proto_compile() != 0:
                    # Failed to compile: wait for a relevant input to have changed.
                    terminal.warn(
                        '\n'
                        'Protoc compilation failed '
                        '... waiting for modification'
                        '\n'
                    )
                    completed = await _wait_for_first_completed(
                        protos_event_task,
                        rc_file_event_task,
                    )
                    if rc_file_event_task in completed:
                        return None
                    terminal.info(
                        '\n'
                        'Application modified; restarting ... '
                        '\n'
                    )
                    continue

                # Else, successfully compiled.
                needs_proto_compile = False

            async with watch(
                [application] + (args.watch or [])
            ) as sources_event_task:

                # TODO(benh): catch just failure to create the subprocess
                # so that we can either try again or just listen for a
                # modified event and then try again.
                async with _run(
                    application,
                    env=env,
                    launcher=sys.executable
                    if args.python is not None else None,
                    subprocesses=subprocesses,
                    application_started_event=application_started_event,
                ) as process:
                    process_wait_task = asyncio.create_task(process.wait())

                    induce_chaos_task = asyncio.create_task(induce_chaos())

                    chaos_task: Optional[asyncio.Task] = None
                    if args.chaos:
                        chaos_task = asyncio.create_task(asyncio.sleep(600))

                    completed = await _wait_for_first_completed(
                        sources_event_task,
                        protos_event_task,
                        process_wait_task,
                        induce_chaos_task,
                        health_check_task,
                        chaos_task,
                        rc_file_event_task,
                    )

                    # Cancel tasks regardless of what completed
                    # first as we won't ever wait on them.
                    induce_chaos_task.cancel()
                    if chaos_task:
                        chaos_task.cancel()

                    if rc_file_event_task in completed:
                        return None
                    elif process_wait_task in completed:
                        terminal.warn(
                            '\n'
                            'Application exited unexpectedly '
                            f'(with code {process_wait_task.result()}) '
                            '... waiting for modification'
                            '\n'
                        )
                        # NOTE: we'll wait for a file system event
                        # below to signal a modification!
                    elif (
                        (induce_chaos_task in completed) or
                        (args.chaos and chaos_task in completed)
                    ):
                        terminal.warn(
                            '\n'
                            'Chaos Monkey Is Restarting Your Application'
                            '\n' + random.choice(monkeys) + '\n'
                            '... disable via --no-chaos if you must'
                            '\n'
                            '\n'
                        )
                        if induce_chaos_task in completed:
                            delay = await induce_chaos_task
                        continue
                    elif health_check_task in completed:
                        # The health check passed, and we were asked to exit
                        # after a health check (otherwise the health check task
                        # continues to run more health checks).
                        return 0

                    # Wait for a source-change task to fire.
                    # TODO: If:
                    # 1. user sources change, causing this wait to return
                    # 2. proto files then additionally change before we
                    #    re-enter the proto watch above
                    # ... then we would miss that event.
                    # See https://github.com/reboot-dev/respect/issues/2940
                    completed = await _wait_for_first_completed(
                        sources_event_task,
                        protos_event_task,
                        rc_file_event_task,
                    )
                    if rc_file_event_task in completed:
                        return None
                    if protos_event_task in completed:
                        needs_proto_compile = True

                    terminal.info(
                        '\n'
                        'Application modified; restarting ... '
                        '\n'
                    )


async def dev_expunge(args) -> None:
    """
    Delete the sidecar state directory for the application with the given name.
    """
    application_directory = (
        Path(dot_rsm_dev_directory()) / (args.name + SIDECAR_SUFFIX)
    )
    try:
        shutil.rmtree(application_directory)
        terminal.info(f"Application '{args.name}' has been expunged")
    except FileNotFoundError:
        terminal.fail(
            f"Could not find application with name '{args.name}' (looked in "
            f"'{application_directory}'); did not expunge"
        )
