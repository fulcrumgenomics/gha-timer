from pathlib import Path

from gha_timer.config import _CHECKMARK
from gha_timer.config import _EX
from gha_timer.config import Config
from gha_timer.config import _get_default_timerrc
from gha_timer.config import _set_default_timerrc
from gha_timer.enums import Color
from gha_timer.enums import Outcome


def _assert_config(config: Config, outcome: Outcome, color: Color, icon: str) -> None:
    assert config[outcome].color == color
    if icon == _CHECKMARK or icon == _EX:
        assert config[outcome].icon == "\x1b[1m" + icon
    else:
        assert config[outcome].icon == icon


def test_config_default() -> None:
    config = Config()
    assert not config.timer_dir.exists(), f"{config.timer_dir} exists"
    for outcome in Outcome:
        assert outcome in config
    _assert_config(config, Outcome.SUCCESS, Color.GREEN, _CHECKMARK)
    _assert_config(config, Outcome.FAILURE, Color.RED, _EX)
    _assert_config(config, Outcome.CANCELLED, Color.YELLOW, _EX)
    _assert_config(config, Outcome.SKIPPED, Color.GRAY, _EX)


def _write_config(path: Path) -> None:
    with path.open("w") as writer:
        writer.write(f"timer_dir: {path.parent}\n")
        writer.write("success:\n")
        writer.write("  color: blue\n")
        writer.write("skipped:\n")
        writer.write("  icon: X\n")
        writer.write("failure:\n")
        writer.write("  color: bright_red\n")
        writer.write("  icon: F\n")


def test_config_timerrc(tmp_path: Path) -> None:
    new_value = tmp_path / ".timerrc"
    old_value = _get_default_timerrc()
    _set_default_timerrc(new_value)
    _DEFAULT_TIMERRC = tmp_path / ".timerrc"  # noqa
    _write_config(path=_DEFAULT_TIMERRC)
    config = Config()
    _set_default_timerrc(old_value)
    assert config.timer_dir.exists()
    _assert_config(config, Outcome.SUCCESS, Color.BLUE, _CHECKMARK)
    _assert_config(config, Outcome.FAILURE, Color.BRIGHT_RED, "F")
    _assert_config(config, Outcome.CANCELLED, Color.YELLOW, _EX)
    _assert_config(config, Outcome.SKIPPED, Color.GRAY, "X")
