import pytest


@pytest.fixture
def test_pdf_doc_info():
    return ("tests.resources", "452.06-win10-win8-win7-release-notes.pdf")


@pytest.fixture
def test_pdf_page_image_info():
    return ("tests.resources", "452.06-win10-win8-win7-release-notes-page-22.png")
