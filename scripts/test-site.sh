#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

fail() {
	printf 'FAIL: %s\n' "$1"
	exit 1
}

assert_path() {
	[[ -e "$1" ]] || fail "missing path: $1"
}

assert_contains() {
	grep -Fq -- "$2" "$1" || fail "expected '$2' in $1"
}

assert_not_contains() {
	if grep -Fq -- "$2" "$1"; then
		fail "did not expect '$2' in $1"
	fi
}

assert_count() {
	local actual
	actual="$(grep -oF -- "$2" "$1" | wc -l | tr -d ' ')"
	[[ "$actual" == "$3" ]] || fail "expected $3 occurrences of '$2' in $1, found $actual"
}

bash -n scripts/build.sh scripts/test-site.sh scripts/validate-generated-output.sh

assert_path assets/sitekit/LICENSE
assert_path assets/sitekit/sitekit.css
assert_path assets/sitekit/sitekit.js
assert_path assets/sitekit/fonts/DepartureMono-Regular.woff2
assert_path assets/sitekit/fonts/DepartureMono-LICENSE.txt

if [[ "${SKIP_BUILD:-0}" == "1" ]]; then
	bash scripts/validate-generated-output.sh output
else
	SITE_URL=https://prompts.robertdevore.com bash scripts/build.sh
fi

expected_routes=(
	output/index.html
	output/page/2/index.html
	output/blog/index.html
	output/about/index.html
	output/contact/index.html
	output/images/index.html
	output/writing/index.html
	output/business/index.html
	output/marketing/index.html
	output/coding/index.html
	output/blog/prompts-coming-soon/index.html
	output/blog/simpsons-character-json-prompts-for-ai-generation/index.html
	output/blog/youtube-thumbnail-generation-with-ai-json-prompts/index.html
	output/blog/metallic-sci-fi-hud/index.html
	output/blog/top-secret-military-patches-json-prompt/index.html
	output/blog/isometric-3d-icon-json-prompt-for-ai-generated-designs/index.html
	output/blog/glowing-neon-icon-json-prompt/index.html
	output/blog/brutally-honest-company-product-diagnostic/index.html
	output/blog/keyword-competitor-content-analysis/index.html
	output/blog/dependabot-security-maintenance-agent/index.html
	output/404.html
	output/feed/index.xml
	output/sitemap.xml
	output/robots.txt
	output/llms.txt
	output/CNAME
	output/assets/sitekit/sitekit.css
	output/assets/sitekit/fonts/DepartureMono-Regular.woff2
	output/assets/js/docs-search-index.json
	output/assets/js/kujo-webmcp.js
	output/.well-known/kujo-site-index.json
)

for route in "${expected_routes[@]}"; do
	assert_path "$route"
done

assert_contains output/index.html 'Prompts built for making.'
assert_contains output/index.html 'Glowing Neon Icons: Design Bold Icons with This JSON Prompt'
assert_contains output/page/2/index.html 'Prompts: Coming Soon'
assert_contains output/contact/index.html 'mailto:me@robertdevore.com'
assert_contains output/about/index.html 'A Better Home for Useful Prompts'
assert_contains output/images/index.html 'data-prompt-category="images"'
assert_contains output/writing/index.html 'data-prompt-category="writing"'
assert_contains output/business/index.html 'href="/blog/brutally-honest-company-product-diagnostic/"'
assert_contains output/marketing/index.html 'href="/blog/keyword-competitor-content-analysis/"'
assert_contains output/coding/index.html 'href="/blog/dependabot-security-maintenance-agent/"'
assert_contains output/images/index.html 'aria-busy="false"'
assert_contains output/writing/index.html 'No prompts in this category yet. Check back soon.'
assert_contains output/business/index.html 'alt="Featured image for Business Prompts"'
assert_contains output/coding/index.html 'alt="Featured image for Coding Prompts"'
assert_contains output/marketing/index.html 'alt="Featured image for Marketing Prompts"'
assert_contains output/writing/index.html 'alt="Featured image for Writing Prompts"'
assert_contains output/images/index.html 'alt="Featured image for Image Prompts"'
assert_contains output/about/index.html 'alt="Featured image for About"'
assert_contains output/contact/index.html 'alt="Featured image for Contact"'
assert_contains output/index.html 'class="menu-overlay"'
assert_contains output/index.html 'class="desktop-navigation" aria-label="Prompt categories"'
assert_contains output/index.html 'href="images/">Images</a>'
assert_contains output/index.html 'icon-tabler-menu-2'
assert_contains output/index.html 'icon-tabler-x'
assert_contains output/index.html 'https://rsms.me/inter/inter.css'
assert_contains output/index.html 'assets/css/style.css?v=20260916.2'
assert_contains output/index.html 'assets/js/docs.js?v=20260809.5'
assert_contains output/index.html 'data-kujo-webmcp'
assert_contains output/index.html 'data-kujo-site-index=".well-known/kujo-site-index.json"'
assert_contains output/blog/glowing-neon-icon-json-prompt/index.html 'data-kujo-site-index="../../.well-known/kujo-site-index.json"'
if grep -Fq 'data-kujo-webmcp' output/404.html; then
	fail "WebMCP runtime leaked onto the 404 page"
