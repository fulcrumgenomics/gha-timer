import collections
from dataclasses import dataclass
from dataclasses import replace
from pathlib import Path
from typing import Iterator

import yaml

from gha_timer.enums import Color
from gha_timer.enums import Outcome

_DEFAULT_TIMERRC: Path = Path("~/.timerrc")

_CHECKMARK: str = "✓"
_EX: str = "✕"


def _get_default_timerrc() -> Path:
    return _DEFAULT_TIMERRC


def _set_default_timerrc(path: Path) -> None:
    """Sets the default `.timerrc` location, useful for tests."""
    global _DEFAULT_TIMERRC
    _DEFAULT_TIMERRC = path  # noqa


@dataclass
class OutcomeConfig:
    """Container for configuration for the outcome of a single GitHub Actions step."""

    outcome: Outcome
    color: Color
    icon: str

    @property
    def value(self) -> str:
        """The value to print for this outcome."""
        return f"{self.color.value}{self.icon}{Color.END}"


_DEFAULT_OUTCOME_CONFIG_VALUES: list[OutcomeConfig] = [
    OutcomeConfig(
        outcome=Outcome.SUCCESS,
        color=Color.GREEN,
        icon=Color.BOLD.value + _CHECKMARK,
    ),
    OutcomeConfig(
        outcome=Outcome.FAILURE,
        color=Color.RED,
        icon=Color.BOLD.value + _EX,
    ),
    OutcomeConfig(
        outcome=Outcome.CANCELLED,
        color=Color.YELLOW,
        icon=Color.BOLD.value + _EX,
    ),
    OutcomeConfig(
        outcome=Outcome.SKIPPED,
        color=Color.GRAY,
        icon=Color.BOLD.value + _EX,
    ),
]


class Config(collections.abc.Mapping[Outcome, OutcomeConfig]):
    """The configuration object for `gha-timer`."""

    config: dict[Outcome, OutcomeConfig]
    timer_dir: Path

    def __init__(self, config: Path | None = None, timer_dir: Path | None = None) -> None:
        """
        Builds the config.

        First, a default set of values are populated.  Next, values
        from `~/.timerrc` overwrite the values (if found).  Finally,
        overwrite the values using the provided config file.

        Args:
            config: the path to the custom configuration file.
            timer_dir: the path to the timer directory.
        """
        self.configs = {c.outcome: c for c in _DEFAULT_OUTCOME_CONFIG_VALUES}
        self.timer_dir = Path(__file__).parent / ".timer" if timer_dir is None else timer_dir

        def parse_config(path: Path) -> None:
            with path.open("r") as reader:
                data = yaml.safe_load(reader)

            if "timer_dir" in data:
                self.timer_dir = Path(data["timer_dir"])
            for outcome in Outcome:
                if outcome.value not in data:
                    continue
                out = data[outcome.value]
                if "color" in out:
                    color = out["color"].upper()
                    color_config = next((c for c in Color if c.name == color), None)
                    if color_config is None:
                        raise ValueError("Color '{color}' not one of '{list(Color)}'")
                    self.configs[outcome] = replace(self.configs[outcome], color=color_config)
                if "icon" in out:
                    self.configs[outcome] = replace(self.configs[outcome], icon=out["icon"])

        timerrc = _DEFAULT_TIMERRC
        if timerrc.exists():
            parse_config(path=timerrc)
        if config is not None:
            parse_config(path=config)

    def __getitem__(self, key: Outcome) -> OutcomeConfig:
        """Gets the `OutcomeConfig` by name."""
        return self.configs[key]

    def __iter__(self) -> Iterator[Outcome]:
        """The `OutcomeConfig` values."""
        return iter(self.config)

    def __len__(self) -> int:
        """The number of `OutcomeConfig` values in the config."""
        return len(self.configs)
