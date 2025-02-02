"""Test if the process_pages module does what it should."""

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
    assert stats["files"]["setup.py"] is True
    assert stats["files"]["setup.cfg"] is True
    assert stats["files"]["pyproject.toml"] is False
    assert stats["files"]["environment.yml"] is False

    assert stats["folders"]["test"] is False
    assert stats["folders"]["tests"] is True
    assert stats["folders"][".github/workflows"] is True

    assert stats["python"]["uses_python"] is True
