import pickle
from bs4 import BeautifulSoup
from multiprocessing import Pool

from ._argparse_code import _parse_args

if __name__ == "__main__":
    args = _parse_args()
    id = "_".join(args.id.split("/"))
    print(f"Loading from: ./storage/{id}.json")

    with open(f"./storage/{id}_filtered.pkl", 'rb') as f:
        paper_pages = pickle.load(f)

    soups = []
    for paper in paper_pages:
        for page in paper:
            soups.append(BeautifulSoup(page, 'html.parser'))
