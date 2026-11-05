"""WCAG 2.x contrast checks for colors and design-token pairs.

Usage:
    contrast.py "#767676" "#ffffff"
    contrast.py --tokens tokens.json --pairs pairs.json

tokens.json follows the Design Tokens Community Group format: `$value` is a
hex string, a `{"colorSpace": "srgb", "components": [r, g, b]}` object, or an
alias like `{color.gray.900}`. pairs.json lists `{"fg", "bg", "use"}` with use
`text` (4.5:1, SC 1.4.3), `large-text` (3:1), or `ui` (3:1, SC 1.4.11).
Exit 1 when any pair fails. The ratio is WCAG 2's formula, which is what
conformance is judged by today; APCA is not used because it is not part of a
published WCAG recommendation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

THRESHOLDS = {"text": 4.5, "large-text": 3.0, "ui": 3.0}


def _channel(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def ratio(fg: str, bg: str) -> float:
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _lookup(tokens: dict, path: str) -> dict:
    node = tokens
    for part in path.split("."):
        node = node[part]
    return node


def resolve(tokens: dict, path: str, seen: tuple[str, ...] = ()) -> str:
    if path in seen:
        raise ValueError(f"alias cycle: {' -> '.join(seen + (path,))}")
    value = _lookup(tokens, path)["$value"]
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        return resolve(tokens, value[1:-1], seen + (path,))
    if isinstance(value, dict):
        if "hex" in value:
            return value["hex"].lower()
        if value.get("colorSpace") == "srgb":
            return "#" + "".join(f"{round(c * 255):02x}" for c in value["components"][:3])
        raise ValueError(f"{path}: color space {value.get('colorSpace')!r} needs a hex fallback")
    return str(value).lower()


def check_pairs(tokens: dict, pairs: list[dict]) -> list[dict]:
    results = []
    for p in pairs:
        r = ratio(resolve(tokens, p["fg"]), resolve(tokens, p["bg"]))
        need = THRESHOLDS[p.get("use", "text")]
        results.append({**p, "ratio": round(r, 2), "need": need, "pass": r >= need})
    return results


def main(argv: list[str]) -> int:
    if len(argv) == 2 and not argv[0].startswith("--"):
        r = ratio(argv[0], argv[1])
        print(f"{r:.2f}:1  text {'pass' if r >= 4.5 else 'fail'}  large/ui {'pass' if r >= 3 else 'fail'}")
        return 0
    if len(argv) == 4 and argv[0] == "--tokens" and argv[2] == "--pairs":
        tokens = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        results = check_pairs(tokens, json.loads(Path(argv[3]).read_text(encoding="utf-8")))
        for r in results:
            print(f"{'ok  ' if r['pass'] else 'FAIL'} {r['fg']} on {r['bg']} ({r['use']}): {r['ratio']}:1, needs {r['need']}:1")
        return 0 if all(r["pass"] for r in results) else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
