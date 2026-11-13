"""Regenerate supplementary tables from saved evidence; baseline remains immutable."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
NA='NOT AVAILABLE — DATA ACCESS REQUIRED'
def rows(name):
 with (P/name).open() as f:return list(csv.DictReader(f))
def write(name,data):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
b=json.loads((P/'baseline-summary.json').read_text());a=json.loads((P/'after-summary.json').read_text())
pages=rows('after.csv')
write('keyword-map.csv',[dict(url=r['url'],topic=r['h1'],intent='Reuse a prompt' if r['page_type']=='post' else 'Discover prompts or publisher',primary_theme=r['title'],secondary_theme=r['meta_description'],related_entities='Robert DeVore; AI prompts',competing_url='',gap='No consolidation needed in publication scope',action='Preserve source; explain fictional roles' if 'ogilvy' in r['url'] else 'No editorial change') for r in pages])
write('search-rankings.csv',[dict(query=q,search_engine='Google / Bing benchmark plan',date='2026-11-12',country='US planned',device='desktop planned',page_found=NA,observed_position_or_range=NA,competing_results=NA,rich_features=NA,ai_result_presence=NA,evidence='No controlled rank measurement',limitations=NA) for q in ['Ogilvy Mather strategic review prompt','marketing strategy review AI prompt','prompts Robert DeVore strategic review']])
write('ai-search-benchmark.csv',[dict(question=q,platform='ChatGPT Search / Bing Copilot / Perplexity benchmark plan',date='2026-11-12',domain_appeared=NA,domain_cited=NA,cited_url=NA,citation_context=NA,citation_order=NA,competing_domains=NA,accurate_representation=NA,content_gap='Measure retrieval of this reusable review framework',evidence='No controlled sessions available',limitations='Planned question, not measured result') for q in ['Where can I copy a prompt to review my marketing strategy?','How can I challenge positioning and buyer assumptions with AI?','What does the Ogilvy and Mather strategic review prompt produce?','How does a strategic review differ from keyword competitor analysis?','How do I stop an AI marketing review from inventing traction?']])
write('issues.csv',[
 dict(id='SEO-03',phase='verification',category='archive validation',severity='P2',affected_urls='/page/3/; /blog/page/3/',affected_count=2,evidence='raw/initial-ci-failure.log; raw/archive-classification.log; raw/final-artifact-tests.log',expected_benefit='Validate archive schema accurately at every page number',confidence='high',difficulty='low',recommended_action='Generalize archive route matching',owner='repository',status='fixed in af5bd75'),
 dict(id='SEO-04',phase='verification',category='CI integrity',severity='P2',affected_urls='site-wide validation',affected_count=26,evidence='raw/initial-ci-failure.log; scripts/test-site.sh; raw/final-ci.json',expected_benefit='Execute forbidden-content scans in CI',confidence='high',difficulty='low',recommended_action='Use available portable grep scans',owner='repository',status='fixed in af5bd75'),
 dict(id='SEO-01',phase='baseline and after',category='optional hostname',severity='P2',affected_urls='https://www.prompts.robertdevore.com/',affected_count=1,evidence='raw/production-baseline.json; raw/production-after.json',expected_benefit='Optional alias availability',confidence='high',difficulty='owner decision',recommended_action='Retain existing canonical host; decide alias policy before DNS changes',owner='site owner',status='pre-existing; outside publication scope'),
 dict(id='SEO-02',phase='baseline and after',category='performance',severity='P2',affected_urls='https://prompts.robertdevore.com/marketing/',affected_count=1,evidence='raw/lighthouse-baseline.json; raw/lighthouse-after.json',expected_benefit='Potential mobile loading improvement',confidence='medium; lab only',difficulty='medium',recommended_action='Evaluate responsive card delivery and font/render blocking with repeated measurements',owner='site owner / repository',status='existing cross-category recommendation; previously recorded in 2026-10-12 audit; not an introduced defect')])
perf=[r for r in rows('performance.csv') if r.get('source')!='Lighthouse lab']
for phase in ['baseline','after']:
 r=json.loads((P/f'raw/lighthouse-{phase}.json').read_text());aud=r.get('audits',{})
 def metric(k):return aud.get(k,{}).get('numericValue',NA)
 perf.append(dict(phase=phase,url=r.get('finalDisplayedUrl',r.get('finalUrl','')),template='category',run_date='2026-11-12',environment='Chrome headless; Lighthouse mobile defaults; production /marketing/',lighthouse_version=r['lighthouseVersion'],html_bytes='',css_bytes='',js_bytes='',image_bytes='',font_bytes='',requests=len(aud.get('network-requests',{}).get('details',{}).get('items',[])),lcp_ms=metric('largest-contentful-paint'),inp_ms=NA,cls=metric('cumulative-layout-shift'),ttfb_ms=metric('server-response-time'),source='Lighthouse lab',notes='One sample; not field CWV; no causal improvement claim. '+str({k:v['score'] for k,v in r['categories'].items()})))
write('performance.csv',perf)
lines=['# Before / after','', '| Metric | Before | After |','|---|---:|---:|']
for key in b:
 if key!='phase':lines.append(f'| {key} | {b[key]} | {a[key]} |')
lines+=['','23 → 26 canonical routes: one new article plus page 3 of home and blog archives. 12 → 13 posts. No removed content or route. P0/P1: 0 → 0. All generated HTML routes are cross-checked by the repository discovery validator. Internal scores not assigned. Lab metrics: performance.csv. No measured search or AI visibility improvement.']
(P/'before-after.md').write_text('\n'.join(lines)+'\n')
(P/'recommendations.md').write_text('''# Comparable follow-up measurements

- 7 days, 2026-11-19: inspect URL discovery, sitemap processing, canonical selection and crawl state in Search Console/Bing; inspect verified crawler logs if available.
- 28 days, 2026-12-10: compare query/page impressions, clicks, CTR, position, country/device and unchanged control pages; repeat stored queries with controlled settings; field LCP/INP/CLS if sampled.
- 60 days, 2027-01-11, and 90 days, 2027-02-10: repeat those windows and exact AI benchmark questions with provider/model, date, locale, citations and cited context. Distinguish AI mentions from citations and referrals.

Responsive thumbnails and font delivery remain the existing separate site-wide performance opportunity. Preserve article originals. Optional www alias needs an owner decision. Existing llms.txt and WebMCP are discovery experiments, not ranking guarantees.
''')
(P/'unresolved.md').write_text('''# Limits and existing recommendations

No unresolved introduced repository defect. Canonical production is tested independently of generated output. Existing optional www hostname is unavailable; no internal links depend on it. DNS policy remains outside this publication. Existing responsive image/font delivery recommendation remains; single lab samples do not establish field impact.

Search Console, Bing account reports, analytics, logs, field CWV, backlink/competitor metrics, controlled ranks and AI citation sessions: NOT AVAILABLE — DATA ACCESS REQUIRED.
''')
(P/'changes.md').write_text('''# Changes

619db85 publishes the verbatim attached Markdown in prompt-sources, an article with usage guidance and fictional-role clarification, contextual links, marketing/business discovery, generated gold ASCII hero, and Howl social cards. Full source equality is checked separately from displayed text and browser clipboard equality. Native hero 1672×941 WebP; social PNG 1200×630. Exact built-in generation prompt and final path are in image-prompts/ogilvy-mather-strategic-review.json.

Adding the thirteenth post requires two new archive routes and corresponding Howl cards. The route contract checks page 3 and the supplied prompt's fidelity. Existing unrelated artwork is unchanged. af5bd75 generalizes archive schema validation beyond hardcoded page 2, shortens the SEO title to fit the existing rendered-title contract, and replaces unavailable ripgrep invocations with portable grep scans so CI actually executes the forbidden-content checks. The initial failed CI log and archive-classification regression receipt are preserved.

The audit preserves the untouched baseline, structured before/after inventory, current official guidance, production/crawler probes and browser evidence. No crawler policy, DNS, schema authorship claims or supplied prompt wording changed.
''')
(P/'executive-summary.md').write_text(f'''# PASS WITH RECOMMENDATIONS — 2026-11-12

Published the exact Ogilvy & Mather Universal Strategic Review prompt with usage guidance, matching generated artwork and Howl social cards. Full-site inventory: {b['canonical_pages']} → {a['canonical_pages']} canonical pages, reflecting one article and two archive pages. P0/P1: 0 before and after. Before/after tables record metadata, links, depth, images, schema and indexability; source, generated artifact and live HTTP evidence remain separate.

Pinned Kujo 1.0.1 builds and repository contract checks, Howl validation, literal source/clipboard comparisons, hero decoding, mobile overflow and no-JavaScript category discovery are the validation gates. See raw build, browser, prompt and production receipts. Existing optional www and site-wide media/font delivery recommendations remain. Internal aggregate scores are omitted; Lighthouse results are lab measurements, not ranking scores.

Search/AI visibility, analytics, field CWV and request logs: NOT AVAILABLE — DATA ACCESS REQUIRED. No rankings, traffic or citations claimed. Measurement dates and exact benchmark questions are preserved in recommendations.md and the benchmark CSVs. Source change list and CI/deployment evidence are in raw/.
''')
print('Report regenerated from receipts.')
