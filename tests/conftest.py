import pytest


@pytest.fixture
def resource_example1():
    orig = "452.06-win10-win8-win7-release-notes"
    norm = "452-06-win10-win8-win7-release-notes"
    return {
        "package": "tests.resources.example1",
        "pdf": f"{orig}.pdf",
        "page_22_image": f"{norm}-page-image-gray-000022.png",
        "info": f"{norm}-info.json",
        "embedded_text": f"{norm}-output-layout-eol-dos.txt",
        "page_22_annotations": f"{norm}-page-image-gray-000022-annotations.png",
        "page_22_predictions": f"{norm}-page-image-gray-000022-predictions.csv",
    }
