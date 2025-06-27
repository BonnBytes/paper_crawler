"""This module provides functionality to crawl paper links from OpenReview."""

import json
import os
import time
from pathlib import Path

import openreview
from dotenv import load_dotenv
from tqdm import tqdm

from ._argparse_code import _parse_args
from .crawl_links_soup import process_link

# from multiprocessing import Pool


def get_openreview_submissions(venueid: str) -> list[str]:
    """Fetch submission links for a given venue ID.

    This functon finds a PDF link for each submission
    and these as a list of strings.

    Args:
        venueid (str): The ID of the venue for which to fetch submissions.

    Returns:
        list[str]: A list of URLs pointing to the PDF files of the submissions.
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
        # v1 api.
        client = openreview.Client(
            baseurl="https://api.openreview.net",
            username=os.environ["OPENREVIEW_USERNAME"],
            password=os.environ["OPENREVIEW_PASSWORD"],
        )
        submissions = client.get_all_notes(content={"venueid": venueid})
        print(f"{venueid} has : {len(submissions)} submissions.")
        # assemble links
        links = []
        for submission in submissions:
            if "openreview.net" not in submission.content["pdf"]:
                links.append("https://openreview.net" + submission.content["pdf"])
            else:
                links.append(submission.content["pdf"])
        return links


if __name__ == "__main__":
    dotenv = load_dotenv()
    args = _parse_args()
    print(f"dotenv loaded: {dotenv}.")
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

            if args.id == "ICLR.cc/2021/Conference":
                print(f"pop: {args.id}")
                links.pop(719)
                links.pop(718)
                links.pop(717)

            # loop through paper links find pdfs
            # with Pool(2) as p:
            #     res = list(tqdm(p.imap(process_link, links), total=len(links)))

            res = []
            for link in (bar := tqdm(links)):
                res.append(process_link(link))
                bar.set_description(f" {link} ")
                # avoid ip-ban.
                time.sleep(2)

            # loop through paper links find pdfs
            # with Pool(2) as p:
            #    res = list(tqdm(p.imap(process_link, links), total=len(links)))

            # do not create a file is res is empty.
            if res:
                with open(storage_file, "w") as f:
                    f.write(json.dumps(res, indent=1))
        except Exception as e:
            print(f"An error occured, {e}.")
    else:
        print(f"Path {path} exists, exiting.")
