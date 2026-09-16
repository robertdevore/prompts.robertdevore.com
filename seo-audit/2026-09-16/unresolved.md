# Unresolved items

Audit date: 2026-09-16

No P0 or P1 issues remain. Open items are P2 recommendations:

1. **`www` host decision (`SEO-003`)** — HTTP and HTTPS `www.prompts.robertdevore.com` do not resolve. Add proxied DNS plus a permanent one-hop redirect if `www` coverage is desired; otherwise document the intentional absence.
2. **Stale search cache (`SEO-004`)** — dated search observations still surfaced the retired WWF article and older page-2 content. Production redirects are correct; request recrawl/removal in Google Search Console and Bing Webmaster Tools.
3. **Field performance evidence (`SEO-005`)** — local Lighthouse LCP ranged from 5.1–7.2 seconds after the changes, with material font and image transfer. Obtain CrUX/RUM first, then test font and responsive-image improvements if field evidence confirms the issue.
4. **Measurement access (`SEO-006`)** — Search Console, Bing, analytics, request logs, CrUX, backlinks, and controlled AI-answer citation sessions were unavailable. Connect or export them to establish real discovery and outcome baselines.
