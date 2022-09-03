import dataclasses
import typing
from xml.etree.ElementTree import Element


@dataclasses.dataclass
class XmlElement:
    """
    A simple xml element.

    <tag attrib>text<child/>...</tag>tail
    """

    attrib: typing.Collection[typing.Tuple[str, str, str]]
    tag: str
    ns: str
    text: str
    tail: str
    children: typing.Collection["XmlElement"]

    def to_dict(self):
        result = {"name": self.tag.strip()}

        value = ((self.text or "").strip() + " " + (self.tail or "").strip()).strip()
        if value:
            result["value"] = value

        attributes = {k.strip(): (v or "").strip() for n, k, v, in self.attrib}
        if attributes:
            result["attributes"] = attributes

        children = [i.to_dict() for i in self.children]
        if children:
            result["children"] = children

        return result

    def __str__(self):
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


def xml_to_dict(element: Element):
    """turn xml into nested dicts"""

    attrib = element.attrib or {}
    tag = element.tag
    text = element.text
    tail = element.tail
    children = []

    for child in element:
        children.append(xml_to_dict(child))

    tag_ns, tag_name = xml_tag_ns(tag)

    attrib_ns = []
    for k, v in attrib.items():
        ns, t = xml_tag_ns(k)
        attrib_ns.append((ns, t, v))

    item = XmlElement(
        attrib=attrib_ns,
        tag=tag_name,
        ns=tag_ns,
        text=text,
        tail=tail,
        children=children,
    )

    return item


def xml_tag_ns(value: str):
    if "}" in value:
        ns, name = value.rsplit("}", maxsplit=1)
        ns = ns.strip("{}")
    else:
        ns = ""
        name = value

    return ns, name
