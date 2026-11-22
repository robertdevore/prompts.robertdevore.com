# Universal Release Explainer publication audit

**PASS WITH RECOMMENDATIONS · November 22, 2026**

The audit covers the new English-language [Universal Release Explainer Prompt](https://prompts.robertdevore.com/blog/universal-release-explainer/) and the library's technical discovery surfaces. The page targets readers looking for an AI prompt that turns software releases into sourced articles and release notes. The Post-Build Technical Educator page addresses a separate tutorial use case and is linked from the new article.

## Before and after

| Check | Baseline | Published |
| --- | ---: | ---: |
| Canonical URLs responding with HTTP 200 | 27 | 28 |
| Technically indexable URLs | 27 | 28 |
| Link checks passed by the site contract | 1,069 | 1,115 |
| Feed items / llms.txt links | 14 / 24 | 15 / 25 |
| Missing or duplicate titles or descriptions | 0 | 0 |
| H1 issues, orphan URLs, broken internal or confirmed broken external links | 0 | 0 |
| Images missing alt text or dimensions, JSON-LD parse errors | 0 | 0 |
| Crawler user-agent probes returning 200 | 36/45 | 45/45 |
| P0/P1 issues in the publication scope | 0 | 0 |
| New article HTTP status | 404 | 200 |

The article has a unique search title and description, an absolute self-canonical URL, Open Graph and X imagery, and BlogPosting markup with the visible author and publication date. Home, the blog archive, and Writing link to it in initial HTML. It appears in the sitemap, RSS, local search, WebMCP index, and experimental llms.txt index. Browser tests verified the exact prompt text in the clipboard, local search, image decoding, and the 390 px layout. The 1,672 × 941 WebP featured image is 71,188 bytes. Howl validated 28 cards and generated the article's 1,200 × 630 social card from the featured art.

## Production and performance

The canonical host serves the post over HTTPS. The HTTP URL permanently redirects and preserves the query string. The slashless path serves a static refresh stub with a canonical that resolves to the slash URL. The nested www alias showed the same DNS failure in both phases and remains outside the canonical host configuration. Crawler requests simulated user-agent strings from one location and verified the HTTP response only.

The new article scored 95 performance, 100 accessibility, and 100 SEO in one Lighthouse 13.0.1 mobile lab navigation. LCP was 2.07 s and CLS was 0. The Writing index LCP was 5.53 s before publication and 6.83 s afterward. Both samples identified the same lazy-loaded Writing header image and missing high priority. This pre-existing category-template opportunity warrants a paired test of eager loading and high fetch priority. Run repeated samples before attributing timing differences to a change.

## Evidence and reproduction

The build chain is prompt source and Markdown front matter → Kujo SSG and Python postprocessors → GitHub Pages → Cloudflare custom origin. The before crawl used the checksum-sealed Pages artifact at `8f927e7`, whose site inputs match the pre-edit checkout `147bdc7`. The after crawl used the checksum-sealed Pages artifact at `89c71e0`. The workflows ran pinned Kujo 1.0.1 on Linux. Both archived artifacts also passed `SKIP_BUILD=1 bash scripts/test-site.sh` with their corresponding source and contract. Slower local macOS build attempts were stopped after the pinned Linux artifacts were available. [Baseline Pages run](https://github.com/robertdevore/prompts.robertdevore.com/actions/runs/44943739583) · [Pre-edit Pages run](https://github.com/robertdevore/prompts.robertdevore.com/actions/runs/44944309587) · [Publication Pages run](https://github.com/robertdevore/prompts.robertdevore.com/actions/runs/45080458025) · [Publication CI](https://github.com/robertdevore/prompts.robertdevore.com/actions/runs/45080458081)

[Before inventory](baseline.csv) · [After inventory](after.csv) · [Crawler probes](crawler-access.csv) · [Redirect probes](redirects.csv) · [Static asset weights](performance.csv) · [Lighthouse measurements](raw/lighthouse-summary.json) · [Browser receipt](raw/browser-after.json) · [Production article receipt](raw/post-live.json). The full lab reports and response receipts are in the local audit workspace. The adjacent November 21 audit contains the collectors used for sitemap reconciliation, structural checks, link graph, edge probes, and weight comparisons. Run them from a fresh audit folder against the extracted Pages artifacts with `SEO_AUDIT_OUTPUT` set to the artifact directory.

## Search and AI visibility

Google recommends descriptive titles, useful page-specific descriptions, consistent canonical signals, and structured data aligned with visible content. Google AI features depend on standard search eligibility. OpenAI documents separate search, user-triggered, and training crawler purposes. Bing exposes page-level AI citation activity through Webmaster Tools. Guidance consulted November 22, 2026. [Google title links](https://developers.google.com/search/docs/appearance/title-link) · [Google snippets](https://developers.google.com/search/docs/appearance/snippet) · [Google canonicals](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) · [Schema.org BlogPosting](https://schema.org/BlogPosting) · [Google AI features](https://developers.google.com/search/docs/appearance/ai-features) · [OpenAI crawlers](https://developers.openai.com/api/docs/bots) · [Bing AI Performance](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/)

Index coverage, impressions, clicks, rankings, field Core Web Vitals, backlinks, referral traffic, and provider citation data are NOT AVAILABLE — DATA ACCESS REQUIRED. At 7 days, check URL inspection and sitemap discovery. At 28 days, collect search performance for the exact page and the themes “software release explainer prompt” and “AI prompt for release notes.” At 60 and 90 days, repeat the same search measurements and test the question “What AI prompt can turn a software release into a fact-checked explainer?” with a fixed locale and recorded provider, date, and cited URLs.
