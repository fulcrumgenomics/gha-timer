import abc
import argparse
import shutil
from argparse import HelpFormatter  # noqa see: https://bugs.python.org/issue41592
from argparse import _SubParsersAction  # noqa see: https://bugs.python.org/issue41592
from datetime import datetime
from pathlib import Path

from gha_timer.config import Config
from gha_timer.enums import Outcome

_TERMINAL_WIDTH: int = min(80, shutil.get_terminal_size().columns - 2)


class Command(abc.ABC):
    """Base class for all commands."""

    @classmethod
    def func(cls, args: argparse.Namespace) -> None:
        """The method to be invoked after parsing args."""
        config: Config = Config(config=args.config)
        cls.run(args, config=config)

    @classmethod
    @abc.abstractmethod
    def add_args(cls, subparsers: _SubParsersAction) -> None:
        """The method all subclasses implement to add arguments to their sub-parser."""
        ...

    @classmethod
    @abc.abstractmethod
    def run(cls, args: argparse.Namespace, config: Config) -> None:
        """The method all subclasses implement to run the command."""
        ...

    @staticmethod
    def _formatter_class(prog: str) -> argparse.HelpFormatter:
        return argparse.RawDescriptionHelpFormatter(prog, width=_TERMINAL_WIDTH)


class Start(Command):
    """The command for `gha-timer start`."""

    @classmethod
    def add_args(cls, subparsers: _SubParsersAction) -> None:
        """Adds this sub-command and its arguments to the given parser."""
        parser = subparsers.add_parser(
            name="start",
            prog="start",
            usage="%(prog)s [options]",
            formatter_class=lambda prog: cls._formatter_class(prog=prog),
            description="Starts the timer.",
        )
        parser.add_argument(
            "-n", "--name", help="Emit a start fold group with the given name", required=False
        )
        parser.set_defaults(func=Start.func)

    @classmethod
    def run(cls, args: argparse.Namespace, config: Config) -> None:
        """
        Runs the start command.

        Creates the directory that stores timestamps, if it doesn't already exist.  Then
        creates a new empty file with the timestamp value as the name.  If the `name` is defined
        in the arguments, prints the start of a fold group for GitHub actions to group logs.

        Args:
            args: the parsed args for this command.
            config: the config.
        """
        config.timer_dir.mkdir(parents=True, exist_ok=True)
        assert config.timer_dir.exists()
        timestamp: str = f"{datetime.now().timestamp()}"
        path: Path = config.timer_dir / timestamp
        if path.exists():
            raise ValueError(f"Path already exists: {path}")
        with path.open("w"):
            pass
        if args.name is not None:
            print(f"::group::{args.name}")


class Stop(Command):
    """The command for `gha-timer stop`."""

    @classmethod
    def add_args(cls, subparsers: _SubParsersAction) -> None:
        """Adds this sub-command and its arguments to the given parser."""
        parser = subparsers.add_parser(
            name="stop",
            prog="stop",
            usage="%(prog)s [options]",
            formatter_class=lambda prog: cls._formatter_class(prog=prog),
            description="",
        )
        parser.set_defaults(func=Stop.func)

    @classmethod
    def run(cls, _args: argparse.Namespace, config: Config) -> None:
        """
        Runs the stop command.

        Cleans up and deletes the directory that stores timestamps, if it exists.

        Args:
            _args: the parsed args for this command.
            config: the config.
        """
        if config.timer_dir.exists():
            for child in config.timer_dir.iterdir():
                if not child.is_file():
                    raise ValueError(f"Path is not a file: {child}")
                child.unlink()
            config.timer_dir.rmdir()


class Elapsed(Command):
    """The command for `gha-timer elapsed`."""

    @classmethod
    def add_args(cls, subparsers: argparse._SubParsersAction) -> None:
        """Adds this sub-command and its arguments to the given parser."""
        parser = subparsers.add_parser(
            name="elapsed",
            prog="elapsed",
            usage="%(prog)s [options]",
            formatter_class=lambda prog: cls._formatter_class(prog=prog),
            description="",
        )
        parser.add_argument(
            "-n", "--name", help="Emit an end fold group with the given name", required=False
        )
        parser.add_argument(
            "-d",
            "--digits",
            type=int,
            help="The number of decimals to use when rounding to seconds.",
            default=1,
        )
        parser.add_argument(
            "-o",
            "--outcome",
            type=Outcome,
            choices=list(Outcome),
            help="The current outcome.",
            required=True,
        )
        parser.set_defaults(func=Elapsed.func)

    @classmethod
    def run(cls, args: argparse.Namespace, config: Config) -> None:
        """
        Runs the elapsed command.

        Finds the latest timestamp, and prints the elapsed time along with
        colored code based on the provided outcome.  If `name` is defined
        in the arguments, prints the end of a fold group for GitHub actions
        to group logs.

        Args:
            args: the parsed args for this command.
            config: the config.
        """
        if not config.timer_dir.exists():
            raise ValueError(
                f"Time directory does not exist: {config.timer_dir}!"
                "\nAre you sure you ran `gha-timer start`?"
            )
        latest: float | None = None
        for child in config.timer_dir.iterdir():
            if not child.is_file():
                raise ValueError(f"Path is not a file: {child}")
            cur = float(child.name)
            if latest is None or cur > latest:
                latest = cur
        if latest is None:
            raise ValueError(
                f"Time directory is empty: {config.timer_dir}!"
                "\nAre you sure you ran `gha-timer start`?"
            )
        out_config = config[args.outcome]
        seconds = datetime.now().timestamp() - latest
        seconds = round(seconds, args.digits)
        value = f"{seconds}s".rjust(76)
        index = len(value) - 1
        while 0 < index:
            if value[index] == " ":
                break
            index -= 1
        value = f"{value[:index]}{out_config.value}{value[index:]}"
        if args.name is not None:
            print(f"::endgroup::{args.name}")
        print(value)
