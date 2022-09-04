import logging
import os
import pathlib
import platform
import shutil
import sys
from datetime import datetime
from importlib.resources import path

import pytest

from leaf_focus import utils
from leaf_focus.cli import main
from leaf_focus.ocr.keras_ocr import OpticalCharacterRecognition
from leaf_focus.ocr.model import TextItem
from leaf_focus.pdf.model import XpdfImageArgs, XpdfInfoArgs, XpdfTextArgs
from leaf_focus.pdf.xpdf import XpdfProgram


@pytest.mark.skipif(
    not os.getenv("TEST_XPDF_EXE_DIR")
    or not pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR")).exists(),
    reason="Requires xpdf executable pdfinfo",
)
def test_xpdf_info(resource_example1, tmp_path):
    package = resource_example1["package"]
    pdf_file = resource_example1["pdf"]
    with path(package, pdf_file) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR"))
    prog = XpdfProgram(exe_dir)
    args = XpdfInfoArgs(include_page_bounding_boxes=True, include_metadata=True)
    result = prog.info(pdf_path, output_path, args)

    assert result.title == "BkNVR450_Win7.book"
    assert not result.subject
    assert not result.keywords
    assert result.author == "ccampa"
    assert result.creator == "FrameMaker 2019.0.4"
    assert result.producer == "Acrobat Distiller 20.0 (Windows)"
    assert result.creation_date == datetime(2020, 8, 13, 11, 9, 0)
    assert result.modification_date == datetime(2020, 8, 14, 14, 58, 43)
    assert result.tagged is False
    assert result.form == "none"
    assert result.pages == 42
    assert result.encrypted is False
    assert result.page_size == "612 x 792 pts (letter) (rotated 0 degrees)"
    assert result.media_box == "0.00     0.00   612.00   792.00"
    assert result.crop_box == "0.00     0.00   612.00   792.00"
    assert result.bleed_box == "0.00     0.00   612.00   792.00"
    assert result.trim_box == "0.00     0.00   612.00   792.00"
    assert result.art_box == "0.00     0.00   612.00   792.00"
    assert result.file_size_bytes == 275855
    assert result.optimized is True
    assert result.pdf_version == "1.5"

    assert result.metadata == {
        "attributes": {
            "xmptk": "Adobe XMP Core 5.6-c017 91.164374, 2020/03/05-20:41:30"
        },
        "children": [
            {
                "children": [
                    {
                        "attributes": {"about": ""},
                        "children": [
                            {"name": "CreatorTool", "value": "FrameMaker 2019.0.4"},
                            {
                                "name": "ModifyDate",
                                "value": "2020-08-14T14:58:43-07:00",
                            },
                            {"name": "CreateDate", "value": "2020-08-13T11:09Z"},
                            {
                                "name": "MetadataDate",
                                "value": "2020-08-14T14:58:43-07:00",
                            },
                            {"name": "format", "value": "application/pdf"},
                            {
                                "children": [
                                    {
                                        "children": [
                                            {
                                                "attributes": {"lang": "x-default"},
                                                "name": "li",
                                                "value": "BkNVR450_Win7.book",
                                            }
                                        ],
                                        "name": "Alt",
                                    }
                                ],
                                "name": "title",
                            },
                            {
                                "children": [
                                    {
                                        "children": [{"name": "li", "value": "ccampa"}],
                                        "name": "Seq",
                                    }
                                ],
                                "name": "creator",
                            },
                            {
                                "name": "Producer",
                                "value": "Acrobat Distiller 20.0 " "(Windows)",
                            },
                            {
                                "name": "DocumentID",
                                "value": "uuid:00610876-6f52-4cf5-80eb-06b821bd1586",
                            },
                            {
                                "name": "InstanceID",
                                "value": "uuid:155960e2-0900-46e3-8d6c-c02b0a9feb4e",
                            },
                        ],
                        "name": "Description",
                    }
                ],
                "name": "RDF",
            }
        ],
        "name": "xmpmeta",
    }


