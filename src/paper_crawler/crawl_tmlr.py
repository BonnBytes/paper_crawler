from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib.request
import json

tmlr_link = "https://jmlr.org/tmlr/papers/"

if __name__ == '__main__':
    tmlr_soup = BeautifulSoup(urllib.request.urlopen(tmlr_link),
                              "html.parser")
    github_links = list(filter(lambda l: "github" in str(l), tmlr_soup.find_all("a")))
    github_links = list(map(lambda l: str(l).split("\"")[1], github_links))
    github_links_parsed = [[urllib.parse.urlparse(cl)]
                            for cl in github_links]

    with open("./storage/tmlr.json", "w") as file:
        file.write(json.dumps(github_links_parsed))

