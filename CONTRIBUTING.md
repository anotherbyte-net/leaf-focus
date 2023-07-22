# Leaf focus contributing guide

## Development

Create a virtual environment:

```bash
python -m venv .venv
```

Install runtime dependencies and development dependencies:

```bash
# Windows MINGW64
source .venv/Scripts/activate

# Linux
source .venv/bin/activate

# Any

# install dependencies
python -m pip install --upgrade pip setuptools wheel
python -m pip install --upgrade -r requirements-dev.txt -r requirements.txt

# check for outdated packages
pip list --outdated
```

## Run tests and linters

Run the tests and linters with multiple python versions using tox.

If the pip dependencies have changed, it might be necessary to 
(un)comment `recreate = true` in the tox section in `pyproject.toml`.

To run using all available python versions:

```bash
# Windows
python install_xpdf.py \
--download-dir=.xpdf/download \
--install-dir=.xpdf/install \
--gpg-key-url=https://www.xpdfreader.com/gpg-key.txt \
--file-sig-url=https://dl.xpdfreader.com/xpdf-tools-win-4.04.zip.sig \
--file-comp-url=https://dl.xpdfreader.com/xpdf-tools-win-4.04.zip

# Windows
export TEST_XPDF_EXE_DIR=.xpdf/install/xpdf-tools-win-4.04/bin64

# Linux
python install_xpdf.py \
--download-dir=.xpdf/download \
--install-dir=.xpdf/install \
--gpg-key-url=https://www.xpdfreader.com/gpg-key.txt \
--file-sig-url=https://dl.xpdfreader.com/xpdf-tools-linux-4.04.tar.gz.sig \
--file-comp-url=https://dl.xpdfreader.com/xpdf-tools-linux-4.04.tar.gz

# Linux
export TEST_XPDF_EXE_DIR=.xpdf/install/xpdf-tools-linux-4.04/bin64

# Any
export TEST_INCLUDE_SLOW=true
python -X dev -m tox
```

To run using the active python:

```bash
python -X dev -m tox -e py
```

## Generate docs

Generate the docs using pdoc3:

```bash
pdoc --docformat google \
  --edit-url leaf_focus=https://github.com/anotherbyte-net/leaf-focus/blob/main/src/leaf_focus/ \
  --search --show-source \
  --output-directory docs \
  ./src/leaf_focus
```

## Create and upload release

Generate the distribution package archives.

```bash
python -X dev -m build
```

Upload archives to Test PyPI first.

```bash
python -X dev -m twine upload --repository testpypi dist/*
```

When uploading:

- for username, use `__token__`
- for password, [create a token](https://test.pypi.org/manage/account/#api-tokens)

Go to the [test project page](https://test.pypi.org/project/leaf-focus) and check that it looks ok.

Then create a new virtual environment, install the dependencies from the main PyPI, and install from Test PyPI.
Make sure to install the dependencies from the main PyPI, as the packages on Test PyPI are not the same.

```bash
deactivate
rm -rf .venv-test
python -m venv .venv-test
source .venv-test/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install --upgrade -r requirements.txt

export LEAF_FOCUS_VERSION='0.6.2'
pip install --index-url https://test.pypi.org/simple/ --no-deps leaf-focus==$LEAF_FOCUS_VERSION
# or
pip install dist/leaf_focus-$LEAF_FOCUS_VERSION-py3-none-any.whl
```

Test the installed package.

```bash
leaf-focus --version
leaf-focus --help

# Windows
leaf-focus tests/resources/example1/452.06-win10-win8-win7-release-notes.pdf \
  .pypi-test/ --ocr \
  --exe-dir .xpdf/install/xpdf-tools-win-4.04/bin64

# Linux
leaf-focus tests/resources/example1/452.06-win10-win8-win7-release-notes.pdf \
  .pypi-test/ --ocr \
  --exe-dir .xpdf/install/xpdf-tools-linux-4.04/bin64
```

If the package seems to work as expected, upload it to the live PyPI.

```bash
python -X dev -m twine upload dist/*
```

When uploading:

- for username, use `__token__`
- for password, [create a token](https://pypi.org/manage/account/#api-tokens)

Go to the [live project page](https://pypi.org/project/leaf-focus) and check that it looks ok.

Done!
