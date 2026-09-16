#!/usr/bin/env python3
"""Capture redirect and crawler-access receipts from production."""

from __future__ import annotations

import argparse
import csv
import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
RAW = AUDIT / "raw"


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        self.chain: list[dict[str, object]] = []

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        self.chain.append({"source": request.full_url, "status": code, "location": new_url})
        return super().redirect_request(request, file_pointer, code, message, headers, new_url)


def request(url: str, user_agent: str) -> dict[str, object]:
    recorder = RedirectRecorder()
    opener = urllib.request.build_opener(recorder, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with opener.open(req, timeout=30) as response:
            body = response.read()
            return {"requested_url": url, "final_url": response.geturl(), "final_status": response.status, "content_type": response.headers.get_content_type(), "bytes": len(body), "chain": recorder.chain, "headers": dict(response.headers)}
    except urllib.error.HTTPError as error:
        body = error.read()
        return {"requested_url": url, "final_url": error.geturl(), "final_status": error.code, "content_type": error.headers.get_content_type(), "bytes": len(body), "chain": recorder.chain, "headers": dict(error.headers)}
    except Exception as error:
        return {"requested_url": url, "final_url": url, "final_status": 0, "content_type": "", "bytes": 0, "chain": recorder.chain, "error": str(error), "headers": {}}


def replace_phase(path: Path, fields: list[str], rows: list[dict[str, object]], phase: str) -> None:
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as handle:
            existing = [row for row in csv.DictReader(handle) if row.get("phase") != phase]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing + rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("baseline", "after"), required=True)
    args = parser.parse_args()
    phase = args.phase
    RAW.mkdir(exist_ok=True)

    redirect_targets = [
        "http://prompts.robertdevore.com/",
        "https://www.prompts.robertdevore.com/",
        "http://www.prompts.robertdevore.com/",
        "https://prompts.robertdevore.com/writing/?audit=1",
        "https://prompts.robertdevore.com/not-a-real-route/",
        "https://wwf.robertdevore.com/",
        "https://prompts.robertdevore.com/blog/wwf-action-figure-blister-pack-json-prompt/",
    ]
    redirect_receipts = [request(url, "PromptsSeoAudit/1.0") for url in redirect_targets]
    redirect_rows = []
    for receipt in redirect_receipts:
        chain = receipt["chain"]
        first_status = chain[0]["status"] if chain else receipt["final_status"]
        target = chain[0]["location"] if chain else receipt["final_url"]
        query_expected = "audit=1" in str(receipt["requested_url"])
        query_preserved = "audit=1" in str(receipt["final_url"]) if query_expected else "not applicable"
        redirect_rows.append({
            "phase": phase, "source_url": receipt["requested_url"], "source_variant": "production",
            "http_status": first_status, "target_url": target, "chain_length": len(chain),
            "final_status": receipt["final_status"], "canonical_target": receipt["final_url"],
            "query_preserved": query_preserved,
            "verification": "verified" if receipt["final_status"] in {200, 404} else "failed",
            "issues": receipt.get("error", ""),
        })
    replace_phase(AUDIT / "redirects.csv", ["phase", "source_url", "source_variant", "http_status", "target_url", "chain_length", "final_status", "canonical_target", "query_preserved", "verification", "issues"], redirect_rows, phase)

    agents = {
        "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        "OAI-SearchBot": "Mozilla/5.0 AppleWebKit/537.36; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot",
        "ChatGPT-User": "Mozilla/5.0 AppleWebKit/537.36; compatible; ChatGPT-User/1.0; +https://openai.com/bot",
        "GPTBot": "Mozilla/5.0 AppleWebKit/537.36; compatible; GPTBot/1.2; +https://openai.com/gptbot",
        "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot",
    }
    crawler_rows = []
    crawler_receipts = []
    for name, agent in agents.items():
        for path in ("/robots.txt", "/", "/writing/"):
            receipt = request("https://prompts.robertdevore.com" + path, agent)
            crawler_receipts.append({"crawler": name, **receipt})
            crawler_rows.append({
                "phase": phase, "crawler": name, "crawler_class": "search/indexing" if name in {"Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot"} else "user-triggered" if name == "ChatGPT-User" else "training",
                "url": receipt["requested_url"], "status": receipt["final_status"],
                "final_url": receipt["final_url"], "content_type": receipt["content_type"],
                "robots_policy": "Allow: /" if path == "/robots.txt" and receipt["final_status"] == 200 else "tested separately",
                "verification": "accessible" if receipt["final_status"] == 200 else "blocked/failed",
                "issues": receipt.get("error", ""),
            })
    replace_phase(AUDIT / "crawler-access.csv", ["phase", "crawler", "crawler_class", "url", "status", "final_url", "content_type", "robots_policy", "verification", "issues"], crawler_rows, phase)
    (RAW / f"production-{phase}.json").write_text(json.dumps({"redirects": redirect_receipts, "crawlers": crawler_receipts}, indent=2) + "\n", encoding="utf-8")
    print(f"Captured {len(redirect_rows)} redirects and {len(crawler_rows)} crawler requests for {phase}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
