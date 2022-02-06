"""Root script for launching the mocked CLI app."""
from argparse import ArgumentParser


def main():
    """Mocks CLI behaviour."""
    parser = ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument("--version", action="version", version="CLI 1.0.0")
    parser.add_argument("--fail", action="store_true")
    args = parser.parse_args()
    if args.fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
