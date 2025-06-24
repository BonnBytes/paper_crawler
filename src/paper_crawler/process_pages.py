"""This module allows parsing the github pages. It extracts file and folder names."""

import pickle
import time
from collections import Counter
from pathlib import Path
from typing import Any

import bs4
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from ._argparse_code import _parse_args


def _get_files_and_folders(
    soup: bs4.BeautifulSoup,
) -> tuple[list[str], list[str], list[bs4.element.Tag]]:
    # filter language, find spans first
    folders_and_files = list(
        filter(lambda table: "folders-and-files" in str(table), soup.find_all("table"))
    )[0]
    cells: list[bs4.element.Tag] = list(
        filter(
            lambda td: "row-name-cell" in str(td),  # type: ignore
            folders_and_files.find_all("td"),  # type: ignore
        )
    )

    folders = []
    files = []
    for cell in cells:
        if "icon-directory" in str(cell):
            folders.append(cell.text)
        else:
            files.append(cell.text)
    return folders, files, cells


def extract_stats(
    paper_soup_and_link: tuple[bs4.BeautifulSoup, str],
) -> dict[str, dict[str, bool]]:
    """Extract statistics from a BeautifulSoup object representing a paper's webpage.

    Args:
        paper_soup_and_link (tuple): A tuple containing a BeautifulSoup object of
            the paper's webpage and the page link where we got the soup from.

    Returns:
        dict[str, bool]: A dictionary containing the presence of specific files,
          folders, and whether Python is mentioned on the page.
            - "files": A dictionary where keys are filenames of interest
                and values are booleans indicating their presence.
            - "folders": A dictionary where keys are folder names of interest
                and values are booleans indicating their presence.
            - "python": A dictionary with a key "uses_python"
                and a boolean value indicating if Python is mentioned on the page.
    """
    # Second position is the page link, use for debugging.
    soup, link = paper_soup_and_link

    python_span = list(
        filter(
            lambda span: "Python" in str(span),
            soup.find_all("span"),
        )
    )

    folders, files, cells = _get_files_and_folders(soup)

    interesting_files = [
        "requirements.txt",
        "noxfile.py",
        "LICENSE.txt",
        "license.txt",
        "License.txt",
        "LICENSE",
        "License",
        "license",
        "COPYING",
        "copying",
        "Copying",
        "COPYING.txt",
        "copying.txt",
        "Copying.txt",
        "README.md",
        "readme.md",
        "Readme.md",
        "README.rst",
        "readme.rst",
        "Readme.rst",
        "tox.toml",
        "tox.ini",
        "setup.py",
        "setup.cfg",
        "pyproject.toml",
        "environment.yml",
        "uv.lock",
        ".pre-commit-config.yaml",
        "poetry.lock",
        "poetry.toml",
        "hatch.toml",
        "pixi.lock",
        "pixi.toml",
        "Pipfile.lock",
    ]
    interesting_folders = [
        "test",
        "tests",
        ".github/workflows",
        ".github",
        "doc",
        "docs",
        "src",
    ]

    result_dict: dict[str, Any] = {}
    result_dict["files"] = {}
    result_dict["folders"] = {}
    result_dict["python"] = {}
    for interesting_file in interesting_files:
        result_dict["files"][interesting_file] = interesting_file in files

    for interesting_folder in interesting_folders:
        result_dict["folders"][interesting_folder] = interesting_folder in folders
    if python_span:
        result_dict["python"]["uses_python"] = True

    def _get_sub_soup(folder: str) -> bs4.BeautifulSoup:
        cell_tuples = [(cell, cell) for cell in cells]
        labels_and_cells = [
            (
                list(filter(lambda str_el: "label" in str_el, str(tcell[0]).split()))[
                    0
                ],
                tcell[1],
            )
            for tcell in cell_tuples
        ]
        pass
        folder_link = (
            str(
                list(filter(lambda lc: folder in str(lc[0]), labels_and_cells))[0][
                    1
                ].find_all("a")[0]
            )
            .split("href")[1]
            .split()[0]
            .split('"')[1]
        )
        folder_link = "https://github.com" + folder_link
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Opens the browser up in background
        # fix for ubuntu https://github.com/SeleniumHQ/selenium/issues/15327
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument(f"--user-data-dir=./tmp_{time.time()}")

        with Chrome(options=chrome_options) as browser:
            browser.get(folder_link)
            time.sleep(4)
            html = browser.page_source

        folder_soup = bs4.BeautifulSoup(html, "html.parser")
        return folder_soup

    # see if we found tests, if not look for nested tests.
    tests_found = result_dict["folders"]["tests"] or result_dict["folders"]["test"]
    if not tests_found:
        if result_dict["folders"]["src"]:
            # beautiful soup into src and looks for test or tests.
            try:
                src_soup = _get_sub_soup("src")
                src_folders, _, _ = _get_files_and_folders(src_soup)
                if "test" in src_folders:
                    result_dict["folders"]["src/test"] = True
                if "tests" in src_folders:
                    result_dict["folders"]["src/tests"] = True
            except Exception:
                # print(f"src folder not found, {e}.")
                pass
        else:
            try:
                packet_name = link.split("/")[-1]
                src_soup = _get_sub_soup(packet_name)
                src_folders, _, _ = _get_files_and_folders(src_soup)
                if "test" in src_folders:
                    result_dict["folders"]["package/test"] = True
                if "tests" in src_folders:
                    result_dict["folders"]["package/tests"] = True
            except Exception:
                # print(f"package folder {packet_name}, not found, {e}.")
                pass
    return result_dict


