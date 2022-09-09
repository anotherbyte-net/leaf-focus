# leaf-focus

Extract structured text from pdf files.

## Install

Download the [Xpdf command line tools](https://www.xpdfreader.com/download.html) and extract the executable files.

Provide the directory containing the executable files as `--exe-dir`.

## Usage

```text
usage: leaf-focus [-h] [--version] --exe-dir EXE_DIR [--page-images] [--ocr]
                  [--first FIRST] [--last LAST]
                  [--log-level {debug,info,warning,error,critical}]
                  input_pdf output_dir

Extract structured text from a pdf file.

positional arguments:
  input_pdf             path to the pdf file to read
  output_dir            path to the directory to save the extracted text files

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --exe-dir EXE_DIR     path to the directory containing xpdf executable files
  --page-images         save each page of the pdf as a separate image
  --ocr                 run optical character recognition on each page of the
                        pdf
  --first FIRST         the first pdf page to process
  --last LAST           the last pdf page to process
  --log-level {debug,info,warning,error,critical}
                        the log level: debug, info, warning, error, critical
```

### Examples

```bash
# Extract the pdf information and embedded text.
leaf-focus --exe-dir [path-to-xpdf-exe-dir] file.pdf file-pages

# Extract the pdf information, embedded text, an image of each page, and Optical Character Recognition results of each page.
leaf-focus --exe-dir [path-to-xpdf-exe-dir] file.pdf file-pages --ocr
```

## Development

Generate the docs using pdoc3:

```bash
pdoc --html --output-dir docs src/leaf_focus --force \
  --config "lunr_search={'fuzziness': 1, 'index_docstrings': True}" \
  --config "git_link_template='https://github.com/anotherbyte-net/leaf-focus/blob/{commit}/{path}#L{start_line}-L{end_line}'"
```
