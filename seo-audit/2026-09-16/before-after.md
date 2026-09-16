# Before and after

Audit date: 2026-09-16

Immediate technical evidence only; search outcomes require post-deployment data and elapsed time.

| Measure | Baseline | After | Interpretation |
| --- | ---: | ---: | --- |
| Canonical/indexable pages | 18/18 | 21/21 | Three intentional prompt additions |
| Missing or duplicate titles | 0 | 0 | Pass |
| Missing or duplicate descriptions | 0 | 0 | Pass |
| H1 issues | 0 | 0 | Pass |
| Broken internal links | 0 | 0 | Pass |
| Confirmed broken external links | 0 | 0 | Pass |
| Orphan pages | 0 | 0 | Pass |
| Image usages | 37 | 55 | New post, listing, and social media usage |
| Missing alt text / dimensions | 0 / 0 | 0 / 0 | Pass |
| JSON-LD parse errors | 0 | 0 | Pass |
| Server-rendered category cards | 0 across five categories | 9 across five categories | Crawlability and no-JS resilience improved |
| Internal technical SEO score | 90/100 | 93/100 | Heuristic; not a search-engine score |
| Internal AI-search readiness | 66/100 | 71/100 | Heuristic; measured citation component unavailable |
| P0 / P1 root causes | 0 / 0 | 0 / 0 | No critical or material blocker found |

## Internal score composition

| SEO health component (weight) | Baseline | After |
| --- | ---: | ---: |
| Crawlability/indexability (20) | 19 | 19 |
| Metadata/SERP presentation (15) | 15 | 15 |
| Architecture/internal linking (15) | 13 | 15 |
| Content quality/currentness (15) | 14 | 15 |
| Structured data (10) | 10 | 10 |
| Performance/CWV evidence (10) | 5 | 5 |
| Media (5) | 5 | 5 |
| Authority/trust (5) | 5 | 5 |
| AI-search readiness contribution (5) | 4 | 4 |
| **Total** | **90** | **93** |

| AI-search readiness component (weight) | Baseline | After |
| --- | ---: | ---: |
| Search crawler access (15) | 15 | 15 |
| Indexability (10) | 10 | 10 |
| Information/entity clarity (10) | 8 | 9 |
| Source attribution/authorship (10) | 8 | 8 |
| Original/citable information (15) | 7 | 9 |
| Semantic/structured data (10) | 8 | 8 |
| Internal topic relationships (10) | 4 | 7 |
| Freshness (5) | 2 | 2 |
| Technical/media readiness (5) | 4 | 3 |
| Measured AI visibility (10) | 0 | 0 |
| **Total** | **66** | **71** |

The after technical/media subscore reflects larger page media and inconclusive lab performance; it was not offset by an unsupported field-performance claim.

## Representative Lighthouse lab results

| Template | Baseline LCP | After LCP | Baseline performance | After performance |
| --- | ---: | ---: | ---: | ---: |
| Home | 6,701 ms | 7,177 ms | 0.65 | 0.64 |
| Writing category | 4,696 ms | 5,122 ms | 0.73 | 0.71 |
| Existing article | 7,021 ms | 6,936 ms | 0.61 | 0.61 |

All six runs scored 1.00 for accessibility, best practices, and Lighthouse SEO. These single local lab runs show variance, not a statistically reliable regression or field Core Web Vitals result. No CrUX data was available.

## Production behavior

- Canonical HTTP redirects to HTTPS in one 301 hop.
- The WWF subdomain redirects to `https://robertdevore.com/` in one 301 hop.
- The retired WWF prompt URL redirects to the prompts homepage in one 301 hop.
- Real missing routes return 404, and query strings are preserved.
- Both `www` host variants fail DNS resolution before and after.
