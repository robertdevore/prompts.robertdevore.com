# Implemented changes

Audit date: 2026-08-10

- Added a deterministic generated-HTML pass that writes real `width` and `height` values for local PNG, WebP, and JPEG images.
- Added accessible names to native and client-rendered listing image links.
- Repaired skipped heading levels in three articles without rewriting their content.
- Gave `/blog/` a distinct factual meta description.
- Added server-rendered, contextual article links to the image-prompt category while retaining its interactive cards.
- Extended repository tests to lock the SEO, media, linking, and accessibility fixes.
- Added a reproducible dated audit workspace with baseline/after crawls, production receipts, Lighthouse evidence, issue register, and measurement plan.
- Pushed three meaningful commits to `main`; CI and GitHub Pages deployment completed successfully, followed by an independent production re-crawl.
