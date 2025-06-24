"""Test the jmlr link scraping code."""

import urllib

from paper_crawler.crawl_jmlr import _parse_links, mloss_link, tmlr_link


def test_tmlr() -> None:
    """Check if tmlr links work."""
    links = _parse_links(tmlr_link)
    assert isinstance(links[0][0], urllib.parse.ParseResult)


def test_mloss() -> None:
    """Check if mloss link crawl code runs."""
    links = _parse_links(mloss_link)
    assert isinstance(links[0][0], urllib.parse.ParseResult)
