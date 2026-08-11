#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KUJO_BIN="${KUJO_BIN:-kujo}"
SITE_URL="${SITE_URL:-}"

cd "$REPO_ROOT"

search_args=(
	--content content
	--output assets/js/docs-search-index.json
)
build_args=("$@")

if [[ -n "$SITE_URL" ]]; then
	search_args+=(--site-url "$SITE_URL")
	build_args+=(--site-url "$SITE_URL")
fi

"$KUJO_BIN" run scripts/docs_search_index.kujo -- "${search_args[@]}"
"$KUJO_BIN" run ./build.kujo -- "${build_args[@]}"
python3 scripts/add-image-dimensions.py output
python3 scripts/fix-generated-accessibility.py output
if [[ -d static ]]; then
	cp -R static/. output/
fi
bash scripts/validate-generated-output.sh output
