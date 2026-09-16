# Recommendations and measurement plan

Audit date: 2026-09-16

## Immediate after deployment

- Inspect or submit `https://prompts.robertdevore.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools.
- Request recrawl of the three new prompt URLs and current category pages.
- Request recrawl/removal for the retired WWF prompt and stale `/page/2/` result while retaining the verified redirects.
- Decide whether the `www` hostname should exist. If yes, add proxied DNS and a one-hop permanent redirect to the canonical host.
- Record the deployment date as the comparison anchor; do not attribute rankings or citations without platform evidence.

## 7-day checks

- Confirm all three new URLs are discovered, canonicalized, and eligible for indexing in Google and Bing.
- Confirm the retired WWF result is dropping or has been replaced.
- Review crawl errors, redirect reports, sitemap processing, and any server/CDN errors.
- Repeat the five fixed AI-answer questions only in controlled, dated sessions and preserve citations/screenshots.

## 28-, 60-, and 90-day comparisons

- Compare Google and Bing clicks, impressions, CTR, and average position by page, query, device, and country against the deployment baseline.
- Compare indexed coverage and crawl errors for all 21 canonical URLs.
- Review analytics landing sessions and conversions for category and article pages.
- Review CDN/origin crawler logs for Googlebot, Bingbot, OAI-SearchBot, GPTBot, ChatGPT-User, and PerplexityBot.
- Compare CrUX/RUM LCP, INP, and CLS by template. If field LCP is weak, test font subsetting/preload and responsive `srcset`/sizes for hero and listing art.
- Repeat the same controlled AI-answer benchmark and record domain appearance, exact cited URL, citation order, competitors, and accuracy. Do not infer citation growth from crawler access alone.

## Editorial decisions

- Publish original Writing prompts when ready; the Writing category is intentionally valid but currently has no article cards.
- Keep each prompt on one canonical, self-contained page with a concise title, descriptive introduction, literal reusable prompt, relevant examples or safety notes, and accurate author/date/schema fields.
- For prompts that request live research or statistics, explicitly require current reputable sources and citations; do not add unsupported claims to the editorial wrapper.
- Maintain distinct category intent and avoid near-duplicate pages competing for the same query theme.
