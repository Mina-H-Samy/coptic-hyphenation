import argparse
import sys

from .reference import SOFT_HYPHEN, Hyphenator
from .rules import DEFAULT_RULES, load


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python3 -m coptic_hyphenation",
        description="Hyphenate Coptic text read from standard input, line by line.",
    )
    parser.add_argument("--mark", default="-", help='break marker (default "-"; "soft" for U+00AD)')
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="rules file")
    args = parser.parse_args()
    mark = SOFT_HYPHEN if args.mark == "soft" else args.mark
    hyphenator = Hyphenator(load(args.rules))
    for line in sys.stdin:
        sys.stdout.write(hyphenator.hyphenate(line, mark))


if __name__ == "__main__":
    main()
