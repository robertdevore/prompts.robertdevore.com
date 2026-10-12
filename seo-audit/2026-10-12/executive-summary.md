# PASS WITH RECOMMENDATIONS — 2026-10-12

The esports logo article is added with the exact supplied v2 JSON, six profiles, three AI-generated logo variations, matching ASCII hero art and a Howl social card. Whole-site canonical coverage changes from 22 to 23; before/after datasets show no broken internal links, missing/duplicate titles or descriptions, missing image dimensions in generated HTML, or JSON-LD parse errors. P0/P1: 0 before, 0 after.

The untouched baseline passed the pinned CI site contract and local artifact revalidation. The resulting build is verified with repository checks, exact JSON/clipboard comparison, image decoding, discovery surfaces and mobile/no-JS browser checks. Deployment and live HTTP/crawler receipts are separate evidence. See raw/*verification.json and raw/*ci*.json. A separate JSON source avoids SSG indentation loss; supported Markdown images avoid escaped raw HTML.

A live Lighthouse baseline found JavaScript replacing correctly rendered category cards with dimensionless images. The fix preserves the build-rendered DOM. Internal SEO/AI scores are not assigned; lab results are in performance.csv and raw Lighthouse receipts, not a ranking metric. Existing optional www DNS and image-delivery recommendations remain; no infrastructure policy was changed.

Search visibility is limited to the dated search sample in raw/search-observations.json. Controlled rankings, traffic, field CWV and AI citations: NOT AVAILABLE — DATA ACCESS REQUIRED. No visibility improvement is claimed. Exact 7/28/60/90-day comparisons are in recommendations.md. Detailed change provenance: changes.md; file changes: raw/changed-files.txt.
