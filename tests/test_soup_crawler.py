"""Test the pdfs from html crawl code."""

import urllib

from paper_crawler.crawl_links_soup import (
    get_icml_2023_pdf,
    get_icml_2024_pdf,
    process_link,
)


def test_icml24() -> None:
    """Check if we got all ICML papers."""
    assert len(get_icml_2024_pdf()) == 2610


def test_icml23() -> None:
    """Check if we got all ICML papers."""
    assert len(get_icml_2023_pdf()) == 1828


def check_process_no_pdf() -> None:
    """Check if no github-link returns None."""
    link = "https://proceedings.mlr.press/v139/abdolshah21a/abdolshah21a.pdf"
    assert process_link(link) is None


def test_process_link() -> None:
    """Check if the process link function works ok."""
    link = "https://proceedings.mlr.press/v139/achituve21a/achituve21a.pdf"
    assert (
        urllib.parse.urlunparse(process_link(link)[0])
        == "https://github.com/IdanAchituve/GP-Tree"
    )


def test_process_no_link() -> None:
    """Check if a paper no repo-link raises an error."""
    link = "https://proceedings.mlr.press/v139/acar21b/acar21b.pdf"
    assert process_link(link) is None
