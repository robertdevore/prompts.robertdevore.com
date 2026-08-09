#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$REPO_ROOT/VERSION")"
PACKAGE_NAME="prompts-robertdevore-com-v$VERSION"
DIST_DIR="$REPO_ROOT/dist"

mkdir -p "$DIST_DIR"
tar -czf "$DIST_DIR/$PACKAGE_NAME.tar.gz" \
	--exclude='.git' \
	--exclude='dist' \
	--exclude='output' \
	--exclude='assets/js/docs-search-index.json' \
	-C "$REPO_ROOT" .

printf 'Created %s\n' "$DIST_DIR/$PACKAGE_NAME.tar.gz"
