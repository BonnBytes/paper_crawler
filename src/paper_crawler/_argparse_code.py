import argparse


def _parse_args():
    """Parse cmd line args for filtering and downloading github-repository pages."""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--id",
        type=str,
        default="icml2024",
        help="Specify the venueid.",
    )
    return parser.parse_args()
