import argparse
from pathlib import Path

from gha_timer.commands import Command
from gha_timer.commands import Elapsed
from gha_timer.commands import Start
from gha_timer.commands import Stop


def _path_type(arg_value: str) -> Path:
    try:
        return Path(arg_value)
    except TypeError as e:
        raise argparse.ArgumentTypeError(f"Not a path: '{arg_value}'") from e


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """
    Parse the command line arguments.

    Returns:
        the parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="gha-timer",
        usage="%(prog)s [options]",
        formatter_class=lambda prog: Command._formatter_class(prog=prog),
        description="""
           Time and group logs for GitHub action.

           1. Start the timer with `timer start`.
           2. Print the elapsed time with `timer elapsed`.
           3. Stop the timer with `timer stop`.

           Configuration will be loaded from the `.timerrc`
           file. Override values with `--config`.
           """,
    )
    parser.add_argument(
        "-c", "--config", help="The path to the configuration file", type=_path_type
    )

    subparsers = parser.add_subparsers(
        title="commands", description="valid commands", help="additional help", required=True
    )

    for command in [Start, Stop, Elapsed]:
        command.add_args(subparsers)

    namespace: argparse.Namespace = parser.parse_args(args=args)

    return namespace


def run() -> None:
    """The main entry point for gha-timer."""
    # parse the args
    args = parse_args()

    # now actually do something
    args.func(args)
