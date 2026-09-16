# Implemented changes

Audit date: 2026-09-16

## `4a72e8a` — fix: layer hero artwork and restore desktop navigation

- Layered category hero artwork behind the heading and description with a contrast gradient.
- Added category links to the desktop navigation.
- Kept the hamburger navigation for tablet/mobile breakpoints.

## `91a42a5` — feat: add business marketing and security prompts

- Added the company/product diagnostic, keyword/competitor analysis, and Dependabot security maintenance prompt articles.
- Added original featured art and validated Howl social cards for all three articles.
- Preserved the attached security prompt as literal source text in the generated article and client search index.
- Added build-time category listing rendering so category-to-article links exist in static HTML.
- Extended route, SEO, image, internal-link, discovery, and literal-prompt tests.

Both commits were pushed to `main`; CI and deployment completed successfully before this audit report was finalized.
