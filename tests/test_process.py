"""Test if the process_pages module does what it should."""

# import urllib
# from bs4 import BeautifulSoup

from paper_crawler.filter_and_download_links import process_repo_link
from paper_crawler.process_pages import extract_stats


def test_requirements_txt() -> None:
    """Test if the requirements.txt file is found."""
    link = "https://github.com/ErikEnglesson/SGN"

    loaded = process_repo_link(link)
    # check debug information
    assert loaded[1] == link
    stats = extract_stats(loaded)

    assert stats["files"]["requirements.txt"] is True
    assert stats["files"]["README.md"] is True
    assert stats["files"]["LICENSE"] is False
    assert stats["files"]["noxfile.py"] is False
    assert stats["files"]["tox.toml"] is False
    assert stats["files"]["tox.ini"] is False
    assert stats["files"]["setup.py"] is False
    assert stats["files"]["setup.cfg"] is False
    assert stats["files"]["pyproject.toml"] is False
    assert stats["files"]["environment.yml"] is False

    assert stats["folders"]["test"] is False
    assert stats["folders"]["tests"] is False
    assert stats["folders"][".github/workflows"] is False

    assert stats["python"]["uses_python"] is True


def test_tests_folder() -> None:
    """Test if the tests folder is found."""
    link = "https://github.com/v0lta/PyTorch-Wavelet-Toolbox"

    loaded = process_repo_link(link)
    # check debug information
    assert loaded[1] == link
    stats = extract_stats(loaded)

    assert stats["files"]["requirements.txt"] is False
    assert stats["files"]["README.md"] is False
    assert stats["files"]["LICENSE"] is True
    assert stats["files"]["noxfile.py"] is True
    assert stats["files"]["tox.toml"] is False
    assert stats["files"]["tox.ini"] is False
    assert stats["files"]["setup.py"] is False
    assert stats["files"]["setup.cfg"] is False
    assert stats["files"]["pyproject.toml"] is True
    assert stats["files"]["environment.yml"] is False

    assert stats["folders"]["test"] is False
    assert stats["folders"]["tests"] is True
    assert stats["folders"][".github/workflows"] is True

    assert stats["python"]["uses_python"] is True


def test_all_false_no_readme() -> None:
    """Test tmlr stats."""
    link = "https://github.com/mas-takayama/LLM-and-SCD"

    loaded = process_repo_link(link)
    # check debug information
    assert loaded[1] == link
    stats = extract_stats(loaded)

    assert stats["files"]["README.md"] is False
    assert stats["files"]["README.rst"] is False
    assert stats["files"]["readme.md"] is False
    assert stats["files"]["readme.rst"] is False
    assert stats["files"]["Readme.md"] is False
    assert stats["files"]["Readme.rst"] is False

    assert stats["files"]["requirements.txt"] is False
    assert stats["files"]["LICENSE"] is False
    assert stats["files"]["noxfile.py"] is False
    assert stats["files"]["tox.toml"] is False
    assert stats["files"]["tox.ini"] is False
    assert stats["files"]["setup.py"] is False
    assert stats["files"]["setup.cfg"] is False
    assert stats["files"]["pyproject.toml"] is False
    assert stats["files"]["environment.yml"] is False
    assert stats["folders"]["test"] is False
    assert stats["folders"]["tests"] is False
    assert stats["folders"][".github/workflows"] is False


def test_a_little_python() -> None:
    """Test tmlr stats."""
    link = "https://github.com/rjiang03/HCL"

    loaded = process_repo_link(link)
    # check debug information
    assert loaded[1] == link
    stats = extract_stats(loaded)

    assert stats["python"]["uses_python"] is True

    assert stats["files"]["README.md"] is True
    assert stats["files"]["README.rst"] is False
    assert stats["files"]["readme.md"] is False
    assert stats["files"]["readme.rst"] is False
    assert stats["files"]["Readme.md"] is False
    assert stats["files"]["Readme.rst"] is False
    assert stats["folders"]["test"] is False
    assert stats["folders"]["tests"] is False


def test_mloss_rey_net() -> None:
    """Check if the ReyNet repo ist processed ok.

    https://www.jmlr.org/papers/volume25/22-0891/22-0891.pdf
    """
    test_url = "https://github.com/makora9143/ReyNet"
    loaded = process_repo_link(test_url)
    stats = extract_stats(loaded)

    assert stats["files"]["requirements.txt"] is True
    assert stats["folders"]["src"] is False
    assert stats["folders"]["test"] is False
    assert stats["folders"]["tests"] is False


def test_mloss_watchtheweight() -> None:
    """Paper: https://www.jmlr.org/papers/volume24/21-1441/21-1441.pdf ."""
    test_url = "https://github.com/juve-xx/watchtheweight"
    loaded = process_repo_link(test_url)
    stats = extract_stats(loaded)

    assert stats["files"]["README.md"] is True
    assert stats["files"]["requirements.txt"] is False
    assert stats["files"]["LICENSE"] is False
    assert stats["folders"]["src"] is False
    assert stats["folders"]["test"] is False
    assert stats["folders"]["tests"] is False


def test_nested_test_folder_src() -> None:
    """Make sure we find nested tests."""
    test_in_src_url = "https://github.com/bd2kccd/causal-compare"
    loaded_test_in_src = process_repo_link(test_in_src_url)
    stats_in_src = extract_stats(loaded_test_in_src)
    assert stats_in_src["folders"]["test"] is False
    assert stats_in_src["folders"]["test"] is False
    assert stats_in_src["folders"]["src/test"] is True


def test_nested_test_folder_packet() -> None:
    """Make sure we find nested tests in a source folder with package name."""
    test_in_pkg_url = "https://github.com/unit8co/darts"
    loaded_test_in_pkg = process_repo_link(test_in_pkg_url)
    stats_in_pkg = extract_stats(loaded_test_in_pkg)
    assert stats_in_pkg["folders"]["test"] is False
    assert stats_in_pkg["folders"]["test"] is False
    assert stats_in_pkg["folders"]["package/tests"] is True


def test_pylock_toml() -> None:
    test_pylock_url = "https://github.com/BonnBytes/paper_crawler"
    loaded_test_in_pkg = process_repo_link(test_pylock_url)
    stats_in_pkg = extract_stats(loaded_test_in_pkg)
    assert stats_in_pkg["folders"]["test"] is False
    assert stats_in_pkg["folders"]["tests"] is True
    assert stats_in_pkg["files"]["pylock.toml"] is True
