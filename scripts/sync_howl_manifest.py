#!/usr/bin/env python3
"""Build the complete Howl social-card manifest from authored site content."""

from __future__ import annotations

import ast
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "howl.json"
CONTENT = ROOT / "content"
FONT = "assets/sitekit/fonts/DepartureMono-Regular.woff2"


def frontmatter(path: Path) -> dict[str, object]:
    match = re.match(
        r"^---\s*\n(.*?)\n---(?:\s*\n|$)",
        path.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"Missing frontmatter: {path.relative_to(ROOT)}")
    result: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        value = raw.strip()
        try:
            result[key.strip()] = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            result[key.strip()] = value
    return result


def text(meta: dict[str, object], key: str, fallback: str = "") -> str:
    value = meta.get(key, fallback)
    return str(value).strip() if value is not None else fallback


def terms(meta: dict[str, object], key: str) -> list[str]:
    value = meta.get(key, [])
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def fit_for_howl(value: str, max_chars: int, max_lines: int) -> str:
    lines: list[str] = []
    current = ""
    for word in value.split():
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    if len(lines) <= max_lines:
        return " ".join(lines)
    kept = lines[:max_lines]
    final_words = kept[-1].split()
    while final_words and len(" ".join(final_words)) + 2 > max_chars:
        final_words.pop()
    kept[-1] = (" ".join(final_words) or kept[-1][: max_chars - 2]).rstrip() + " …"
    return " ".join(kept)


def card(
    *,
    card_id: str,
    route: str,
    title: str,
    tagline: str,
    source: str,
    label: str,
    concepts: list[str] | None = None,
    language: str = "markdown",
) -> dict[str, object]:
    return {
        "id": card_id,
        "title": fit_for_howl(title, 20, 3),
        "tagline": fit_for_howl(tagline, 47, 2),
        "file": source,
        "language": language,
        "concepts": concepts or [label.lower()],
        "caption": f"{title}: {tagline}" if tagline else title,
        "cta": "Explore Prompts by Robert DeVore.",
        "url": f"https://prompts.robertdevore.com{route}",
        "variant": "social",
        "label": label.upper(),
        "font_file": FONT,
        "show_url": False,
    }


def content_card(path: Path, kind: str) -> dict[str, object]:
    meta = frontmatter(path)
    slug = text(meta, "custom_url", path.stem)
    title = text(meta, "seo_title", text(meta, "title"))
    tagline = text(meta, "description")
    relative = path.relative_to(ROOT).as_posix()
    if kind == "post":
        categories = terms(meta, "categories")
        label = categories[0] if categories else "PROMPT GUIDE"
        concepts = categories + terms(meta, "tags")
    else:
        label = "PROMPT CATEGORY" if text(meta, "template") == "category" else "PROMPT LIBRARY"
        concepts = [slug, "AI prompts"]
    return card(
        card_id=slug,
        route=f"/{'blog/' if kind == 'post' else ''}{slug}/",
        title=title,
        tagline=tagline,
        source=relative,
        label=label,
        concepts=concepts,
    )


def build_manifest() -> dict[str, object]:
    cards = [
        card(
            card_id="home",
            route="/",
            title="Prompts by Robert DeVore",
            tagline="A curated library of high-quality prompts built for making",
            source="templates/page-home.html",
            label="CURATED AI PROMPT LIBRARY",
            concepts=["AI prompts", "structured prompts", "creative workflows"],
            language="html",
        ),
        card(
            card_id="blog",
            route="/blog/",
            title="Prompt Library",
            tagline="Reusable prompts, complete structures, examples, and practical notes",
            source="templates/page-blog.html",
            label="LATEST PROMPTS",
            concepts=["AI prompts", "prompt archive"],
            language="html",
        ),
    ]

    post_count = len(list((CONTENT / "posts").glob("*.md")))
    config = (ROOT / "kujo-ssg.yml").read_text(encoding="utf-8")
    match = re.search(r"(?m)^posts_per_page:\s*(\d+)\s*$", config)
    posts_per_page = int(match.group(1)) if match else 6
    page_count = max(1, math.ceil(post_count / posts_per_page))
    for number in range(2, page_count + 1):
        cards.extend(
            [
                card(
                    card_id=f"prompt-library-page-{number}",
                    route=f"/page/{number}/",
                    title=f"Prompt Library — Page {number}",
                    tagline="More structured prompts for creative and professional work with AI",
                    source="templates/page-home.html",
                    label="PROMPT ARCHIVE",
                    language="html",
                ),
                card(
                    card_id=f"blog-page-{number}",
                    route=f"/blog/page/{number}/",
                    title=f"Latest Prompts — Page {number}",
                    tagline="More reusable prompts, examples, and practical AI workflows",
                    source="templates/page-blog.html",
                    label="PROMPT ARCHIVE",
                    language="html",
                ),
            ]
        )

    cards.extend(content_card(path, "page") for path in sorted((CONTENT / "pages").glob("*.md")))
    cards.extend(content_card(path, "post") for path in sorted((CONTENT / "posts").glob("*.md")))
    cards.sort(key=lambda item: str(item["url"]))
    ids = [str(item["id"]) for item in cards]
    urls = [str(item["url"]) for item in cards]
    if len(ids) != len(set(ids)) or len(urls) != len(set(urls)):
        raise SystemExit("Howl manifest generation produced duplicate card IDs or routes.")
    return {
        "project": {
            "name": "Prompts by Robert DeVore",
            "tagline": "A curated library of reusable AI prompts.",
            "url": "https://prompts.robertdevore.com",
        },
        "theme": {"name": "signal", "mode": "light"},
        "cards": cards,
    }


def write_manifest() -> int:
    manifest = build_manifest()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Synced {len(manifest['cards'])} Howl card definitions.")
    return len(manifest["cards"])


if __name__ == "__main__":
    write_manifest()
