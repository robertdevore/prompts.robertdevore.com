#!/usr/bin/env python3
"""Validate crawler discovery files and their relationship to canonical HTML."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


ORIGIN = "https://prompts.robertdevore.com"
SITEMAP_URL = f"{ORIGIN}/sitemap.xml"
FEED_URL = f"{ORIGIN}/feed/index.xml"


class DiscoveryHeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.links.append(values)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def meta_content(parser: DiscoveryHeadParser, name: str) -> str:
    for item in parser.meta:
        if item.get("name") == name:
            return item.get("content", "").strip()
    return ""


def link_href(parser: DiscoveryHeadParser, rel: str, mime: str = "") -> str:
    for item in parser.links:
        if rel in item.get("rel", "").split() and (not mime or item.get("type") == mime):
            return item.get("href", "").strip()
    return ""


def local_path_for_url(root: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if f"{parsed.scheme}://{parsed.netloc}" != ORIGIN:
        return None
    path = parsed.path
    if path.endswith("/"):
        return root / path.lstrip("/") / "index.html"
    return root / path.lstrip("/")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    errors: list[str] = []
    canonical_routes: dict[str, str] = {}

    html_files = sorted(root.rglob("index.html"))
    for path in html_files:
        route = path.relative_to(root).as_posix()
        parser = DiscoveryHeadParser()
        parser.feed(path.read_text(encoding="utf-8").split("</head>", 1)[0])
        canonical = link_href(parser, "canonical")
        robots = meta_content(parser, "robots").lower()
        if "noindex" not in robots:
            if not canonical:
                fail(errors, f"{route}: indexable page lacks a canonical URL")
            elif canonical in canonical_routes:
                fail(errors, f"{route}: canonical duplicates {canonical_routes[canonical]}")
            else:
                canonical_routes[canonical] = route
        rss_href = link_href(parser, "alternate", "application/rss+xml")
        if urljoin(canonical or ORIGIN + "/", rss_href) != FEED_URL:
            fail(errors, f"{route}: RSS autodiscovery does not resolve to {FEED_URL}")

    robots_path = root / "robots.txt"
    robots = robots_path.read_text(encoding="utf-8") if robots_path.is_file() else ""
    if not robots.startswith("User-agent: *\n"):
        fail(errors, "robots.txt: wildcard user-agent group is missing")
    if "Allow: /" not in robots:
        fail(errors, "robots.txt: public crawl allowance is missing")
    if re.search(r"(?im)^Disallow:\s*\S", robots):
        fail(errors, "robots.txt: a non-empty Disallow rule blocks crawlers")
    if f"Sitemap: {SITEMAP_URL}" not in robots:
        fail(errors, "robots.txt: production sitemap declaration is missing")

    sitemap_path = root / "sitemap.xml"
    sitemap_urls: list[str] = []
    try:
        sitemap_root = ET.parse(sitemap_path).getroot()
    except (ET.ParseError, OSError) as exc:
        fail(errors, f"sitemap.xml: invalid XML: {exc}")
    else:
        if sitemap_root.tag != "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset":
            fail(errors, "sitemap.xml: root element is not the Sitemap protocol urlset")
        sitemap_urls = [
            (item.text or "").strip()
            for item in sitemap_root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        ]
        if len(sitemap_urls) != len(set(sitemap_urls)):
            fail(errors, "sitemap.xml: duplicate URLs found")
        for url in sitemap_urls:
            parsed = urlparse(url)
            if f"{parsed.scheme}://{parsed.netloc}" != ORIGIN:
                fail(errors, f"sitemap.xml: URL is outside the HTTPS production origin: {url}")
            local_path = local_path_for_url(root, url)
            if local_path is None or not local_path.is_file():
                fail(errors, f"sitemap.xml: URL has no generated page: {url}")
        expected = set(canonical_routes)
        actual = set(sitemap_urls)
        for missing in sorted(expected - actual):
            fail(errors, f"sitemap.xml: indexable canonical URL is missing: {missing}")
        for extra in sorted(actual - expected):
            fail(errors, f"sitemap.xml: noncanonical or nonindexable URL is present: {extra}")

    feed_path = root / "feed/index.xml"
    feed_links: set[str] = set()
    try:
        feed_root = ET.parse(feed_path).getroot()
    except (ET.ParseError, OSError) as exc:
        fail(errors, f"feed/index.xml: invalid XML: {exc}")
    else:
        if feed_root.tag != "rss" or feed_root.get("version") != "2.0":
            fail(errors, "feed/index.xml: root must be RSS 2.0")
        channel = feed_root.find("channel")
        if channel is None:
            fail(errors, "feed/index.xml: channel is missing")
        else:
            required_channel = {
                "title": "Prompts by Robert DeVore",
                "link": f"{ORIGIN}/",
                "language": "en-us",
                "generator": "Kujo SSG",
                "ttl": "60",
            }
            for tag, expected_value in required_channel.items():
                if (channel.findtext(tag) or "").strip() != expected_value:
                    fail(errors, f"feed/index.xml: channel {tag} is incomplete")
            atom_self = channel.find("{http://www.w3.org/2005/Atom}link")
            if atom_self is None or atom_self.get("href") != FEED_URL or atom_self.get("rel") != "self":
                fail(errors, "feed/index.xml: Atom self-discovery link is missing")
            for item in channel.findall("item"):
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                guid = (item.findtext("guid") or "").strip()
                description = (item.findtext("description") or "").strip()
                guid_element = item.find("guid")
                if not title or not description:
                    fail(errors, "feed/index.xml: item title or description is missing")
                if link != guid or guid_element is None or guid_element.get("isPermaLink") != "true":
                    fail(errors, f"feed/index.xml: item GUID is not its permalink: {link}")
                if link in feed_links:
                    fail(errors, f"feed/index.xml: duplicate item link: {link}")
                feed_links.add(link)
                if link not in canonical_routes:
                    fail(errors, f"feed/index.xml: item is not a canonical generated page: {link}")
                try:
                    parsedate_to_datetime((item.findtext("pubDate") or "").strip())
                except (TypeError, ValueError, OverflowError):
                    fail(errors, f"feed/index.xml: invalid pubDate for {link}")
                if not item.findall("category"):
                    fail(errors, f"feed/index.xml: item has no categories: {link}")
                if "&apos;" in description or "&amp;" in description:
                    fail(errors, f"feed/index.xml: item description contains a double-escaped entity: {link}")

    expected_feed_links = {
        url for url in canonical_routes
        if re.fullmatch(rf"{re.escape(ORIGIN)}/blog/[^/]+/", url)
    }
    if feed_links != expected_feed_links:
        for missing in sorted(expected_feed_links - feed_links):
            fail(errors, f"feed/index.xml: post is missing from the feed: {missing}")

    llms_path = root / "llms.txt"
    llms = llms_path.read_text(encoding="utf-8") if llms_path.is_file() else ""
    nonempty_lines = [line.strip() for line in llms.splitlines() if line.strip()]
    if not nonempty_lines or nonempty_lines[0] != "# Prompts by Robert DeVore":
        fail(errors, "llms.txt: required site H1 is missing")
    if len(nonempty_lines) < 2 or not nonempty_lines[1].startswith("> "):
        fail(errors, "llms.txt: project summary blockquote is missing")
    llms_links = {match[1] for match in re.findall(r"\[([^]]+)]\((https://[^)]+)\)", llms)}
    for url in sorted(llms_links):
        local_path = local_path_for_url(root, url)
        if local_path is None or not local_path.is_file():
            fail(errors, f"llms.txt: link is off-origin or missing locally: {url}")
    required_llms_links = {
        url for url in canonical_routes
        if url == f"{ORIGIN}/" or not re.search(r"/(?:blog/)?page/\d+/$", url)
    } - {f"{ORIGIN}/blog/"}
    required_llms_links.update({FEED_URL, SITEMAP_URL})
    for missing in sorted(required_llms_links - llms_links):
        fail(errors, f"llms.txt: important site resource is missing: {missing}")

    if errors:
        for error in errors:
            print(f"DISCOVERY ERROR: {error}")
        print(f"Discovery validation failed: {len(errors)} error(s)")
        return 1

    print(
        "Discovery validation passed: "
        f"{len(canonical_routes)} canonical routes, {len(sitemap_urls)} sitemap URLs, "
        f"{len(feed_links)} feed items, {len(llms_links)} llms.txt links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
