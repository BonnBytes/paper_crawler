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


def get_icml_2024_pdf() -> list[bs4.element.Tag]:
    """Get all ICML 2024 paper links."""
    return get_icml_pdf(2024)


def get_icml_2023_pdf() -> list[bs4.element.Tag]:
    """Get all ICML 2024 paper links."""
    return get_icml_pdf(2023)


def get_icml_pdf(year: int) -> list[bs4.element.Tag]:
    """Fetch the PDF links from the ICML 2024 proceedings page.

    This function opens the ICML 2024 proceedings page, parses the HTML content,
    and filters out the links that contain "pdf" in their href attribute.
    Returns:
        list: A list of BeautifulSoup tag objects that contain the PDF links.
    """
    return get_icml(f"https://proceedings.mlr.press/v{imcl_dict[year]}/")


def get_icml(url: str) -> list[bs4.element.Tag]:
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
    if args.id == "icml2024":
        pdf_soup = get_icml_2024_pdf()
    elif args.id == "icml2023":
        pdf_soup = get_icml_2023_pdf()
    elif args.id == "icml2022":
        pdf_soup = get_icml_pdf(2022)
    elif "icml" in args.id:
        pdf_soup = get_icml_pdf(int(args.id[4:]))
    else:
        raise ValueError("Unkown conference.")

    path = Path(f"./storage/{args.id}.json")

    if not os.path.exists("./storage/"):
        os.makedirs("./storage/")

    if not path.exists():
        links = [
            list(filter(lambda s: "href" in s, str(pdf_soup_el).split()))[0].split("=")[
                -1
            ][1:-1]
            for pdf_soup_el in pdf_soup
        ]

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
