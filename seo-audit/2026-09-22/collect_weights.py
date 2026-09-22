#!/usr/bin/env python3
"""Record static referenced asset weights; these are not network or CWV measurements."""
import argparse
import csv
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--phase", choices=("baseline", "after"), required=True)
args = parser.parse_args()
out = ROOT / "output"
rows = []
for route in ("/", "/coding/", "/blog/dependabot-security-maintenance-agent/"):
    path = out / route.strip("/") / "index.html"
    soup = BeautifulSoup(path.read_text(), "html.parser")
    sizes = {"css": 0, "js": 0, "image": 0}
    paths = set()
    for selector, attr, kind in (("link[rel=stylesheet]", "href", "css"), ("script[src]", "src", "js"), ("img[src]", "src", "image")):
        for node in soup.select(selector):
            parsed = urlparse(node[attr])
            if parsed.netloc or parsed.scheme:
                continue
            asset = ((out / parsed.path.lstrip("/")) if parsed.path.startswith("/") else (path.parent / parsed.path)).resolve()
            if asset.is_file() and asset not in paths:
                sizes[kind] += asset.stat().st_size
                paths.add(asset)
    rows.append(dict(phase=args.phase, url="https://prompts.robertdevore.com" + route,
                     template="home" if route == "/" else "category" if route == "/coding/" else "post",
                     run_date="2026-09-22", environment="downloaded pinned CI artifact",
                     lighthouse_version="13.5.0 (baseline failed: NO_FCP)", html_bytes=path.stat().st_size,
                     css_bytes=sizes["css"], js_bytes=sizes["js"], image_bytes=sizes["image"],
                     font_bytes="not measured", requests="not measured", lcp_ms="not available", inp_ms="NOT AVAILABLE — DATA ACCESS REQUIRED",
                     cls="not available", ttfb_ms="not measured", source="generated files",
                     notes="Uncompressed unique local references only; excludes external fonts, dynamic fetches and caching; not transfer size. No valid comparable Lighthouse baseline."))
target = AUDIT / "performance.csv"
with target.open() as f:
    prior = [row for row in csv.DictReader(f) if row.get("phase") != args.phase]
with target.open("w") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(prior + rows)
print(f"Recorded {len(rows)} static asset profiles for {args.phase}")
