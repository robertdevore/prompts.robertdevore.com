#!/usr/bin/env python3
"""Normalize Lighthouse JSON receipts into the audit performance schema."""

from __future__ import annotations

import csv
import json
from pathlib import Path


AUDIT = Path(__file__).resolve().parents[1]
FIELDS = "phase,url,template,run_date,environment,lighthouse_version,html_bytes,css_bytes,js_bytes,image_bytes,font_bytes,requests,lcp_ms,inp_ms,cls,ttfb_ms,source,notes".split(",")
TEMPLATES = {"home": "home listing", "post": "BlogPosting", "category": "category CollectionPage"}


def value(audits: dict, key: str) -> object:
    return audits.get(key, {}).get("numericValue", "NOT AVAILABLE — DATA ACCESS REQUIRED")


def main() -> int:
    rows: list[dict[str, object]] = []
    runs = (
        ("baseline", "baseline", "production baseline"),
        ("after", "after", "local generated output"),
        ("after", "after-production", "production post-deploy"),
    )
    for phase, filename_phase, environment in runs:
        for name, template in TEMPLATES.items():
            path = AUDIT / "raw" / f"{filename_phase}-lighthouse-{name}.json"
            report = json.loads(path.read_text(encoding="utf-8"))
            audits = report["audits"]
            requests = audits.get("network-requests", {}).get("details", {}).get("items", [])
            totals = {"Document": 0, "Stylesheet": 0, "Script": 0, "Image": 0, "Font": 0}
            for item in requests:
                kind = item.get("resourceType")
                if kind in totals:
                    totals[kind] += int(item.get("transferSize", 0) or 0)
            rows.append({
                "phase": phase,
                "url": report["finalDisplayedUrl"],
                "template": template,
                "run_date": "2026-08-10",
                "environment": environment,
                "lighthouse_version": report["lighthouseVersion"],
                "html_bytes": totals["Document"],
                "css_bytes": totals["Stylesheet"],
                "js_bytes": totals["Script"],
                "image_bytes": totals["Image"],
                "font_bytes": totals["Font"],
                "requests": len(requests),
                "lcp_ms": round(float(value(audits, "largest-contentful-paint")), 2),
                "inp_ms": value(audits, "interaction-to-next-paint"),
                "cls": round(float(value(audits, "cumulative-layout-shift")), 4),
                "ttfb_ms": round(float(value(audits, "server-response-time")), 2),
                "source": f"raw/{path.name}",
                "notes": "Single Lighthouse lab run; compare directionally. INP requires field or interaction data when unavailable.",
            })
    with (AUDIT / "performance.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} Lighthouse rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
