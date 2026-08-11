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

Representative Lighthouse evidence is in `performance.csv`. Production baseline scores were home 26, article 63, category 32; local post-change scores were home 89, article 93, category 73. Environments differ, so this is build validation rather than a production performance claim. Accessibility reached 100 on all three local templates after the heading and link-name fixes.
