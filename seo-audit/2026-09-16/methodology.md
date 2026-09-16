# Methodology

Audit date: 2026-09-16

## Scope

Full repository and production audit of `https://prompts.robertdevore.com/`: canonical pages, generated output, metadata, links, schema, media, crawl/index controls, redirects, crawler access, representative Lighthouse lab measurements, observable search results, and AI-search readiness. DNS/CDN changes, Search Console, analytics, request logs, and third-party AI answer sessions were read-only or unavailable.

## Evidence sequence

1. Confirmed a clean `main` worktree and read repository instructions.
2. Built the untouched 18-route site and preserved a SHA-256-addressed compressed baseline (`ba65c538480a2b88ea5b03977e18e27bcb1f59c1558556e209322115f07fe6d4`) locally under `raw/`.
3. Crawled sitemap routes in local output and production, then recorded normalized baseline CSV/JSON data.
4. Collected production redirect, robots, crawler-user-agent, search-result, and representative Lighthouse evidence.
5. Implemented the requested content/layout/navigation work plus the crawlability fix justified by the audit.
6. Rebuilt, reran the same inventory, validated the repository contract, deployed, and repeated production checks.

## Current primary guidance consulted

See `research-sources.md`. Only current first-party search/crawler guidance and the Schema.org vocabulary support material technical claims. `llms.txt` and WebMCP are labeled experimental.

## Build and crawl commands

```text
SITE_URL=https://prompts.robertdevore.com bash scripts/build.sh
python3 seo-audit/2026-09-16/collect_audit.py --phase baseline|after
python3 seo-audit/2026-09-16/collect_production.py --phase baseline|after
bash scripts/test-site.sh
npx lighthouse <representative-local-url> --output=json --only-categories=performance,accessibility,best-practices,seo
```

## Interpretation limits

- Internal SEO and AI-readiness scores are transparent audit heuristics, not Google, Bing, OpenAI, or Perplexity scores.
- Lighthouse runs are controlled local lab observations and are not Core Web Vitals field data.
- Search observations are dated results from the available web-search connector; locale, personalization, and exact universal position are not controllable.
- A successful crawler-user-agent request proves technical access at test time, not indexing, ranking, training use, or citation.
- External 401/403/405/429 responses are classified as blocked/indeterminate, not automatically broken.
- Search and AI outcomes require elapsed time plus platform/property data.
