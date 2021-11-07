"""Entrypoint file"""
import sys

from app.svg.parsing import parse_svg
from app.utils import plotting


def main():
    """Program entrypoint - Here comes the main logic"""
    paths = parse_svg(r"app\svg\sample_svgs\arc_test2.svg")
    for path in paths:
        plotting.plot_path(path)
    plotting.show()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import pytest

        sys.exit(pytest.main(["-x", "tests"]))

    main()
