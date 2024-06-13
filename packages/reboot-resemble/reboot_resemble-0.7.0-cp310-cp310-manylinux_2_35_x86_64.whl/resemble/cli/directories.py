import argparse
import git
# mypy fails with 'error: Trying to read deleted variable "exc"' if we use
# 'git.exc'
import git.exc as gitexc
import os
from contextlib import contextmanager
from pathlib import Path
from resemble.cli.rc import ArgumentParser, SubcommandParser
from resemble.cli.terminal import fail, info


def add_working_directory_options(subcommand: SubcommandParser) -> None:
    subcommand.add_argument(
        '--working-directory',
        type=Path,
        help=(
            "directory in which to execute; defaults to the location of the "
            "`.rsmrc` file."
        ),
    )


def is_on_path(file):
    """Helper to check if a file is on the PATH."""
    for directory in os.environ['PATH'].split(os.pathsep):
        if os.path.exists(os.path.join(directory, file)):
            return True
    return False


def dot_rsm_directory() -> str:
    """Helper for determining the '.rsm' directory."""
    try:
        repo = git.Repo(search_parent_directories=True)
    except gitexc.InvalidGitRepositoryError:
        return os.path.join(os.getcwd(), '.rsm')
    else:
        return os.path.join(repo.working_dir, '.rsm')


def dot_rsm_dev_directory() -> str:
    """Helper for determining the '.rsm/dev' directory."""
    return os.path.join(dot_rsm_directory(), 'dev')


@contextmanager
def chdir(directory):
    """Context manager that changes into a directory and then changes back
    into the original directory before control is returned."""
    cwd = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cwd)


def compute_working_directory(
    args: argparse.Namespace,
    parser: ArgumentParser,
) -> Path:
    working_directory: Path
    if args.working_directory is not None:
        working_directory = Path(args.working_directory)
    elif parser.dot_rc is not None:
        working_directory = Path(parser.dot_rc).parent
    else:
        fail(
            "Either a `.rsmrc` file must be configured, or the "
            "`--working-directory` option must be specified."
        )

    return working_directory.absolute().resolve()


@contextmanager
def use_working_directory(
    args: argparse.Namespace,
    parser: ArgumentParser,
    verbose: bool = False,
):
    """Context manager that changes into an explicitly specified
    --working-directory, or else the location of the `.rsmrc` file.

    `add_working_directory_options` must have been called to register
    the option which is used here.
    """
    working_directory = compute_working_directory(args, parser)

    if verbose:
        if parser.dot_rc is not None:
            info(
                f"Using {parser.dot_rc_filename} "
                f"(from {os.path.relpath(parser.dot_rc, os.getcwd())}) "
                f"and working directory {os.path.relpath(working_directory, os.getcwd())}"
            )
        else:
            info(
                f"Using working directory {os.path.relpath(working_directory, os.getcwd())}"
            )

    with chdir(working_directory):
        yield
