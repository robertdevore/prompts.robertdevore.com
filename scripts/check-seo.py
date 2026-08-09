#!/usr/bin/env python3
"""Validate SEO, social-card, and structured-data contracts for generated routes."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.json_ld: list[str] = []
        self._json_ld_buffer: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._json_ld_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self._json_ld_buffer is not None:
            self.json_ld.append("".join(self._json_ld_buffer).strip())
            self._json_ld_buffer = None

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self._json_ld_buffer is not None:
            self._json_ld_buffer.append(data)


def meta_content(parser: HeadParser, key: str, value: str) -> str:
    for item in parser.meta:
        if item.get(key) == value:
            return item.get("content", "").strip()
    return ""


def link_href(parser: HeadParser, rel: str) -> str:
    for item in parser.links:
        if rel in item.get("rel", "").split():
            return item.get("href", "").strip()
    return ""


def expected_schema(route: str) -> str:
    if route == "index.html":
        return "WebSite"
    if route == "404.html":
        return "WebPage"
    if route == "about/index.html":
        return "AboutPage"
    if route == "contact/index.html":
        return "ContactPage"
    if route.startswith("blog/") and route not in {"blog/index.html", "blog/page/2/index.html"}:
        return "BlogPosting"
    if route in {
        "page/2/index.html",
        "blog/index.html",
        "blog/page/2/index.html",
        "images/index.html",
        "writing/index.html",
        "business/index.html",
        "marketing/index.html",
        "coding/index.html",
    }:
        return "CollectionPage"
    return "WebPage"


def fail(errors: list[str], route: str, message: str) -> None:
    errors.append(f"{route}: {message}")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    files = sorted(root.rglob("index.html"))
    not_found = root / "404.html"
    if not_found.exists():
        files.append(not_found)

    errors: list[str] = []
    canonicals: dict[str, str] = {}
    checked = 0

    for path in files:
        route = path.relative_to(root).as_posix()
        source = path.read_text(encoding="utf-8")
        parser = HeadParser()
        parser.feed(source)
        checked += 1

        head = source.split("</head>", 1)[0]
        if "{{" in head:
            fail(errors, route, "unresolved template placeholder in document head")

        title = parser.title.strip()
        description = meta_content(parser, "name", "description")
        keywords = meta_content(parser, "name", "keywords")
        author = meta_content(parser, "name", "author")
        robots = meta_content(parser, "name", "robots")
        canonical = link_href(parser, "canonical")
        og_image = meta_content(parser, "property", "og:image")

        if not title:
            fail(errors, route, "missing title")
        elif route != "404.html" and len(title) > 65:
            fail(errors, route, f"title is {len(title)} characters (maximum 65)")
        if not description:
            fail(errors, route, "missing meta description")
        elif route != "404.html" and not 50 <= len(description) <= 160:
            fail(errors, route, f"description is {len(description)} characters (expected 50-160)")
        if not keywords or "Static Site Generator" in keywords:
            fail(errors, route, "missing or placeholder keywords")
        if author != "Robert DeVore":
            fail(errors, route, "author metadata is not Robert DeVore")
        if route == "404.html":
            if "noindex" not in robots:
                fail(errors, route, "404 must be noindex")
        elif "index" not in robots or "follow" not in robots:
            fail(errors, route, "route must be index, follow")
        if not canonical.startswith("https://prompts.robertdevore.com/"):
            fail(errors, route, "canonical URL is missing or not absolute")
        elif route != "404.html":
            if canonical in canonicals:
                fail(errors, route, f"canonical duplicates {canonicals[canonical]}")
            canonicals[canonical] = route

        required_property = [
            "og:title", "og:description", "og:url", "og:type", "og:site_name",
            "og:locale", "og:image", "og:image:secure_url", "og:image:type", "og:image:alt",
        ]
        for prop in required_property:
            if not meta_content(parser, "property", prop):
                fail(errors, route, f"missing {prop}")
        required_twitter = [
            "twitter:card", "twitter:title", "twitter:description", "twitter:site",
            "twitter:creator", "twitter:image", "twitter:image:alt",
        ]
        for name in required_twitter:
            if not meta_content(parser, "name", name):
                fail(errors, route, f"missing {name}")

        parsed_image = urlparse(og_image)
        if parsed_image.scheme != "https" or parsed_image.netloc != "prompts.robertdevore.com":
            fail(errors, route, "Open Graph image must use the production HTTPS origin")
        elif not (root / parsed_image.path.lstrip("/")).is_file():
            fail(errors, route, f"Open Graph image does not exist: {parsed_image.path}")

        if len(parser.json_ld) != 1:
            fail(errors, route, "expected exactly one JSON-LD block")
        else:
            try:
                structured = json.loads(parser.json_ld[0])
            except json.JSONDecodeError as exc:
                fail(errors, route, f"invalid JSON-LD: {exc}")
            else:
                schema = expected_schema(route)
                if structured.get("@context") != "https://schema.org":
                    fail(errors, route, "JSON-LD context is not Schema.org")
                if structured.get("@type") != schema:
                    fail(errors, route, f"JSON-LD type is {structured.get('@type')!r}, expected {schema}")
                if structured.get("url") != canonical:
                    fail(errors, route, "JSON-LD URL does not match canonical")
                if structured.get("image") != og_image:
                    fail(errors, route, "JSON-LD image does not match og:image")
                if schema == "BlogPosting":
                    for field in ("author", "datePublished", "dateModified", "mainEntityOfPage", "keywords"):
                        if not structured.get(field):
                            fail(errors, route, f"BlogPosting JSON-LD is missing {field}")
                    for prop in ("article:published_time", "article:author", "article:section", "article:tag"):
                        if not meta_content(parser, "property", prop):
                            fail(errors, route, f"article metadata is missing {prop}")

    if errors:
        for error in errors:
            print(f"SEO ERROR: {error}")
        print(f"SEO validation failed: {len(errors)} error(s) across {checked} routes")
        return 1

    print(f"SEO validation passed: {checked} routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
