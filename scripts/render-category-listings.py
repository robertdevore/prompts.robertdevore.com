#!/usr/bin/env python3
"""Render category cards into generated HTML for no-JS users and crawlers."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlparse


EMPTY_GRID = '<ul class="card-grid category-results" data-category-results aria-live="polite" aria-busy="true"></ul>'
LOADING_STATUS = '<p class="category-status" data-category-status>Loading prompts...</p>'


def card(item: dict[str, object]) -> str:
    title = html.escape(str(item.get("title", "")))
    description = html.escape(str(item.get("description", "")))
    parsed = urlparse(str(item.get("url", "")))
    route = html.escape(parsed.path or "/", quote=True)
    image = str(item.get("featured_image", "")).strip()
    if image:
        media = (
            f'<a class="listing-card-image-link" aria-label="View {title}" href="{route}">'
            f'<img src="{html.escape(image, quote=True)}" alt="Featured image for {title}" '
            'class="listing-card-image" loading="lazy" decoding="async"></a>'
        )
    else:
        media = (
            f'<a class="listing-card-image-link" aria-label="View {title}" href="{route}">'
            '<span class="listing-card-image-placeholder" aria-hidden="true"></span></a>'
        )
    labels = "".join(
        f'<span class="tag listing-tag">{html.escape(str(label))}</span>'
        for label in list(item.get("tags", []))[:3]
    )
    return (
        f'<li class="listing-card">{media}<div class="listing-card-body">'
        f'<div class="listing-card-tags">{labels}</div>'
        f'<h2 class="listing-card-title"><a href="{route}" class="text-links">{title}</a></h2>'
        f'<p class="listing-card-excerpt">{description}</p>'
        f'<a href="{route}" class="listing-card-button">Read Prompt</a>'
        '</div></li>'
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("index", type=Path)
    args = parser.parse_args()
    items = json.loads(args.index.read_text(encoding="utf-8")).get("items", [])
    rendered = 0
    cards = 0
    for page in args.output.glob("*/index.html"):
        source = page.read_text(encoding="utf-8")
        marker = 'data-prompt-category="'
        if marker not in source:
            continue
        category = source.split(marker, 1)[1].split('"', 1)[0].strip().lower()
        matches = [
            item for item in items
            if category in {str(value).lower() for value in item.get("categories", [])}
        ]
        listing = (
            '<ul class="card-grid category-results" data-category-results aria-live="polite" aria-busy="false">'
            + "".join(card(item) for item in matches)
            + "</ul>"
        )
        if EMPTY_GRID not in source or LOADING_STATUS not in source:
            raise SystemExit(f"Category rendering markers missing in {page}")
        source = source.replace(EMPTY_GRID, listing, 1)
        status = (
            '<p class="category-status" data-category-status hidden>Prompts loaded.</p>'
            if matches
            else '<p class="category-status" data-category-status>No prompts in this category yet. Check back soon.</p>'
        )
        page.write_text(source.replace(LOADING_STATUS, status, 1), encoding="utf-8")
        rendered += 1
        cards += len(matches)
    print(f"Rendered {cards} category cards across {rendered} generated pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
