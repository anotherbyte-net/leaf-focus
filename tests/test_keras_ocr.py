import os
from importlib.resources import path

import pytest

from leaf_focus.ocr import keras_ocr


@pytest.mark.skipif(
    os.getenv("TEST_INCLUDE_SLOW") != "true",
    reason="This is a slow test, specify env var 'TEST_INCLUDE_SLOW=true' to run it",
)
def test_keras_ocr_image(test_pdf_page_image_info, tmp_path, capsys):
    with path(*test_pdf_page_image_info) as p:
        image_file = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    prog = keras_ocr.OpticalCharacterRecognition()
    result = prog.recognise_text(image_file, output_path)

    expected_lines = 33
    assert len(result.items) == expected_lines

    assert result.annotations_file.stat().st_size > 0
    assert len(result.predictions_file.read_text().splitlines()) == 305

    stdout, stderr = capsys.readouterr()

    assert "craft_mlt_25k.h5" in stdout
    assert "crnn_kurapan.h5" in stdout
    assert "Saving OCR image to" in stdout
    assert "Saving OCR predictions to" in stdout
    assert "Arranging text into lines." in stdout

    assert stderr == ""
