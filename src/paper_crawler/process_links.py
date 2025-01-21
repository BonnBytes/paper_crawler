import json
import urllib
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Pool


def process_paper_links(links: list[str]) -> list[str]:
    filtered = []
    try:
        for paper_link in links:
            github_link = urllib.parse.urlunparse(paper_link)
            page = urllib.request.urlopen(github_link)
            soup = BeautifulSoup(page, 'html.parser')
            # look for the branch picker.
            buttons = soup.find_all("button")
            has_branch_picker = any(map(lambda bs: "branch-picker" in str(bs), buttons))
            if has_branch_picker:
                filtered.append(page)
    except Exception as e:
            print(f"Page {github_link} produced an error {e}.")
    return filtered


if __name__ == '__main__':
    with open("./storage/icml2024.json", 'r') as f:
        links = json.load(f)


    # clean the data.
    filtered_pages = []
    # for papers_links in tqdm(links):
    #    filtered_pages.extend(process_paper_links(papers_links))

    with Pool(2) as p:
        filtered_pages.extend(tqdm(p.imap(process_paper_links, links), total=len(links)))

    pass
