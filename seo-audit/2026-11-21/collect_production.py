#!/usr/bin/env python3
"""Capture redirect and crawler-access receipts from production."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from urllib.parse import urljoin
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
RAW = AUDIT / "raw"


def request(url: str, user_agent: str, timeout: int = 20, include_body: bool = False) -> dict[str, object]:
    result = subprocess.run(
        ["curl", "-sS", "-L", "--max-redirs", "8", "--max-time", str(timeout),
         "-A", user_agent, "-D", "-", "-w", "\n%{http_code} %{url_effective}", url],
        capture_output=True,
    )
    payload, _, stats = result.stdout.rpartition(b"\n")
    status, _, effective = stats.decode(errors="replace").partition(" ")
    chain = []
    current_url = url
    headers = {}
    while payload.startswith(b"HTTP/"):
        block, _, payload = payload.partition(b"\r\n\r\n")
        first_line, *lines = block.decode("iso-8859-1").splitlines()
        headers = {key.lower(): value.strip() for line in lines if ":" in line
                   for key, value in [line.split(":", 1)]
                   if key.lower() not in {"set-cookie", "authorization", "cookie"}}
        if "location" in headers and first_line.split()[1] in {"301", "302", "303", "307", "308"}:
            destination = urljoin(current_url, headers["location"])
            chain.append({"source": current_url, "status": int(first_line.split()[1]), "location": destination})
            current_url = destination
    record = {"requested_url": url, "final_url": effective or url, "final_status": int(status or 0),
              "content_type": headers.get("content-type", ""), "bytes": len(payload), "chain": chain, "headers": headers}
    if result.returncode:
        record["error"] = result.stderr.decode(errors="replace").strip()
    if include_body:
        record["body"] = payload.decode(errors="replace")
    return record


def replace_phase(path: Path, fields: list[str], rows: list[dict[str, object]], phase: str) -> None:
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as handle:
            existing = [row for row in csv.DictReader(handle) if row.get("phase") != phase]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
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
        "https://prompts.robertdevore.com/robots.txt",
        "https://prompts.robertdevore.com/sitemap.xml",
        "https://prompts.robertdevore.com/feed/index.xml",
        "http://prompts.robertdevore.com/images?audit=1",
        "https://prompts.robertdevore.com/blog/wwf-action-figure-blister-pack-json-prompt/",
    ]
    slug = "post-build-technical-educator"
    redirect_targets.extend([
        f"http://prompts.robertdevore.com/blog/{slug}/?audit=1",
        f"https://prompts.robertdevore.com/blog/{slug}",
        f"https://prompts.robertdevore.com/blog/{slug}/?audit=1",
        f"https://www.prompts.robertdevore.com/blog/{slug}/?audit=1",
    ])
    redirect_receipts = [request(url, "PromptsSeoAudit/1.0") for url in dict.fromkeys(redirect_targets)]
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
        "Claude-SearchBot": "Claude-SearchBot/1.0",
        "Claude-User": "Claude-User/1.0",
        "ClaudeBot": "ClaudeBot/1.0",
        "GPTBot": "Mozilla/5.0 AppleWebKit/537.36; compatible; GPTBot/1.2; +https://openai.com/gptbot",
        "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot",
    }
    robots = request("https://prompts.robertdevore.com/robots.txt", "Mozilla/5.0", include_body=True)
    (RAW / f"robots-{phase}.txt").write_text(robots["body"])
    robots_policy = "allow all" if robots["final_status"] == 200 and robots["body"].startswith("User-agent: *\nAllow: /\n") and "Disallow:" not in robots["body"] else "see captured robots.txt"
    crawler_rows = []
    crawler_receipts = []
    for name, agent in agents.items():
        for path in ("/robots.txt", "/", "/sitemap.xml", "/coding/", f"/blog/{slug}/"):
            receipt = request("https://prompts.robertdevore.com" + path, agent)
            crawler_receipts.append({"crawler": name, **receipt})
            crawler_rows.append({
                "phase": phase, "crawler": name, "crawler_class": "search/indexing" if name in {"Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot", "Claude-SearchBot"} else "user-triggered" if name in {"ChatGPT-User", "Claude-User"} else "training",
                "url": receipt["requested_url"], "status": receipt["final_status"],
                "final_url": receipt["final_url"], "content_type": receipt["content_type"],
                "robots_policy": robots_policy if path == "/robots.txt" else "see robots.txt receipt",
                "verification": "accessible" if receipt["final_status"] == 200 else "blocked/failed",
                "issues": receipt.get("error", ""),
            })
    replace_phase(AUDIT / "crawler-access.csv", ["phase", "crawler", "crawler_class", "url", "status", "final_url", "content_type", "robots_policy", "verification", "issues"], crawler_rows, phase)
    (RAW / f"production-{phase}.json").write_text(json.dumps({"redirects": redirect_receipts, "crawlers": crawler_receipts}, indent=2) + "\n", encoding="utf-8")
    print(f"Captured {len(redirect_rows)} redirects and {len(crawler_rows)} crawler requests for {phase}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
