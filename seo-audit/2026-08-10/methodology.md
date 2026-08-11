# Methodology

Audit date: 2026-08-10

## Scope

The canonical repository, generated output, and production origin `https://prompts.robertdevore.com` were audited. Repository-safe remediation and push/deployment verification were authorized; DNS, search consoles, analytics, CDN settings, and crawler-training policy were not changed.

## Evidence sequence

1. Inspected repository instructions and confirmed a clean starting worktree.
2. Built the untouched site with the pinned local Kujo release binary.
3. Copied all 78 generated baseline files to `raw/baseline-output/` before editing source.
4. Crawled all 19 sitemap canonicals and their crawlable HTML links; separately probed production.
5. Researched current first-party search, schema, and AI-crawler guidance.
6. Implemented evidence-backed source/build fixes, rebuilt, reran the same crawl, and diffed normalized datasets.
7. Ran repository validators and representative Lighthouse checks.

## Current primary guidance consulted

See `research-sources.md`. Requirements, recommendations, best practices, and experiments are labeled separately.

## Build and crawl commands

```bash
KUJO_BIN=/Users/robertdevore/2026/Kujolang/kujo-repos/kujo/target/release/kujo SITE_URL=https://prompts.robertdevore.com bash scripts/build.sh
KUJO_BIN=/usr/bin/true bash scripts/test-site.sh
python3 seo-audit/2026-08-10/scripts/audit_snapshot.py --root output --audit seo-audit/2026-08-10 --phase after --production
python3 seo-audit/2026-08-10/scripts/production_probe.py --audit seo-audit/2026-08-10 --phase baseline
npx --yes lighthouse@12.8.2 <url> --output=json --chrome-path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --chrome-flags='--headless --no-sandbox' --quiet
```

## Interpretation limits

- Internal scores are transparent audit heuristics, not Google, Bing, or AI-platform scores.
- Search-result observations are dated samples and do not establish stable rank.
- AI citations, traffic outcomes, index coverage, field CWV, backlinks, and conversions were not inferred.
- Local Lighthouse runs verify rendered output but are not directly comparable with production network conditions; production post-deployment runs are required for outcome comparison.
