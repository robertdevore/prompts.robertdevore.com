# Methodology — 2026-11-12

Scope: publish the supplied strategic review prompt verbatim with matching artwork; verify Howl and the site's SEO/AI discovery contracts. English prompt library; conversion is discovering and copying a useful prompt. Canonical origin: https://prompts.robertdevore.com. Starting source: clean main at 1cbd2732e050044c44fc4c26fe81c0342acbedf1.

Delivery: authored Markdown and literal prompt sources → vendored Kujo SSG and Python postprocessors → generated output → GitHub Pages on main → canonical custom domain. CI pins checksum-verified Kujo 1.0.1. Howl uses the installed runtime, independently of SSG. No DNS, CDN, analytics, or crawler-training policy changes.

The pinned local build remained CPU-bound and was stopped once the identical unchanged commit passed Actions run 43344358494. Its downloaded artifact passed the complete site contract locally. Before content edits, baseline-output.tar.gz was sealed and hashed; the hash is committed, the archive stays ignored locally. Baseline receipts/tables and older audits remain immutable.

Collectors preserve prior field schemas and compare sitemap inventory with generated routes using the repository discovery/link validators. Local status means artifact route existence; live response status is separate. BFS measures depth. Content review groups posts as reusable primary prompt artifacts, categories as discovery pages, and About/Contact as publisher identity. The new review complements the focused company diagnostic and keyword analysis rather than replacing them. Fictional role names are explained visibly and are not authorship claims.

Schema parsing and content alignment do not prove rich-result eligibility. Public crawler user-agent probes do not prove verified-IP access; robots and HTTP access are separate observations. No account data or complete request logs are available. Uncontrolled search rankings, competitor comparisons and AI citations are not invented.

Reproduce from repository root: python3 seo-audit/2026-11-12/collect_audit.py --phase after; collect_production.py --phase after; collect_weights.py --phase after; verify_post.py. Never rerun baseline into this directory. Serve output on port 4179 and run verify_browser.cjs with PLAYWRIGHT_MODULE resolving installed Playwright. Browser checks verify clipboard fidelity, image decoding, mobile overflow, and no-JavaScript category discovery.

Lighthouse 13.0.1, mobile defaults, headless Chrome, live /marketing/, performance/accessibility/SEO. One sample per phase is directional; no field or statistical claim. Static weights are uncompressed local references, excluding external fonts and dynamic fetches. Internal SEO/AI readiness scores omitted because missing platform measurements make aggregate scores misleading.
