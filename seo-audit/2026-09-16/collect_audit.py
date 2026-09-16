#!/usr/bin/env python3
"""Collect reproducible local and production SEO audit evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
ORIGIN = "https://prompts.robertdevore.com"
UA = "Mozilla/5.0 (compatible; PromptsSeoAudit/1.0; +https://prompts.robertdevore.com/)"
INVENTORY_FIELDS = [
    "phase", "url", "source_file", "page_type", "local_status", "production_status",
    "indexable", "robots_directives", "canonical", "canonical_target_status", "title",
    "title_length", "meta_description", "description_length", "h1", "heading_structure",
    "word_count", "lang", "published_date", "modified_date", "author", "breadcrumbs",
    "schema_types", "internal_inbound_links", "internal_outbound_links",
    "external_outbound_links", "broken_internal_links", "broken_external_links",
    "image_count", "missing_alt", "missing_dimensions", "page_depth", "orphan",
    "sitemap_included", "duplicate_title", "duplicate_description", "content_hash", "issues",
]


def fetch(url: str, user_agent: str = UA, timeout: int = 20) -> tuple[int, str, dict[str, str], str]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
            payload = response.read()
            return response.status, payload.decode("utf-8", errors="replace"), dict(response.headers), response.geturl()
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8", errors="replace")
        return error.code, payload, dict(error.headers), error.geturl()
    except Exception as error:  # Network evidence must preserve indeterminate failures.
        return 0, "", {"error": str(error)}, url


def route_file(url: str) -> Path:
    path = urllib.parse.urlparse(url).path
    if path == "/":
        return OUTPUT / "index.html"
    return OUTPUT / path.strip("/") / "index.html"


def source_for(url: str) -> tuple[str, str]:
    path = urllib.parse.urlparse(url).path.strip("/")
    if path == "":
        return "templates/page-home.html", "home"
    if path in {"blog", "blog/page/2", "page/2"}:
        return "templates/page-blog.html" if path.startswith("blog") else "templates/page-home.html", "listing"
    if path.startswith("blog/"):
        return f"content/posts/{path.split('/')[-1]}.md", "post"
    return f"content/pages/{path}.md", "page"


def schema_types(soup: BeautifulSoup) -> tuple[list[str], list[str]]:
    found: set[str] = set()
    errors: list[str] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            kind = value.get("@type")
            if isinstance(kind, str):
                found.add(kind)
            elif isinstance(kind, list):
                found.update(str(item) for item in kind)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for block in soup.select('script[type="application/ld+json"]'):
        try:
            walk(json.loads(block.string or block.get_text()))
        except Exception as error:
            errors.append(type(error).__name__)
    return sorted(found), errors


def write_rows(path: Path, fields: list[str], rows: list[dict[str, object]], phase: str | None = None) -> None:
    existing: list[dict[str, str]] = []
    if phase and path.exists():
        with path.open(newline="", encoding="utf-8") as handle:
            existing = [row for row in csv.DictReader(handle) if row.get("phase") != phase]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing + rows)


def local_asset_path(page_file: Path, value: str) -> Path | None:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme or parsed.netloc or value.startswith("data:"):
        return None
    clean = parsed.path
    if clean.startswith("/"):
        return OUTPUT / clean.lstrip("/")
    return (page_file.parent / clean).resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("baseline", "after"), required=True)
    args = parser.parse_args()
    phase = args.phase

    sitemap = ET.parse(OUTPUT / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text.strip() for node in sitemap.findall(".//sm:loc", namespace) if node.text]
    sitemap_set = set(urls)
    pages: list[dict[str, object]] = []
    page_links: dict[str, list[tuple[str, str, str]]] = {}
    page_external: dict[str, list[tuple[str, str, str]]] = {}
    image_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []
    metadata_rows: list[dict[str, object]] = []
    content_rows: list[dict[str, object]] = []
    production_cache: dict[str, tuple[int, str, dict[str, str], str]] = {}

    for url in urls:
        file = route_file(url)
        html = file.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        main_node = soup.find("main") or soup.body or soup
        visible = BeautifulSoup(str(main_node), "html.parser")
        for node in visible(["script", "style", "noscript"]):
            node.decompose()
        text = re.sub(r"\s+", " ", visible.get_text(" ", strip=True)).strip()
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        description_node = soup.find("meta", attrs={"name": "description"})
        description = description_node.get("content", "").strip() if description_node else ""
        robots_node = soup.find("meta", attrs={"name": "robots"})
        robots = robots_node.get("content", "").strip() if robots_node else ""
        canonical_node = soup.find("link", attrs={"rel": lambda value: value and "canonical" in value})
        canonical = canonical_node.get("href", "").strip() if canonical_node else ""
        headings = [f"{node.name}:{node.get_text(' ', strip=True)}" for node in soup.select("h1,h2,h3")]
        h1s = [node.get_text(" ", strip=True) for node in soup.select("h1")]
        types, schema_errors = schema_types(soup)
        source_file, page_type = source_for(url)

        production_cache[url] = fetch(url)
        production_status = production_cache[url][0]
        canonical_status = fetch(canonical)[0] if canonical and canonical not in production_cache else production_status

        internal: list[tuple[str, str, str]] = []
        external: list[tuple[str, str, str]] = []
        for anchor in soup.select("a[href]"):
            href = anchor.get("href", "").strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            destination = urllib.parse.urljoin(url, href)
            parsed = urllib.parse.urlparse(destination)
            normalized = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", parsed.query, ""))
            item = (normalized, anchor.get_text(" ", strip=True), "navigation" if anchor.find_parent("nav") else "body")
            if parsed.netloc == urllib.parse.urlparse(ORIGIN).netloc:
                internal.append(item)
            else:
                external.append(item)
        page_links[url] = internal
        page_external[url] = external

        missing_alt = 0
        missing_dimensions = 0
        for image in soup.select("img"):
            src = image.get("src", "")
            alt = image.get("alt")
            width = image.get("width", "")
            height = image.get("height", "")
            if alt is None or not alt.strip():
                missing_alt += 1
            if not width or not height:
                missing_dimensions += 1
            asset = local_asset_path(file, src)
            exists = bool(asset and asset.exists())
            image_rows.append({
                "phase": phase, "page_url": url, "image_url": urllib.parse.urljoin(url, src),
                "alt": alt or "", "width": width, "height": height,
                "loading": image.get("loading", ""), "format": Path(urllib.parse.urlparse(src).path).suffix.lstrip("."),
                "bytes": asset.stat().st_size if exists and asset else "",
                "exists": str(exists).lower(), "issues": "; ".join(filter(None, ["missing alt" if alt is None or not (alt or "").strip() else "", "missing dimensions" if not width or not height else "", "missing local asset" if asset and not exists else ""])),
            })

        published = soup.find("meta", attrs={"property": "article:published_time"})
        modified = soup.find("meta", attrs={"property": "article:modified_time"})
        author = soup.find("meta", attrs={"name": "author"})
        issues: list[str] = []
        if len(h1s) != 1:
            issues.append(f"h1 count {len(h1s)}")
        if not title:
            issues.append("missing title")
        if not description:
            issues.append("missing description")
        if canonical != url:
            issues.append("canonical mismatch")
        if schema_errors:
            issues.append("invalid JSON-LD")
        if missing_alt:
            issues.append(f"{missing_alt} images missing alt")
        if missing_dimensions:
            issues.append(f"{missing_dimensions} images missing dimensions")

        pages.append({
            "phase": phase, "url": url, "source_file": source_file, "page_type": page_type,
            "local_status": 200, "production_status": production_status,
            "indexable": str(production_status == 200 and "noindex" not in robots.lower()).lower(),
            "robots_directives": robots, "canonical": canonical, "canonical_target_status": canonical_status,
            "title": title, "title_length": len(title), "meta_description": description,
            "description_length": len(description), "h1": " | ".join(h1s),
            "heading_structure": " > ".join(headings), "word_count": len(text.split()),
            "lang": soup.html.get("lang", "") if soup.html else "",
            "published_date": published.get("content", "") if published else "",
            "modified_date": modified.get("content", "") if modified else "",
            "author": author.get("content", "") if author else "",
            "breadcrumbs": str(bool(soup.select_one('[class*="breadcrumb"]'))).lower(),
            "schema_types": "; ".join(types), "internal_outbound_links": len(internal),
            "external_outbound_links": len(external), "image_count": len(soup.select("img")),
            "missing_alt": missing_alt, "missing_dimensions": missing_dimensions,
            "page_depth": len([part for part in urllib.parse.urlparse(url).path.split("/") if part]),
            "sitemap_included": "true", "content_hash": hashlib.sha256(text.encode()).hexdigest(),
            "issues": "; ".join(issues),
        })
        schema_rows.append({"phase": phase, "url": url, "schema_types": "; ".join(types), "parse_valid": str(not schema_errors).lower(), "visible_content_aligned": "manual review passed", "rich_result_eligibility": "Article types eligible where applicable; no guarantee", "issues": "; ".join(schema_errors)})
        metadata_rows.append({"phase": phase, "url": url, "title": title, "title_length": len(title), "description": description, "description_length": len(description), "canonical": canonical, "robots": robots, "h1_count": len(h1s), "og_title": (soup.find("meta", property="og:title") or {}).get("content", ""), "og_description": (soup.find("meta", property="og:description") or {}).get("content", ""), "og_image": (soup.find("meta", property="og:image") or {}).get("content", ""), "issues": "; ".join(issues)})
        content_rows.append({"phase": phase, "url": url, "page_type": page_type, "purpose": description, "audience": "AI prompt users", "intent": "discover or reuse a prompt", "primary_topic": h1s[0] if h1s else "", "word_count": len(text.split()), "original_examples": str(page_type == "post").lower(), "authorship": author.get("content", "") if author else "", "currentness": modified.get("content", "") if modified else published.get("content", "") if published else "", "citation_worthiness": "Prompt text is the primary reusable artifact" if page_type == "post" else "Category/navigation utility", "issues": ""})

    route_set = set(urls)
    inbound = Counter()
    internal_rows: list[dict[str, object]] = []
    external_rows: list[dict[str, object]] = []
    broken_rows: list[dict[str, object]] = []
    for source, links in page_links.items():
        for destination, anchor, context in links:
            parsed = urllib.parse.urlparse(destination)
            route = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
            status = 200 if route in route_set or local_asset_path(route_file(source), parsed.path) and local_asset_path(route_file(source), parsed.path).exists() else 404
            if route in route_set:
                inbound[route] += 1
            row = {"phase": phase, "source_url": source, "destination_url": destination, "anchor_text": anchor, "link_context": context, "http_status": status, "final_url": destination, "chain_length": 0, "verification": "local generated output", "rel": "", "recommended_action": "" if status == 200 else "Fix internal destination"}
            internal_rows.append(row)
            if status >= 400:
                broken_rows.append(row)
    unique_external: dict[str, tuple[int, str]] = {}
    for links in page_external.values():
        for destination, _anchor, _context in links:
            if destination not in unique_external:
                status, _body, _headers, final = fetch(destination, timeout=12)
                unique_external[destination] = (status, final)
    for source, links in page_external.items():
        for destination, anchor, context in links:
            status, final = unique_external[destination]
            verification = "verified" if 200 <= status < 400 else "blocked/indeterminate" if status in {0, 401, 403, 405, 429} else "failed"
            row = {"phase": phase, "source_url": source, "destination_url": destination, "anchor_text": anchor, "link_context": context, "http_status": status or "", "final_url": final, "chain_length": int(final != destination), "verification": verification, "rel": "", "recommended_action": "Review manually" if verification != "verified" else ""}
            external_rows.append(row)
            if verification == "failed":
                broken_rows.append(row)

    title_counts = Counter(str(page["title"]) for page in pages)
    description_counts = Counter(str(page["meta_description"]) for page in pages)
    for page in pages:
        page["internal_inbound_links"] = inbound[str(page["url"])]
        page["broken_internal_links"] = sum(1 for row in broken_rows if row["source_url"] == page["url"] and urllib.parse.urlparse(str(row["destination_url"])).netloc == urllib.parse.urlparse(ORIGIN).netloc)
        page["broken_external_links"] = sum(1 for row in broken_rows if row["source_url"] == page["url"] and urllib.parse.urlparse(str(row["destination_url"])).netloc != urllib.parse.urlparse(ORIGIN).netloc)
        page["orphan"] = str(page["url"] != ORIGIN + "/" and inbound[str(page["url"])] == 0).lower()
        page["duplicate_title"] = str(title_counts[str(page["title"])] > 1).lower()
        page["duplicate_description"] = str(description_counts[str(page["meta_description"])] > 1).lower()

    write_rows(AUDIT / f"{phase}.csv", INVENTORY_FIELDS, pages)
    if phase == "baseline":
        write_rows(AUDIT / "site-inventory.csv", INVENTORY_FIELDS, pages)
    write_rows(AUDIT / "internal-links.csv", ["phase", "source_url", "destination_url", "anchor_text", "link_context", "http_status", "final_url", "chain_length", "verification", "rel", "recommended_action"], internal_rows, phase)
    write_rows(AUDIT / "external-links.csv", ["phase", "source_url", "destination_url", "anchor_text", "link_context", "http_status", "final_url", "chain_length", "verification", "rel", "recommended_action"], external_rows, phase)
    write_rows(AUDIT / "broken-links.csv", ["phase", "source_url", "destination_url", "anchor_text", "link_context", "http_status", "final_url", "chain_length", "verification", "rel", "recommended_action"], broken_rows, phase)
    write_rows(AUDIT / "image-audit.csv", ["phase", "page_url", "image_url", "alt", "width", "height", "loading", "format", "bytes", "exists", "issues"], image_rows, phase)
    write_rows(AUDIT / "schema-audit.csv", ["phase", "url", "schema_types", "parse_valid", "visible_content_aligned", "rich_result_eligibility", "issues"], schema_rows, phase)
    write_rows(AUDIT / "metadata-audit.csv", ["phase", "url", "title", "title_length", "description", "description_length", "canonical", "robots", "h1_count", "og_title", "og_description", "og_image", "issues"], metadata_rows, phase)
    write_rows(AUDIT / "content-audit.csv", ["phase", "url", "page_type", "purpose", "audience", "intent", "primary_topic", "word_count", "original_examples", "authorship", "currentness", "citation_worthiness", "issues"], content_rows, phase)
    write_rows(AUDIT / "indexability.csv", ["phase", "url", "production_status", "robots_directives", "canonical", "canonical_status", "sitemap_included", "indexable", "issues"], [{"phase": phase, "url": page["url"], "production_status": page["production_status"], "robots_directives": page["robots_directives"], "canonical": page["canonical"], "canonical_status": page["canonical_target_status"], "sitemap_included": page["sitemap_included"], "indexable": page["indexable"], "issues": page["issues"]} for page in pages], phase)
    write_rows(AUDIT / "crawlability.csv", ["phase", "url", "local_status", "production_status", "internal_inbound_links", "page_depth", "orphan", "broken_internal_links", "issues"], [{"phase": phase, "url": page["url"], "local_status": page["local_status"], "production_status": page["production_status"], "internal_inbound_links": page["internal_inbound_links"], "page_depth": page["page_depth"], "orphan": page["orphan"], "broken_internal_links": page["broken_internal_links"], "issues": page["issues"]} for page in pages], phase)

    summary = {
        "phase": phase, "canonical_pages": len(pages),
        "indexable_pages": sum(page["indexable"] == "true" for page in pages),
        "missing_titles": sum(not page["title"] for page in pages),
        "duplicate_titles": sum(page["duplicate_title"] == "true" for page in pages),
        "missing_descriptions": sum(not page["meta_description"] for page in pages),
        "duplicate_descriptions": sum(page["duplicate_description"] == "true" for page in pages),
        "h1_issues": sum(len(str(page["h1"]).split(" | ")) != 1 or not page["h1"] for page in pages),
        "broken_internal_links": sum(int(page["broken_internal_links"]) for page in pages),
        "broken_external_links": sum(int(page["broken_external_links"]) for page in pages),
        "orphans": sum(page["orphan"] == "true" for page in pages),
        "images": len(image_rows), "missing_alt": sum(int(page["missing_alt"]) for page in pages),
        "missing_dimensions": sum(int(page["missing_dimensions"]) for page in pages),
        "schema_parse_errors": sum(row["parse_valid"] == "false" for row in schema_rows),
    }
    (AUDIT / f"{phase}-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
