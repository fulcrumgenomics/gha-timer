# gha_timer

[![PyPI Release](https://badge.fury.io/py/gha_timer.svg)](https://badge.fury.io/py/gha_timer)
[![CI](https://github.com/fulcrumgenomics/gha-timer/actions/workflows/python_package.yml/badge.svg?branch=main)](https://github.com/fulcrumgenomics/gha-timer/actions/workflows/python_package.yml?query=branch%3Amain)
[![Python Versions](https://img.shields.io/badge/python-3.11_|_3.12_|_3.13-blue)](https://github.com/fulcrumgenomics/gha-timer)
[![MyPy Checked](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://docs.astral.sh/ruff/)

Time and group logs for GitHub actions

## Quickstart

Start a timer:

```console
$ gha-timer start
```

Get the elapsed time:

```console
$ gha-timer elapsed --outcome success
                                                                      ✓ 10.8s
$ gha-timer elapsed --outcome failure
                                                                      ✕ 20.2s
$ gha-timer elapsed --outcome cancelled
                                                                      ✕ 33.6s
$ gha-timer elapsed --outcome skipped  
                                                                      ✕ 37.3s
```

Stop the timer:

```console
$ gha-timer stop
```

Use the `--name` option to add [group log lines][group-log-lines-link]:

```console
$ gha-timer start --name "Build the project"
::group::Build the project
$ gha-timer elapsed --outcome success --name "Build the project"
::endgroup::Build the project
                                                                      ✓ 19.2s
```

Specify a custom configuration file with `--config` (or just create a `~/.timerrc`) to control the color and icon for
each _outcome_ ([`steps.<step_id>.outcome`: `success`, `failure`, `cancelled`, or `skipped`][steps-context-link]). 
Below is the default configuration:

```yaml
success:
  color: green
  icon: "✓"
failure:
  color: red
  icon: "✕"
cancelled:
  color: yellow
  icon: "✕"
skipped:
  color: gray
  icon: "✕"
```

Supported colors are: `red`, `green`, `yellow`, `blue`, `cyan`, `bright_red`, `bright_green`, `white`, `gray`, 
and `bg_grey`.

[group-log-lines-link]: https://github.com/actions/toolkit/blob/main/docs/commands.md#group-and-ungroup-log-lines
[steps-context-link]: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#steps-context



## Recommended Installation

Install the Python package and dependency management tool [`poetry`](https://python-poetry.org/docs/#installation) using official documentation.
You must have Python 3.11 or greater available on your system path, which could be managed by [`mamba`](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), [`pyenv`](https://github.com/pyenv/pyenv), or another package manager. 
Finally, install the dependencies of the project with:

```console
poetry install
```

To check successful installation, run:

```console
poetry run gha_timer hello --name Fulcrum
```

## Installing into a Mamba Environment

Install the Python package and dependency management tool [`poetry`](https://python-poetry.org/docs/#installation) and the environment manager [`mamba`](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) using official documentation.
Create and activate a virtual environment with Python 3.11 or greater:

```console
mamba create -n gha_timer python=3.11
mamba activate gha_timer
```

Then, because Poetry will auto-detect an activated environment, install the project with:

```console
poetry install
```

To check successful installation, run:

```console
gha_timer hello --name Fulcrum
```

## Development and Testing

See the [contributing guide](./CONTRIBUTING.md) for more information.
