#!/usr/bin/env python3
"""Rebuild supplementary audit tables and narrative from preserved receipts."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
NA='NOT AVAILABLE — DATA ACCESS REQUIRED'
def rows(name):
 with (P/name).open() as f:return list(csv.DictReader(f))
def write(name,data,fields=None):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(data[0]));w.writeheader();w.writerows(data)
b=json.loads((P/'baseline-summary.json').read_text());a=json.loads((P/'after-summary.json').read_text())
pages=rows('after.csv')
write('keyword-map.csv',[dict(url=r['url'],topic=r['h1'],intent='Reuse a specific prompt' if r['page_type']=='post' else 'Browse prompts or identify the publisher',primary_theme=r['title'],secondary_theme=r['meta_description'],related_entities='Robert DeVore; AI prompts',competing_url='',gap='No substantive overlap requiring consolidation identified',action='Preserve original supplied prompt and its distinct examples' if 'esports' in r['url'] else 'No editorial change') for r in pages])
write('search-rankings.csv',[dict(query=q,search_engine='web search tool sample',date='2026-10-12',country='uncontrolled',device='uncontrolled',page_found='No target esports URL in sampled results before publication',observed_position_or_range=NA,competing_results='Promptkoi; Morphic; PromptCreek; Logofai',rich_features=NA,ai_result_presence=NA,evidence='raw/search-observations.json',limitations='Merged sampled results; not a rank tracker or a complete SERP') for q in ['esports logo JSON prompt team name colors','site:prompts.robertdevore.com esports logo']])
questions=['How do I generate an esports logo with an exact team name?','Where can I copy a JSON prompt for a gaming team logo?','How do I keep lettering consistent in an AI logo?','How do modern esports and pixel-retro logo styles differ?','What is the esports logo prompt on prompts.robertdevore.com?']
write('ai-search-benchmark.csv',[dict(question=q,platform='ChatGPT Search / Bing Copilot / Perplexity (benchmark plan)',date='2026-10-12',domain_appeared=NA,domain_cited=NA,cited_url=NA,citation_context=NA,citation_order=NA,competing_domains=NA,accurate_representation=NA,content_gap='Measure exact-name and typography guidance citations',evidence='No controlled answer session available',limitations='Planned questions only; no synthetic answers presented as measurements') for q in questions])
issues=[dict(id='SEO-01',phase='baseline → after',category='media / client rendering',severity='P2',affected_urls='All category routes',affected_count=5,evidence='raw/lighthouse-baseline.json unsized-images; assets/js/docs.js; raw/browser-verification.json',expected_benefit='Preserve intrinsic dimensions and avoid redundant DOM replacement',confidence='high',difficulty='low',recommended_action='Retain pre-rendered category cards when aria-busy=false',owner='repository',status='fixed'),dict(id='SEO-02',phase='baseline and after',category='optional hostname',severity='P2',affected_urls='https://www.prompts.robertdevore.com/; http://www.prompts.robertdevore.com/',affected_count=2,evidence='raw/production-baseline.json; raw/production-after.json',expected_benefit='Optional alias access',confidence='high',difficulty='owner decision',recommended_action='Confirm whether the optional www subdomain should exist before DNS/CDN changes',owner='site owner',status='pre-existing; blocked on hostname policy; canonical host works'),dict(id='SEO-03',phase='baseline and after',category='performance',severity='P2',affected_urls='https://prompts.robertdevore.com/images/',affected_count=1,evidence='raw/lighthouse-baseline.json; raw/lighthouse-after.json; performance.csv',expected_benefit='Reduce image transfer and mobile loading time',confidence='medium: lab only',difficulty='medium',recommended_action='Evaluate responsive category thumbnails and font delivery with repeatable lab and field measurements; preserve full-resolution article examples',owner='site owner / repository',status='recommendation; separate image-delivery change and visual review required; no field impact claimed')]
write('issues.csv',issues)
# Append actual lab results, preserving static asset rows.
perf=[r for r in rows('performance.csv') if r.get('source')!='Lighthouse lab']
for phase in ['baseline','after']:
 r=json.loads((P/f'raw/lighthouse-{phase}.json').read_text());aud=r.get('audits',{})
 def metric(k):return aud.get(k,{}).get('numericValue',NA)
 perf.append(dict(phase=phase,url=r.get('finalDisplayedUrl',r.get('finalUrl','')),template='category',run_date='2026-10-12',environment='Chrome headless; Lighthouse mobile defaults; same machine; production /images/',lighthouse_version=r['lighthouseVersion'],html_bytes='',css_bytes='',js_bytes='',image_bytes='',font_bytes='',requests=len(aud.get('network-requests',{}).get('details',{}).get('items',[])),lcp_ms=metric('largest-contentful-paint'),inp_ms=NA,cls=metric('cumulative-layout-shift'),ttfb_ms=metric('server-response-time'),source='Lighthouse lab',notes='One sample per phase; machine/network variability; not field CWV. Runtime error: '+str(r.get('runtimeError'))))
write('performance.csv',perf)
(P/'methodology.md').write_text('''# Methodology — 2026-10-12

Scope: add the exact user-supplied esports v2 JSON prompt, three original AI-generated examples and a matching ASCII header; run Howl and a full-site SEO/AI discovery audit. Canonical origin https://prompts.robertdevore.com; English; audience: creators reusing prompts; conversion: discover and copy a prompt. Source began clean on main at 83d33eb932f6ede070644dfbd285f3e3b2a21ebd.

Delivery: content/templates → vendored Kujo SSG + build postprocessors → output → main-triggered GitHub Pages workflow → custom domain. CI pins checksum-verified Kujo 1.0.1. Local 1.5.0 runs Howl only. No DNS/CDN, training-crawler policy or analytics changes are authorized or made.

A transient ENOSPC and slow local build led to a fresh unchanged-commit Actions baseline, run 38295639335. Downloaded generated artifact passed SKIP_BUILD=1 bash scripts/test-site.sh locally. The ignored baseline-output.tar.gz was sealed with its committed checksum before article edits; all baseline tables and receipts remain preserved. Older audit directories are immutable.

Collectors reused from 2026-09-22 preserve field schemas and BFS link depth. Local indexability is separate from production status. Sitemap inventory is independently cross-checked against every generated HTML route with check-discovery.py and check-internal-links.py. Full-site page purpose is reviewed by content type; posts expose primary prompt text, navigation pages group it, About/Contact identify the author. New esports context explains actual style profiles and raster examples without claims of guaranteed production-ready logos. Structured data parsing is distinct from rich-result eligibility.

Baseline user-agent probes cover homepage, robots and a category. After probes additionally cover sitemap and the new article; these added requests have no one-to-one baseline. User-agent spoofing does not verify crawler-IP access. Optional www DNS and historical redirects are recorded, not silently changed. Sensitive cookie headers are excluded. No logs available to enumerate all 4xx/5xx requests.

Reproduce: python3 collect_audit.py --phase baseline|after; python3 collect_production.py --phase baseline|after; python3 collect_weights.py --phase baseline|after (from this directory using absolute script paths or repository-root-relative paths). Do not rerun baseline in place; use a new audit directory to preserve evidence. Run verify_new_post.py from the repository; serve output on port 4179 and run verify_browser.cjs with PLAYWRIGHT_MODULE pointing to installed Playwright. Browser covers JSON/clipboard equality, all three images, mobile overflow, category image dimensions, empty category and no-JS discovery.

Lighthouse 13.5.0 uses headless Chrome, mobile defaults, the live /images/ URL and performance/accessibility/SEO categories; JSON receipts retain settings and timestamps. The after Lighthouse sample at 8c820b6 uses byte-identical /images/index.html to the final b8a30bc artifact (raw/lighthouse-category-equivalence.json). Final CI/Pages run: 38297133738. One sample per phase is directional, with host contention and network variance; no statistical improvement claimed. Static byte totals are uncompressed references, not network transfer. Scores from Lighthouse are lab tool results only; internal SEO/AI readiness scores omitted because unavailable account data would make them misleading.
''')
(P/'changes.md').write_text('''# Changes

- 6d3c73f: published the exact 41,192-character supplied JSON, practical use guidance, all six profiles, three generated example variations, descriptive alt text, intrinsic dimensions, lazy loading, gold ASCII header and a Howl 1200×630 social card. Generation prompts and actual native sizes recorded in image-prompts/esports-logo-generator.json. Example names: Rogue Rebels, Dungeon Lords, Pixel Runners. Article date reflects this publication, 2026-10-12.
- 8c820b6: preserve pre-rendered category cards instead of replacing them with dimensionless JavaScript cards. Updated script cache version and its existing assertion.
- Complete 23-card Howl manifest validates and renders; existing social assets remain unchanged. Source JSON parses and matches the user's exact text hash; browser clipboard check independently verifies rendering.
- b8a30bc: moved verbatim JSON into prompt-sources and extended the existing literal renderer/search enrichment for JSON; changed examples to supported Markdown image syntax after browser checks caught escaped HTML; article examples receive lazy loading and async decoding. Final rendered-output and clipboard verification follows this correction.
- No unrelated content, canonical routes, DNS, crawler policy or schema claims changed.
''')
lines=['# Before / after','', '| Metric | Before | After |','|---|---:|---:|']
for key in b:
 if key!='phase':lines.append(f'| {key} | {b[key]} | {a[key]} |')
lines+=['','Canonical route count intentionally increases by one new article; 12 posts fit the existing two archive pages. P0/P1: 0 → 0. Five category routes retain their generated cards; the baseline mobile Lighthouse identified six dimensionless images on /images/. Browser verification confirms dimensions remain after JavaScript executes. No ranking, traffic or citation outcomes measured.','', 'Lab measurements and static weights: performance.csv; runtime settings and diagnostics: raw/lighthouse-*.json. Internal scores: not assigned.']
(P/'before-after.md').write_text('\n'.join(lines)+'\n')
(P/'recommendations.md').write_text('''# Measurement and recommendations

At 7 days (2026-10-19): verify new URL discovery, sitemap processing, selected canonical and crawl state in Google Search Console and Bing Webmaster Tools; check real crawler logs and 4xx/5xx errors if access is granted.

At 28 days (2026-11-09): compare page/query impressions, clicks, CTR, position, devices and country for the new URL plus unchanged controls. Repeat the stored keyword queries with controlled engine/location/device settings. Review mobile field LCP/INP/CLS if sufficient samples exist.

At 60 days (2026-12-11) and 90 days (2027-01-10): repeat those windows and the exact AI benchmark questions with recorded platform/model, session time, locale, citations, competing domains and cited context. Keep provider visibility separate from general search traffic. Compare Bing AI Performance where authorized.

Evaluate responsive card thumbnails and font delivery independently of full-resolution article examples; repeat performance on representative home, category and post templates before claiming a site-wide improvement. Optional www alias requires an owner policy decision and DNS access; canonical host is healthy. Maintain existing crawler-training policy. No llms.txt/WebMCP visibility guarantees.
''')
(P/'unresolved.md').write_text('''# Unresolved / access limits

- Existing optional www.prompts.robertdevore.com hostname does not resolve. Canonical host works and no internal route depends on www. DNS/CDN policy changes require owner approval; no changes made.
- Mobile /images/ lab performance remains a measurement and image-delivery follow-up. Baseline category-card dimension loss is fixed. Full-resolution cards/external fonts remain candidates for a separately verified responsive delivery change. One sample cannot establish user impact or causality.
- Search Console, Bing account/AI Performance, analytics, server/CDN logs, backlinks, field CWV and controlled AI citation measurements: NOT AVAILABLE — DATA ACCESS REQUIRED.
- Native generated examples are 1254×1254; the user profile recommends 2048×2048 but the tool returned smaller rasters. Actual dimensions are truthful; no artificial upscaling or editable-vector claim.

No unresolved introduced repository defect. No claim that publication guarantees indexing, rankings or AI citations.
''')
(P/'executive-summary.md').write_text(f'''# PASS WITH RECOMMENDATIONS — 2026-10-12

The esports logo article is added with the exact supplied v2 JSON, six profiles, three AI-generated logo variations, matching ASCII hero art and a Howl social card. Whole-site canonical coverage changes from {b['canonical_pages']} to {a['canonical_pages']}; before/after datasets show no broken internal links, missing/duplicate titles or descriptions, missing image dimensions in generated HTML, or JSON-LD parse errors. P0/P1: 0 before, 0 after.

The untouched baseline passed the pinned CI site contract and local artifact revalidation. The resulting build is verified with repository checks, exact JSON/clipboard comparison, image decoding, discovery surfaces and mobile/no-JS browser checks. Deployment and live HTTP/crawler receipts are separate evidence. See raw/*verification.json and raw/*ci*.json. A separate JSON source avoids SSG indentation loss; supported Markdown images avoid escaped raw HTML.

A live Lighthouse baseline found JavaScript replacing correctly rendered category cards with dimensionless images. The fix preserves the build-rendered DOM. Internal SEO/AI scores are not assigned; lab results are in performance.csv and raw Lighthouse receipts, not a ranking metric. Existing optional www DNS and image-delivery recommendations remain; no infrastructure policy was changed.

Search visibility is limited to the dated search sample in raw/search-observations.json. Controlled rankings, traffic, field CWV and AI citations: NOT AVAILABLE — DATA ACCESS REQUIRED. No visibility improvement is claimed. Exact 7/28/60/90-day comparisons are in recommendations.md. Detailed change provenance: changes.md; file changes: raw/changed-files.txt.
''')
print('Audit supplementary tables and report generated.')
