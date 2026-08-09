#!/usr/bin/env python3
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.links.append((tag, values["href"] or ""))
        if tag in {"img", "script", "source"} and values.get("src"):
            self.links.append((tag, values["src"] or ""))


def local_target(root: Path, source: Path, value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or value.startswith(("mailto:", "tel:", "data:")):
        return None
    path = unquote(parsed.path)
    if not path or path == "/":
        return root / "index.html"
    if path.startswith("/"):
        target = root / path.lstrip("/")
    else:
        target = source.parent / path
    if path.endswith("/"):
        target /= "index.html"
    elif not target.suffix:
        target /= "index.html"
    return target.resolve()


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    failures: list[str] = []
    checked = 0
    for html_file in sorted(root.rglob("*.html")):
        parser = LinkParser()
        parser.feed(html_file.read_text(errors="replace"))
        for tag, value in parser.links:
            target = local_target(root, html_file, value)
            if target is None:
                continue
            checked += 1
            if root not in target.parents and target != root:
                failures.append(f"path escape in {html_file.relative_to(root)}: {value}")
            elif not target.exists():
                failures.append(f"missing {tag} target in {html_file.relative_to(root)}: {value}")
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        return 1
    print(f"Internal links passed: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
