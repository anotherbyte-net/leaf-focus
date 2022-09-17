import os
import pathlib
import typing

from leaf_focus.pdf.model import XpdfTextArgs
from leaf_focus.utils import str_norm

keras_max_version_minor = 9

check_skip_xpdf_exe_dir_msg = (
    "This test requires xpdf executables, "
    "run it by specifying the dir using env var 'TEST_XPDF_EXE_DIR'."
)
check_skip_slow_msg = (
    "This test is slow, run it by specifying env var 'TEST_INCLUDE_SLOW=true'."
)


def check_skip_xpdf_exe_dir():
    test_exe_dir = os.getenv("TEST_XPDF_EXE_DIR")
    return not test_exe_dir or not pathlib.Path(test_exe_dir).exists()


def check_skip_slow():
    return os.getenv("TEST_INCLUDE_SLOW") != "true"


class OutputFile:
    def __init__(self, package: str, prefix: str, metadata: dict):
        self._package = package
        self._prefix = prefix
        self._prefix_norm = str_norm(prefix)
        self._metadata = metadata

    @property
    def package(self):
        return self._package

    @property
    def prefix(self):
        return self._prefix

    @property
    def prefix_norm(self):
        return self._prefix_norm

    @property
    def metadata(self):
        return self._metadata

    @property
    def pdf_name(self):
        return f"{self._prefix}.pdf"

    @property
    def info_name(self):
        return f"{self._prefix_norm}-info.json"

    def text_name(
        self,
        page_first: typing.Optional[int] = None,
        page_last: typing.Optional[int] = None,
    ):
        extra = []
        if page_first is not None:
            extra.extend(["f", str(page_first)])
        if page_last is not None:
            extra.extend(["l", str(page_last)])
        if extra:
            extra = f"-{'-'.join(extra)}"

        eol = XpdfTextArgs.get_line_ending()

        return f"{self._prefix_norm}-output{extra}-layout-eol-{eol}.txt"

    @property
    def image_stem(self):
        return f"{self._prefix_norm}-page-image-gray"

    def page_image_stem(self, page: int):
        return f"{self.image_stem}-{page:06}"

    def page_image(self, page: int):
        return f"{self.page_image_stem(page)}.png"

    def page_annotations(self, page: int):
        return f"{self.page_image_stem(page)}-annotations.png"

    def page_predictions(self, page: int):
        return f"{self.page_image_stem(page)}-predictions.csv"
