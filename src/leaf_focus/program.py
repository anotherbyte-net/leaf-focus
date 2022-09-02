import dataclasses
import pathlib
import platform
import subprocess
import typing
from datetime import datetime
from defusedxml import ElementTree as ET
from leaf_focus import model
from leaf_focus.utils import xml_to_dict


class XpdfProgram:
    """Interact with xpdf tools."""

    OPTS_TEXT_ENCODING = [
        "Latin1",
        "ASCII7",
        "Symbol",
        "ZapfDingbats",
        "UTF-8",
        "UCS-2",
    ]
    OPTS_TEXT_LINE_ENDING = ["unix", "dos", "mac"]
    OPTS_IMAGE_ROTATION = [0, 90, 180, 270]
    OPTS_IMAGE_FREETYPE = ["yes", "no"]
    OPTS_IMAGE_ANTI_ALIAS = ["yes", "no"]
    OPTS_IMAGE_VEC_ANTI_ALIAS = ["yes", "no"]

    def __init__(self, directory: pathlib.Path):
        """
        Create a new xpdf program class to interact with xpdf tools.

        :param directory: path to the directory containing xpdf tools
        """
        self._directory = directory

    def info(
        self, pdf_path: pathlib.Path, xpdf_args: model.XpdfInfoArgs
    ) -> model.XpdfInfoResult:
        """
        Get information from a pdf file.

        :param pdf_path: path to the pdf file
        :param xpdf_args: xpdf tool arguments
        :return: pdf file information
        """

        # validation
        enc = xpdf_args.encoding
        self.validate("text encoding", enc, self.OPTS_TEXT_ENCODING)

        if not pdf_path.exists():
            raise FileNotFoundError(str(pdf_path))

        # build command
        exe_path = self.select_exe(self._directory / "pdfinfo")
        cmd = [str(exe_path)]

        cmd_args = self.build_cmd(xpdf_args)

        cmd.extend(cmd_args)
        cmd.append(str(pdf_path.resolve()))

        # execute program
        result = subprocess.run(
            cmd, capture_output=True, check=True, timeout=30, text=True
        )
        lines = result.stdout.splitlines()

        fields_map = dict(
            [
                (field.metadata.get("leaf_focus", {}).get("name"), field)
                for field in dataclasses.fields(model.XpdfInfoResult)
            ]
        )
        metadata_line_index: typing.Optional[int] = None

        data = {i.name: None for i in fields_map.values()}
        for index, line in enumerate(lines):
            if line.startswith("Metadata:"):
                metadata_line_index = index
                break

            key, value = line.split(":", maxsplit=1)
            key = key.strip()

            field = fields_map.get(key)
            if not field:
                raise ValueError(f"Unknown pdf info key '{key}' in '{pdf_path}'.")

            data_key = field.name
            if data.get(data_key) is not None:
                raise ValueError(f"Duplicate pdf info key '{key}' in '{pdf_path}'.")

            if field.type == str or str in typing.get_args(field.type):
                value = value.strip()
            elif field.type == datetime or datetime in typing.get_args(field.type):
                value = self.parse_date(value.strip())
            elif field.type == bool or bool in typing.get_args(field.type):
                value = value.strip().lower() == "yes"
            elif field.type == int or int in typing.get_args(field.type):
                if data_key == "file_size_bytes":
                    value = value.replace(" bytes", "")
                value = int(value.strip().lower())
            else:
                raise ValueError(f"Unknown key '{key}' type '{field.type}'")

            data[data_key] = value

        # metadata
        if metadata_line_index is not None:
            start = metadata_line_index + 1
            metadata = "\n".join(lines[start:])
            root = ET.fromstring(metadata)
            data["metadata"] = xml_to_dict(root).to_dict()

        return model.XpdfInfoResult(**data)

    def text(
        self,
        pdf_path: pathlib.Path,
        output_path: pathlib.Path,
        xpdf_args: model.XpdfTextArgs,
    ) -> model.XpdfTextResult:
        """
        Get the text from a pdf file.

        :param xpdf_args:
        :param pdf_path: path to the pdf file
        :param output_path: directory to save output files
        :return: pdf file text file info
        """

        # validation
        eol = xpdf_args.line_end_type
        self.validate("end of line", eol, self.OPTS_TEXT_LINE_ENDING)

        if not pdf_path.exists():
            raise FileNotFoundError(str(pdf_path))

        # build command
        exe_path = self.select_exe(self._directory / "pdftotext")

        cmd = [str(exe_path)]
        cmd_args = self.build_cmd(xpdf_args)

        output_file = self.output_root("output", output_path, cmd_args).with_suffix(
            ".txt"
        )
        cmd.extend(cmd_args + [str(pdf_path), str(output_file)])

        # execute program
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            timeout=30,
            text=True,
        )

        return model.XpdfTextResult(
            stdout=(result.stdout or "").splitlines(),
            stderr=(result.stderr or "").splitlines(),
            output_path=output_file,
        )

    def image(
        self,
        pdf_path: pathlib.Path,
        output_path: pathlib.Path,
        xpdf_args: model.XpdfImageArgs,
    ) -> model.XpdfImageResult:
        """
        Create images of pdf pages.

        :param xpdf_args:
        :param pdf_path: path to the pdf file
        :param output_path: directory to save output files
        :return: pdf file image info
        """
        # validation
        rot = xpdf_args.rotation
        self.validate("rotation", rot, self.OPTS_IMAGE_ROTATION)

        ft = xpdf_args.free_type
        self.validate("freetype", ft, self.OPTS_IMAGE_FREETYPE)

        aa = xpdf_args.anti_aliasing
        self.validate("anti-aliasing", aa, self.OPTS_IMAGE_ANTI_ALIAS)

        aav = xpdf_args.anti_aliasing
        self.validate("vector anti-aliasing", aav, self.OPTS_IMAGE_VEC_ANTI_ALIAS)

        if not pdf_path.exists():
            raise FileNotFoundError(str(pdf_path))

        # build command
        exe_path = self.select_exe(self._directory / "pdftopng")
        cmd = [str(exe_path)]

        cmd_args = self.build_cmd(xpdf_args)

        output_dir = self.output_root("output", output_path, cmd_args)
        cmd.extend(cmd_args + [str(pdf_path), str(output_dir)])

        # execute program
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            timeout=30,
            text=True,
        )
        output_files = [
            i for i in output_dir.parent.iterdir() if i.is_file() and i.suffix == ".png"
        ]
        return model.XpdfImageResult(
            stdout=(result.stdout or "").splitlines(),
            stderr=(result.stderr or "").splitlines(),
            output_dir=output_dir,
            output_files=output_files,
        )

    def parse_date(self, value: str) -> typing.Optional[datetime]:
        """Parse a date from a string."""
        formats = [
            # e.g. 'Thu Aug 13 11:09:00 2020'
            "%a %b %d %H:%M:%S %Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        return None

    def validate(self, name: str, value, expected: typing.List):
        """Validate that a value is one of the expected values."""
        if value is not None and value not in expected:
            opts = ", ".join(sorted([str(i) for i in expected]))
            raise ValueError(f"Invalid {name} '{value}'. Expected one of '{opts}'.")

    def select_exe(self, path: pathlib.Path) -> pathlib.Path:
        if platform.system() == "Windows":
            path = path.with_suffix(".exe")

        if not path.exists():
            raise FileNotFoundError(str(path))

        return path

    def build_cmd(self, tool_args):
        """Build the command arguments from a data class."""
        arg_class = tool_args.__class__
        cmd_args = []
        for field in dataclasses.fields(arg_class):
            name = field.name
            value = getattr(tool_args, name)

            field_default = field.default

            # TODO: account for default_factory
            # field_default_factory = field.default_factory

            # validate the arg config
            cmd_key = field.metadata.get("leaf_focus", {}).get("cmd")
            if not cmd_key:
                raise ValueError(
                    f"Args incorrectly configured: missing 'cmd' for '{name}'."
                )

            cmd_type = field.metadata.get("leaf_focus", {}).get("cmd_type")
            if not cmd_type:
                raise ValueError(
                    f"Args incorrectly configured: missing 'cmd_type' for '{name}'."
                )

            # add the arg
            if cmd_type == "bool":
                if value is not None and value is not True and value is not False:
                    raise ValueError(
                        f"Argument '{name}' must be None, True, or False, "
                        f"not '{value}'."
                    )

                if value is True:
                    cmd_args.extend([cmd_key])

            elif cmd_type == "single":
                if field_default is None and value is not None:
                    cmd_args.extend([cmd_key, value])
                elif field_default != value:
                    cmd_args.extend([cmd_key, value])

            else:
                raise ValueError(
                    f"Argument '{name}' has unknown cmd_type '{cmd_type}'. "
                    f"Expected one of 'bool, single'."
                )

        return cmd_args

    def output_root(
        self,
        output_type: str,
        output_path: pathlib.Path,
        cmd_args: typing.Collection[str],
    ):
        file_date = datetime.utcnow().isoformat(timespec="seconds").replace(":", "-")

        cmd_str = "-".join([i.strip("-") for i in cmd_args])
        cmd_str = cmd_str.replace(".", "-").replace("_", "-")

        items = [i for i in [file_date, output_type, cmd_str] if i]

        name = "-".join(items)
        output = output_path / name

        return output