@pytest.mark.skipif(
    not os.getenv("TEST_XPDF_EXE_DIR")
    or not pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR")).exists(),
    reason="Requires xpdf executable pdftotext",
)
def test_xpdf_text(resource_example1, tmp_path):
    package = resource_example1["package"]
    pdf = resource_example1["pdf"]
    with path(package, pdf) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR"))

    prog = XpdfProgram(exe_dir)
    args = XpdfTextArgs(
        line_end_type="dos",
        use_verbose=True,
        use_simple2_layout=True,
    )
    result = prog.text(pdf_path, output_path, args)

    assert result.output_path.read_text().startswith(
        "Release 450 Driver for Windows, Version"
    )


@pytest.mark.skipif(
    not os.getenv("TEST_XPDF_EXE_DIR")
    or not pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR")).exists(),
    reason="Requires xpdf executable pdftopng",
)
@pytest.mark.skipif(
    os.getenv("TEST_INCLUDE_SLOW") != "true",
    reason="This is a slow test, specify env var 'TEST_INCLUDE_SLOW=true' to run it",
)
def test_xpdf_image(resource_example1, tmp_path):
    package = resource_example1["package"]
    pdf = resource_example1["pdf"]
    with path(package, pdf) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("TEST_XPDF_EXE_DIR"))

    prog = XpdfProgram(exe_dir)
    args = XpdfImageArgs(first_page=22, last_page=22)
    result = prog.image(pdf_path, output_path, args)

    assert result.output_dir
    assert len(result.output_files) == 1
    assert result.output_files[0].name.endswith("-000022.png")


@pytest.mark.skipif(
    os.getenv("TEST_INCLUDE_SLOW") != "true",
    reason="This is a slow test, specify env var 'TEST_INCLUDE_SLOW=true' to run it",
)
def test_keras_ocr_image(resource_example1, tmp_path, capsys):
    package = resource_example1["package"]
    pdf_pg22_image = resource_example1["page_22_image"]
    with path(package, pdf_pg22_image) as p:
        image_file = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    prog = OpticalCharacterRecognition()

    if sys.version_info.major == 3 and sys.version_info.minor > 9:
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


def test_cli_pdf_ocr_existing_files(capsys, caplog, tmp_path, resource_example1):
    output_dir = tmp_path / "output-dir"
    output_dir.mkdir(exist_ok=True, parents=True)

    package = resource_example1["package"]
    pdf_name = resource_example1["pdf"]
    with path(package, pdf_name) as p:
        shutil.copyfile(p, output_dir / p.name)
    with path(package, resource_example1["page_22_image"]) as p:
        shutil.copyfile(p, output_dir / p.name)
    with path(package, resource_example1["info"]) as p:
        shutil.copyfile(p, output_dir / p.name)
    with path(package, resource_example1["embedded_text"]) as p:
        shutil.copyfile(p, output_dir / p.name)
    with path(package, resource_example1["page_22_annotations"]) as p:
        shutil.copyfile(p, output_dir / p.name)
    with path(package, resource_example1["page_22_predictions"]) as p:
        shutil.copyfile(p, output_dir / p.name)

    exe_dir = tmp_path / "exe_dir"
    exe_dir.mkdir(parents=True, exist_ok=True)

    caplog.set_level(logging.INFO)

    result = main(
        [
            str(output_dir / pdf_name),
            str(output_dir),
            "--exe-dir",
            str(exe_dir),
            "--ocr",
        ]
    )
    assert result == 0

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

    assert len(caplog.record_tuples) == 7
    assert caplog.record_tuples[:-1] == [
        ("leaf_focus.app", 20, "Starting leaf-focus"),
        ("leaf_focus.app", 20, f"Using output directory '{output_dir}'."),
        ("leaf_focus.pdf.xpdf", 20, "Loading existing pdf info file."),
        (
            "leaf_focus.pdf.xpdf",
            20,
            "Loading extracted embedded text from existing file.",
        ),
        ("leaf_focus.pdf.xpdf", 20, "Saving each pdf page as an image."),
        ("leaf_focus.pdf.xpdf", 20, "Found existing pdf images."),
    ]
    assert caplog.record_tuples[-1][0] == "leaf_focus.app"
    assert caplog.record_tuples[-1][1] == 20
    assert caplog.record_tuples[-1][2].startswith("Finished (duration 0:00:0")
