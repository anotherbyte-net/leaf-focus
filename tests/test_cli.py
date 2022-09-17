import logging
import shutil

from importlib_resources import as_file, files

from leaf_focus.cli import main


def test_cli_pdf_ocr_existing_files(capsys, caplog, tmp_path, resource_example1):
    output_dir = tmp_path / "output-dir"
    output_dir.mkdir(exist_ok=True, parents=True)

    package = resource_example1["package"]
    package_path = files(package)

    pdf_name = resource_example1["pdf"]
    normalised_stem = resource_example1["normalised_stem"]

    with as_file(package_path.joinpath(pdf_name)) as p:
        shutil.copyfile(p, output_dir / p.name)
    with as_file(package_path.joinpath(resource_example1["page_22_image"])) as p:
        shutil.copyfile(p, output_dir / p.name)
    with as_file(package_path.joinpath(resource_example1["info"])) as p:
        shutil.copyfile(p, output_dir / p.name)
    with as_file(package_path.joinpath(resource_example1["embedded_text"])) as p:
        shutil.copyfile(
            p, output_dir / f"{normalised_stem}-output-f-22-l-22-layout-eol-dos.txt"
        )
    with as_file(package_path.joinpath(resource_example1["page_22_annotations"])) as p:
        shutil.copyfile(p, output_dir / p.name)
    with as_file(package_path.joinpath(resource_example1["page_22_predictions"])) as p:
        predictions_file = output_dir / p.name
        shutil.copyfile(p, predictions_file)

    exe_dir = tmp_path / "exe_dir"
    exe_dir.mkdir(parents=True, exist_ok=True)

    caplog.set_level(logging.DEBUG)

    result = main(
        [
            str(output_dir / pdf_name),
            str(output_dir),
            "--exe-dir",
            str(exe_dir),
            "--ocr",
            "--first",
            "22",
            "--last",
            "22",
            "--log-level",
            "debug",
        ]
    )

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

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
        (
            "leaf_focus.ocr.keras_ocr",
            10,
            f"Predictions and annotations files already exist for '{resource_example1['page_22_image_stem']}'.",
        ),
        ("leaf_focus.ocr.model", 10, "Loading OCR output items."),
        (
            "leaf_focus.ocr.model",
            10,
            f"Loaded 304 OCR items from '{predictions_file}'.",
        ),
        ("leaf_focus.ocr.model", 10, "Arranging text into lines."),
    ]
    assert caplog.record_tuples[-1][0] == "leaf_focus.app"
    assert caplog.record_tuples[-1][1] == 20
    assert caplog.record_tuples[-1][2].startswith("Finished (duration 0:00:0")

    assert result == 0
