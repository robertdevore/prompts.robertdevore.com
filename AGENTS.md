# Agent Guide

This repository is the canonical source for prompts.robertdevore.com.

## Canonical surfaces

- `content/`: page and article content.
- `templates/`: semantic Kujo SSG templates.
- `assets/css/style.css`: site-specific styles composed from SiteKit tokens.
- `assets/sitekit/`: vendored, unmodified SiteKit distribution.
- `assets/js/docs.js`: mobile navigation, local search, and code-copy behavior.
- `build.kujo`: vendored Kujo SSG entrypoint.
- `static/`: root-level passthrough files copied by the build script.

## Rules

- Preserve the public route structure recorded in `scripts/test-site.sh`.
- Do not hand-edit or commit `output/` or `assets/js/docs-search-index.json`.
- Keep SiteKit's `fonts/` directory beside `sitekit.css`.
- Use SiteKit tokens in site CSS instead of raw color, spacing, typography, border, or motion values.
- Preserve the black background, white text, yellow accents, Inter body typeface, and Departure Mono titles and controls.
- Use semantic HTML, real controls, ordered headings, visible focus, useful alt text, and reduced-motion-safe behavior.

## Validation

```bash
bash scripts/test-site.sh
```
