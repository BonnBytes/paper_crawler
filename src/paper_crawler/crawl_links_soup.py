"""
This module containes code to fetche PDF links from the ICML 2024 proceedings page.

It processes each PDF to extract GitHub links, and to stores the results in a JSON file.
"""

import json
import urllib
from multiprocessing import Pool
import os
from pathlib import Path

import pdfx
import argparse
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
    2014: 32
}

def get_icml_2024_pdf():
    return get_icml_pdf(2024)

def get_icml_2023_pdf():
    return get_icml_pdf(2023)

def get_icml_pdf(year: int) -> list:
    """Fetch the PDF links from the ICML 2024 proceedings page.

    This function opens the ICML 2024 proceedings page, parses the HTML content,
    and filters out the links that contain "pdf" in their href attribute.
    Returns:
        list: A list of BeautifulSoup tag objects that contain the PDF links.
    """
    return get_icml(f"https://proceedings.mlr.press/v{imcl_dict[year]}/")


def get_icml(url: str) -> list:
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    pdf_soup = list(filter(lambda line: "pdf" in str(line), soup.find_all("a")))
    return pdf_soup


def process_link(url: str) -> list[str]:
    """Process a given URL to extract and filter GitHub links from a PDF.

    Args:
        url (str): The URL of the PDF to be processed.

    Returns:
        list: A list of GitHub links extracted from the PDF.
          If an error occurs, returns None.

    Raises:
        ValueError: If not GitHub-Links are found.
        Exception: If there is an error during the processing of the PDF. # noqa: DAR402
    """
    try:
        reader = pdfx.PDFx(url)
        urls = list(reader.get_references_as_dict()["url"])
        urls_filter_broken = list(filter(lambda url: "http" in url, urls))
        urls_filter_github = list(
            filter(lambda url: "github" in url, urls_filter_broken)
        )
        if urls_filter_github:
            github_links = [urllib.parse.urlparse(cl) for cl in urls_filter_github]
            return github_links
        else:
            raise ValueError("No GitHub-Links found.")
    except Exception as e:
        print(f"{url}, throws {e}")
        return None


def _parse_args():
    """Parse cmd line args for filtering and downloading github-repository pages."""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--id",
        type=str,
        default="icml2024",
        help="Specify the venueid.",
    )
    return parser.parse_args()




if __name__ == "__main__":

    args = _parse_args()
    if args.id == 'icml2024':
        pdf_soup = get_icml_2024_pdf()
    elif args.id == 'icml2023':
        pdf_soup = get_icml_2023_pdf()
    elif args.id == 'icml2022':
        pdf_soup = get_icml_pdf(2022)
    elif "icml" in args.id:
        pdf_soup = get_icml_pdf(int(args.id[4:]))
    else:
        raise ValueError("Unkown conference.")

    path = Path(f"./storage/{args.id}.json")

    if not path.exists():
        link_soup = [
            list(filter(lambda s: "href" in s, str(pdf_soup_el).split()))[0].split("=")[-1][
                1:-1
            ]
            for pdf_soup_el in pdf_soup
        ]

        # loop through paper links find pdfs
        with Pool(12) as p:
            res = list(tqdm(p.imap(process_link, link_soup), total=len(link_soup)))

        with open(f"./storage/{args.id}.json", "w") as f:
            f.write(json.dumps(res))
    else:
        print(f"Path {path} exists, exiting.")