#!/usr/bin/env python3
"""Copy the five selected, already compiled PDFs into the website."""

import argparse
from pathlib import Path


WEBSITE_ROOT = Path(__file__).resolve().parents[1]
NOTES = (
    ("MAT495/Notes/main.pdf", "random-matrix-products.pdf"),
    ("MAT436/Homework/Paper1.pdf", "pontryagin-duality.pdf"),
    ("research/paper reading/PSW.pdf", "psw.pdf"),
    ("MAT495/On research /notes.pdf", "limit-sets-and-flag-varieties.pdf"),
    ("MAT464/notes.pdf", "mat464.pdf"),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path.home() / "Documents" / "Latex_docs",
        help="path to Latex_docs (default: ~/Documents/Latex_docs)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report differences without copying; exit 1 if a copy needs updating",
    )
    args = parser.parse_args()
    source_root = args.source_root.expanduser().resolve()
    destination_root = WEBSITE_ROOT / "files" / "notes"

    # Check every source before copying anything. Only these selected PDFs
    # belong on the site; do not copy other notes or LaTeX source files.
    updates = []
    try:
        for source_name, destination_name in NOTES:
            source = source_root / source_name
            content = source.read_bytes()
            if not content.startswith(b"%PDF-"):
                parser.exit(2, f"Not a PDF: {source}\nNo files copied.\n")
            destination = destination_root / destination_name
            if not destination.exists() or destination.read_bytes() != content:
                updates.append((destination, content))
    except OSError as error:
        parser.exit(2, f"Cannot read notes: {error}\nNo files copied.\n")

    if not updates:
        print("All five website PDFs match the local compiled PDFs.")
        return 0

    if args.check:
        for destination, _ in updates:
            print(f"Needs update: {destination.relative_to(WEBSITE_ROOT)}")
        return 1

    try:
        destination_root.mkdir(parents=True, exist_ok=True)
        for destination, content in updates:
            destination.write_bytes(content)
            print(f"Updated: {destination.relative_to(WEBSITE_ROOT)}")
    except OSError as error:
        parser.exit(2, f"Copy failed: {error}\nRerun after resolving the error.\n")

    print("Local website copies refreshed. Commit and push to publish them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
