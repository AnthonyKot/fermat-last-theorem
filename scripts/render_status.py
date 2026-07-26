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
    "stated": "Assumed",
    "outlined": "Outlined",
    "conditional": "Conditional",
    "described": "Described",
}

PLANNED_LABELS = {
    "proved": "To prove",
    "stated": "To assume",
    "outlined": "To complete",
    "conditional": "Conditional",
    "described": "To describe",
}

CHAPTER_MODE_LABELS = {
    "proved": "Proved",
    "stated": "Assumed",
    "outlined": "Outlined",
    "conditional": "Conditional",
    "described": "Described",
}

ROLE_LABELS = {
    "required_for_flt": "FLT chain",
    "background": "Background",
}


def closes_required_debt(item: dict, accepted_ids: set[str]) -> bool:
    if item["availability"] != "available":
        return False
    return item["register"] == "proved" or item["id"] in accepted_ids


def load_register() -> tuple[list[dict], dict]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    items = raw.get("proof_register")
    if not isinstance(items, list):
        raise ValueError("data/ledger.json must contain a proof_register list")
    policy = raw.get("completion_policy")
    if not isinstance(policy, dict):
        raise ValueError("data/ledger.json must contain a completion_policy object")
    if policy.get("required_role") != "required_for_flt":
        raise ValueError("completion_policy.required_role must be required_for_flt")
    accepted = policy.get("accepted_assumption_ids")
    if (
        not isinstance(accepted, list)
        or not all(isinstance(item_id, str) for item_id in accepted)
        or len(accepted) != len(set(accepted))
    ):
        raise ValueError("completion_policy.accepted_assumption_ids must be a unique string list")

    ids: set[str] = set()
    for item in items:
        missing = {"id", "register", "availability", "role", "essays", "text"} - item.keys()
        if missing:
            raise ValueError(f"proof-register item is missing {sorted(missing)}: {item}")
        if item["id"] in ids:
            raise ValueError(f"duplicate proof-register id: {item['id']}")
        ids.add(item["id"])
        if item["register"] not in REGISTER_LABELS:
            raise ValueError(f"unknown register for {item['id']}: {item['register']}")
        if item["availability"] not in {"available", "planned"}:
            raise ValueError(f"unknown availability for {item['id']}: {item['availability']}")
        if item["role"] not in ROLE_LABELS:
            raise ValueError(f"unknown role for {item['id']}: {item['role']}")
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
            marker_sources = []
            for path in essay_files:
                source = path.read_text(encoding="utf-8")
                if marker in source:
                    marker_sources.append((path, source))
            marker_count = sum(source.count(marker) for _path, source in marker_sources)
            if marker_count != 1:
                raise ValueError(
                    f"{item['id']} must appear exactly once in its essay ledger; found {marker_count}"
                )
            source = marker_sources[0][1]
            ledger = source.split('<section class="ledger">', 1)[1].split("</section>", 1)[0]
            marker_position = ledger.index(marker)
            columns = re.findall(r'<div class="col ([^"]+)">', ledger[:marker_position])
            if not columns:
                raise ValueError(f"{item['id']} is not inside a ledger column")
            expected_column = {
                "proved": "proved-here",
                "stated": "assumed-here",
                "outlined": "owed",
                "conditional": "owed",
                "described": "owed",
            }[item["register"]]
            if expected_column not in columns[-1].split():
                raise ValueError(
                    f"{item['id']} belongs in {expected_column}, not {columns[-1]}"
                )
            item_match = re.search(
                rf'<li\b[^>]*{re.escape(marker)}[^>]*>.*?</li>',
                ledger,
                re.S,
            )
            if item_match is None:
                raise ValueError(f"cannot parse the ledger item for {item['id']}")
            expected_mode = (
                f'<span class="ledger-mode ledger-mode--{item["register"]}">'
                f'{CHAPTER_MODE_LABELS[item["register"]]}</span>'
            )
            expected_role = (
                f'<span class="ledger-role ledger-role--{item["role"]}">'
                f'{ROLE_LABELS[item["role"]]}</span>'
            )
            if expected_mode not in item_match.group(0):
                raise ValueError(f"{item['id']} is missing its canonical proof-mode badge")
            if expected_role not in item_match.group(0):
                raise ValueError(f"{item['id']} is missing its canonical role badge")

    unknown_accepted = set(accepted) - ids
    if unknown_accepted:
        raise ValueError(f"completion policy names unknown items: {sorted(unknown_accepted)}")
    required_stated = {
        item["id"]
        for item in items
        if item["role"] == "required_for_flt" and item["register"] == "stated"
    }
    if set(accepted) != required_stated:
        missing = sorted(required_stated - set(accepted))
        extra = sorted(set(accepted) - required_stated)
        raise ValueError(
            "accepted assumptions must equal the required stated records; "
            f"missing={missing}, extra={extra}"
        )
    return items, policy


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
            label = PLANNED_LABELS[register]
        text = html.escape(item["text"], quote=False)
        refs = essay_refs(item["essays"])
        lines.extend(
            [
                f'        <li data-proof-id="{item["id"]}">',
                f'          <span class="scope-mode scope-mode--{register}">{label}</span>',
                f'          <span class="scope-role scope-role--{item["role"]}">'
                f'{ROLE_LABELS[item["role"]]}</span>',
                f"          {text} <span class=\"scope-essays\">({refs})</span>",
                "        </li>",
            ]
        )
    lines.append("      </ul>")
    return lines


def render_block(items: list[dict], policy: dict) -> str:
    accepted_ids = set(policy["accepted_assumption_ids"])
    proved = [
        item
        for item in items
        if item["availability"] == "available" and item["register"] == "proved"
    ]
    imported = [
        item
        for item in items
        if item["availability"] == "available" and item["id"] in accepted_ids
    ]
    owed = [
        item
        for item in items
        if item["role"] == "required_for_flt"
        and not closes_required_debt(item, accepted_ids)
    ]
    background = [
        item
        for item in items
        if item["role"] == "background"
        and not (item["availability"] == "available" and item["register"] == "proved")
    ]

    lines = [
        START,
        "    <h3>Proved in the written essays</h3>",
        '    <p class="scope-note">This list is generated from <code>data/ledger.json</code>. An item',
        "      appears here only when it is both available and marked proved.</p>",
        *render_items(proved),
        "",
        "    <h3>Explicitly assumed, not proved here</h3>",
        '    <p class="scope-note">These available inputs are named in the completion policy. They',
        "      close a dependency without being presented as proofs.</p>",
        *render_items(imported),
        "",
        "    <h3>Still owed by the FLT chain</h3>",
        '    <p class="scope-note">An item remains here while its essay is unwritten, its treatment is',
        "      only outlined or conditional, or it has not yet reached its declared imported state.</p>",
        *render_items(owed),
        "",
        "    <h3>Background outside the closing debt</h3>",
        '    <p class="scope-note">These claims support orientation or historical context. Their proof',
        "      status remains visible, but they do not determine whether the FLT chain closes.</p>",
        *render_items(background),
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

    items, policy = load_register()
    before = ABOUT.read_text(encoding="utf-8")
    after = replace_block(before, render_block(items, policy))

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
    accepted_ids = set(policy["accepted_assumption_ids"])
    owed_count = sum(
        item["role"] == "required_for_flt"
        and not closes_required_debt(item, accepted_ids)
        for item in items
    )
    print(
        "proof register and about.html agree; "
        f"{owed_count} required item(s) still owed; "
        f"{len(accepted_ids)} accepted assumption record(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
