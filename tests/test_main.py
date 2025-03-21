import time
from pathlib import Path

import pytest

from gha_timer.config import Config
from gha_timer.enums import Outcome
from gha_timer.main import parse_args


@pytest.fixture
def default_config(tmp_path: Path) -> Config:
    config: Config = Config(timer_dir=tmp_path / ".timer_dir")
    return config


@pytest.fixture
def config_path(default_config: Config) -> Path:
    path: Path = default_config.timer_dir.parent / "config.yaml"
    with path.open("w") as writer:
        writer.write(f"timer_dir: {default_config.timer_dir}\n")
    return path


def _run(argv: list[str]) -> None:
    args = parse_args(argv)
    args.func(args)


def test_sequence(
    default_config: Config, config_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert not default_config.timer_dir.exists()
    _run([f"--config={config_path}", "start"])
    assert default_config.timer_dir.exists()
    assert len(list(default_config.timer_dir.iterdir())) == 1

    _run([f"--config={config_path}", "start"])
    assert default_config.timer_dir.exists()
    assert len(list(default_config.timer_dir.iterdir())) == 2

    # this should make the output be one second
    time.sleep(1)

    for outcome in Outcome:
        _run([f"--config={config_path}", "elapsed", "--outcome", f"{outcome.value}"])
        stream = capsys.readouterr()
        assert stream.out.endswith("1.0s\n")
        assert stream.err == ""

    # this should make the output be two seconds
    time.sleep(1)

    for outcome in Outcome:
        _run([f"--config={config_path}", "elapsed", "--outcome", f"{outcome.value}"])
        stream = capsys.readouterr()
        assert stream.out.endswith("2.0s\n")
        assert stream.err == ""

    _run([f"--config={config_path}", "start"])
    assert default_config.timer_dir.exists()
    assert len(list(default_config.timer_dir.iterdir())) == 3

    # this should make the output be two seconds
    time.sleep(2)

    for outcome in Outcome:
        _run([f"--config={config_path}", "elapsed", "--outcome", f"{outcome.value}"])
        stream = capsys.readouterr()
        assert stream.out.endswith("2.0s\n")
        assert stream.err == ""

    _run([f"--config={config_path}", "stop"])
    assert not default_config.timer_dir.exists()

    _run([f"--config={config_path}", "start"])
    assert default_config.timer_dir.exists()
    assert len(list(default_config.timer_dir.iterdir())) == 1
