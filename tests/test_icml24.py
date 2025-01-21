from src.paper_crawler.crawl_links import get_icml_2024_pdf

def test_icml24() -> None:
    assert len(get_icml_2024_pdf()) == 2610