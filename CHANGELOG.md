# Change log

## [v0.7.0](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.7.0)

Release 2024-11-17.

- Introduce release publish via PyPI Trusted Publishing.
- Add GitHub Actions for checking coverage, Actions security, test coverage, linters.
- Lots of minor code updates to satisfy linters.
- Deploy docs via GitHub Actions.


## [v0.6.2](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.6.2)

[full change log](https://github.com/anotherbyte-net/leaf-focus/compare/v0.6.1...v0.6.2)

- Validate first page and last page
- Additional tests for first page and last page
- Linter changes
- Improved contribution docs

## [v0.6.1](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.6.1)

[full change log](https://github.com/anotherbyte-net/leaf-focus/compare/v0.6.0...v0.6.1)

- Relax dependency specifications even more, to allow installing leaf-focus as a library.
- Fix test failing due to Windows text encoding.

## [v0.6.0](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.6.0)

[full change log](https://github.com/anotherbyte-net/leaf-focus/compare/v0.5.3...v0.6.0)

- Update dependencies.
- Move back to keras-ocr 0.8.9 to allow using Python >= 3.10.
- Address some linter suggestions.
- Also test using Python 3.12.
- Add xpdf to GitHub actions.

## [v0.5.3](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.5.3)

[full change log](https://github.com/anotherbyte-net/leaf-focus/compare/v0.5.2...v0.5.3)

- Update dependencies

## [v0.5.2](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.5.2)

[full change log](https://github.com/anotherbyte-net/leaf-focus/compare/v0.5.0...v0.5.2)

- Change dependency specification to use compatibility format
- use pdoc to generate html docs
- Explore other approaches to tests

## [v0.5.0](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.5.0)

[full change log](https://github.com/anotherbyte-net/leaf-focus/compare/v0.4.1...v0.5.0)

- Dependency updates
- Added tests that can be run without external binaries and tensorflow
- Improved tests

## [v0.4.1](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.4.1)

[full change log](https://github.com/anotherbyte-net/leaf-focus/compare/v0.4.0...v0.4.1)

- Dependency updates
- Improved OCR tests
- Improved tests when running in CI

## [v0.4.0](https://github.com/anotherbyte-net/leaf-focus/releases/tag/v0.4.0)

- Implement wrapper for [keras-ocr](https://github.com/faustomorales/keras-ocr)
- Implement wrapper for [xpdf tools](https://www.xpdfreader.com/about.html)
- Implement initial cli using Python's argparse
- Add docs and doc generation using [pdoc3](https://github.com/pdoc3/pdoc)
