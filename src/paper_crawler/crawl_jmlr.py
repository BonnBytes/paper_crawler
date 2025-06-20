"""Get jmlr code repo-links."""

import json
import urllib.request

from bs4 import BeautifulSoup

tmlr_link = "https://jmlr.org/tmlr/papers/"
mloss_link = "https://jmlr.org/mloss/"


def _parse_links(url: str) -> list[list[str]]:
    tmlr_soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    github_links = list(
        filter(lambda link: "github" in str(link), tmlr_soup.find_all("a"))
    )
    github_links = list(map(lambda link: str(link).split('"')[1], github_links))
    github_links_parsed = [[urllib.parse.urlparse(cl)] for cl in github_links]
    return github_links_parsed


if __name__ == "__main__":
    tmlr_github_links_parsed = _parse_links(tmlr_link)
    with open("./storage/tmlr.json", "w") as file:
        file.write(json.dumps(tmlr_github_links_parsed))

    mloss_github_links_parsed = _parse_links(mloss_link)
    with open("./storage/mloss.json", "w") as file:
        file.write(json.dumps(mloss_github_links_parsed))
