# Executive summary

Audit date: 2026-09-16

## Overall status

PASS WITH RECOMMENDATIONS

Internal technical SEO health improved from 90/100 to 93/100. Internal AI-search readiness improved from 66/100 to 71/100. These are transparent audit heuristics, not platform scores: technical SEO weights crawl/index controls, metadata, links, schema, media, production behavior, and performance; AI readiness weights crawl access, answer-ready content, entity/source clarity, machine-readable discovery, and measured citation evidence. The measured AI-citation component received no credit because controlled platform data was unavailable.

The audit covered all 21 final canonical pages. Three pages were added, five category listings received server-rendered cards, and the shared navigation changed across the site. P0/P1 issues were 0/0 at baseline and 0/0 after remediation; two P2 repository issues were resolved and four P2 follow-ups remain open.

## Where the site was

The untouched build exposed 18 canonical, indexable pages. Titles, descriptions, headings, canonical tags, internal links, schema, image alternatives, image dimensions, sitemap membership, robots controls, and real 404 behavior were technically sound. Existing branded and exact-match prompt searches returned relevant site pages in the available dated search observations.

## What was wrong

Five category grids relied on client JavaScript to expose post links, reducing resilience for non-rendering crawlers and no-JavaScript users. The `www` host variants did not resolve. Search observations still showed stale results for the retired WWF article and an older page-2 composition. Representative Lighthouse lab runs showed slow LCP, but no CrUX or RUM field data was available. Search Console, Bing, analytics, logs, backlink, and controlled AI-citation data were also unavailable.

## What changed

Category cards are now emitted in generated HTML while retaining client enhancement. Desktop navigation exposes all five categories, category hero art is layered behind its text, and three new primary-source prompt articles were added with unique metadata, literal prompt text, sitemap/feed/search-index coverage, and original image/social assets. Initial overlong titles for the new articles were shortened before release.

## Where the site is now

The after-build contains 21/21 canonical and indexable pages. It has zero missing or duplicate titles/descriptions, zero H1 issues, zero broken internal or confirmed-broken external links, zero orphan pages, zero missing image alt text/dimensions, and zero JSON-LD parse errors. Production crawler probes returned 200 for Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, GPTBot, and PerplexityBot. Canonical HTTP, the retired WWF subdomain, and the retired WWF article each resolve through a verified one-hop permanent redirect.

## Available measurements

Repository/build evidence, immutable baseline inventory, production HTTP/DNS/redirect probes, crawler access tests, limited dated search-result observations, and local Lighthouse lab data for three representative templates.

## Unavailable measurements

Google Search Console, Bing Webmaster Tools, analytics/conversions, CDN/origin logs, CrUX/RUM, backlinks, and controlled ChatGPT/Perplexity/Claude citations. These are explicitly recorded as `NOT AVAILABLE — DATA ACCESS REQUIRED`; no ranking, traffic, citation, or Core Web Vitals improvement is claimed.

## Next actions

Submit or inspect the current sitemap in Google Search Console and Bing Webmaster Tools, request recrawl/removal for the retired URLs, decide whether the absent `www` host is intentional, and establish 7/28/60/90-day platform baselines. Obtain field performance data before prioritizing font subsetting/preload or responsive-image work.
