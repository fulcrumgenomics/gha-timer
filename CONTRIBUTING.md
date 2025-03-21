# Development and Testing

## Primary Development Commands

To check and resolve linting issues in the codebase, run:

```console
poetry run ruff check --fix
```

To check and resolve formatting issues in the codebase, run:

```console
poetry run ruff format
```

To check the unit tests in the codebase, run:

```console
poetry run pytest
```

To check the typing in the codebase, run:

```console
poetry run mypy
```

To generate a code coverage report after testing locally, run:

```console
poetry run coverage html
```

To check the lock file is up to date:

```console
poetry check --lock
```

## Shortcut Task Commands

###### For Running Individual Checks

```console
poetry task check-lock
poetry task check-format
poetry task check-lint
poetry task check-tests
poetry task check-typing
```

###### For Running All Checks

```console
poetry task check-all
```

###### For Running Individual Fixes

```console
poetry task fix-format
poetry task fix-lint
```

###### For Running All Fixes

```console
poetry task fix-all
```

###### For Running All Fixes and Checks

```console
poetry task fix-and-check-all
```

## Creating a release on PyPI

> [!NOTE]
> This project follows [Semantic Versioning](https://semver.org/), aka SemVer. In brief:
> 
> - MAJOR version when you make incompatible API changes
> - MINOR version when you add functionality in a backwards compatible manner
> - PATCH version when you make backwards compatible bug fixes

> [!IMPORTANT]
> Consider editing the changelog if there are any errors or necessary enhancements.

1. Clone the repository recursively, ensure you are on the main branch, and that the working directory is clean.
2. Check out a new branch to prepare the library for release.
3. Bump the version of the library to the desired SemVer with `poetry version #.#.#`.
4. Commit the version bump changes with a Git commit message like `chore(release): bump to #.#.#`.
5. Push the commit, open a PR, ensure tests pass, and seek reviews.
6. Squash merge the PR into the `main` branch.
7. Tag the new commit on the main branch with the bumped version number.

> [!WARNING]
> The tag **must** be a valid SemVer version number and **must** match the version set by `poetry version` in (3). The [publishing GitHub Action](.github/workflows/publish_gha_timer) is activated by a new tag on the `main` branch containing a valid SemVer version.

GitHub Actions will take care of the remainder of the deployment and release process:

1. Unit tests will be re-run.
2. A source distribution will be built.
3. A multi-arch multi-Python wheel (binary) distributions will be built.
4. Assets will be deployed to PyPi with the new version.
5. A [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/)-aware changelog will be drafted.
6. A GitHub release will be created with the new version tag and the drafted changelog.
