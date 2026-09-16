#!/usr/bin/env python3
"""Add literal raw-prompt sources to the generated client search index."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SENTINEL = re.compile(r"%%RAW_PROMPT:([a-z0-9-]+)%%")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=Path)
    parser.add_argument("content", type=Path)
    parser.add_argument("sources", type=Path)
    args = parser.parse_args()
    data = json.loads(args.index.read_text(encoding="utf-8"))
    items = data.get("items", [])
    by_route = {str(item.get("route", "")).strip("/"): item for item in items}
    enriched = 0
    for post in args.content.glob("*.md"):
        source = post.read_text(encoding="utf-8")
        match = SENTINEL.search(source)
        if not match:
            continue
        slug = match.group(1)
        item = by_route.get(f"blog/{slug}")
        if item is None:
            raise SystemExit(f"Search-index item missing for raw prompt: {slug}")
        prompt_path = args.sources / f"{slug}.md"
        prompt = prompt_path.read_text(encoding="utf-8").strip()
        item["text"] = (str(item.get("text", "")).replace(match.group(0), "") + " " + prompt).strip()
        headings = [heading.strip() for heading in re.findall(r"^#{1,6}\s+(.+)$", prompt, flags=re.MULTILINE)]
        item["headings"] = list(dict.fromkeys(list(item.get("headings", [])) + headings))
        enriched += 1
    args.index.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Enriched {enriched} search-index prompt source(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
