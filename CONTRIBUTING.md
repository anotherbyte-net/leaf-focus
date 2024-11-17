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
python -m pip install --upgrade pip tox build
```

If you change the dependencies, re-generate the `requirements.txt` file:

```bash
python -X dev -m tox run -e pip-compile
```

## Run tests and linters

Run the tests and linters with multiple python versions using tox.

Install dependencies:

```bash
# Windows
python install_xpdf.py \
--download-dir=.xpdf/download \
--install-dir=.xpdf/install \
--gpg-key-url=https://www.xpdfreader.com/gpg-key.txt \
--file-sig-url=https://dl.xpdfreader.com/xpdf-tools-win-4.05.zip.sig \
--file-comp-url=https://dl.xpdfreader.com/xpdf-tools-win-4.05.zip

# Linux
python install_xpdf.py \
--download-dir=.xpdf/download \
--install-dir=.xpdf/install \
--gpg-key-url=https://www.xpdfreader.com/gpg-key.txt \
--file-sig-url=https://dl.xpdfreader.com/xpdf-tools-linux-4.05.tar.gz.sig \
--file-comp-url=https://dl.xpdfreader.com/xpdf-tools-linux-4.05.tar.gz
```

To run using all available python versions:

```bash
python -X dev -m tox run -e py310-tests
python -X dev -m tox run -e coverage-report
python -X dev -m tox run -e py310-lint-style
python -X dev -m tox run -e lint-docs
```

To run using the active python:

```bash
python -X dev -m tox -e py
```

## Test a release locally

Generate the distribution package archives.

```bash
python -X dev -m build
```

Then create a new virtual environment, install the dependencies, and install from the local wheelTest PyPI.

```bash
rm -rf .venv-test
python -m venv .venv-test
source .venv-test/bin/activate

python -m pip install --upgrade pip

pip install dist/*.whl
```

## Test the installed package

```bash
leaf-focus --version
leaf-focus --help

# Windows
leaf-focus tests/resources/example1/452.06-win10-win8-win7-release-notes.pdf \
  .pypi-test/ --ocr \
  --exe-dir .xpdf/install/xpdf-tools-win-4.05/bin64

# Linux
leaf-focus tests/resources/example1/452.06-win10-win8-win7-release-notes.pdf \
  .pypi-test/ --ocr \
  --exe-dir .xpdf/install/xpdf-tools-linux-4.05/bin64
```

## Test a release from Test PyPI

If the package seems to work as expected, push changes to the `main` branch.

The `pypi-package.yml` GitHub Actions workflow will deploy a release to Test PyPI.

Then follow the same process as testing a release locally, except install from Test PyPI.

```bash
rm -rf .venv-test
python -m venv .venv-test
source .venv-test/bin/activate

python -m pip install --upgrade pip

# use the requirements file to install dependencies from the production PyPI,
# as the packages may not be on Test PyPI, or they might be different (potentially malicious!) packages.
python -m pip install --upgrade -r requirements.txt

pip install --index-url https://test.pypi.org/simple/ --no-deps leaf-focus==$LEAF_FOCUS_VERSION
```

Go to the [test project page](https://test.pypi.org/project/leaf-focus) and check that it looks ok.

## Create a release to PyPI

Create a tag on the `main` branch.

The `pypi-package.yml` GitHub Actions workflow will deploy a release to PyPI.

Go to the [live project page](https://pypi.org/project/leaf-focus) and check that it looks ok.

Done!
