URLS=[
"leaf_focus/index.html",
"leaf_focus/app.html",
"leaf_focus/cli.html",
"leaf_focus/ocr/index.html",
"leaf_focus/ocr/keras_ocr.html",
"leaf_focus/ocr/model.html",
"leaf_focus/pdf/index.html",
"leaf_focus/pdf/model.html",
"leaf_focus/pdf/xpdf.html",
"leaf_focus/utils.html"
];
INDEX=[
{
"ref":"leaf_focus",
"url":0,
"doc":"Documentation for the leaf focus package.  leaf-focus Extract structured text from pdf files.  Install Install from PyPI using pip:   pip install leaf-focus   [![PyPI](https: img.shields.io/pypi/v/leaf-focus)](https: pypi.org/project/leaf-focus/) ![PyPI - Python Version](https: img.shields.io/pypi/pyversions/leaf-focus) ![GitHub Workflow Status (branch)](https: img.shields.io/github/workflow/status/anotherbyte-net/leaf-focus/Create%20Package/main) Download the [Xpdf command line tools](https: www.xpdfreader.com/download.html) and extract the executable files. Provide the directory containing the executable files as   exe-dir .  Usage   usage: leaf-focus [-h] [ version]  exe-dir EXE_DIR [ page-images] [ ocr] [ first FIRST] [ last LAST] [ log-level {debug,info,warning,error,critical}] input_pdf output_dir Extract structured text from a pdf file. positional arguments: input_pdf path to the pdf file to read output_dir path to the directory to save the extracted text files optional arguments: -h,  help show this help message and exit  version show program's version number and exit  exe-dir EXE_DIR path to the directory containing xpdf executable files  page-images save each page of the pdf as a separate image  ocr run optical character recognition on each page of the pdf  first FIRST the first pdf page to process  last LAST the last pdf page to process  log-level {debug,info,warning,error,critical} the log level: debug, info, warning, error, critical    Examples    Extract the pdf information and embedded text. leaf-focus  exe-dir [path-to-xpdf-exe-dir] file.pdf file-pages  Extract the pdf information, embedded text, an image of each page, and Optical Character Recognition results of each page. leaf-focus  exe-dir [path-to-xpdf-exe-dir] file.pdf file-pages  ocr    Change log  [v0.4.0](https: github.com/anotherbyte-net/leaf-focus/releases/tag/v0.4.0) - Implement wrapper for [keras-ocr](https: github.com/faustomorales/keras-ocr) - Implement wrapper for [xpdf tools](https: www.xpdfreader.com/about.html) - Implement initial cli using Python's argparse - Add docs and doc generation using [pdoc3](https: github.com/pdoc3/pdoc)"
},
{
"ref":"leaf_focus.app",
"url":1,
"doc":"Main application."
},
{
"ref":"leaf_focus.app.AppArgs",
"url":1,
"doc":"Arguments for running the application."
},
{
"ref":"leaf_focus.app.AppArgs.input_pdf",
"url":1,
"doc":"path to the pdf file"
},
{
"ref":"leaf_focus.app.AppArgs.output_dir",
"url":1,
"doc":"path to the output directory to save text files"
},
{
"ref":"leaf_focus.app.AppArgs.first_page",
"url":1,
"doc":"the first pdf page to process"
},
{
"ref":"leaf_focus.app.AppArgs.last_page",
"url":1,
"doc":"the last pdf page to process"
},
{
"ref":"leaf_focus.app.AppArgs.save_page_images",
"url":1,
"doc":"save each page of the pdf to a separate image"
},
{
"ref":"leaf_focus.app.AppArgs.run_ocr",
"url":1,
"doc":"run OCR over each page of the pdf"
},
{
"ref":"leaf_focus.app.AppArgs.log_level",
"url":1,
"doc":"the log level"
},
{
"ref":"leaf_focus.app.App",
"url":1,
"doc":"The main application. Create a new instance of the application. Args: exe_dir: The path to the directory containing the executable files."
},
{
"ref":"leaf_focus.app.App.run",
"url":1,
"doc":"Run the application. Args: app_args: The application arguments. Returns: bool: True if the text extraction succeeded, otherwise false.",
"func":1
},
{
"ref":"leaf_focus.app.App.pdf_info",
"url":1,
"doc":"Get the pdf file information. Args: prog: The program to run. app_args: The application arguments. Returns: pdf_model.XpdfInfoResult: The result from the program.",
"func":1
},
{
"ref":"leaf_focus.app.App.pdf_text",
"url":1,
"doc":"Get the text embedded in the pdf. Args: prog: The program to run. app_args: The application arguments. Returns: pdf_model.XpdfTextResult: The result from the program.",
"func":1
},
{
"ref":"leaf_focus.app.App.pdf_images",
"url":1,
"doc":"Get each page in the pdf as a separate image. Args: prog: The program to run. app_args: The application arguments. Returns: pdf_model.XpdfImageResult: The result from the program.",
"func":1
},
{
"ref":"leaf_focus.app.App.pdf_ocr",
"url":1,
"doc":"Recognise text on the pdf page images. Args: xpdf_image: The result from the pdf image program. app_args: The application arguments. Returns: typing.Generator[ocr_model.KerasOcrResult, typing.Any, None]: Yield text recognition results for each pdf page image.",
"func":1
},
{
"ref":"leaf_focus.cli",
"url":2,
"doc":"Command line for leaf focus."
},
{
"ref":"leaf_focus.cli.main",
"url":2,
"doc":"Run as a command line program. Args: args: The program arguments. Returns: int: Program exit code.",
"func":1
},
{
"ref":"leaf_focus.ocr",
"url":3,
"doc":"Optical Character Recognition feature."
},
{
"ref":"leaf_focus.ocr.keras_ocr",
"url":4,
"doc":"OCR using keras-ocr."
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition",
"url":4,
"doc":"OCR implementation using keras-ocr. Create a new OpticalCharacterRecognition."
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition.engine_create",
"url":4,
"doc":"Create the OCR engine. Returns: None",
"func":1
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition.engine_run",
"url":4,
"doc":"Run the recognition engine. Args: image_file: The path to the image file. Returns: typing.Tuple[typing.List, typing.Any]: The list of images and list of recognition results.",
"func":1
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition.engine_annotate",
"url":4,
"doc":"Run the annotation engine. Args: image: The image data. predictions: The recognised text from the image. axis: The plot axis for drawing annotations. Returns: None",
"func":1
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition.recognise_text",
"url":4,
"doc":"Recognise text in an image file. Args: image_file: The path to the image file. output_dir: The directory to write the results. Returns: model.KerasOcrResult: The text recognition results.",
"func":1
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition.save_figure",
"url":4,
"doc":"Save the annotated image. Args: annotation_file: The path to the file containing annotations. image: The image data. predictions: The text recognition results. Returns: None",
"func":1
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition.convert_predictions",
"url":4,
"doc":"Convert predictions to items. Args: predictions: The list of recognised text. Returns: typing.List[typing.List[model.TextItem : The equivalent text items.",
"func":1
},
{
"ref":"leaf_focus.ocr.keras_ocr.OpticalCharacterRecognition.save_items",
"url":4,
"doc":"Save items to csv file. Args: items_file: Write the text items to this file. items: The text items to save. Returns: None",
"func":1
},
{
"ref":"leaf_focus.ocr.model",
"url":5,
"doc":"Models for OCR processing."
},
{
"ref":"leaf_focus.ocr.model.TextItem",
"url":5,
"doc":"One found text item (could be a word or phrase) in an image."
},
{
"ref":"leaf_focus.ocr.model.TextItem.text",
"url":5,
"doc":"The recognised text."
},
{
"ref":"leaf_focus.ocr.model.TextItem.top_left_x",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.top_left_y",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.top_right_x",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.top_right_y",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.bottom_right_x",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.bottom_right_y",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.bottom_left_x",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.bottom_left_y",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.line_number",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.line_order",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.TextItem.top_left",
"url":5,
"doc":"Get the top left point. Returns: The x and y coordinates."
},
{
"ref":"leaf_focus.ocr.model.TextItem.top_right",
"url":5,
"doc":"Get the top right point. Returns: The x and y coordinates."
},
{
"ref":"leaf_focus.ocr.model.TextItem.bottom_right",
"url":5,
"doc":"Get the bottom right point. Returns: The x and y coordinates."
},
{
"ref":"leaf_focus.ocr.model.TextItem.bottom_left",
"url":5,
"doc":"Get the bottom left point. Returns: The x and y coordinates."
},
{
"ref":"leaf_focus.ocr.model.TextItem.top_length",
"url":5,
"doc":"Get the length of the top side. Returns: float: The length."
},
{
"ref":"leaf_focus.ocr.model.TextItem.left_length",
"url":5,
"doc":"Get the length of the left side. Returns: float: The length."
},
{
"ref":"leaf_focus.ocr.model.TextItem.line_bounds",
"url":5,
"doc":"Line bounds from top of text to bottom of text."
},
{
"ref":"leaf_focus.ocr.model.TextItem.is_same_line",
"url":5,
"doc":"Check if the vertical midpoints of this item and another item overlap. Calculated as the midpoint +- 1/3 of the height of the text. Args: other (TextItem): The text item to compare. Returns: bool: True if this item and the other item overlap, otherwise false.",
"func":1
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_top_left_right",
"url":5,
"doc":"Get the top slope from the left to the right. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_top_right_left",
"url":5,
"doc":"Get the top slope from the right to the left. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_left_top_bottom",
"url":5,
"doc":"Get the left slope from the top to the bottom. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_left_bottom_top",
"url":5,
"doc":"Get the left slope from the bottom to the top. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_bottom_left_right",
"url":5,
"doc":"Get the bottom slope from the left to the right. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_bottom_right_left",
"url":5,
"doc":"Get the bottom slope from the right to the left. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_right_top_bottom",
"url":5,
"doc":"Get the right slope from the top to the bottom. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.slope_right_bottom_top",
"url":5,
"doc":"Get the right slope from the bottom to the top. Returns: float: The slope."
},
{
"ref":"leaf_focus.ocr.model.TextItem.is_horizontal_level",
"url":5,
"doc":"Check whether the left-to-right slope is approximately horizontal. Returns: bool: True if the item is approximately horizontal."
},
{
"ref":"leaf_focus.ocr.model.TextItem.is_vertical_level",
"url":5,
"doc":"Check whether the top-to-bottom slope is approximately vertical. Returns: bool: True if the item is approximately vertical."
},
{
"ref":"leaf_focus.ocr.model.TextItem.save",
"url":5,
"doc":"Save found text items to a file. Args: path: Write the items to this file. items: The items to save. Returns: None",
"func":1
},
{
"ref":"leaf_focus.ocr.model.TextItem.load",
"url":5,
"doc":"Load found text items from a file. Args: path: The path to the file containing items. Returns: typing.Generator[\"TextItem\", typing.Any, None]: Items from the file.",
"func":1
},
{
"ref":"leaf_focus.ocr.model.TextItem.from_prediction",
"url":5,
"doc":"Convert from (text, box) to item. Box is (top left, top right, bottom right, bottom left). Its structure is  startX,startY], [endX,startY], [endX,endY], [startX, endY . Args: prediction: The text recognised in an image. Returns: TextItem: A text item representing the recognised text.",
"func":1
},
{
"ref":"leaf_focus.ocr.model.TextItem.order_text_lines",
"url":5,
"doc":"Put items into lines of text (top -> bottom, left -> right).",
"func":1
},
{
"ref":"leaf_focus.ocr.model.TextItem.to_prediction",
"url":5,
"doc":"Convert to prediction format."
},
{
"ref":"leaf_focus.ocr.model.KerasOcrResult",
"url":5,
"doc":"Result from running keras-ocr."
},
{
"ref":"leaf_focus.ocr.model.KerasOcrResult.output_dir",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.KerasOcrResult.annotations_file",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.KerasOcrResult.predictions_file",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.ocr.model.KerasOcrResult.items",
"url":5,
"doc":""
},
{
"ref":"leaf_focus.pdf",
"url":6,
"doc":"Pdf document text extraction feature."
},
{
"ref":"leaf_focus.pdf.model",
"url":7,
"doc":"PDF processing models."
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs",
"url":7,
"doc":"xpdf arguments common to all commands."
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs.owner_password",
"url":7,
"doc":"Specify the owner password for the PDF file. Providing this will bypass all security restrictions. -opw  : owner password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs.user_password",
"url":7,
"doc":"Specify the user password for the PDF file. -upw  : user password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs.first_page",
"url":7,
"doc":"Specifies the first page to convert. -f  : first page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs.last_page",
"url":7,
"doc":"Specifies the last page to convert. -l  : last page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs.use_verbose",
"url":7,
"doc":"Print a status message (to stdout) before processing each page. -verbose : print per-page status information"
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs.config_file",
"url":7,
"doc":"Read config-file in place of ~/.xpdfrc or the system-wide config file. -cfg  : configuration file to use in place of .xpdfrc"
},
{
"ref":"leaf_focus.pdf.model.XpdfArgs.program_info",
"url":7,
"doc":"Print copyright and version information. -v : print copyright and version info"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs",
"url":7,
"doc":"Arguments for xpdf pdfinfo program."
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.include_page_bounding_boxes",
"url":7,
"doc":"Prints the page box bounding boxes: MediaBox, CropBox, BleedBox, TrimBox, and ArtBox. -box : print the page bounding boxes"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.include_metadata",
"url":7,
"doc":"Prints document-level metadata. This is the \"Metadata\" stream from the PDF file\u2019s Catalog object. -meta : print the document metadata (XML)"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.include_raw_dates",
"url":7,
"doc":"Prints the raw (undecoded) date strings, directly from the PDF file. -rawdates : print the undecoded date strings directly from the PDF file"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.encoding",
"url":7,
"doc":"Sets the encoding to use for text output. The encoding\u2212name must be defined with the unicodeMap command. This defaults to \"Latin1\" (which is a built-in encoding). -enc  : output text encoding name"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.owner_password",
"url":7,
"doc":"Specify the owner password for the PDF file. Providing this will bypass all security restrictions. -opw  : owner password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.user_password",
"url":7,
"doc":"Specify the user password for the PDF file. -upw  : user password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.first_page",
"url":7,
"doc":"Specifies the first page to convert. -f  : first page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.last_page",
"url":7,
"doc":"Specifies the last page to convert. -l  : last page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.use_verbose",
"url":7,
"doc":"Print a status message (to stdout) before processing each page. -verbose : print per-page status information"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.config_file",
"url":7,
"doc":"Read config-file in place of ~/.xpdfrc or the system-wide config file. -cfg  : configuration file to use in place of .xpdfrc"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoArgs.program_info",
"url":7,
"doc":"Print copyright and version information. -v : print copyright and version info"
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult",
"url":7,
"doc":"Result from xpdf pdfinfo program."
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.title",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.subject",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.keywords",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.author",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.creator",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.producer",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.creation_date",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.modification_date",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.tagged",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.form",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.pages",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.encrypted",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.page_size",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.media_box",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.crop_box",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.bleed_box",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.trim_box",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.art_box",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.file_size_bytes",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.optimized",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.pdf_version",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfInfoResult.metadata",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs",
"url":7,
"doc":"Arguments for xpdf pdftotext program."
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_original_layout",
"url":7,
"doc":"Maintain (as best as possible) the original physical layout of the text. -layout : maintain original physical layout"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_simple_layout",
"url":7,
"doc":"optimized for simple one-column pages. This mode will do a better job of maintaining horizontal spacing, but it will only work properly with a single column of text. -simple : simple one-column page layout"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_simple2_layout",
"url":7,
"doc":"handles slightly rotated text (e.g., OCR output) better. Only works for pages with a single column of text. -simple2 : simple one-column page layout, version 2"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_table_layout",
"url":7,
"doc":"Table mode is similar to physical layout mode, but optimized for tabular data, with the goal of keeping rows and columns aligned (at the expense of inserting extra whitespace). If the \u2212fixed option is given, character spacing within each line will be determined by the specified character pitch. -table : similar to -layout, but optimized for tables"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_line_printer",
"url":7,
"doc":"Line printer mode uses a strict fixed-character-pitch and -height layout. That is, the page is broken into a grid, and characters are placed into that grid. If the grid spacing is too small for the actual characters, the result is extra whitespace. If the grid spacing is too large, the result is missing whitespace. The grid spacing can be specified using the \u2212fixed and \u2212linespacing options. If one or both are not given on the command line, pdftotext will attempt to compute appropriate value(s). -lineprinter : use strict fixed-pitch/height layout"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_raw_string_order",
"url":7,
"doc":"Keep the text in content stream order. Depending on how the PDF file was generated, this may or may not be useful. -raw : keep strings in content stream order"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_text_clip",
"url":7,
"doc":"Text which is hidden because of clipping is removed before doing layout, and then added back in. This can be helpful for tables where clipped (invisible) text would overlap the next column. -clip : separate clipped text"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_no_diag",
"url":7,
"doc":"Diagonal text, i.e., text that is not close to one of the 0, 90, 180, or 270 degree axes, is discarded. This is useful to skip watermarks drawn on top of body text, etc. -nodiag : discard diagonal text"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_no_page_break",
"url":7,
"doc":"Don't insert a page break (form feed character) at the end of each page. -nopgbrk : don't insert a page break at the end of each page"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_bom",
"url":7,
"doc":"Insert a Unicode byte order marker (BOM) at the start of the text output. -bom : insert a Unicode BOM at the start of the text file"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.use_verbose",
"url":7,
"doc":"Print a status message (to stdout) before processing each page. -verbose : print per-page status information"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.fixed_text_number",
"url":7,
"doc":"Specify the character pitch (character width), in points, for physical layout, table, or line printer mode. This is ignored in all other modes. -fixed  : assume fixed-pitch (or tabular) text"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.line_space_number",
"url":7,
"doc":"Specify the line spacing, in points, for line printer mode. This is ignored in all other modes. -linespacing  : fixed line spacing for LinePrinter mode"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.line_end_type",
"url":7,
"doc":"Sets the end-of-line convention to use for text output. -eol  : output end-of-line convention (unix, dos, or mac)"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.margin_left_number",
"url":7,
"doc":"Specifies the left margin, in points. Text in the left margin (i.e., within that many points of the left edge of the page) is discarded. The default value is zero. -marginl  : left page margin"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.margin_right_number",
"url":7,
"doc":"Specifies the right margin, in points. Text in the right margin (i.e., within that many points of the right edge of the page) is discarded. The default value is zero. -marginr  : right page margin"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.margin_topnumber",
"url":7,
"doc":"Specifies the top margin, in points. Text in the top margin (i.e., within that many points of the top edge of the page) is discarded. The default value is zero. -margint  : top page margin"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.margin_bottom_number",
"url":7,
"doc":"Specifies the bottom margin, in points. Text in the bottom margin (i.e., within that many points of the bottom edge of the page) is discarded. The default value is zero. -marginb  : bottom page margin"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.get_line_ending",
"url":7,
"doc":"Get the line endings based on the current platform. Returns: The line ending style.",
"func":1
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.owner_password",
"url":7,
"doc":"Specify the owner password for the PDF file. Providing this will bypass all security restrictions. -opw  : owner password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.user_password",
"url":7,
"doc":"Specify the user password for the PDF file. -upw  : user password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.first_page",
"url":7,
"doc":"Specifies the first page to convert. -f  : first page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.last_page",
"url":7,
"doc":"Specifies the last page to convert. -l  : last page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.config_file",
"url":7,
"doc":"Read config-file in place of ~/.xpdfrc or the system-wide config file. -cfg  : configuration file to use in place of .xpdfrc"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextArgs.program_info",
"url":7,
"doc":"Print copyright and version information. -v : print copyright and version info"
},
{
"ref":"leaf_focus.pdf.model.XpdfTextResult",
"url":7,
"doc":"Result for xpdf pdftotext program."
},
{
"ref":"leaf_focus.pdf.model.XpdfTextResult.output_path",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfTextResult.stdout",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfTextResult.stderr",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs",
"url":7,
"doc":"Arguments for xpdf pdftopng program."
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.resolution",
"url":7,
"doc":"Specifies the resolution, in DPI. The default is 150 DPI. -r  : resolution, in DPI (default is 150)"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.use_monochrome",
"url":7,
"doc":"Generate a monochrome image (instead of a color image). -mono : generate a monochrome PNG file"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.use_grayscale",
"url":7,
"doc":"Generate a grayscale image (instead of a color image). -gray : generate a grayscale PNG file"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.use_alpha_channel",
"url":7,
"doc":"Generate an alpha channel in the PNG file. This is only useful with PDF files that have been constructed with a transparent background. The \u2212alpha flag cannot be used with \u2212mono. -alpha : include an alpha channel in the PNG file"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.rotation",
"url":7,
"doc":"Rotate pages by 0 (the default), 90, 180, or 270 degrees. -rot  : set page rotation: 0, 90, 180, or 270"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.free_type",
"url":7,
"doc":"Enable or disable FreeType (a TrueType / Type 1 font rasterizer). This defaults to \"yes\". -freetype  : enable FreeType font rasterizer: yes, no"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.anti_aliasing",
"url":7,
"doc":"Enable or disable font anti-aliasing. This defaults to \"yes\". -aa  : enable font anti-aliasing: yes, no"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.vector_anti_aliasing",
"url":7,
"doc":"Enable or disable vector anti-aliasing. This defaults to \"yes\". -aaVector  : enable vector anti-aliasing: yes, no"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.owner_password",
"url":7,
"doc":"Specify the owner password for the PDF file. Providing this will bypass all security restrictions. -opw  : owner password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.user_password",
"url":7,
"doc":"Specify the user password for the PDF file. -upw  : user password (for encrypted files)"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.first_page",
"url":7,
"doc":"Specifies the first page to convert. -f  : first page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.last_page",
"url":7,
"doc":"Specifies the last page to convert. -l  : last page to convert"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.use_verbose",
"url":7,
"doc":"Print a status message (to stdout) before processing each page. -verbose : print per-page status information"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.config_file",
"url":7,
"doc":"Read config-file in place of ~/.xpdfrc or the system-wide config file. -cfg  : configuration file to use in place of .xpdfrc"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageArgs.program_info",
"url":7,
"doc":"Print copyright and version information. -v : print copyright and version info"
},
{
"ref":"leaf_focus.pdf.model.XpdfImageResult",
"url":7,
"doc":"Result for xpdf pdftopng program."
},
{
"ref":"leaf_focus.pdf.model.XpdfImageResult.output_dir",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfImageResult.output_files",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfImageResult.stdout",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.model.XpdfImageResult.stderr",
"url":7,
"doc":""
},
{
"ref":"leaf_focus.pdf.xpdf",
"url":8,
"doc":"Text extraction from pdf using xpdf tools."
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram",
"url":8,
"doc":"Interact with xpdf tools. Create a new xpdf program class to interact with xpdf tools. Args: directory: The path to the directory containing xpdf tools."
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.OPTS_TEXT_ENCODING",
"url":8,
"doc":""
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.OPTS_TEXT_LINE_ENDING",
"url":8,
"doc":""
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.OPTS_IMAGE_ROTATION",
"url":8,
"doc":""
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.OPTS_IMAGE_FREETYPE",
"url":8,
"doc":""
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.OPTS_IMAGE_ANTI_ALIAS",
"url":8,
"doc":""
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.OPTS_IMAGE_VEC_ANTI_ALIAS",
"url":8,
"doc":""
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.info",
"url":8,
"doc":"Get information from a pdf file. Args: pdf_path: The path to the pdf file. output_dir: The directory to save pdf info file. xpdf_args: The program arguments. Returns: The pdf file information.",
"func":1
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.text",
"url":8,
"doc":"Get the text from a pdf file. Args: pdf_path: The path to the pdf file. output_path: The directory to save output files. xpdf_args: The pdf program arguments. Returns: The result from running the text extraction program.",
"func":1
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.image",
"url":8,
"doc":"Create images of pdf pages. Args: pdf_path: The path to the pdf file. output_path: The directory to save output files. xpdf_args: The program arguments. Returns: The pdf file image info.",
"func":1
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.build_cmd",
"url":8,
"doc":"Build the command arguments from a data class.",
"func":1
},
{
"ref":"leaf_focus.pdf.xpdf.XpdfProgram.find_images",
"url":8,
"doc":"Find image files in a directory.",
"func":1
},
{
"ref":"leaf_focus.utils",
"url":9,
"doc":"Small utility functions."
},
{
"ref":"leaf_focus.utils.get_name_dash",
"url":9,
"doc":"Get the package name with word separated by dashes.",
"func":1
},
{
"ref":"leaf_focus.utils.get_name_under",
"url":9,
"doc":"Get the package name with word separated by underscores.",
"func":1
},
{
"ref":"leaf_focus.utils.get_version",
"url":9,
"doc":"Get the package version.",
"func":1
},
{
"ref":"leaf_focus.utils.parse_date",
"url":9,
"doc":"Parse a date from a string.",
"func":1
},
{
"ref":"leaf_focus.utils.validate",
"url":9,
"doc":"Validate that a value is one of the expected values.",
"func":1
},
{
"ref":"leaf_focus.utils.validate_path",
"url":9,
"doc":"Validate a path.",
"func":1
},
{
"ref":"leaf_focus.utils.select_exe",
"url":9,
"doc":"Select the executable path based on the platform.",
"func":1
},
{
"ref":"leaf_focus.utils.output_root",
"url":9,
"doc":"Build the path to the output.",
"func":1
},
{
"ref":"leaf_focus.utils.str_norm",
"url":9,
"doc":"Normalise a string into the 'slug' format.",
"func":1
},
{
"ref":"leaf_focus.utils.CustomJsonEncoder",
"url":9,
"doc":"A custom json encoder. Constructor for JSONEncoder, with sensible defaults. If skipkeys is false, then it is a TypeError to attempt encoding of keys that are not str, int, float or None. If skipkeys is True, such items are simply skipped. If ensure_ascii is true, the output is guaranteed to be str objects with all incoming non-ASCII characters escaped. If ensure_ascii is false, the output can contain non-ASCII characters. If check_circular is true, then lists, dicts, and custom encoded objects will be checked for circular references during encoding to prevent an infinite recursion (which would cause an RecursionError). Otherwise, no such check takes place. If allow_nan is true, then NaN, Infinity, and -Infinity will be encoded as such. This behavior is not JSON specification compliant, but is consistent with most JavaScript based encoders and decoders. Otherwise, it will be a ValueError to encode such floats. If sort_keys is true, then the output of dictionaries will be sorted by key; this is useful for regression tests to ensure that JSON serializations can be compared on a day-to-day basis. If indent is a non-negative integer, then JSON array elements and object members will be pretty-printed with that indent level. An indent level of 0 will only insert newlines. None is the most compact representation. If specified, separators should be an (item_separator, key_separator) tuple. The default is (', ', ': ') if  indent is  None and (',', ': ') otherwise. To get the most compact JSON representation, you should specify (',', ':') to eliminate whitespace. If specified, default is a function that gets called for objects that can't otherwise be serialized. It should return a JSON encodable version of the object or raise a  TypeError ."
},
{
"ref":"leaf_focus.utils.CustomJsonEncoder.default",
"url":9,
"doc":"Conversion used by default.",
"func":1
},
{
"ref":"leaf_focus.utils.XmlElement",
"url":9,
"doc":"A simple xml element.  text  . tail"
},
{
"ref":"leaf_focus.utils.XmlElement.attrib",
"url":9,
"doc":""
},
{
"ref":"leaf_focus.utils.XmlElement.tag",
"url":9,
"doc":""
},
{
"ref":"leaf_focus.utils.XmlElement.name_space",
"url":9,
"doc":""
},
{
"ref":"leaf_focus.utils.XmlElement.text",
"url":9,
"doc":""
},
{
"ref":"leaf_focus.utils.XmlElement.tail",
"url":9,
"doc":""
},
{
"ref":"leaf_focus.utils.XmlElement.children",
"url":9,
"doc":""
},
{
"ref":"leaf_focus.utils.XmlElement.to_dict",
"url":9,
"doc":"Convert xml element to a dict.",
"func":1
},
{
"ref":"leaf_focus.utils.xml_to_element",
"url":9,
"doc":"Convert xml into nested dicts.",
"func":1
},
{
"ref":"leaf_focus.utils.xml_tag_ns",
"url":9,
"doc":"Get the XML namespace and name. Args: value: The combined namespace and name Returns: The separate namespace and name",
"func":1
},
{
"ref":"leaf_focus.utils.LeafFocusException",
"url":9,
"doc":"A custom error."
}
]