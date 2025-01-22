import pickle
from bs4 import BeautifulSoup
from multiprocessing import Pool
from collections import Counter
from tqdm import tqdm

from ._argparse_code import _parse_args

def search_folders_and_files(str) -> list[str]:
    pass


if __name__ == "__main__":
    args = _parse_args()
    id = "_".join(args.id.split("/"))
    print(f"./storage/{id}_filtered.pkl")

    with open(f"./storage/{id}_filtered.pkl", 'rb') as f:
        paper_pages = pickle.load(f)

    results = []
    error_counter = 0
    for paper_soup_and_link in tqdm(paper_pages):
        # paper_soup = paper_soup_and_link[0]
        
        paper_soup = paper_soup_and_link
        # for page in paper:
            # find file list
        # folders and files exists once per page.
        try:
            folders_and_files = list(filter(lambda table: 'folders-and-files' in str(table), paper_soup.find_all("table")))[0]
            cells = list(filter(lambda td: 'row-name-cell' in str(td), folders_and_files.find_all("td")))

            folders = []
            files = []
            for cell in cells:
                if 'icon-directory' in str(cell):
                    folders.append(cell.text)
                else:
                    files.append(cell.text)

            interesting_files = ["requirements.txt", "noxfile.py", "LICENSE", "README.md", "README.rst", "tox.toml", "tox.ini",  "setup.py", "setup.cfg", "pyproject.toml"]
            interesting_folders = ["test", "tests", ".github/workflows"]

            result_dict = {}
            result_dict['files'] = {}
            result_dict['folders'] = {}
            for interesting_file in interesting_files:
                result_dict['files'][interesting_file] = interesting_file in files

            for interesting_folder in interesting_folders:
                result_dict['folders'][interesting_folder] = interesting_folder in folders

            results.append(result_dict)
        except Exception as e:
                print(f"Error: {e}")
                error_counter += 1

    print(f"Problems {error_counter}.")
    files = []
    for res in results:
        files.extend(list(filter(lambda res: res[1] == True, list(res['files'].items()))))

    file_counter = Counter(files)
    page_total = len(results)
    print("Files:")
    print(f"total: {file_counter.items()} of {page_total}")
    print(f"ratios: {[(mc[0], mc[1]/float(page_total)) for mc in file_counter.items()]}")


    folders = []
    for res in results:
        folders.extend(list(filter(lambda res: res[1] == True, list(res['folders'].items()))))

    folders_counter = Counter(folders)
    print("Folders")
    print(f"total: {folders_counter.items()} of {page_total}")
    print(f"ratios: {[(mc[0], mc[1]/float(page_total)) for mc in folders_counter.items()]}")

    pass