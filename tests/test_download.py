# TODO: remove sys when done.
import sys
sys.path.append("./src")

import json
import pytest
import urllib
from paper_crawler.filter_and_download_links import process_paper_links


def test_download():
    links = [['https', 'github.com', '/huggingface/', '', '', ''],
             ['https', 'github.com', '/Ryan0v0/multilingual_borders', '', '', ''], 
             ['https', 'github.com', '/huggingface/peft', '', '', '']]

    res = process_paper_links(links)

    # huggingface in an organization, we do not need it.
    assert urllib.parse.urlunparse(links[1]) == res[0][1]
    assert urllib.parse.urlunparse(links[2]) == res[1][1]
    assert len(res) == 2


def test_pth():
    links = [['https', 'github.com', '/rwightman/pytorch-image-models/releases/download/v0.1-vitjx/jx_vit_base_p16_224-80ecf9dd.pth', '', '', '']]
    res = process_paper_links(links)
    assert len(res) == 0