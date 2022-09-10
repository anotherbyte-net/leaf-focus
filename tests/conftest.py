import pytest


@pytest.fixture
def resource_example1():
    orig = "452.06-win10-win8-win7-release-notes"
    norm = "452-06-win10-win8-win7-release-notes"
    return {
        "package": "tests.resources.example1",
        "original_stem": orig,
        "normalised_stem": norm,
        "pdf": f"{orig}.pdf",
        "page_22_image": f"{norm}-page-image-gray-000022.png",
        "info": f"{norm}-info.json",
        "embedded_text": f"{norm}-output-layout-eol-dos.txt",
        "page_22_annotations": f"{norm}-page-image-gray-000022-annotations.png",
        "page_22_predictions": f"{norm}-page-image-gray-000022-predictions.csv",
        "metadata": {
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
                                            "children": [
                                                {"name": "li", "value": "ccampa"}
                                            ],
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
        },
    }
