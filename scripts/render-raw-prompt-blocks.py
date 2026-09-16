#!/usr/bin/env python3
"""Replace generated raw-prompt sentinels with literal, copyable code blocks."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


SENTINEL = re.compile(r"<p>%%RAW_PROMPT:([a-z0-9-]+)%%</p>")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("sources", type=Path)
    args = parser.parse_args()
    rendered = 0
    for page in args.output.rglob("*.html"):
        source = page.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            nonlocal rendered
            slug = match.group(1)
            prompt_path = args.sources / f"{slug}.md"
            if not prompt_path.is_file():
                raise SystemExit(f"Raw prompt source is missing: {prompt_path}")
            rendered += 1
            prompt = prompt_path.read_text(encoding="utf-8").rstrip()
            return f'<pre><code class="language-markdown">{html.escape(prompt)}</code></pre>'

        updated = SENTINEL.sub(replace, source)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
    if any("%%RAW_PROMPT:" in page.read_text(encoding="utf-8") for page in args.output.rglob("*.html")):
        raise SystemExit("An unresolved raw prompt sentinel remains in generated output.")
    print(f"Rendered {rendered} literal prompt block(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
