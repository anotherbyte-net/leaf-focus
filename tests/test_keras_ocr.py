import pathlib
import sys

import pytest
from importlib_resources import as_file, files

from helper import check_skip_slow, check_skip_slow_msg, keras_max_version_minor
from leaf_focus import utils
from leaf_focus.ocr.keras_ocr import OpticalCharacterRecognition
from leaf_focus.ocr.model import TextItem


@pytest.mark.skipif(check_skip_slow(), reason=check_skip_slow_msg)
def test_keras_ocr_image_with_tensorflow(capsys, caplog, resource_example1, tmp_path):
    package = resource_example1["package"]
    package_path = files(package)

    pdf_pg22_image = resource_example1["page_22_image"]
    with as_file(package_path.joinpath(pdf_pg22_image)) as p:
        image_file = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    prog = OpticalCharacterRecognition()

    if sys.version_info.major == 3 and sys.version_info.minor > keras_max_version_minor:
        with pytest.raises(
            utils.LeafFocusException, match="Cannot run ocr on this Python version."
        ):
            prog.recognise_text(image_file, output_path)

    else:
        result = prog.recognise_text(image_file, output_path)
        expected_lines = 33
        expected_items = 300
        assert len(result.items) == expected_lines
        assert len([item for line in result.items for item in line]) == expected_items

        loaded_items = list(TextItem.load(result.predictions_file))
        loaded_items = TextItem.order_text_lines(loaded_items)

        assert len(loaded_items) == expected_lines
        assert len([item for line in loaded_items for item in line]) == expected_items

        stdout, stderr = capsys.readouterr()

        assert "craft_mlt_25k.h5" in stdout
        assert "crnn_kurapan.h5" in stdout

        assert stderr == ""

        assert caplog.record_tuples == []


def test_keras_ocr_image_without_tensorflow(
    capsys, caplog, resource_example1, tmp_path, monkeypatch
):
    package = resource_example1["package"]
    package_path = files(package)

    pdf_pg22_image = resource_example1["page_22_image"]
    with as_file(package_path.joinpath(pdf_pg22_image)) as p:
        image_file = p

    pdf_pg22_pred = resource_example1["page_22_predictions"]
    with as_file(package_path.joinpath(pdf_pg22_pred)) as p:
        pred_file = p

    pdf_pg22_anno = resource_example1["page_22_annotations"]
    with as_file(package_path.joinpath(pdf_pg22_anno)) as p:
        anno_file = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    prog = OpticalCharacterRecognition()

    if sys.version_info.major == 3 and sys.version_info.minor > keras_max_version_minor:
        with pytest.raises(
            utils.LeafFocusException, match="Cannot run ocr on this Python version."
        ):
            prog.recognise_text(image_file, output_path)

    else:

        def mock_engine_create():
            pass

        monkeypatch.setattr(prog, "engine_create", mock_engine_create)

        def mock_engine_run(image_path: pathlib.Path):
            import cv2

            image = cv2.imread(str(image_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            prediction_groups = TextItem.load(pred_file)
            prediction_groups = [i.to_prediction for i in prediction_groups]
            return [image], [prediction_groups]

        monkeypatch.setattr(prog, "engine_run", mock_engine_run)

        def mock_engine_annotate(image, predictions, axis):
            pass

        monkeypatch.setattr(prog, "engine_annotate", mock_engine_annotate)

        result = prog.recognise_text(image_file, output_path)
        expected_lines = 33
        expected_items = 300
        assert len(result.items) == expected_lines
        assert len([item for line in result.items for item in line]) == expected_items

        loaded_items = list(TextItem.load(result.predictions_file))
        loaded_items = TextItem.order_text_lines(loaded_items)

        assert len(loaded_items) == expected_lines
        assert len([item for line in loaded_items for item in line]) == expected_items

        stdout, stderr = capsys.readouterr()

        assert stdout == ""
        assert stderr == ""

        output_annotated_png = output_path / anno_file.name
        assert output_annotated_png.exists()
        assert output_annotated_png.stat().st_size > 0

        assert caplog.record_tuples == []
