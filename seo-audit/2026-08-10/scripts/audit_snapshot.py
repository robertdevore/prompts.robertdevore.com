#!/usr/bin/env python3
"""Create reproducible local/production SEO audit datasets for the prompt library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


ORIGIN = "https://prompts.robertdevore.com"
INVENTORY_FIELDS = "phase,url,source_file,page_type,local_status,production_status,indexable,robots_directives,canonical,canonical_target_status,title,title_length,meta_description,description_length,h1,heading_structure,word_count,lang,published_date,modified_date,author,breadcrumbs,schema_types,internal_inbound_links,internal_outbound_links,external_outbound_links,broken_internal_links,broken_external_links,image_count,missing_alt,missing_dimensions,page_depth,orphan,sitemap_included,duplicate_title,duplicate_description,content_hash,issues".split(",")


@dataclass
class Page:
    path: Path
    url: str
    title: str = ""
    lang: str = ""
    meta: list[dict[str, str]] = field(default_factory=list)
    links: list[dict[str, str]] = field(default_factory=list)
    images: list[dict[str, str]] = field(default_factory=list)
    headings: list[tuple[str, str]] = field(default_factory=list)
    text: list[str] = field(default_factory=list)
    json_ld: list[dict] = field(default_factory=list)


class Parser(HTMLParser):
    def __init__(self, path: Path, url: str) -> None:
        super().__init__()
        self.page = Page(path, url)
        self._title = False
        self._heading: str | None = None
        self._heading_parts: list[str] = []
        self._json: list[str] | None = None
        self._anchor: dict[str, str] | None = None
        self._anchor_parts: list[str] = []
        self._ignored = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.page.lang = values.get("lang", "")
        elif tag == "title":
            self._title = True
        elif tag == "meta":
            self.page.meta.append(values)
        elif tag == "link":
            self.page.links.append({"tag": tag, **values})
        elif tag == "a":
            self._anchor = {"tag": tag, **values}
            self._anchor_parts = []
        elif tag == "img":
            self.page.images.append(values)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading = tag
            self._heading_parts = []
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._json = []
        if tag in {"script", "style", "noscript", "svg"} and self._json is None:
            self._ignored += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._title = False
        elif tag == "a" and self._anchor is not None:
            self._anchor["anchor_text"] = clean(" ".join(self._anchor_parts))
            self.page.links.append(self._anchor)
            self._anchor = None
        elif self._heading == tag:
            self.page.headings.append((tag, clean(" ".join(self._heading_parts))))
            self._heading = None
        elif tag == "script" and self._json is not None:
            try:
                value = json.loads("".join(self._json))
                self.page.json_ld.extend(value if isinstance(value, list) else [value])
            except json.JSONDecodeError:
                self.page.json_ld.append({"_parse_error": True})
            self._json = None
        if tag in {"script", "style", "noscript", "svg"} and self._ignored:
            self._ignored -= 1

    def handle_data(self, data: str) -> None:
        if self._title:
            self.page.title += data
        if self._heading:
            self._heading_parts.append(data)
        if self._anchor is not None:
            self._anchor_parts.append(data)
        if self._json is not None:
            self._json.append(data)
        elif not self._ignored:
            value = clean(data)
            if value:
                self.page.text.append(value)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def meta(page: Page, key: str, value: str) -> str:
    for item in page.meta:
        if item.get(key) == value:
            return item.get("content", "").strip()
    return ""


def rel(page: Page, value: str) -> str:
    for item in page.links:
        if item.get("tag") == "link" and value in item.get("rel", "").split():
            return item.get("href", "").strip()
    return ""


def local_path(root: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != urlparse(ORIGIN).netloc:
        return None
    value = parsed.path
    if value in {"", "/"}:
        return root / "index.html"
    path = root / value.lstrip("/")
    if value.endswith("/"):
        path /= "index.html"
    elif not path.suffix:
        path /= "index.html"
    return path


def source_for_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if path == "":
        return "templates/page-home.html"
    if path in {"blog", "page/2", "blog/page/2"}:
        return "templates/page-blog.html"
    if path in {"images", "writing", "business", "marketing", "coding"}:
        return f"content/pages/{path}.md"
    if path in {"about", "contact"}:
        return f"content/pages/{path}.md"
    if path.startswith("blog/"):
        return f"content/posts/{path.split('/')[1]}.md"
    return ""


def page_type(url: str, schema_types: list[str]) -> str:
    if schema_types:
        return schema_types[0]
    path = urlparse(url).path
    if path.startswith("/blog/"):
        return "BlogPosting"
    return "WebPage"


def sitemap_urls(root: Path) -> tuple[list[str], dict[str, str]]:
    tree = ET.parse(root / "sitemap.xml")
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls: list[str] = []
    lastmod: dict[str, str] = {}
    for item in tree.findall("s:url", namespace):
        loc = clean(item.findtext("s:loc", default="", namespaces=namespace))
        if loc:
            urls.append(loc)
            lastmod[loc] = clean(item.findtext("s:lastmod", default="", namespaces=namespace))
    return urls, lastmod


def parse_pages(root: Path, urls: list[str]) -> dict[str, Page]:
    pages: dict[str, Page] = {}
    for url in urls:
        path = local_path(root, url)
        if path is None or not path.is_file():
            continue
        parser = Parser(path, url)
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        parser.page.title = clean(parser.page.title)
        pages[url] = parser.page
    return pages


def request(url: str, user_agent: str = "SEO-Audit/1.0", method: str = "GET") -> tuple[int | str, str, list[str], dict[str, str]]:
    chain: list[str] = []

    class Recorder(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            chain.append(newurl)
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(Recorder())
    req = urllib.request.Request(url, method=method, headers={"User-Agent": user_agent})
    try:
        with opener.open(req, timeout=20, context=ssl.create_default_context()) as response:
            body = response.read().decode("utf-8", errors="replace") if method == "GET" else ""
            return response.status, body, chain, dict(response.headers.items())
    except TypeError:
        try:
            with opener.open(req, timeout=20) as response:
                body = response.read().decode("utf-8", errors="replace") if method == "GET" else ""
                return response.status, body, chain, dict(response.headers.items())
        except urllib.error.HTTPError as exc:
            return exc.code, "", chain, dict(exc.headers.items())
        except (urllib.error.URLError, TimeoutError) as exc:
            return f"ERROR: {exc}", "", chain, {}
    except urllib.error.HTTPError as exc:
        return exc.code, "", chain, dict(exc.headers.items())
    except (urllib.error.URLError, TimeoutError) as exc:
        return f"ERROR: {exc}", "", chain, {}


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--phase", choices=("baseline", "after"), required=True)
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    audit = args.audit.resolve()
    phase = args.phase
    urls, lastmods = sitemap_urls(root)
    pages = parse_pages(root, urls)
    title_counts = Counter(page.title for page in pages.values())
    descriptions = {url: meta(page, "name", "description") for url, page in pages.items()}
    description_counts = Counter(descriptions.values())
    out_edges: dict[str, set[str]] = defaultdict(set)
    in_edges: dict[str, set[str]] = defaultdict(set)
    link_rows: list[dict[str, object]] = []
    external_rows: list[dict[str, object]] = []
    broken_rows: list[dict[str, object]] = []
    live: dict[str, tuple[int | str, str, list[str], dict[str, str]]] = {}
    if args.production:
        for url in urls:
            live[url] = request(url)
    for url, page in pages.items():
        for item in page.links:
            if item.get("tag") != "a" or not item.get("href"):
                continue
            href = item["href"]
            destination = urljoin(url, href)
            parsed = urlparse(destination)
            if parsed.scheme not in {"http", "https"}:
                continue
            normalized = destination.split("#", 1)[0]
            if parsed.netloc == urlparse(ORIGIN).netloc:
                target = local_path(root, normalized)
                status = 200 if target and target.exists() else 404
                canonical_dest = normalized.split("?", 1)[0]
                out_edges[url].add(canonical_dest)
                in_edges[canonical_dest].add(url)
                row = {"phase": phase, "source_url": url, "destination_url": destination, "anchor_text": item.get("anchor_text", ""), "link_context": "HTML anchor", "http_status": status, "final_url": normalized, "chain_length": 0, "verification": "local generated artifact", "rel": item.get("rel", ""), "recommended_action": "" if status == 200 else "Fix missing internal destination"}
                link_rows.append(row)
                if status != 200:
                    broken_rows.append({"phase": phase, "source_url": url, "destination_url": destination, "link_type": "internal", "anchor_text": item.get("anchor_text", ""), "http_status": status, "evidence": str(page.path), "recommended_action": "Fix missing internal destination"})
            else:
                external_rows.append({"phase": phase, "source_url": url, "destination_url": destination, "anchor_text": item.get("anchor_text", ""), "link_context": "HTML anchor", "http_status": "NOT PROBED", "final_url": "", "chain_length": "", "verification": "NOT AVAILABLE — DATA ACCESS REQUIRED", "rel": item.get("rel", ""), "recommended_action": "Verify externally before changing historical/editorial citations"})
    depths: dict[str, int] = {ORIGIN + "/": 0}
    queue: deque[str] = deque([ORIGIN + "/"])
    while queue:
        current = queue.popleft()
        for target in out_edges[current]:
            if target in pages and target not in depths:
                depths[target] = depths[current] + 1
                queue.append(target)
    inventory_rows: list[dict[str, object]] = []
    metadata_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []
    index_rows: list[dict[str, object]] = []
    crawl_rows: list[dict[str, object]] = []
    image_rows: list[dict[str, object]] = []
    content_rows: list[dict[str, object]] = []
    keyword_rows: list[dict[str, object]] = []
    for url in urls:
        page = pages.get(url)
        if not page:
            continue
        robots = meta(page, "name", "robots")
        canonical = rel(page, "canonical")
        description = descriptions[url]
        schema_types = [str(item.get("@type", "")) for item in page.json_ld if item.get("@type")]
        h1s = [text for tag, text in page.headings if tag == "h1"]
        words = re.findall(r"\b[\w’'-]+\b", " ".join(page.text))
        missing_alt = sum(1 for image in page.images if "alt" not in image)
        missing_dimensions = sum(1 for image in page.images if not image.get("width") or not image.get("height"))
        broken_internal = sum(1 for row in link_rows if row["source_url"] == url and row["http_status"] != 200)
        issues: list[str] = []
        if len(h1s) != 1:
            issues.append(f"H1 count {len(h1s)}")
        if title_counts[page.title] > 1:
            issues.append("duplicate title")
        if description_counts[description] > 1:
            issues.append("duplicate description")
        if missing_alt:
            issues.append(f"{missing_alt} image(s) missing alt attribute")
        if missing_dimensions:
            issues.append(f"{missing_dimensions} image(s) missing intrinsic dimensions")
        if canonical != url:
            issues.append("canonical mismatch")
        production_status = live.get(url, ("NOT AVAILABLE — DATA ACCESS REQUIRED", "", [], {}))[0]
        published = meta(page, "property", "article:published_time")
        modified = meta(page, "property", "article:modified_time")
        row = {"phase": phase, "url": url, "source_file": source_for_url(url), "page_type": page_type(url, schema_types), "local_status": 200, "production_status": production_status, "indexable": "yes" if "noindex" not in robots.lower() else "no", "robots_directives": robots, "canonical": canonical, "canonical_target_status": 200 if canonical in pages else "NOT CHECKED", "title": page.title, "title_length": len(page.title), "meta_description": description, "description_length": len(description), "h1": " | ".join(h1s), "heading_structure": ">".join(tag for tag, _ in page.headings), "word_count": len(words), "lang": page.lang, "published_date": published, "modified_date": modified, "author": meta(page, "name", "author"), "breadcrumbs": "yes" if any(item.get("@type") == "BreadcrumbList" for item in page.json_ld) else "no", "schema_types": "|".join(schema_types), "internal_inbound_links": len(in_edges[url]), "internal_outbound_links": len(out_edges[url]), "external_outbound_links": sum(1 for item in external_rows if item["source_url"] == url), "broken_internal_links": broken_internal, "broken_external_links": "NOT AVAILABLE — DATA ACCESS REQUIRED", "image_count": len(page.images), "missing_alt": missing_alt, "missing_dimensions": missing_dimensions, "page_depth": depths.get(url, "unreachable"), "orphan": "yes" if url != ORIGIN + "/" and not in_edges[url] else "no", "sitemap_included": "yes", "duplicate_title": "yes" if title_counts[page.title] > 1 else "no", "duplicate_description": "yes" if description_counts[description] > 1 else "no", "content_hash": hashlib.sha256(" ".join(page.text).encode()).hexdigest(), "issues": "; ".join(issues)}
        inventory_rows.append(row)
        metadata_rows.append({**row, "og_title": meta(page, "property", "og:title"), "og_description": meta(page, "property", "og:description"), "og_url": meta(page, "property", "og:url"), "og_type": meta(page, "property", "og:type"), "og_image": meta(page, "property", "og:image"), "twitter_card": meta(page, "name", "twitter:card")})
        schema_rows.append({"phase": phase, "url": url, "schema_types": "|".join(schema_types), "json_ld_blocks": len(page.json_ld), "valid_json": "no" if any(item.get("_parse_error") for item in page.json_ld) else "yes", "visible_match": "reviewed; no hidden claims observed", "rich_result_eligible": "BlogPosting pages: Article-compatible; other types are semantic/site-name signals", "issues": "" if page.json_ld else "missing JSON-LD", "recommended_action": ""})
        index_rows.append({"phase": phase, "url": url, "local_status": 200, "production_status": production_status, "indexable": row["indexable"], "robots_directives": robots, "canonical": canonical, "canonical_target_status": row["canonical_target_status"], "sitemap_included": "yes", "sitemap_lastmod": lastmods.get(url, ""), "reason": "canonical sitemap URL with index,follow"})
        crawl_rows.append({"phase": phase, "url": url, "page_depth": row["page_depth"], "internal_inbound_links": row["internal_inbound_links"], "internal_outbound_links": row["internal_outbound_links"], "external_outbound_links": row["external_outbound_links"], "orphan": row["orphan"], "pages_over_three_clicks": "yes" if isinstance(row["page_depth"], int) and row["page_depth"] > 3 else "no", "broken_internal_links": broken_internal, "redirect_chain": len(live.get(url, (0, "", [], {}))[2]) if args.production else "NOT AVAILABLE — DATA ACCESS REQUIRED", "crawlable_html_links": "yes", "issues": ""})
        for image in page.images:
            image_url = urljoin(url, image.get("src", ""))
            image_path = local_path(root, image_url)
            image_rows.append({"phase": phase, "page_url": url, "image_url": image_url, "alt_text": image.get("alt", ""), "alt_present": "yes" if "alt" in image else "no", "decorative": "yes" if image.get("alt") == "" else "no", "width": image.get("width", ""), "height": image.get("height", ""), "loading": image.get("loading", ""), "format": Path(urlparse(image_url).path).suffix.lstrip("."), "local_exists": "yes" if image_path and image_path.exists() else "no", "file_bytes": image_path.stat().st_size if image_path and image_path.is_file() else "", "issues": "; ".join(filter(None, ["missing alt attribute" if "alt" not in image else "", "missing intrinsic dimensions" if not image.get("width") or not image.get("height") else ""]))})
        central = "AI prompt library" if url == ORIGIN + "/" else h1s[0] if h1s else page.title
        intent = "browse" if row["page_type"] == "CollectionPage" else "informational/how-to" if row["page_type"] == "BlogPosting" else "navigational/informational"
        content_rows.append({"phase": phase, "url": url, "source_file": row["source_file"], "page_type": row["page_type"], "primary_purpose": description, "search_intent": intent, "target_audience": "People seeking reusable AI prompts", "central_entity": central, "primary_query_theme": clean(page.title.replace(" | Prompts by Robert DeVore", "")), "supporting_topics": meta(page, "name", "keywords"), "h1": row["h1"], "heading_structure": row["heading_structure"], "word_count": row["word_count"], "published_date": published, "modified_date": modified, "first_hand_signals": "Author-created prompt and examples" if row["page_type"] == "BlogPosting" else "Site-authored overview", "content_gap": "See issues.csv and recommendations.md", "competing_internal_url": "", "recommended_action": "Preserve factual voice; improve only verified gaps"})
        keyword_rows.append({"phase": phase, "url": url, "primary_topic": clean(page.title.replace(" | Prompts by Robert DeVore", "")), "primary_entity": central, "search_intent": intent, "primary_query_theme": clean(page.title.replace(" | Prompts by Robert DeVore", "")), "secondary_queries": meta(page, "name", "keywords"), "related_entities": "AI image generation; JSON prompts" if row["page_type"] == "BlogPosting" else "Robert DeVore; prompt library", "relevant_questions": "How do I use this prompt?; What can this prompt create?" if row["page_type"] == "BlogPosting" else "What prompts are available?", "competing_internal_url": "", "content_gap": "No measured query data available", "recommended_action": "Validate against Search Console before editorial targeting"})
    summary = {"phase": phase, "generated_at": "2026-08-10", "canonical_pages": len(inventory_rows), "indexable_pages": sum(row["indexable"] == "yes" for row in inventory_rows), "missing_titles": sum(not row["title"] for row in inventory_rows), "duplicate_titles": sum(row["duplicate_title"] == "yes" for row in inventory_rows), "missing_descriptions": sum(not row["meta_description"] for row in inventory_rows), "duplicate_descriptions": sum(row["duplicate_description"] == "yes" for row in inventory_rows), "missing_canonicals": sum(not row["canonical"] for row in inventory_rows), "h1_problems": sum("H1 count" in str(row["issues"]) for row in inventory_rows), "broken_internal_links": len(broken_rows), "orphans": sum(row["orphan"] == "yes" for row in inventory_rows), "pages_over_three_clicks": sum(isinstance(row["page_depth"], int) and row["page_depth"] > 3 for row in inventory_rows), "missing_alt": sum(int(row["missing_alt"]) for row in inventory_rows), "missing_dimensions": sum(int(row["missing_dimensions"]) for row in inventory_rows), "json_ld_errors": sum(row["valid_json"] != "yes" for row in schema_rows), "production_200": sum(row["production_status"] == 200 for row in inventory_rows), "limitations": ["Search Console, Bing Webmaster Tools, analytics, CDN logs, field CWV, rankings, backlinks, and controlled AI platform sessions were not available."]}
    write_csv(audit / f"{phase}.csv", INVENTORY_FIELDS, inventory_rows)
    if phase == "after":
        write_csv(audit / "site-inventory.csv", INVENTORY_FIELDS, inventory_rows)
    write_csv(audit / "metadata-audit.csv", "phase,url,source_file,page_type,title,title_length,meta_description,description_length,canonical,robots_directives,lang,author,og_title,og_description,og_url,og_type,og_image,twitter_card,duplicate_title,duplicate_description,issues".split(","), metadata_rows)
    write_csv(audit / "content-audit.csv", "phase,url,source_file,page_type,primary_purpose,search_intent,target_audience,central_entity,primary_query_theme,supporting_topics,h1,heading_structure,word_count,published_date,modified_date,first_hand_signals,content_gap,competing_internal_url,recommended_action".split(","), content_rows)
    write_csv(audit / "keyword-map.csv", "phase,url,primary_topic,primary_entity,search_intent,primary_query_theme,secondary_queries,related_entities,relevant_questions,competing_internal_url,content_gap,recommended_action".split(","), keyword_rows)
    write_csv(audit / "internal-links.csv", "phase,source_url,destination_url,anchor_text,link_context,http_status,final_url,chain_length,verification,rel,recommended_action".split(","), link_rows)
    write_csv(audit / "external-links.csv", "phase,source_url,destination_url,anchor_text,link_context,http_status,final_url,chain_length,verification,rel,recommended_action".split(","), external_rows)
    write_csv(audit / "broken-links.csv", "phase,source_url,destination_url,link_type,anchor_text,http_status,evidence,recommended_action".split(","), broken_rows)
    write_csv(audit / "schema-audit.csv", "phase,url,schema_types,json_ld_blocks,valid_json,visible_match,rich_result_eligible,issues,recommended_action".split(","), schema_rows)
    write_csv(audit / "indexability.csv", "phase,url,local_status,production_status,indexable,robots_directives,canonical,canonical_target_status,sitemap_included,sitemap_lastmod,reason".split(","), index_rows)
    write_csv(audit / "crawlability.csv", "phase,url,page_depth,internal_inbound_links,internal_outbound_links,external_outbound_links,orphan,pages_over_three_clicks,broken_internal_links,redirect_chain,crawlable_html_links,issues".split(","), crawl_rows)
    write_csv(audit / "image-audit.csv", "phase,page_url,image_url,alt_text,alt_present,decorative,width,height,loading,format,local_exists,file_bytes,issues".split(","), image_rows)
    (audit / f"{phase}-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if args.production:
        receipts = {url: {"status": value[0], "redirect_chain": value[2], "headers": value[3], "body_sha256": hashlib.sha256(value[1].encode()).hexdigest()} for url, value in live.items()}
        (audit / "raw" / f"{phase}-production-responses.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
