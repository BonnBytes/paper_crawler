"""Get TMLR code repo-links."""

import json
import urllib.request

from bs4 import BeautifulSoup

tmlr_link = "https://jmlr.org/tmlr/papers/"

if __name__ == "__main__":
    tmlr_soup = BeautifulSoup(urllib.request.urlopen(tmlr_link), "html.parser")
    github_links = list(
        filter(lambda link: "github" in str(link), tmlr_soup.find_all("a"))
    )
    github_links_str = list(map(lambda link: str(link).split('"')[1], github_links))
    github_links_parsed = [[urllib.parse.urlparse(cl)] for cl in github_links_str]

    with open("./storage/tmlr.json", "w") as file:
        file.write(json.dumps(github_links_parsed))
