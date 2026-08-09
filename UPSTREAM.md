# Upstream versions

| Dependency | Version | Vendored path | Source |
| --- | --- | --- | --- |
| Kujo SSG | 1.0.0 (`0020115`) | `build.kujo`, search and validation scripts | <https://github.com/kujolang/ssg/releases/tag/v1.0.0> |
| SiteKit | 1.0.0 (`245c24d`) | `assets/sitekit/` | <https://github.com/kujolang/site-kit/releases/tag/v1.0.0> |

The SiteKit distribution is copied without modification.

The vendored SSG entrypoint carries two intentional local patches:

- The default action for custom-collection cards reads `Read More` instead of `View Product`.
- Fenced-code normalization restores literal emphasis and inline-code delimiters that the native Markdown inline pass would otherwise turn into HTML inside `<code>`.

All other SSG behavior remains pinned to 1.0.0.
