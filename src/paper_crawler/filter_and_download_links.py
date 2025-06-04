"""Filter the GitHub links and download the front page for each link."""

import json
import pickle
import urllib
import urllib.parse
import urllib.request
from pathlib import Path
from multiprocessing import Pool
from typing import Union

from bs4 import BeautifulSoup
from tqdm import tqdm

from ._argparse_code import _parse_args


def process_repo_link(repo_link: str) -> Union[tuple[BeautifulSoup, str], None]:
    """
    Process a link to a GitHub repo.

    This returns a BeautifulSoup object and the URL if the page has a branch picker.

    Args:
        repo_link (str): A list of URLs to process.

    Returns:
        list: A list of url and soups with a branch picker.

    Raises: # noqa: DAR402, DAR401
        Exception: If an error occurs while processing a link,
            it will be caught and printed.
    """
    print(repo_link)
    try:
        if repo_link.split(".")[-1] in ["pth", "pkl"]:
            raise ValueError("Pickled or model file found.")
        page = urllib.request.urlopen(repo_link)
        soup = BeautifulSoup(page, "html.parser")
        # look for the branch picker.
        buttons = soup.find_all("button")
        has_branch_picker = any(map(lambda bs: "branch-picker" in str(bs), buttons))
        if has_branch_picker:
            return (soup, repo_link)
        else:
            return None
    except Exception as e:
        tqdm.write(f"Page {repo_link} produced an error {e}.")
        return None


if __name__ == "__main__":
    args = _parse_args()
    id = "_".join(args.id.split("/"))
    print(f"Loading from: ./storage/{id}.json")

    save_path = Path(f"./storage/{id}_filtered.pkl")

    if not save_path.exists():

        with open(f"./storage/{id}.json", "r") as f_read:
            links = json.load(f_read)

        if id == "ICLR.cc_2024_Conference":
            # this one is broken.
            links.pop(1809)
        
        flat_links = []
        for page_links in links:
            if page_links:
                for link in page_links:
                    flat_links.append(link)



        str_links_map = list(map(lambda link: str(urllib.parse.urlunparse(link)), flat_links))
        # remove links to zipped files.
        # str_links = list(filter(lambda l: "tar.gz" not in l, str_links))
        # str_links = list(filter(lambda l: ".bin" not in l, str_links))
        # str_links = list(filter(lambda l: ".zip" not in l, str_links))
        # str_links = list(filter(lambda l: ".pt" not in l, str_links)

        ignore_list = ['tar.gz', ".bin", ".zip", ".pt", ".gif", ".jpeg"]
        str_links = []
        for l in str_links_map:
            append = True
            for ignore in ignore_list:
                if ignore in l:
                    append = False
            if append:
                str_links.append(l)

        # remove duplicates, not doing it means frequently used repos have more weight.
        # str_links = list(set(str_links))

        # clean the data.
        filtered_pages = list(
            tqdm(
                map(process_repo_link, str_links),
                    total=len(str_links),
                    desc=f"downloading {id}.",
            )
        )

        with open(save_path, "wb") as f_write:
            pickle.dump(filtered_pages, f_write)
    else:
        print(f"{save_path} exists, exiting.")