fi
python3 - <<'PY'
import json
from pathlib import Path

index = json.loads(Path("output/.well-known/kujo-site-index.json").read_text())
assert index["schema"] == "kujo-ssg-site-index/v1"
assert index["site"]["url"] == "https://prompts.robertdevore.com"
assert {entry["name"] for entry in index["content_types"]} == {"pages", "posts"}
assert len(index["items"]) >= 10
assert all(item["url"].startswith("/") for item in index["items"])
assert all(set(item) <= {"id", "type", "slug", "url", "title", "description", "summary", "language", "searchable", "taxonomies", "published", "updated"} for item in index["items"])
PY
assert_contains output/index.html '<code class="language-json">'
assert_contains output/index.html '<link rel="author" href="https://robertdevore.com/">'
if grep -Fq 'Copy the structure, swap in your idea, and start creating.' output/index.html; then
	fail "obsolete homepage helper copy leaked into generated output"
fi
assert_count output/index.html '<li class="listing-card">' 6
assert_contains output/index.html '<a class="footer-author" href="https://robertdevore.com/">Robert DeVore</a>'
assert_contains output/index.html 'This website was built with <a class="footer-kujo" href="https://kujolang.ai/">Kujo</a>.'
if rg -n 'site-brand-mark' output --glob '*.html' --glob '*.css'; then
	fail "legacy header icon leaked into generated output"
fi
if rg -n 'menu-overlay-backdrop' output --glob '*.html' --glob '*.css'; then
	fail "obsolete menu backdrop leaked into generated output"
fi
assert_contains output/blog/youtube-thumbnail-generation-with-ai-json-prompts/index.html 'EXTREME LEADERSHIP'
assert_contains output/blog/top-secret-military-patches-json-prompt/index.html 'alt="Patch 4"'
assert_contains output/blog/top-secret-military-patches-json-prompt/index.html 'keywords *or* a weighted fallback pool'
assert_contains output/assets/css/style.css '--prompts-accent: var(--sk-state-warning)'
assert_contains output/assets/css/style.css '--prompts-body-font: "InterVariable"'
assert_contains output/assets/css/style.css '.article-header h1 { max-inline-size: 15ch; padding-inline: 0; border: var(--sk-border-0)'
assert_contains output/assets/css/style.css '.article-shell { inline-size: min(100% - var(--sk-space-8), var(--sk-size-content-md)); }'
assert_contains output/assets/css/style.css 'grid-template-columns: minmax(0, 1fr) minmax(11rem, 14rem);'
assert_contains output/assets/css/style.css '.site-home .card-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }'
assert_contains output/assets/css/style.css '.desktop-navigation { display: flex;'
assert_contains output/assets/css/style.css '.site-menu-button { display: none;'
assert_contains output/assets/css/style.css '.site-menu-button { display: inline-grid; }'
assert_contains output/assets/css/style.css '.listing-visual, .article-visual { position: absolute; inset: 0;'
assert_contains output/blog/glowing-neon-icon-json-prompt/index.html '<div class="article-visual"><img '
assert_count output/blog/glowing-neon-icon-json-prompt/index.html 'alt="Featured image for Glowing Neon Icons: Design Bold Icons with This JSON Prompt"' 1
assert_not_contains output/blog/glowing-neon-icon-json-prompt/index.html 'alt="Glowing Neon Icon Example"'
assert_contains output/blog/dependabot-security-maintenance-agent/index.html 'alt="Featured image for Autonomous Dependabot Security Maintenance Agent Prompt"'
assert_contains output/assets/css/style.css '.card-grid, .site-home .card-grid { grid-template-columns: 1fr; }'
assert_contains output/assets/css/style.css 'background: transparent; color: var(--prompts-accent); border: var(--sk-border-0); cursor: pointer;'
assert_contains output/assets/css/style.css 'inset-block-start: var(--sk-space-3)'
assert_contains output/assets/css/style.css '.search-results { position: absolute'
assert_contains output/assets/css/style.css '.json-token.json-key { color: var(--prompts-accent); }'
assert_contains output/assets/css/style.css '.code-block-toolbar { position: sticky;'
if rg -n 'text-stroke|paint-order' output/assets/css/style.css; then
	fail "outlined title styling leaked into generated output"
