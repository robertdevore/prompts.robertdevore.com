# Before and after

| Measure | Initial publication | Verified deployment |
| --- | ---: | ---: |
| Canonical URLs returning 200 | 27 | 27 |
| Technically indexable pages | 27 | 27 |
| Missing or duplicate titles or descriptions | 0 | 0 |
| Pages with H1 problems or orphan URLs | 0 | 0 |
| Broken internal or confirmed broken external links | 0 | 0 |
| Broken images and missing alt text or dimensions | 0 | 0 |
| JSON-LD parse errors | 0 | 0 |
| Successful crawler user-agent probes | 45/45 | 45/45 |
| P0 or P1 issues | 0 | 0 |
| P2 issues in the issue register | 3 | 2 |
| New article Lighthouse mobile performance | 76 | 98 |
| New article Lighthouse mobile accessibility / SEO | 100 / 100 | 100 / 100 |
| New article mobile lab LCP | 4.22 s | 1.88 s |

The measured post-change mobile LCP was 2.34 s lower (55%) in the paired lab samples. Lighthouse's LCP request discovery checks passed after the hero change. Each column is one lab navigation, so the magnitude should be treated as an observation. Field CWV, rankings, and citations require separate measurements.

Both pinned build artifacts passed 1,069 internal link checks and contained 14 feed items. The desktop and mobile browser checks confirmed full prompt copy fidelity, image decoding, and JavaScript-free listing discovery. The source-to-output comparison verified 16 article headers with eager, high-priority images, and matched listing and inline image attributes. The live HTTP request for the new slug without a trailing slash serves a static zero-delay refresh stub with a relative canonical that resolves to the indexed path. The slash-plus-query variant has the absolute article canonical. HTTPS remains the canonical scheme. The optional nested www alias remains outside provisioned DNS.
