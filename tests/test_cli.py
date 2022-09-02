import logging
import os

import pytest

from leaf_focus import cli


def test_cli_no_args(capsys, caplog):
    with pytest.raises(SystemExit, match="2"):
        cli.main([])

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == (
        "usage: leaf-focus [-h] exe_dir input_pdf output_dir\n"
        "leaf-focus: error: the following arguments are required: exe_dir, input_pdf, "
        "output_dir\n"
    )
    assert caplog.record_tuples == []


def test_cli_with_exe_no_input_output(capsys, caplog):
    with pytest.raises(SystemExit, match="2"):
        cli.main(["exe-dir"])

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == (
        "usage: leaf-focus [-h] exe_dir input_pdf output_dir\n"
        "leaf-focus: error: the following arguments are required: input_pdf, "
        "output_dir\n"
    )
    assert caplog.record_tuples == []


def test_cli_with_exe_input_no_output(capsys, caplog):
    with pytest.raises(SystemExit, match="2"):
        cli.main(["exe-dir", "input-pdf-arg"])

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == (
        "usage: leaf-focus [-h] exe_dir input_pdf output_dir\n"
        "leaf-focus: error: the following arguments are required: output_dir\n"
    )
    assert caplog.record_tuples == []


def test_cli_with_exe_input_output_invalid_exe(capsys, caplog):
    result = cli.main(["exe-dir", "input-pdf-arg", "output-dir-arg"])
    assert result == 1

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""
    assert caplog.record_tuples == [
        (
            "leaf_focus",
            logging.ERROR,
            "Error: LeafFocusException - Could not find the exe dir: 'exe-dir'.",
        )
    ]


def test_cli_with_exe_input_output_invalid_input(capsys, tmp_path, caplog):
    exe_dir = tmp_path / "exe_dir"
    exe_dir.mkdir(parents=True, exist_ok=True)

    result = cli.main([str(exe_dir), "input-pdf-arg", "output-dir-arg"])
    assert result == 1

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""
    assert caplog.record_tuples == [
        (
            "leaf_focus",
            logging.ERROR,
            "Error: LeafFocusException - Could not find the input pdf file: "
            "'input-pdf-arg'.",
        )
    ]


def test_cli_with_exe_input_output_invalid_output(capsys, tmp_path, caplog):
    exe_dir = tmp_path / "exe_dir"
    exe_dir.mkdir(parents=True, exist_ok=True)

    input_file = tmp_path / "input-file"
    input_file.touch()

    output_dir = tmp_path / "?~!@#$%^&*()_+-=<>?,./;:'{}[]"

    caplog.set_level(logging.INFO)

    result = cli.main([str(exe_dir), str(input_file), str(output_dir)])
    assert result == 2

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""
    assert len(caplog.record_tuples) == 3
    assert caplog.record_tuples[0] == (
        "leaf_focus.app",
        logging.INFO,
        "Starting leaf-focus",
    )
    assert caplog.record_tuples[1] == (
        "leaf_focus.app",
        logging.WARNING,
        f"Creating output directory '{output_dir}'.",
    )
    assert caplog.record_tuples[2][0] == "leaf_focus"
    assert caplog.record_tuples[2][1] == logging.ERROR
    assert "Error: OSError" in caplog.record_tuples[2][2]


def test_cli_with_exe_input_output_valid_with_invalid_input(capsys, tmp_path, caplog):
    exe_dir = tmp_path / "exe_dir"
    exe_dir.mkdir(parents=True, exist_ok=True)

    input_file = tmp_path / "input-file"
    input_file.touch()

    output_dir = tmp_path / "output-dir"

    caplog.set_level(logging.INFO)

    result = cli.main([str(exe_dir), str(input_file), str(output_dir)])
    assert result == 0

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""
    assert caplog.record_tuples == [
        ("leaf_focus.app", logging.INFO, "Starting leaf-focus"),
        (
            "leaf_focus.app",
            logging.WARNING,
            f"Creating output directory '{output_dir}'.",
        ),
        ("leaf_focus.app", logging.INFO, "Finished"),
    ]
