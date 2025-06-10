"""
This module containes code to fetche PDF links from the ICML 2024 proceedings page.

It processes each PDF to extract GitHub links, and to stores the results in a JSON file.
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

cvpr_day_dict = {
    2018: ["2018-06-19", "2018-06-20", "2018-06-21"],
    2019: ["2019-06-18", "2019-06-19", "2019-06-20"],
    2020: ["2020-06-16", "2020-06-17", "2020-06-18"],
}


def get_cvpr_pdf(year: int, cvpr_url: str) -> list[bs4.element.Tag]:
    """Fetch PDF links for CVPR papers.

    Args:
        year (int): Year of interest.
        cvpr_url (str): CVPR base url

    Returns:
        list: A list of links that contain "pdf" in their href attribute.
    """
    if year <= 2017:
        return get_pdf_links(f"{cvpr_url}CVPR{year}/")
    elif year >= 2018 and year <= 2020:
        year_links = []
        for day in cvpr_day_dict[year]:
            links = get_pdf_links(f"{cvpr_url}CVPR{year}?day={day}/")
            year_links.extend(links)
        return year_links
    return get_pdf_links(f"{cvpr_url}CVPR{year}?day=all/")


def get_icml_2024_pdf() -> list[bs4.element.Tag]:
    """Get all ICML 2024 paper links."""
    return get_icml_pdf(2024)


def get_icml_2023_pdf() -> list[bs4.element.Tag]:
    """Get all ICML 2023 paper links."""
    return get_icml_pdf(2023)


def get_icml_pdf(year: int) -> list[bs4.element.Tag]:
    """Fetch the PDF links from the ICML 2024 proceedings page.

    This function opens the ICML 2024 proceedings page, parses the HTML content,
    and filters out the links that contain "pdf" in their href attribute.
    Returns:
        list: A list of BeautifulSoup tag objects that contain the PDF links.
    """
    return get_pdf_links(f"https://proceedings.mlr.press/v{imcl_dict[year]}/")


def get_pdf_links(url: str) -> list[bs4.element.Tag]:
    """Fetch PDF links from an URL.

    Args:
        url (str): The URL where we want to look for PDF links.

    Returns:
        list: A list of links that contain "pdf" in their href attribute.
    """
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    pdf_soup = list(filter(lambda line: "pdf" in str(line), soup.find_all("a")))
    return pdf_soup  # type: ignore


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
    base_url = ""
    if args.id == "icml2024":
        pdf_soup = get_icml_2024_pdf()
    elif args.id == "icml2023":
        pdf_soup = get_icml_2023_pdf()
    elif args.id == "icml2022":
        pdf_soup = get_icml_pdf(2022)
    elif "icml" in args.id:
        pdf_soup = get_icml_pdf(int(args.id[4:]))
    elif "cvpr" in args.id:
        base_url = "https://openaccess.thecvf.com/"
        pdf_soup = get_cvpr_pdf(int(args.id[4:]), base_url)
    else:
        raise ValueError("Unkown conference.")

    path = Path(f"./storage/{args.id}.json")

    if not os.path.exists("./storage/"):
        os.makedirs("./storage/")

    if not path.exists():
        if "CVPR" not in args.id.upper():
            links = [
                list(filter(lambda s: "href" in s, str(pdf_soup_el).split()))[0].split(
                    "="
                )[-1][1:-1]
                for pdf_soup_el in pdf_soup
            ]
        else:
            links = [base_url + str(pdf_soup_el["href"]) for pdf_soup_el in pdf_soup]

        # loop through paper links find pdfs
        res = []
        for steps, current_link in enumerate((bar := tqdm(links))):
            bar.set_description(current_link)
            res.append(process_link(current_link))
            if steps % 100 == 0:
                with open(f"./storage/{args.id}.json", "w") as f:
                    f.write(json.dumps(res))

        with open(f"./storage/{args.id}.json", "w") as f:
            f.write(json.dumps(res))

    else:
        print(f"Path {path} exists, exiting.")
