"""Small utility functions."""

from __future__ import annotations

import dataclasses
import json
import logging
import pathlib
import platform
import re
import unicodedata

from datetime import date, datetime, time, timezone
from enum import Enum
from xml.etree.ElementTree import Element

from beartype import beartype, typing
from importlib_metadata import PackageNotFoundError, distribution
from importlib_resources import as_file, files


logger = logging.getLogger(__name__)


@beartype
def get_name_dash() -> str:
    """Get the package name with word separated by dashes."""
    return "leaf-focus"


@beartype
def get_name_under() -> str:
    """Get the package name with word separated by underscores."""
    return "leaf_focus"


@beartype
def get_version() -> str | None:
    """Get the package version."""
    try:
        dist = distribution(get_name_dash())
    except PackageNotFoundError:
        pass

    else:
        return str(dist.version)

    try:
        with as_file(files(get_name_under()).joinpath("cli.py")) as file_path:
            version_text = (file_path.parent.parent.parent / "VERSION").read_text()
            return str(version_text.strip())
    except FileNotFoundError:
        pass

    return None


@beartype
def parse_date(value: str) -> datetime | None:
    """Parse a date from a string."""
    formats = [
        # e.g. 'Thu Aug 13 11:09:00 2020'
        "%a %b %d %H:%M:%S %Y",
        # e.g. '2011-11-04T00:05:23Z'
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:  # noqa: PERF203
            logger.debug("Value '%s' did not match date format '%s'.", value, fmt)
    return None


@beartype
def validate(
    name: str, value: str | int | None, expected: typing.Iterable[str | int | None]
) -> None:
    """Validate that a value is one of the expected values."""
    if value is not None and value not in expected:
        opts = ", ".join(sorted([str(i) for i in expected]))
        msg = f"Invalid {name} '{value}'. Expected one of '{opts}'."
        raise LeafFocusError(msg)


@beartype
class ValidatePathMethod(Enum):
    """Options for how to validate a path."""

    NO_OPINION = 0
    MUST_EXIST = 1


@beartype
def validate_path(
    name: str,
    value: pathlib.Path,
    must_exist: ValidatePathMethod = ValidatePathMethod.NO_OPINION,
) -> pathlib.Path:
    """Validate a path."""
    if not value:
        msg = f"Must provide path {name}."
        raise LeafFocusError(msg)

    try:
        if must_exist == ValidatePathMethod.MUST_EXIST:
            abs_path = value.resolve(strict=True)
        else:
            abs_path = value.absolute()

    except Exception as error:
        msg = f"Invalid path '{value}'."
        raise LeafFocusError(msg) from error

    else:
        return abs_path


@beartype
def validate_pages(first_page: int | None, last_page: int | None) -> None:
    """Validate the page range.

    Args:
        first_page: The first page.
        last_page: The last page.

    Returns:
        None
    """
    if first_page is None or last_page is None:
        return
    if first_page > last_page:
        msg = (
            f"First page ({first_page}) must be less than or equal "
            f"to last page ({last_page})."
        )
        raise LeafFocusError(msg)


@beartype
def select_exe(value: pathlib.Path) -> pathlib.Path:
    """Select the executable path based on the platform."""
    if platform.system() == "Windows":
        value = value.with_suffix(".exe")

    if not value.exists():
        msg = f"Exe file not found '{value}'."
        raise LeafFocusError(msg) from FileNotFoundError(value)

    return value


@beartype
def output_root(
    input_file: pathlib.Path,
    output_type: str,
    output_path: pathlib.Path,
    additional: typing.Collection[str] | None = None,
) -> pathlib.Path:
    """Build the path to the output."""
    name_parts = [input_file.stem, output_type]
    name_parts.extend(additional or [])
    name_parts = [str(i) for i in name_parts if i is not None]
    name_parts = [str_norm(i.strip("-")) for i in name_parts if i and i.strip()]

    name = "-".join(name_parts)

    output = output_path / name

    return output


_slug_re_1 = re.compile(r"[^\w\s-]")
_slug_re_2 = re.compile(r"[-\s]+")


@beartype
def str_norm(value: str) -> str:
    """Normalise a string into the 'slug' format."""
    separator = "-"
    encoding = "utf-8"

    norm = unicodedata.normalize("NFKD", value)
    enc = norm.encode(encoding, "ignore")
    de_enc = enc.decode(encoding)
    alpha_num_only = _slug_re_1.sub("", de_enc)
    alpha_num_tidy = alpha_num_only.strip().lower()
    result = _slug_re_2.sub(separator, alpha_num_tidy)
    return result


class IsDataclass(typing.Protocol):
    """A protocol to allow typing for dataclasses."""

    __dataclass_fields__: typing.ClassVar[dict[str, typing.Any]]


@beartype
class CustomJsonEncoder(json.JSONEncoder):
    """A custom json encoder."""

    def default(self, o: IsDataclass | datetime | date | time) -> str | typing.Any:
        """Conversion used by default."""
        if isinstance(o, datetime | date | time):
            return o.isoformat()

        return super().default(o)


@beartype
@dataclasses.dataclass
class XmlElement:
    """A simple xml element.

    <tag attrib>text<child/>...</tag>tail
    """

    attrib: typing.Collection[tuple[str, str, str]]
    tag: str
    name_space: str
    text: str
    tail: str
    children: typing.Collection[XmlElement]

    def to_dict(self) -> dict[str, typing.Any]:
        """Convert xml element to a dict."""
        result: dict[str, typing.Any] = {"name": self.tag.strip()}

        value = ((self.text or "").strip() + " " + (self.tail or "").strip()).strip()
        if value:
            result["value"] = value

        attributes = {k.strip(): (v or "").strip() for n, k, v in self.attrib}
        if attributes:
            result["attributes"] = attributes

        children = [i.to_dict() for i in self.children]
        if children:
            result["children"] = children

        return result

    def __str__(self) -> str:
        """Convert to a string."""
        tag1 = (self.tag or "").strip()
        tag2 = f"</{tag1}>"
        text = (self.text or "").strip()
        tail = (self.tail or "").strip()

        count = len(self.children)
        if count == 0:
            children = ""
        elif count == 1:
            children = "(1 child)"
        else:
            children = f"({count} children)"

        if text and children:
            children = " " + children

        if not text and not children:
            tag2 = ""

        count_attrib = len(self.attrib)
        if count_attrib == 0:
            attrib = ""
        elif count_attrib == 1:
            attrib = " (1 attribute)"
        else:
            attrib = f" ({count} attributes)"

        return f"<{tag1}{attrib}>{text}{children}{tag2}{tail}"


@beartype
def xml_to_element(element: Element) -> XmlElement:
    """Convert xml into nested dicts."""
    attrib = element.attrib or {}
    tag = element.tag
    text = element.text
    tail = element.tail

    children = [xml_to_element(child) for child in element]

    tag_ns, tag_name = xml_tag_ns(tag)

    attrib_ns = []
    for key, value in attrib.items():
        extracted_ns, extracted_tag = xml_tag_ns(key)
        attrib_ns.append((extracted_ns, extracted_tag, value))

    item = XmlElement(
        attrib=attrib_ns,
        tag=tag_name,
        name_space=tag_ns,
        text=text or "",
        tail=tail or "",
        children=children,
    )

    return item


@beartype
def xml_tag_ns(value: str) -> tuple[str, str]:
    """Get the XML namespace and name.

    Args:
        value: The combined namespace and name

    Returns:
        The separate namespace and name
    """
    if "}" in value:
        name_space, name = value.rsplit("}", maxsplit=1)
        name_space = name_space.strip("{}")
    else:
        name_space = ""
        name = value

    return name_space, name


@beartype
class LeafFocusError(Exception):
    """A custom error for leaf focus."""
