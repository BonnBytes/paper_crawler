"""Test the pdfs from html crawl code."""

from paper_crawler.crawl_links_soup import get_icml_2024_pdf


def test_icml24() -> None:
    """Check if we got all ICML papers."""
    assert len(get_icml_2024_pdf()) == 2610

