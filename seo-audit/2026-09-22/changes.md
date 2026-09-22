# Changes and verification

Content commit: 6ca0e57e8645b3d5c8d4631e9d14b52fb10dc2f2 (main).

- Added content/posts/kujo-repository-hardening-performance-efficiency.md with coding taxonomy, publication date, author, unique metadata, usage context and related links.
- Stored the complete 2,729-word, 19-phase user-supplied text verbatim in prompt-sources/kujo-repository-hardening-performance-efficiency.md. Existing raw-prompt renderer exposes a literal copyable block; no new renderer was needed.
- Generated the hero with the built-in image tool and the site's existing ASCII-grunge JSON guide. Final source: assets/images/ascii-grunge/kujo-repository-hardening.webp (1672×941, 216,608 bytes). Complete generation prompt: raw/image-generation-prompt.txt. Generated source kept in the tool-managed image directory. No image API fallback was used.
- Rerendered all 22 Howl cards using the existing script; only the new SVG/PNG, manifest and route-map additions changed. New committed PNG: assets/social/kujo-repository-hardening-performance-efficiency-social.png (1200×630). Kujo SSG generates a fingerprinted WebP social derivative, which is the actual og:image; verified its live hash against the CI artifact.
- Extended the existing site contract for the new route, category link and final-phase search text.

No existing prompt was rewritten. No runtime, template, public API, route, configuration, environment-variable, crawler-policy or dependency contract changed. No sibling repository changes.

## Verification receipts

- Fresh untouched pinned build: GitHub Actions 35762731309, c080e07, PASS (build and deploy).
- Content build/deploy: GitHub Actions 35763204064, 6ca0e57, PASS; separate CI 35763204092, PASS.
- Actual workflow command: bash scripts/test-site.sh with checksum-verified Linux Kujo 1.0.1.
- Download both github-pages artifacts; SKIP_BUILD=1 bash scripts/test-site.sh: PASS before and after. Local macOS full build was interrupted under host contention and is not claimed as passing.
- python3 seo-audit/2026-09-22/collect_audit.py --phase baseline and --phase after: PASS, complete 21/22-route inventories.
- python3 seo-audit/2026-09-22/collect_production.py --phase baseline and --phase after: canonical site and relevant crawlers accessible; existing www DNS absence retained.
- KUJO=/Users/robertdevore/.local/bin/kujo HOWL_BIN=/Users/robertdevore/2026/Kujolang/kujo-repos/howl/bin/howl python3 scripts/render_howl_social.py: PASS, 22 cards.
- python3 seo-audit/2026-09-22/verify_new_post.py: PASS (verbatim output, metadata, images and all discovery surfaces).
- python3 seo-audit/2026-09-22/collect_weights.py --phase baseline and --phase after: PASS; no timing inference.
- Playwright desktop 1440×1000 and mobile 390×844: PASS; rendered text equals source, real clipboard content equals source, no mobile page overflow, coding link visible. raw/browser-verification.json and screenshots preserve evidence.
- Live article prompt equals source; generated hero/social match CI artifact hashes: raw/live-post-verification.json. Default Python user agent received 403; the declared audit user agent and all six tested crawler user agents received 200. No WAF policy change was made.
- git diff --check: PASS.

Lighthouse 13.5.0 did not produce a valid baseline: errors are retained, not reported as passing scores. Remote-build and live receipts are authoritative for this release.
