#!/usr/bin/env python3
"""Apply deterministic accessibility fixes to generated listing controls."""

from __future__ import annotations

import re
import sys
from pathlib import Path


IMAGE_LINK_RE = re.compile(r'<a class="listing-card-image-link"(?![^>]*\baria-label=)([^>]*)>')


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    changed_files = 0
    changed_links = 0
    for html_file in sorted(root.rglob("*.html")):
        source = html_file.read_text(encoding="utf-8")

        def label(match: re.Match[str]) -> str:
            nonlocal changed_links
            changed_links += 1
            return '<a class="listing-card-image-link" aria-label="View prompt details"' + match.group(1) + ">"

        updated = IMAGE_LINK_RE.sub(label, source)
        if updated != source:
            html_file.write_text(updated, encoding="utf-8")
            changed_files += 1
    print(f"Added accessible names to {changed_links} listing image links across {changed_files} HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
