import os
import pathlib
from datetime import datetime
from importlib.resources import path

import pytest

from leaf_focus import model, program

test_file = ("tests.resources", "452.06-win10-win8-win7-release-notes.pdf")


@pytest.mark.skipif(
    not os.getenv("XPDF_EXE_DIR")
    or not pathlib.Path(os.getenv("XPDF_EXE_DIR")).exists(),
    reason="Requires xpdf executable pdfinfo",
)
def test_xpdf_info():
    with path(*test_file) as p:
        pdf_path = p

    exe_dir = pathlib.Path(os.getenv("XPDF_EXE_DIR"))
    prog = program.XpdfProgram(exe_dir)
    args = model.XpdfInfoArgs(include_page_bounding_boxes=True, include_metadata=True)
    result = prog.info(pdf_path, args)

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
    not os.getenv("XPDF_EXE_DIR")
    or not pathlib.Path(os.getenv("XPDF_EXE_DIR")).exists(),
    reason="Requires xpdf executable pdftotext",
)
def test_xpdf_text(tmp_path):
    with path(*test_file) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("XPDF_EXE_DIR"))

    prog = program.XpdfProgram(exe_dir)
    args = model.XpdfTextArgs(
        line_end_type="dos",
        use_verbose=True,
        use_simple2_layout=True,
    )
    result = prog.text(pdf_path, output_path, args)

    assert result.output_path.read_text().startswith(
        "Release 450 Driver for Windows, Version"
    )


@pytest.mark.skipif(
    not os.getenv("XPDF_EXE_DIR")
    or not pathlib.Path(os.getenv("XPDF_EXE_DIR")).exists(),
    reason="Requires xpdf executable pdftopng",
)
@pytest.mark.skipif(
    os.getenv("TEST_INCLUDE_SLOW") != "true",
    reason="This is a slow test, specify env var 'TEST_INCLUDE_SLOW=true' to run it",
)
def test_xpdf_image(tmp_path):
    with path(*test_file) as p:
        pdf_path = p

    output_path = tmp_path / "output-dir"
    output_path.mkdir(exist_ok=True, parents=True)

    exe_dir = pathlib.Path(os.getenv("XPDF_EXE_DIR"))

    prog = program.XpdfProgram(exe_dir)
    args = model.XpdfImageArgs()
    result = prog.image(pdf_path, output_path, args)

    assert result.output_dir
    assert len(result.output_files) == 42
