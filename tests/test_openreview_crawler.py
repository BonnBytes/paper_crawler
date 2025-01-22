"""See if the openreview crawler works as we would expect."""
from paper_crawler.crawl_links_openreview import get_openreview_submissions
from dotenv import load_dotenv

def test_iclr24() -> None:
    """Check if we got all ICLR 2024 papers."""
    load_dotenv()
    venueid = "ICLR.cc/2024/Conference"
    links = get_openreview_submissions(venueid)
    assert len(links) == 2260
