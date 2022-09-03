import pathlib
import platform
import typing
from datetime import datetime


def parse_date(value: str) -> typing.Optional[datetime]:
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


def validate(name: str, value, expected: typing.List):
    """Validate that a value is one of the expected values."""

    if value is not None and value not in expected:
        opts = ", ".join(sorted([str(i) for i in expected]))
        raise ValueError(f"Invalid {name} '{value}'. Expected one of '{opts}'.")


def select_exe(path: pathlib.Path) -> pathlib.Path:
    """Select the executable path based on the platform."""

    if platform.system() == "Windows":
        path = path.with_suffix(".exe")

    if not path.exists():
        raise FileNotFoundError(str(path))

    return path


def output_root(
    output_type: str,
    output_path: pathlib.Path,
    additional: typing.Optional[typing.Collection[str]] = None,
):
    file_date = datetime.utcnow().isoformat(timespec="seconds").replace(":", "-")

    add_str = "-".join([i.strip("-") for i in (additional or [])])
    add_str = add_str.replace(".", "-").replace("_", "-")

    items = [i for i in [file_date, output_type, add_str] if i]

    name = "-".join(items)
    output = output_path / name

    return output
