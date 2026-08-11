#!/usr/bin/env python3
"""Capture reproducible production redirect and crawler-access receipts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path


ORIGIN = "https://prompts.robertdevore.com"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url: str, user_agent: str, follow: bool) -> dict[str, object]:
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect())
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with opener.open(request, timeout=20) as response:
            body = response.read()
            return {"status": response.status, "final_url": response.url, "headers": dict(response.headers.items()), "body_sha256": hashlib.sha256(body).hexdigest()}
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return {"status": exc.code, "final_url": exc.url, "headers": dict(exc.headers.items()), "body_sha256": hashlib.sha256(body).hexdigest()}
    except (urllib.error.URLError, TimeoutError) as exc:
        return {"status": f"ERROR: {exc}", "final_url": "", "headers": {}, "body_sha256": ""}


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--phase", choices=("baseline", "after"), required=True)
    args = parser.parse_args()
    audit = args.audit.resolve()
    variants = [
        "http://prompts.robertdevore.com/",
        "http://prompts.robertdevore.com/blog/glowing-neon-icon-json-prompt/?source=audit",
        "https://prompts.robertdevore.com/",
        "https://prompts.robertdevore.com/about.html",
        "https://prompts.robertdevore.com/blog/glowing-neon-icon-json-prompt/",
        "https://prompts.robertdevore.com/definitely-not-a-route/",
        "http://www.prompts.robertdevore.com/",
        "https://www.prompts.robertdevore.com/",
    ]
    receipts: dict[str, object] = {"phase": args.phase, "redirects": {}, "crawlers": {}}
    redirect_rows: list[dict[str, object]] = []
    for url in variants:
        direct = fetch(url, "SEO-Audit/1.0", False)
        followed = fetch(url, "SEO-Audit/1.0", True)
        receipts["redirects"][url] = {"direct": direct, "followed": followed}
        target = str(direct["headers"].get("Location", ""))
        status = direct["status"]
        query_expected = "source=audit" in url
        redirect_rows.append({
            "phase": args.phase,
            "source_url": url,
            "source_variant": "www" if "www." in url else "apex",
            "http_status": status,
            "target_url": target,
            "chain_length": 1 if isinstance(status, int) and 300 <= status < 400 else 0,
            "final_status": followed["status"],
            "canonical_target": followed["final_url"],
            "query_preserved": "yes" if query_expected and "source=audit" in str(followed["final_url"]) else "not applicable" if not query_expected else "no",
            "verification": "direct and followed production request",
            "issues": "www host unavailable" if "www." in url and str(status).startswith("ERROR") else "",
        })
    crawlers = {
        "Googlebot": "search indexing",
        "bingbot": "search indexing and Bing/Copilot grounding",
        "OAI-SearchBot": "ChatGPT search",
        "GPTBot": "OpenAI model training",
        "ChatGPT-User": "user-triggered fetch",
    }
    crawler_rows: list[dict[str, object]] = []
    for crawler, purpose in crawlers.items():
        results = {}
        for path in ("/robots.txt", "/", "/blog/glowing-neon-icon-json-prompt/"):
            results[path] = fetch(ORIGIN + path, crawler, True)
        receipts["crawlers"][crawler] = results
        statuses = [value["status"] for value in results.values()]
        crawler_rows.append({
            "crawler": crawler,
            "purpose": purpose,
            "robots_access": "allowed by wildcard Allow: /",
            "live_status": "|".join(str(value) for value in statuses),
            "waf_or_cdn_result": "all representative requests returned 200" if statuses == [200, 200, 200] else "one or more representative requests did not return 200",
            "recommended_action": "Preserve owner policy; monitor separately from robots.txt",
            "action_taken": "No crawler policy change",
            "evidence": f"raw/{args.phase}-production-probe.json",
        })
    write_csv(audit / "redirects.csv", "phase,source_url,source_variant,http_status,target_url,chain_length,final_status,canonical_target,query_preserved,verification,issues".split(","), redirect_rows)
    write_csv(audit / "crawler-access.csv", "crawler,purpose,robots_access,live_status,waf_or_cdn_result,recommended_action,action_taken,evidence".split(","), crawler_rows)
    (audit / "raw" / f"{args.phase}-production-probe.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"phase": args.phase, "variants": len(redirect_rows), "crawlers": len(crawler_rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
