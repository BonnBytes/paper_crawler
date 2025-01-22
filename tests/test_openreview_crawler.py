"""See if the openreview crawler works as we would expect."""

def test_iclr24() -> None:
    """Check if we got all ICLR papers."""
    assert len(get_icml_2024_pdf()) == 2610
