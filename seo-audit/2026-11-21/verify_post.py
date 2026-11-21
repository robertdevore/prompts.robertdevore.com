#!/usr/bin/env python3
"""Verify the focused article and its discovery paths on a local or live origin."""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from PIL import Image

from collect_production import request


BASE = "https://prompts.robertdevore.com"
SLUG = "post-build-technical-educator"
ROUTE = f"/blog/{SLUG}/"
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "prompt-sources" / f"{SLUG}.md"
TITLE = "Post-Build Technical Educator Prompt"


def fetch(url):
    return subprocess.check_output(["curl", "-fsSL", "--max-time", "20", url])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=BASE)
    parser.add_argument("--phase", choices=("baseline", "after"), required=True)
    args = parser.parse_args()
    url = f"{args.base}{ROUTE}"
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    canonical = BASE + ROUTE
    source = SOURCE.read_text().rstrip()
    assert soup.select_one('link[rel=canonical]')["href"] == canonical
    assert soup.select_one("main h1").get_text(strip=True) == TITLE
    assert soup.select_one('meta[property="og:url"]')["content"] == canonical
    assert "noindex" not in soup.select_one('meta[name=robots]')["content"]
    assert soup.select_one("pre > code.language-markdown").get_text() == source

    meta = soup.select_one('meta[name=description]')["content"]
    if args.phase == "after":
        expected = 'Turn finished AI coding work into a tutorial grounded in code, with hands-on exercises.'
        assert meta == expected
        assert soup.select_one('meta[property="og:description"]')["content"] == expected

    blocks = [json.loads(script.get_text()) for script in soup.select('script[type="application/ld+json"]')]
    article = next(block for block in blocks if block.get("@type") in {"Article", "BlogPosting"})
    assert article["headline"] == TITLE
    assert article["description"] == meta
    assert article["mainEntityOfPage"]["@id"] == canonical
    author = article["author"]
    assert author["name"] == "Robert DeVore"
    assert article["datePublished"].startswith("2026-11-21")

    image = soup.select_one(".article-visual img.featured-image")
    priority = (image.get("loading"), image.get("fetchpriority"))
    assert priority == (("lazy", None) if args.phase == "baseline" else ("eager", "high"))
    assert (image["width"], image["height"]) == ("1672", "941")
    og_image = soup.select_one('meta[property="og:image"]')["content"]
    assert soup.select_one('meta[property="og:image:alt"]')["content"]
    for image_url, expected_size in ((urljoin(url, image["src"]), (1672, 941)),
                                     (urljoin(args.base, og_image.removeprefix(BASE)), (1200, 630))):
        with Image.open(BytesIO(fetch(image_url))) as media:
            assert media.size == expected_size
            media.verify()

    for path in ("/", "/blog/", "/coding/"):
        listing = BeautifulSoup(fetch(args.base + path), "html.parser")
        assert any(urljoin(BASE + path, link["href"]) == canonical for link in listing.select("main a[href]")), path
    for path in ("/feed/index.xml", "/sitemap.xml", "/llms.txt", "/assets/js/docs-search-index.json"):
        assert canonical.encode() in fetch(args.base + path), path
    assert ROUTE.encode() in fetch(args.base + "/.well-known/kujo-site-index.json")
    if args.base == BASE:
        for path in (ROUTE.rstrip("/"), ROUTE + "?audit=1"):
            variant_url = args.base + path
            receipt = request(variant_url, "Mozilla/5.0", include_body=True)
            assert receipt["final_status"] == 200
            variant = BeautifulSoup(receipt["body"], "html.parser")
            assert urljoin(variant_url, variant.select_one('link[rel=canonical]')["href"]) == canonical
            if receipt["final_url"] == variant_url and not path.endswith("?audit=1"):
                refresh = variant.select_one('meta[http-equiv=refresh]')["content"]
                delay, target = refresh.split("; url=", maxsplit=1)
                assert delay == "0" and urljoin(variant_url, target) == canonical
    print(json.dumps({"status": "pass", "phase": args.phase, "url": url, "canonical": canonical,
                      "prompt_sha256": hashlib.sha256(source.encode()).hexdigest(),
                      "article_schema": article["@type"], "hero_priority": priority,
                      "og_image": og_image}, indent=2))


if __name__ == "__main__":
    main()
