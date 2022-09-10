import os
import pathlib

keras_max_version_minor = 9

check_skip_xpdf_exe_dir_msg = "Test requires xpdf executable pdfinfo, specify the path using env var 'TEST_XPDF_EXE_DIR'."
check_skip_slow_msg = (
    "Test is slow, run it by specifying env var 'TEST_INCLUDE_SLOW=true'."
)


def check_skip_xpdf_exe_dir():
    test_exe_dir = os.getenv("TEST_XPDF_EXE_DIR")
    return not test_exe_dir or not pathlib.Path(test_exe_dir).exists()


def check_skip_slow():
    return os.getenv("TEST_INCLUDE_SLOW") != "true"