fi
assert_contains output/assets/js/docs.js 'copyBlockText'
assert_contains output/assets/js/docs.js "document.querySelectorAll('code.language-json').forEach(highlightJson);"
assert_contains output/assets/js/docs.js "toolbar.className = 'code-block-toolbar';"
assert_contains output/index.html 'data-theme="kujo-dark"'
assert_contains output/index.html 'assets/sitekit/sitekit.css'
assert_contains output/CNAME 'prompts.robertdevore.com'
assert_contains output/sitemap.xml 'https://prompts.robertdevore.com/contact/'
assert_contains output/robots.txt 'Allow: /'
assert_contains output/robots.txt 'Sitemap: https://prompts.robertdevore.com/sitemap.xml'
assert_contains output/feed/index.xml 'xmlns:atom="http://www.w3.org/2005/Atom"'
assert_contains output/feed/index.xml '<atom:link href="https://prompts.robertdevore.com/feed/index.xml" rel="self" type="application/rss+xml"/>'
assert_contains output/feed/index.xml '<generator>Kujo SSG</generator>'
assert_contains output/feed/index.xml '<category>json prompts</category>'
if grep -Fq '&amp;apos;' output/feed/index.xml; then
	fail "double-escaped apostrophe leaked into RSS output"
fi
assert_contains output/llms.txt '> Explore a growing library of high-quality AI prompts'
assert_contains output/llms.txt '- [Prompt Library](https://prompts.robertdevore.com/)'
assert_contains output/blog/glowing-neon-icon-json-prompt/index.html '<meta property="og:image:width" content="1200">'
assert_contains output/blog/glowing-neon-icon-json-prompt/index.html '<meta property="og:image:height" content="630">'
assert_contains output/blog/glowing-neon-icon-json-prompt/index.html '<meta property="article:modified_time" content="2025-05-19">'
assert_contains output/blog/glowing-neon-icon-json-prompt/index.html '<meta property="article:author" content="https://robertdevore.com">'
assert_contains output/index.html 'width="1024" height="1024">'
assert_contains output/blog/index.html 'Browse reusable AI prompts with complete JSON structures, examples, and practical notes for image generation, design, and creative work.'
assert_contains output/assets/js/docs-search-index.json '"url": "https://prompts.robertdevore.com/blog/glowing-neon-icon-json-prompt/"'
assert_contains output/assets/js/docs-search-index.json 'minimum secure dependency version'
if grep -Fq '%%RAW_PROMPT:' output/assets/js/docs-search-index.json; then
	fail "raw prompt sentinel leaked into the search index"
fi
if rg -n '"url": "https://prompts\.robertdevore\.com/posts/|"url": "/posts/' output/assets/js/docs-search-index.json; then
	fail "legacy /posts/ routes leaked into the image prompt grid"
fi
if grep -Fq 'wwf-action-figure-blister-pack-json-prompt' output/assets/js/docs-search-index.json; then
	fail "removed WWF prompt leaked into the generated search index"
fi
if grep -Fq '<div class="category-introduction docs-body"><ul>' output/images/index.html; then
	fail "redundant image prompt list leaked into the category page"
fi
assert_contains output/blog/glowing-neon-icon-json-prompt/index.html '<h2>JSON Prompt</h2>'
assert_contains output/index.html 'class="listing-card-image-link" aria-label="View prompt details"'
assert_contains output/page/2/index.html 'alt="Featured image for Prompts: Coming Soon"'
assert_contains output/blog/brutally-honest-company-product-diagnostic/index.html 'raw truth, not sugar-coated trash'
assert_contains output/blog/keyword-competitor-content-analysis/index.html 'Competitor Content Evaluation:'
assert_contains output/blog/dependabot-security-maintenance-agent/index.html 'CLEAN — No open Dependabot alerts.'
assert_contains output/blog/dependabot-security-maintenance-agent/index.html '<pre><code class="language-markdown">You are an autonomous dependency-security maintenance agent.'
if grep -Fq '%%RAW_PROMPT:' output/blog/dependabot-security-maintenance-agent/index.html; then
	fail "unresolved raw prompt sentinel leaked into generated output"
fi
assert_contains output/assets/js/docs.js "imageLink.setAttribute('aria-label', 'View ' + item.title);"

if rg -n 'stattic\.site|tailwind\.min\.css|quicksand-' output --glob '*.html' --glob '*.css'; then
	fail "legacy Stattic presentation leaked into generated output"
fi

python3 scripts/check-internal-links.py output
python3 scripts/check-seo.py output
python3 scripts/check-discovery.py output

printf 'Site contract passed\n'
