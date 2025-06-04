"""This module provides functionality to crawl paper links from OpenReview."""

import json
import os
from pathlib import Path
from multiprocessing import Pool

import openreview
from dotenv import load_dotenv
from tqdm import tqdm

from ._argparse_code import _parse_args
from .crawl_links_soup import process_link


def get_openreview_submissions(venueid: str) -> list[str]:
    """ Fetch submission links for a given venue ID.

    This functon finds a PDF link for each submission
    and these as a list of strings.

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
    # print("openreview user:", os.environ["OPENREVIEW_USERNAME"])
    client = openreview.api.OpenReviewClient(
        baseurl="https://api2.openreview.net",
        username=os.environ["OPENREVIEW_USERNAME"],
        password=os.environ["OPENREVIEW_PASSWORD"],
    )

    # check version.
    # https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-check-the-api-version-of-a-venue
    # if v2:
    if client.get_group(venueid).domain:
        submissions = client.get_all_notes(content={"venueid": venueid})

        print(f"{venueid} has : {len(submissions)} submissions.")

        # assemble links
        links = [
            "https://openreview.net" + submission.content["pdf"]["value"]
            for submission in submissions
        ]
        return links
    else:
        # legacy v1 api
        # print("v1 openreview conference")
        # group = client.get_group(venueid)
        # submission_id = list(filter(lambda s: "SUBMISSION_ID" in s, group.to_json()['web'].split("\n")))[0]
        # submission_id = submission_id.split("'")[1]
        # submissions = client.get_all_notes(
        #         invitation=submission_id
        #     )
        # pass
        # len(submissions) is 0 ;-( .
        # This does not work. 
        raise ValueError("v1 api-venue is not supported.")




if __name__ == "__main__":
    load_dotenv()
    args = _parse_args()
    storage_id = "_".join(args.id.split("/"))
    storage_file = f"./storage/{storage_id}.json"
    venueid = args.id
    print(f"getting pdf-links from {venueid}, saving at {storage_file}")

    if not os.path.exists("./storage/"):
        os.makedirs("./storage/")

    path = Path(storage_file)
    print(path, path.exists())
    if not path.exists():
        try:
            links = get_openreview_submissions(venueid)

            # loop through paper links find pdfs
            with Pool(2) as p:
                res = list(tqdm(p.imap(process_link, links), total=len(links)))

            with open(storage_file, "w") as f:
                f.write(json.dumps(res, indent=1))
        except Exception as e:
            print(f"An error occured, {e}.")
    else:
        print(f"Path {path} exists, exiting.")
