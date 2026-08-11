#!/usr/bin/env python3
"""Verify unique external HTML links without misclassifying access blocks."""

from __future__ import annotations

import argparse
import csv
import urllib.error
import urllib.request
from pathlib import Path


FIELDS = "phase,source_url,destination_url,anchor_text,link_context,http_status,final_url,chain_length,verification,rel,recommended_action".split(",")


def probe(url: str) -> tuple[object, str, int, str]:
    redirects: list[str] = []

    class Recorder(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            redirects.append(newurl)
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(Recorder())
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 SEO-Audit/1.0"})
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, response.url, len(redirects), "verified"
    except urllib.error.HTTPError as exc:
        if exc.code in {401, 403, 405, 429}:
            return exc.code, exc.url, len(redirects), "blocked or indeterminate; not classified as broken"
        return exc.code, exc.url, len(redirects), "HTTP error"
    except (urllib.error.URLError, TimeoutError) as exc:
        return f"ERROR: {exc}", "", len(redirects), "network indeterminate"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.csv.open(encoding="utf-8")))
    results: dict[str, tuple[object, str, int, str]] = {}
    for row in rows:
        url = row["destination_url"]
        if url not in results:
            results[url] = probe(url)
        status, final_url, chain_length, verification = results[url]
        row.update({"http_status": status, "final_url": final_url, "chain_length": chain_length, "verification": verification, "recommended_action": "Review destination" if verification in {"HTTP error", "network indeterminate"} else ""})
    with args.csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Checked {len(results)} unique external destinations across {len(rows)} links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
