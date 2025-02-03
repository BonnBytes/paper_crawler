import argparse


def _parse_args() -> argparse.Namespace:
    """Cmd line args for filtering and downloading and analyzing ML-conferences."""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--id",
        type=str,
        default="icml2024",
        help="Specify the venueid.",
    )
    return parser.parse_args()
