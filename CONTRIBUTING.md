# Leaf focus contributing guide

## Development

Create a virtual environment:

```bash
python -m venv .venv
```

Install runtime dependencies and development dependencies:

```bash
# Windows
.venv\Scripts\activate.ps1

# Linux
source .venv/bin/activate

# install dependencies
python -m pip install --upgrade -r requirements-dev.txt -r requirements.txt

# check for outdated packages
pip list --outdated
```

## Run tests and linters

```bash
# Tests - multiple python versions using tox
# (it might be necessary to (un)comment `recreate = true` in pyproject.toml)
python -X dev -m tox

# Tests - Run tests with coverage
python -X dev -m coverage run -m pytest --tb=line --doctest-modules

# Tests - Coverage report
python -X dev -m coverage report

# Linter - flake8
python -X dev -m flake8 src --count --show-source --statistics

# Linter - mypy
python -X dev -m mypy src

# Linter - black
python -X dev -m black --check src

# Linter - pylint
python -X dev -m pylint src

# Linter - pydocstyle
python -X dev -m pydocstyle src

# Linter - pyright
python -X dev -m pyright src

# Linter - pytype
python -X dev -m pytype -j auto
```

## Generate docs

Generate the docs using pdoc3:

```bash
pdoc --html --output-dir docs src/leaf_focus --force \
  --config "lunr_search={'fuzziness': 1, 'index_docstrings': True}" \
  --config "git_link_template='https://github.com/anotherbyte-net/leaf-focus/blob/{commit}/{path}#L{start_line}-L{end_line}'"
```

## Create and upload release

```bash
#  generate the distribution package archives
python -X dev -m build

# upload archives to Test PyPI first
python -X dev -m twine upload --repository testpypi dist/*
```
When uploading:

- for username, use `__token__`
- for password, create a token at https://test.pypi.org/manage/account/#api-tokens

Go to the [project page](https://test.pypi.org/project/leaf-focus) and check that it looks ok.

(TODO: upload to prod PyPI)