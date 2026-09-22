# Methodology

Scope: add the supplied Kujo repository hardening prompt to coding, matching artwork and social card; audit whole-site discovery before and after. The supplied mega prompt is publication content, not an instruction to audit sibling software repositories.

Origin: https://prompts.robertdevore.com; English; audience: people reusing AI prompts. Desired action: discover and copy a prompt.

Starting branch: main. Starting SHA: c080e07ffb92dcce2a959af8b6c64b85e3e7cd2b. Initially clean worktree.

Delivery: content + templates → vendored Kujo SSG → build postprocessors → output → GitHub Pages main-branch deployment → custom-domain edge. Generated output is ignored.

Use checksum-verified macOS x64 Kujo 1.0.1 (same version as CI), not the unrelated installed 1.4.0 compiler. Preserve baseline output tarball and SHA before editing content. Reuse prior audit collectors in this new date directory, correcting depth to actual BFS link depth and separating local indexability from live deployment status. Existing older audit files remain unchanged.

Commands: KUJO_BIN="$PWD/tmp/kujo-1.0.1/kujo" bash scripts/test-site.sh; python3 seo-audit/2026-09-22/collect_audit.py --phase baseline|after; python3 seo-audit/2026-09-22/collect_production.py --phase baseline|after. Lighthouse uses the same production coding URL/settings before and after; machine load and network variation limit comparison.

Inventory covers sitemap routes; repository discovery/link validators independently enumerate generated HTML and verify sitemap/feed/llms coverage, assets, canonicals and schema. Source inspection covers author/contact provenance and page intent. No editorial rewrites of existing prompts or crawler-policy changes.

Scores are omitted: no new platform evidence justifies a numeric visibility score. Missing platform data is stated explicitly; no indexing, traffic or citation gain is inferred.

A separate interpreter-mode probe in ignored output_interpreter was stopped after it showed no practical speed advantage. It did not replace the default-VM baseline or alter source; only the complete default-VM validation is used as build evidence.

The local macOS baseline build made progress but was stopped because of severe host contention. The authoritative untouched baseline is a fresh GitHub Actions deployment build at starting SHA c080e07ffb92dcce2a959af8b6c64b85e3e7cd2b, run 35762731309, with pinned Linux Kujo 1.0.1 and the complete site contract. Its artifact is downloaded and independently revalidated locally. No incomplete local build is claimed as passing.

Browser reproduction: serve output with `python3 -m http.server 4179 --bind 127.0.0.1 --directory output`, then run `PLAYWRIGHT_MODULE=/path/to/playwright node seo-audit/2026-09-22/verify_browser.cjs` from the repository root. The original temporary script and this saved copy differ only in the configurable Playwright module path. Screenshots inspected visually after successful clipboard/mobile checks.

Full-site content review: posts are reusable primary prompt artifacts; category pages serve navigation intent; About identifies Robert DeVore and Contact exposes a direct contact route. Existing image-prompt articles remain distinct from the new coding audit. New article context accurately summarizes the supplied prompt without adding results or claims of proven security/performance gains.

Baseline raw output tarball is intentionally gitignored by repository convention, preserved locally with a committed SHA-256 receipt; all normalized before/after data and CI receipts are committed. HTTP cookie/auth headers are excluded from durable receipts.
