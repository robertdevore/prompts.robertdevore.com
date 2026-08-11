#!/usr/bin/env python3
"""Add intrinsic dimensions to local images in generated HTML."""

from __future__ import annotations

import re
import struct
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
SRC_RE = re.compile(r'\bsrc=["\']([^"\']+)["\']', re.IGNORECASE)


def image_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        payload = data[20:]
        if chunk == b"VP8X" and len(payload) >= 10:
            return 1 + int.from_bytes(payload[4:7], "little"), 1 + int.from_bytes(payload[7:10], "little")
        if chunk == b"VP8L" and len(payload) >= 5 and payload[0] == 0x2F:
            b1, b2, b3, b4 = payload[1:5]
            return 1 + (((b2 & 0x3F) << 8) | b1), 1 + (((b4 & 0x0F) << 10) | (b3 << 2) | ((b2 & 0xC0) >> 6))
        if chunk == b"VP8 ":
            marker = payload.find(b"\x9d\x01\x2a")
            if marker >= 0 and len(payload) >= marker + 7:
                return (
                    int.from_bytes(payload[marker + 3 : marker + 5], "little") & 0x3FFF,
                    int.from_bytes(payload[marker + 5 : marker + 7], "little") & 0x3FFF,
                )
    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset + 9 < len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            marker = data[offset + 1]
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                return struct.unpack(">HH", data[offset + 5 : offset + 9])[::-1]
            if marker in {0xD8, 0xD9}:
                offset += 2
                continue
            length = int.from_bytes(data[offset + 2 : offset + 4], "big")
            offset += 2 + length
    return None


def local_image(root: Path, html_file: Path, src: str) -> Path | None:
    parsed = urlparse(src)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    target = root / path.lstrip("/") if path.startswith("/") else html_file.parent / path
    target = target.resolve()
    if root != target and root not in target.parents:
        return None
    return target


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    changed_files = 0
    changed_images = 0
    for html_file in sorted(root.rglob("*.html")):
        source = html_file.read_text(encoding="utf-8")

        def add_dimensions(match: re.Match[str]) -> str:
            nonlocal changed_images
            tag = match.group(0)
            if re.search(r"\bwidth\s*=", tag, re.IGNORECASE) and re.search(r"\bheight\s*=", tag, re.IGNORECASE):
                return tag
            src_match = SRC_RE.search(tag)
            if not src_match:
                return tag
            target = local_image(root, html_file, src_match.group(1))
            if target is None or not target.is_file():
                return tag
            dimensions = image_size(target)
            if dimensions is None:
                return tag
            width, height = dimensions
            changed_images += 1
            return tag[:-1] + f' width="{width}" height="{height}">'

        updated = IMG_RE.sub(add_dimensions, source)
        if updated != source:
            html_file.write_text(updated, encoding="utf-8")
            changed_files += 1
    print(f"Added intrinsic dimensions to {changed_images} images across {changed_files} HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
