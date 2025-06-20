"""
This module containes code to fetche PDF links from proceedings pages.

It processes each PDF to extract GitHub links,
and to stores the results in a JSON file.
"""

import json
import os
import urllib
from pathlib import Path
from typing import Union

import bs4
import pdfx
from bs4 import BeautifulSoup
from tqdm import tqdm

from ._argparse_code import _parse_args
from .crawl_links_selenium import get_iclr_pdf_2018, get_iclr_pdf_2019

imcl_dict = {
    2024: 235,
    2023: 202,
    2022: 162,
    2021: 139,
    2020: 119,
    2019: 97,
    2018: 80,
    2017: 70,
    2016: 48,
    2015: 37,
    2014: 32,
}

aistats_dict = {
    2025: 258,
    2024: 238,
    2023: 206,
    2022: 151,
    2021: 130,
    2020: 108,
    2019: 89,
    2018: 84,
    2017: 54,
    2016: 51,
    2015: 38,
    2014: 33,
}


def get_icml_2024_pdf() -> list[str]:
    """Get all ICML 2024 paper links."""
    return get_icml_pdf(2024)


def get_icml_2023_pdf() -> list[str]:
    """Get all ICML 2024 paper links."""
    return get_icml_pdf(2023)


def get_icml_pdf(year: int) -> list[str]:
    """Fetch the PDF links from the PMLR proceedings page.

    This function opens the PMLR 2024 proceedings page,
    looks for ICML-links and parses the HTML
    content, and filters out the links that contain "pdf" in
    their href attribute.

    Returns:
        list: A list of urls that contain the PDF links.
    """
    return get_pmlr(f"https://proceedings.mlr.press/v{imcl_dict[year]}/")


def get_aistats_pdf(year: int) -> list[str]:
    """Fetch the PDF links from the ICML 2024 proceedings page.

    This function opens the PMLR 2024 proceedings page,
    looks for aistats links and parses the HTML
    content, and filters out the links that contain "pdf" in
    their href attribute.

    Returns:
        list: A list of urls that contain the PDF links.
    """
    return get_pmlr(f"https://proceedings.mlr.press/v{aistats_dict[year]}/")


def get_pmlr(url: str) -> list[str]:
    """Fetch PDF links from an URL.

    Args:
        url (str): The URL where we want to look for PDF links.

    Returns:
        list: A list of links that contain "pdf" in their href attribute.
    """
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    pdf_soup = list(filter(lambda line: "pdf" in str(line), soup.find_all("a")))
    pdf_soup
    links = [
        list(filter(lambda s: "href" in s, str(pdf_soup_el).split()))[0].split(
            "="
        )[-1][1:-1]
        for pdf_soup_el in pdf_soup
    ]
    return links  


def get_nips_pdf(year: int) -> list[str]:
    """Return links to pdfs from the neurips proceedings page.

    Args:
        year (int): The conference year.

    Returns:
        list[str]: A list with links.
    """
    url_str = f"https://papers.nips.cc/paper_files/paper/{year}"
    soup = BeautifulSoup(urllib.request.urlopen(url_str), "html.parser")
    paper_list = soup.find_all("ul", {"class": "paper-list"})[0]
    paper_links = paper_list.find_all("a")  # type: ignore
    process_link = lambda link: str(link).split()[1][6:-1]  # noqa E731
    paper_links = list(map(process_link, paper_links))
    pdf_links = []
    # get the pdf
    for paper_link in tqdm(paper_links, total=len(paper_links), desc=url_str):
        try:
            full_url = "https://papers.nips.cc" + paper_link
            sub_soup = BeautifulSoup(urllib.request.urlopen(full_url), "html.parser")
            pdf_soup = list(
                filter(lambda line: "pdf" in str(line), sub_soup.find_all("a"))
            )
            extract_link = (
                lambda link: "https://papers.nips.cc"
                + str(link).split()[-1].split('"')[1]
            )
            links = list(map(extract_link, pdf_soup))
            pdf_links.extend(links)
        except Exception as e:
            tqdm.write(f"{paper_link}, throws {e}")
    return pdf_links


def get_iclr_2016_pdf() -> list[str]:
    """Fetch the list of PDF URLs for accepted papers at ICLR 2016.

    Returns:
        list[str]: A list of strings, each representing the direct URL
            to a PDF of an accepted paper.
    """
    url = "https://www.iclr.cc/archive/www/doku.php%3Fid=iclr2016:accepted-main.html"
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    pdf_soup = list(filter(lambda line: "arxiv" in str(line), soup.find_all("a")))
    filter_soup = list(
        map(lambda ps: str(ps).split()[2].split('"')[1].replace("abs", "pdf"), pdf_soup)
    )
    return filter_soup


def process_link(url: str) -> Union[list[str], None]:
    """Process a given URL to extract and filter GitHub links from a PDF.

    Args:
        url (str): The URL of the PDF to be processed.

    Returns:
        list: A list of GitHub links extracted from the PDF.
          If an error occurs, returns None.

    Raises:
        ValueError: If no GitHub links are found.
            Is immediately caught and logged on the console.
    """
    try:
        reader = pdfx.PDFx(url)
        urls = list(reader.get_references_as_dict()["url"])
        urls_filter_broken = list(filter(lambda url: "http" in url, urls))
        urls_filter_github = list(
            filter(lambda url: "github" in url, urls_filter_broken)
        )
        # avoid block
        if urls_filter_github:
            github_links = [urllib.parse.urlparse(cl) for cl in urls_filter_github]
            return github_links
        else:
            raise ValueError("No GitHub-Links found.")
    except Exception as e:
        tqdm.write(f"{url}, throws {e}")
        return None


if __name__ == "__main__":
    args = _parse_args()

    if not os.path.exists("./storage/"):
        os.makedirs("./storage/")

    save_path = Path(f"./storage/{args.id}.json")
    print(f"Checking {save_path}.")

    if not save_path.exists():
        print(f"save_path {save_path} does not exist.")
        if args.id == "icml2024":
            pdf_soup = get_icml_2024_pdf()
        elif args.id == "icml2023":
            pdf_soup = get_icml_2023_pdf()
        elif args.id == "icml2022":
            pdf_soup = get_icml_pdf(2022)
        elif "icml" in args.id:
            pdf_soup = get_icml_pdf(int(args.id[4:]))
        elif "nips" in args.id:
            pdf_soup = get_nips_pdf(int(args.id[4:]))
        elif "aistats" in args.id:
            pdf_soup = get_aistats_pdf(int(args.id[7:]))
        elif "iclr2018" in args.id:
            pdf_soup = get_iclr_pdf_2018()
        elif "iclr2019" in args.id:
            pdf_soup = get_iclr_pdf_2019()
        elif "iclr2016" in args.id:
            pdf_soup = get_iclr_2016_pdf()
        else:
            raise ValueError("Unkown conference.")

        # loop through paper links find pdfs
        res = []
        for steps, current_link in enumerate((bar := tqdm(pdf_soup))):
            bar.set_description(f" {current_link} ")
            res.append(process_link(current_link))
            if steps % 100 == 0:
                with open(f"./storage/{args.id}.json", "w") as f:
                    f.write(json.dumps(res))
        with open(save_path, "w") as f:
            f.write(json.dumps(res))
    else:
        print(f"save_path {save_path} exists, exiting.")
