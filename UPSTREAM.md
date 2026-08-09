# Upstream versions

| Dependency | Version | Vendored path | Source |
| --- | --- | --- | --- |
| Kujo SSG | 1.0.0 (`0020115`) | `build.kujo`, search and validation scripts | <https://github.com/kujolang/ssg/releases/tag/v1.0.0> |
| SiteKit | 1.0.0 (`245c24d`) | `assets/sitekit/` | <https://github.com/kujolang/site-kit/releases/tag/v1.0.0> |

The SiteKit distribution is copied without modification.

The vendored SSG entrypoint carries three intentional local patches:

- The default action for custom-collection cards reads `Read More` instead of `View Product`.
- Fenced-code normalization restores literal emphasis and inline-code delimiters that the native Markdown inline pass would otherwise turn into HTML inside `<code>`.
- Social metadata supports a site-wide fallback image, per-entry Open Graph overrides, image alt/type tags, Twitter attribution, article taxonomy tags, page-specific Schema.org types, and noindex control for non-content routes. The native renderer still handles full page bodies; a small interpreted shell replaces only the generated `<head>` so these site-specific fields do not regress render throughput.

All other SSG behavior remains pinned to 1.0.0.