if __name__ == "__main__":
    args = _parse_args()
    id = "_".join(args.id.split("/"))
    load_path = f"./storage/{id}_filtered.pkl"
    save_path = Path(f"./storage/{id}_stored_counters.pkl")

    if not save_path.exists():
        with open(load_path, "rb") as f_read:
            paper_pages = pickle.load(f_read)

        results = []

        error_counter = 0
        problems = []
        for paper_soup_and_link in (bar := tqdm(paper_pages)):
            # folders and files exists once per page.
            try:
                bar.set_description(f" {paper_soup_and_link[1]} ")
                results.append(extract_stats(paper_soup_and_link))
            except Exception as e:
                #     # print(f"Error: {e}")
                problems.append(e)
                error_counter += 1

        # print(f"Problems: {problems}")
        print(f"Problems {error_counter}.")
        files: list[tuple[str, bool]] = []
        for res in results:
            files.extend(
                list(filter(lambda res: res[1] is True, list(res["files"].items())))
            )

        python_use: list[tuple[str, bool]] = []
        for res in results:
            python_use.extend(
                list(filter(lambda res: res[1] is True, list(res["python"].items())))
            )
        python_counter = Counter(python_use)

        try:
            python_total = list(python_counter.items())[0][1]
        except IndexError as e:
            print(f"No python code found, {e}")
            python_total = 0

        file_counter = Counter(files)
        page_total = len(results)

        print(f"Python total: {python_total}.")
        print(f"Python share: {python_total / float(page_total)}.")

        print("Files:")
        print(f"total: {file_counter.items()} of {page_total}")
        ratios = [(mc[0], mc[1] / float(page_total)) for mc in file_counter.items()]
        print(f"ratios: {ratios}")
        ratios = [(mc[0], mc[1] / float(python_total)) for mc in file_counter.items()]
        print(f"python-ratios: {ratios}")

        folders = []
        for res in results:
            folders.extend(
                list(filter(lambda res: res[1] is True, list(res["folders"].items())))
            )

        folders_counter = Counter(folders)
        print("Folders")
        print(f"total: {folders_counter.items()} of {page_total}")
        print(
            f"ratios: {[(mc[0], mc[1] / float(page_total))
                       for mc in folders_counter.items()]}"
        )

        with open(save_path, "wb") as f_write:
            pickle.dump(
                {
                    "files": file_counter,
                    "folders": folders_counter,
                    "language": python_counter,
                    "page_total": page_total,
                },
                f_write,
            )
    else:
        print(f"{save_path} exists, exiting.")
