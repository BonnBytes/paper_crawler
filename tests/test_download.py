import json
from src.paper_crawler.filter_and_download_links import process_paper_links


def test_download():
    openid = "ICLR.cc/2024/Conference"
    id = "_".join(openid.split("/"))
    print(f"Loading from: ./storage/{id}.json")

    with open(f"./storage/{id}.json", "r") as f:
        links = json.load(f)

    results = []
    # for i in range(1800, 1820):
    #     print(i)
    res = process_paper_links(links[1809])
    results.append(res)
    pass

