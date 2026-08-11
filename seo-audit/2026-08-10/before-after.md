# Before and after

Audit date: 2026-08-10

Immediate technical evidence only; search outcomes require post-deployment data and elapsed time.

| Metric | Baseline | After rebuild |
| --- | ---: | ---: |
| Canonical/indexable pages | 19 / 19 | 19 / 19 |
| Missing titles/descriptions/canonicals | 0 / 0 / 0 | 0 / 0 / 0 |
| Duplicate title instances | 0 | 0 |
| Duplicate description instances | 2 | 0 |
| H1 problems | 0 | 0 |
| Broken internal links | 0 | 0 |
| Orphans / pages deeper than 3 clicks | 0 / 0 | 0 / 0 |
| Missing alt attributes | 0 | 0 |
| Image instances missing dimensions | 27 | 0 |
| JSON-LD parse errors | 0 | 0 |
| P0 / P1 root causes | 0 / 0 | 0 / 0 |
| P2 root causes open | 5 | 2 measurement/performance recommendations |
| Internal SEO health heuristic | 80 / 100 | 91 / 100 |
| Internal AI-search readiness heuristic | 74 / 100 | 80 / 100 |

Score weights follow `artifact-schemas.md`. The AI score awards zero for measured AI visibility because controlled platform data was unavailable. Improvements come from distinct metadata, static category relationships, complete media dimensions, and stronger semantics—not inferred rankings or citations.

Representative Lighthouse evidence is in `performance.csv`. Production baseline performance scores were home 26, article 63, category 32; production post-deployment runs were 65, 66, and 58. Home LCP moved from 7,521 ms to 2,030 ms, while category CLS moved from 0.2029 to 0.0430. These are encouraging single-run lab observations, not field CWV or durable outcome claims. Accessibility reached 100 on all three post-change templates after the heading and link-name fixes.
