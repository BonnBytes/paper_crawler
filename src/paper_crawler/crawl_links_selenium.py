"""This module extracts PDF links for ICLR papers using Selenium and BeautifulSoup."""

import time

import bs4
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def _get_links_selenium(fun_url: str) -> list[bs4.element.PageElement]:
    """Extract pdf-links from openreview using selenium to load the javascript.

    Args:
        fun_url (str): The URL of the iclr openreview page to crawl.

    Returns:
        list[bs4.element.PageElement]: A list of BeautifulSoup elemets
            that contain pdf-links in their content.

    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background
    # fix for ubuntu https://github.com/SeleniumHQ/selenium/issues/15327
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument(f"--user-data-dir=./tmp_{time.time()}")

    with Chrome(options=chrome_options) as browser:
        browser.get(fun_url)
        time.sleep(20)
        html = browser.page_source

    page_soup = BeautifulSoup(html, "html.parser")
    pdf_soup = list(
        filter(lambda line: "pdf-link" in str(line), page_soup.find_all("a"))
    )
    return pdf_soup


def get_iclr_pdf_2019() -> list[str]:
    """Get ICLR 2019 PDFs."""
    url = "https://openreview.net/group?id=ICLR.cc/2019/Conference#poster-presentations"
    pdf_links = _get_links_selenium(url)
    url = "https://openreview.net/group?id=ICLR.cc/2019/Conference#oral-presentations"
    pdf_links_oral = _get_links_selenium(url)

    all_pdf_links = pdf_links + pdf_links_oral

    # filter strings.
    filter_fun = lambda tag: str(tag).split()[2].split('"')[1]  # noqa: E731
    all_pdf_links_split = list(map(filter_fun, all_pdf_links))

    add_trunk = lambda link: "https://openreview.net" + link  # noqa: E731
    all_pdf_links_full = list(map(add_trunk, all_pdf_links_split))
    return all_pdf_links_full


def get_iclr_pdf_2018() -> list[str]:
    """Get ICLR 2018 PDFs.

    2018 somehow as all submissions in the html???
    We need to filter by div.
    """
    url_oral = (
        "https://openreview.net/group?id=ICLR.cc/2018/Conference#accepted-oral-papers"
    )
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background
    # fix for ubuntu https://github.com/SeleniumHQ/selenium/issues/15327
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    with Chrome(options=chrome_options) as browser:
        browser.get(url_oral)
        time.sleep(20)
        html = browser.page_source

    page_soup = BeautifulSoup(html, "html.parser")
    divs = page_soup.find("div", {"id": "accepted-oral-papers"})
    if divs:
        pdf_links_oral: list[str] = list(
            filter(lambda line: "pdf-link" in str(line), divs.find_all("a"))  # type: ignore
        )
    else:
        pdf_links_oral = []

    url_poster = (
        "https://openreview.net/group?id=ICLR.cc/2018/Conference#accepted-poster-papers"
    )
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background

    with Chrome(options=chrome_options) as browser:
        browser.get(url_poster)
        time.sleep(20)
        html = browser.page_source

    page_soup = BeautifulSoup(html, "html.parser")
    divs = page_soup.find("div", {"id": "accepted-poster-papers"})
    if divs:
        pdf_links_poster: list[str] = list(
            filter(lambda line: "pdf-link" in str(line), divs.find_all("a"))  # type: ignore
        )
    else:
        pdf_links_poster = []

    all_pdf_links = pdf_links_poster + pdf_links_oral
    # filter strings.
    filter_fun = lambda tag: str(tag).split()[2].split('"')[1]  # noqa: E731
    all_pdf_links = list(map(filter_fun, all_pdf_links))

    add_trunk = lambda link: "https://openreview.net" + link  # noqa: E731
    all_pdf_links = list(map(add_trunk, all_pdf_links))

    return all_pdf_links
