"""
This module containes code to fetche PDF links from the ICML 2024 proceedings page.

It processes each PDF to extract GitHub links, and to stores the results in a JSON file.
"""

import json
import urllib
from multiprocessing import Pool

import pdfx
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_icml_2024_pdf():
    """Fetch the PDF links from the ICML 2024 proceedings page.

    This function opens the ICML 2024 proceedings page, parses the HTML content,
    and filters out the links that contain "pdf" in their href attribute.
    Returns:
        list: A list of BeautifulSoup tag objects that contain the PDF links.
    """

    def open_icml24():
        return urllib.request.urlopen("https://proceedings.mlr.press/v235/")

    soup = BeautifulSoup(open_icml24(), "html.parser")

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


if __name__ == "__main__":

    pdf_soup = get_icml_2024_pdf()

    link_soup = [
        list(filter(lambda s: "href" in s, str(pdf_soup_el).split()))[0].split("=")[-1][
            1:-1
        ]
        for pdf_soup_el in pdf_soup
    ]

    # loop through paper links find pdfs
    with Pool(10) as p:
        res = list(tqdm(p.imap(process_link, link_soup), total=len(link_soup)))

    with open("./storage/icml2024.json", "w") as f:
        f.write(json.dumps(res))
