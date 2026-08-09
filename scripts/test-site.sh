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

bash -n scripts/build.sh scripts/test-site.sh scripts/validate-generated-output.sh

assert_path assets/sitekit/LICENSE
assert_path assets/sitekit/sitekit.css
assert_path assets/sitekit/sitekit.js
assert_path assets/sitekit/fonts/DepartureMono-Regular.woff2
assert_path assets/sitekit/fonts/DepartureMono-LICENSE.txt

SITE_URL=https://prompts.robertdevore.com bash scripts/build.sh

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
	output/blog/wwf-action-figure-blister-pack-json-prompt/index.html
	output/blog/simpsons-character-json-prompts-for-ai-generation/index.html
	output/blog/youtube-thumbnail-generation-with-ai-json-prompts/index.html
	output/blog/metallic-sci-fi-hud/index.html
	output/blog/top-secret-military-patches-json-prompt/index.html
	output/blog/isometric-3d-icon-json-prompt-for-ai-generated-designs/index.html
	output/blog/glowing-neon-icon-json-prompt/index.html
	output/404.html
	output/feed/index.xml
	output/sitemap.xml
	output/robots.txt
	output/llms.txt
	output/CNAME
	output/assets/sitekit/sitekit.css
	output/assets/sitekit/fonts/DepartureMono-Regular.woff2
	output/assets/js/docs-search-index.json
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
assert_contains output/index.html 'class="menu-overlay"'
assert_contains output/index.html 'href="images/">Images</a>'
if rg -n 'site-brand-mark' output --glob '*.html' --glob '*.css'; then
	fail "legacy header icon leaked into generated output"
fi
assert_contains output/blog/wwf-action-figure-blister-pack-json-prompt/index.html 'vintage wwf wrestling action figure in blister pack'
assert_contains output/blog/youtube-thumbnail-generation-with-ai-json-prompts/index.html 'EXTREME LEADERSHIP'
assert_contains output/blog/top-secret-military-patches-json-prompt/index.html 'alt="Patch 4"'
assert_contains output/blog/top-secret-military-patches-json-prompt/index.html 'keywords *or* a weighted fallback pool'
assert_contains output/assets/css/style.css '--prompts-accent: var(--sk-state-warning)'
assert_contains output/assets/css/style.css 'inset-block-start: var(--sk-space-3)'
assert_contains output/assets/css/style.css '.search-results { position: absolute'
if rg -n 'text-stroke|paint-order' output/assets/css/style.css; then
	fail "outlined title styling leaked into generated output"
fi
assert_contains output/assets/js/docs.js 'copyBlockText'
assert_contains output/index.html 'data-theme="kujo-dark"'
assert_contains output/index.html 'assets/sitekit/sitekit.css'
assert_contains output/CNAME 'prompts.robertdevore.com'
assert_contains output/sitemap.xml 'https://prompts.robertdevore.com/contact/'
assert_contains output/robots.txt 'Allow: /'

if rg -n 'stattic\.site|tailwind\.min\.css|quicksand-' output --glob '*.html' --glob '*.css'; then
	fail "legacy Stattic presentation leaked into generated output"
fi

python3 scripts/check-internal-links.py output

printf 'Site contract passed\n'
