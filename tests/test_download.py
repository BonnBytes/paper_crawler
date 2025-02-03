"""Test the download code frome the 'filter_and_download_links' module."""

import urllib

from paper_crawler.filter_and_download_links import process_repo_link


def test_download() -> None:
    """Test the process repo functions for actual repos and an organization page."""
    links = [
        ["https", "github.com", "/huggingface/", "", "", ""],
        ["https", "github.com", "/Ryan0v0/multilingual_borders", "", "", ""],
        ["https", "github.com", "/huggingface/peft", "", "", ""],
    ]
    links = list(map(urllib.parse.urlunparse, links))  # type: ignore

    res = list(map(process_repo_link, links))

    # huggingface in an organization, we do not need it.
    assert res[0] is None
    assert type(res[1]) is tuple
    assert type(res[2]) is tuple


def test_pth() -> None:
    """Make sure a weight object file is filtered properly."""
    links = urllib.parse.urlunparse(
        [
            "https",
            "github.com",
            "/rwightman/pytorch-image-models/releases/download/v0.1-vitjx/jx_vit_base_p16_224-80ecf9dd.pth",
            "",
            "",
            "",
        ]
    )
    res = process_repo_link(links)
    assert res is None
