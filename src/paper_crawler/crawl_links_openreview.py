"""This module provides functionality to crawl paper links from OpenReview."""

import json
import os
from multiprocessing import Pool

import openreview
from dotenv import load_dotenv
from tqdm import tqdm

from .crawl_links_soup import process_link


def get_openreview_submissions(venueid: str) -> list[str]:
    """Fetch submission links for a given venue ID.

    This functon finds a PDF link for each submission and these as a list of strings.
    Args:
        venueid (str): The ID of the venue for which to fetch submissions.
    Returns:
        list[str]: A list of URLs pointing to the PDF files of the submissions.
    Raises:
        KeyError: If the environment variables
            'OPENREVIEW_USERNAME' or 'OPENREVIEW_PASSWORD' are not set.
        openreview.OpenReviewException:
             If there is an error with the OpenReview API request.
    """
    # API V2
    print(os.environ["OPENREVIEW_USERNAME"])
    client = openreview.api.OpenReviewClient(
        baseurl="https://api2.openreview.net",
        username=os.environ["OPENREVIEW_USERNAME"],
        password=os.environ["OPENREVIEW_PASSWORD"],
    )

    submissions = client.get_all_notes(content={"venueid": venueid})

    print(f"{venueid} has : {len(submissions)} submissions.")

    # assemble links
    links = [
        "https://openreview.net" + submission.content["pdf"]["value"]
        for submission in submissions
    ]

    return links


if __name__ == "__main__":
    load_dotenv()

    venueid = "ICLR.cc/2024/Conference"

    links = get_openreview_submissions(venueid)

    # loop through paper links find pdfs
    with Pool(2) as p:
        res = list(tqdm(p.imap(process_link, links), total=len(links)))

    with open(f"./storage/{"_".join(venueid.split("/"))}.json", "w") as f:
        f.write(json.dumps(res, indent=1))
