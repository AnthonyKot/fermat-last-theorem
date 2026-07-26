#!/usr/bin/env python3
"""Render the About page's proof-status block from the canonical ledger data.

Serving the site still has no build step: generated HTML is committed. During
authoring, use --write after changing data/ledger.json. verify.sh uses --check
and fails when the committed page has drifted from the register.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ledger.json"
ABOUT = ROOT / "about.html"
START = "<!-- proof-register:start -->"
END = "<!-- proof-register:end -->"

REGISTER_LABELS = {
    "proved": "Proved",
    "stated": "Stated",
    "outlined": "Outlined",
    "conditional": "Conditional",
    "described": "Described",
}


def load_register() -> list[dict]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    items = raw.get("proof_register")
    if not isinstance(items, list):
        raise ValueError("data/ledger.json must contain a proof_register list")

    ids: set[str] = set()
    for item in items:
        missing = {"id", "register", "availability", "essays", "text"} - item.keys()
        if missing:
            raise ValueError(f"proof-register item is missing {sorted(missing)}: {item}")
        if item["id"] in ids:
            raise ValueError(f"duplicate proof-register id: {item['id']}")
        ids.add(item["id"])
        if item["register"] not in REGISTER_LABELS:
            raise ValueError(f"unknown register for {item['id']}: {item['register']}")
        if item["availability"] not in {"available", "planned"}:
            raise ValueError(f"unknown availability for {item['id']}: {item['availability']}")
        if not item["essays"] or not all(isinstance(n, int) and 1 <= n <= 25 for n in item["essays"]):
            raise ValueError(f"invalid essay list for {item['id']}")
        if item["availability"] == "available":
            essay_files = [
                path
                for number in item["essays"]
                for path in (ROOT / "chapters").glob(f"{number:02d}-*.html")
            ]
            found_numbers = {int(path.name[:2]) for path in essay_files}
            missing_essays = [number for number in item["essays"] if number not in found_numbers]
            if missing_essays:
                raise ValueError(
                    f"{item['id']} is marked available but has no essay file for {missing_essays}"
                )
            marker = f'data-proof-id="{item["id"]}"'
            marker_count = sum(
                path.read_text(encoding="utf-8").count(marker) for path in essay_files
            )
            if marker_count != 1:
                raise ValueError(
                    f"{item['id']} must appear exactly once in its essay ledger; found {marker_count}"
                )
    return items


def essay_refs(numbers: list[int]) -> str:
    refs = []
    for number in numbers:
        matches = sorted((ROOT / "chapters").glob(f"{number:02d}-*.html"))
        label = f"essay {number:02d}"
        if matches:
            target = matches[0].relative_to(ROOT).as_posix()
            refs.append(f'<a href="{target}">{label}</a>')
        else:
            refs.append(label)
    if len(refs) == 1:
        return refs[0]
    if len(refs) == 2:
        return " and ".join(refs)
    return ", ".join(refs[:-1]) + ", and " + refs[-1]


def render_items(items: list[dict]) -> list[str]:
    lines = ['      <ul class="scope-register">']
    for item in items:
        register = item["register"]
        label = REGISTER_LABELS[register]
        if item["availability"] == "planned":
            label = {
                "proved": "To prove",
                "stated": "To state",
                "outlined": "To outline",
                "conditional": "Conditional",
                "described": "To describe",
            }[register]
        text = html.escape(item["text"], quote=False)
        refs = essay_refs(item["essays"])
        lines.extend(
            [
                f'        <li data-proof-id="{item["id"]}">',
                f'          <span class="scope-mode scope-mode--{register}">{label}</span>',
                f"          {text} <span class=\"scope-essays\">({refs})</span>",
                "        </li>",
            ]
        )
    lines.append("      </ul>")
    return lines


def render_block(items: list[dict]) -> str:
    proved = [
        item
        for item in items
        if item["availability"] == "available" and item["register"] == "proved"
    ]
    qualified = [
        item
        for item in items
        if item["availability"] == "available" and item["register"] != "proved"
    ]
    planned = [item for item in items if item["availability"] == "planned"]

    lines = [
        START,
        "    <h3>Currently proved in full</h3>",
        '    <p class="scope-note">This list is generated from <code>data/ledger.json</code>. An item',
        "      appears here only when the register marks it as both available and proved.</p>",
        *render_items(proved),
        "",
        "    <h3>Present, but not proved in full</h3>",
        *render_items(qualified),
        "",
        "    <h3>Boundary for the unwritten essays</h3>",
        *render_items(planned),
        END,
    ]
    return "\n".join(lines)


def replace_block(source: str, block: str) -> str:
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(source):
        raise ValueError(f"{ABOUT} is missing the generated proof-register markers")
    return pattern.sub(lambda _match: block, source, count=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail if about.html is out of date")
    mode.add_argument("--write", action="store_true", help="update about.html in place")
    args = parser.parse_args()

    items = load_register()
    before = ABOUT.read_text(encoding="utf-8")
    after = replace_block(before, render_block(items))

    if args.write:
        if before != after:
            ABOUT.write_text(after, encoding="utf-8")
            print("updated about.html from data/ledger.json")
        else:
            print("about.html already up to date")
        return 0

    if before != after:
        print("about.html is out of date; run: python3 scripts/render_status.py --write")
        return 1
    print("proof register and about.html agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
