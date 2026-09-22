#!/usr/bin/env python3
"""Verify the published prompt survives rendering and every discovery surface."""
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
SLUG = "kujo-repository-hardening-performance-efficiency"
URL = f"https://prompts.robertdevore.com/blog/{SLUG}/"
source = (ROOT / f"prompt-sources/{SLUG}.md").read_text().rstrip()
page = BeautifulSoup((ROOT / f"output/blog/{SLUG}/index.html").read_text(), "html.parser")
blocks = page.select("pre code.language-markdown")
assert len(blocks) == 1 and blocks[0].get_text() == source, "Prompt text changed during rendering"
assert "%%RAW_PROMPT:" not in str(page), "Unresolved source marker"
assert len(page.select("h1")) == 1
assert page.select_one('link[rel="canonical"]')["href"] == URL
social_url = page.select_one('meta[property="og:image"]')["content"]
social_path = ROOT / "output" / urlparse(social_url).path.lstrip("/")
assert social_path.is_file() and social_path.name.startswith(f"{SLUG}-social-")
with Image.open(social_path) as im:
    assert im.size == (1200, 630) and im.format == "WEBP"
for path in ("coding/index.html", "index.html", "blog/index.html"):
    soup = BeautifulSoup((ROOT / "output" / path).read_text(), "html.parser")
    assert any(SLUG in a["href"] for a in soup.select("a[href]")), path
for path in ("sitemap.xml", "feed/index.xml", "llms.txt"):
    assert URL in (ROOT / "output" / path).read_text(), path
for path in ("sitemap.xml", "feed/index.xml"):
    ET.parse(ROOT / "output" / path)
index = json.loads((ROOT / "output/assets/js/docs-search-index.json").read_text())
item = next(item for item in index["items"] if SLUG in item["url"])
assert source in item["text"], "Local search omitted full prompt"
webmcp = json.loads((ROOT / "output/.well-known/kujo-site-index.json").read_text())
assert any(SLUG in item["url"] for item in webmcp["items"])
for block in page.select('script[type="application/ld+json"]'):
    json.loads(block.string)
hero = ROOT / "assets/images/ascii-grunge/kujo-repository-hardening.webp"
social = ROOT / f"assets/social/{SLUG}-social.png"
with Image.open(hero) as im:
    hero_size = im.size
    assert im.format == "WEBP"
with Image.open(social) as im:
    assert im.size == (1200, 630) and im.format == "PNG"
receipt = dict(result="PASS", url=URL, prompt_words=len(source.split()),
               prompt_sha256=hashlib.sha256(source.encode()).hexdigest(),
               phases=sum(line.startswith("Phase ") for line in source.splitlines()),
               hero_dimensions=hero_size, hero_bytes=hero.stat().st_size,
               social_dimensions=[1200, 630], social_bytes=social.stat().st_size,
               generated_social_url=social_url, generated_social_bytes=social_path.stat().st_size,
               checks="verbatim prompt; category/home/archive links; sitemap/feed/llms; local search; WebMCP; canonical; social metadata; JSON-LD; images")
(AUDIT / "raw/new-post-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
