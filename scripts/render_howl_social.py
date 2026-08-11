#!/usr/bin/env python3
"""Render committed URL-free Howl SVG and PNG social cards."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

from sync_howl_manifest import write_manifest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "howl.json"
SVG_OUTPUT = ROOT / "assets" / "social" / "howl"
PNG_OUTPUT = ROOT / "assets" / "social"
ROUTE_MAP = PNG_OUTPUT / "social-image-map.json"
HOWL_BRAND_PREFIX = "KUJOLANG.AI  //  "
GRAIN_OVERLAY = '<rect width="1200" height="630" filter="url(#grain)" opacity=".7"/>\n'
EMBEDDED_FONT_STACK = "font-family:'HowlMono','Departure Mono',monospace"
PORTABLE_FONT_STACK = "font-family:'Departure Mono',monospace"
BRAND_ART = """<g aria-hidden="true" opacity=".92">
<rect x="792" y="112" width="326" height="382" rx="4" fill="#0d0d0d" stroke="#2d2d2d" stroke-width="2"/>
<rect x="792" y="112" width="326" height="48" rx="4" fill="#141414"/>
<circle cx="820" cy="136" r="5" fill="#f7df1e"/><circle cx="840" cy="136" r="5" fill="#666"/><circle cx="860" cy="136" r="5" fill="#333"/>
<path d="M834 205h150M834 244h214M834 283h176M834 322h236M834 361h126M834 400h198" stroke="#f7df1e" stroke-width="6" stroke-linecap="square" opacity=".9"/>
<path d="M1030 205h54M1068 244h42M1028 283h72M1090 322h20M980 361h112M1050 400h58" stroke="#fff" stroke-width="6" stroke-linecap="square" opacity=".22"/>
<path d="M760 80h410M760 526h410" stroke="#f7df1e" stroke-width="1" opacity=".35"/>
</g>\n"""


def howl_binary() -> str:
    configured = os.environ.get("HOWL_BIN", "").strip()
    if configured:
        return configured
    discovered = shutil.which("howl")
    if discovered:
        return discovered
    raise SystemExit("Howl is unavailable; install it on PATH or set HOWL_BIN.")


def apply_prompts_brand(svg: str) -> str:
    """Restyle Howl's social layout to match the site's black/yellow system."""
    replacements = {
        HOWL_BRAND_PREFIX: "PROMPTS.ROBERTDEVORE.COM  //  ",
        '<rect width="1200" height="630" fill="#f4f4f1"/>\n': '<rect width="1200" height="630" fill="#060606"/>\n' + BRAND_ART,
        'stop-color="#fff" stop-opacity=".98"': 'stop-color="#060606" stop-opacity=".99"',
        'stop-color="#fff" stop-opacity=".88"': 'stop-color="#060606" stop-opacity=".96"',
        'stop-color="#fff" stop-opacity=".18"': 'stop-color="#060606" stop-opacity=".45"',
        'stop-color="#fff" stop-opacity="0"': 'stop-color="#060606" stop-opacity=".08"',
        ".label{font-size:18px;letter-spacing:4px;fill:#111}": ".label{font-size:18px;letter-spacing:4px;fill:#f7df1e}",
        "fill:#050505;letter-spacing:-2px": "fill:#fff;letter-spacing:-2px",
        ".social-tag{font-size:24px;fill:#282828}": ".social-tag{font-size:24px;fill:#bdbdbd}",
        ".social-url{font-size:17px;letter-spacing:1px;fill:#111}": ".social-url{font-size:17px;letter-spacing:1px;fill:#f7df1e}",
        'fill="none" stroke="#111" stroke-width="1"': 'fill="none" stroke="#303030" stroke-width="1"',
        '<rect x="78" y="570" width="84" height="4" fill="#111"/>': '<rect x="78" y="570" width="84" height="4" fill="#f7df1e"/>',
    }
    branded = svg
    for old, new in replacements.items():
        if old not in branded:
            raise SystemExit(f"Expected Howl SVG marker is missing: {old[:72]}")
        branded = branded.replace(old, new, 1)
    return branded


def main() -> int:
    write_manifest()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest.get("cards", [])
    if not cards:
        raise SystemExit("Howl manifest has no cards to render.")

    binary = howl_binary()
    subprocess.run([binary, "validate", "--manifest", str(MANIFEST)], cwd=ROOT, check=True)
    SVG_OUTPUT.mkdir(parents=True, exist_ok=True)
    PNG_OUTPUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="prompts-howl-") as temporary:
        rendered = Path(temporary)
        font_config = rendered / "fonts.conf"
        font_config.write_text(
            '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n'
            f'<fontconfig><dir>{ROOT / "assets" / "sitekit" / "fonts"}</dir></fontconfig>\n',
            encoding="utf-8",
        )
        os.environ["FONTCONFIG_FILE"] = str(font_config)
        import cairosvg

        subprocess.run(
            [binary, "render", "--manifest", str(MANIFEST), "--out", str(rendered), "--format", "svg"],
            cwd=ROOT,
            check=True,
        )

        route_map: dict[str, str] = {}
        for card in cards:
            card_id = str(card["id"])
            source = rendered / f"{card_id}.svg"
            svg = source.read_text(encoding="utf-8")
            branded_svg = apply_prompts_brand(svg)
            (SVG_OUTPUT / source.name).write_text(branded_svg, encoding="utf-8")

            portable_svg = branded_svg.replace(GRAIN_OVERLAY, "", 1).replace(
                EMBEDDED_FONT_STACK, PORTABLE_FONT_STACK, 1
            )
            raw_png = PNG_OUTPUT / f".{card_id}-social.raw.png"
            cairosvg.svg2png(
                bytestring=portable_svg.encode("utf-8"),
                write_to=str(raw_png),
                output_width=1200,
                output_height=630,
            )
            png_target = PNG_OUTPUT / f"{card_id}-social.png"
            with Image.open(raw_png) as image:
                image.convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(
                    png_target, optimize=True
                )
            raw_png.unlink()

            route = urlparse(str(card.get("url", ""))).path or "/"
            if route in route_map:
                raise SystemExit(f"Duplicate Howl social route: {route}")
            route_map[route] = f"/assets/social/{png_target.name}"

    expected_svg = {f"{card['id']}.svg" for card in cards}
    expected_png = {f"{card['id']}-social.png" for card in cards}
    for stale in SVG_OUTPUT.glob("*.svg"):
        if stale.name not in expected_svg:
            stale.unlink()
    for stale in PNG_OUTPUT.glob("*-social.png"):
        if stale.name not in expected_png:
            stale.unlink()
    ROUTE_MAP.write_text(json.dumps(dict(sorted(route_map.items())), indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {len(cards)} branded, URL-free Howl social cards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
