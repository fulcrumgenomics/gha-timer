import enum


@enum.unique
class Color(enum.StrEnum):
    """The ANSI escape codes for colors."""

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    WHITE = "\033[37m\033[97m"
    GRAY = "\033[38;5;244m"
    BG_GREY = "\033[48;5;235m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    END = "\033[0m"


@enum.unique
class Outcome(enum.StrEnum):
    """The GitHub Actions step outcome (`steps.<step_id>.outcome`)."""

    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"
