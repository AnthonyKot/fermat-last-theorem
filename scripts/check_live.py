#!/usr/bin/env python3
"""Assert the PUBLISHED site matches this checkout and its canonical register.

The local verifier proves that generated HTML agrees with data/ledger.json.
This checker closes the other half: it fetches github.io with cache-busting and
compares every served page and the served register with this checkout byte for
byte. A local-only change, an unpushed commit, a failed Pages build, a stale CDN
response, and a partial deploy therefore all fail for the same concrete reason:
the published artifact differs.

What it asserts, per page:
  * HTTP 200;
  * the response body equals the corresponding committed source;
  * the HTML parses with no tag outside the known set, catching math or entities
    that leaked into markup on the way through the CDN.
The full run also fetches data/ledger.json and requires it to equal the local
canonical register, so a completion report cannot silently mix local status with
an older public site.

Usage:
    python3 scripts/check_live.py             # all pages + canonical register
    python3 scripts/check_live.py 24 25       # just those essays
    python3 scripts/check_live.py --expect 25 "Two assumptions"
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://anthonykot.github.io/fermat-last-theorem"
KNOWN = {
    "meta", "title", "link", "script", "header", "div", "a", "nav", "button", "main", "p",
    "h1", "h2", "h3", "span", "section", "ul", "ol", "li", "em", "strong", "table", "thead",
    "tbody", "tr", "th", "td", "br", "footer", "code", "hr", "sup", "sub", "abbr", "figure",
    "figcaption", "blockquote", "b", "i", "details", "summary",
}


class TagCheck(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.bogus: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag not in KNOWN:
            self.bogus.append(tag)


def fetch(path: str, tries: int = 3) -> str:
    url = f"{BASE}/{path}?cb={int(time.time()*1000)}"
    last: Exception | None = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status != 200:
                    raise RuntimeError(f"HTTP {r.status}")
                return r.read().decode("utf-8")
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{path}: {last}")


def paths(selection: list[str]) -> list[str]:
    chapters = sorted(p.name for p in (ROOT / "chapters").glob("*.html"))
    if selection:
        wanted = set(selection)
        chapters = [c for c in chapters if c[:2] in wanted]
        return [f"chapters/{c}" for c in chapters]
    return [
        "index.html",
        "about.html",
        "data/ledger.json",
        *[f"chapters/{c}" for c in chapters],
    ]


def short_diff(path: str, expected: str, actual: str) -> list[str]:
    diff = difflib.unified_diff(
        expected.splitlines(),
        actual.splitlines(),
        fromfile=f"checkout/{path}",
        tofile=f"published/{path}",
        lineterm="",
        n=2,
    )
    lines = list(diff)
    if len(lines) > 18:
        return lines[:18] + [f"... {len(lines) - 18} more diff line(s)"]
    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("essays", nargs="*", help="two-digit essay numbers; default is every page")
    ap.add_argument("--expect", nargs=2, action="append", metavar=("PAGE", "TEXT"),
                    help='assert TEXT appears in a page ("index", "about" or an essay number)')
    args = ap.parse_args()

    problems = 0
    fetched: dict[str, str] = {}
    for path in paths(args.essays):
        try:
            body = fetch(path)
        except RuntimeError as exc:
            print(f"  FAIL {path}: {exc}")
            problems += 1
            continue
        fetched[path] = body
        expected = (ROOT / path).read_text(encoding="utf-8")
        flags = []
        if body != expected:
            flags.append("published bytes differ from this checkout")
        if path.endswith(".html"):
            checker = TagCheck()
            checker.feed(body)
            if checker.bogus:
                flags.append(f"bogus tags {sorted(set(checker.bogus))}")
        if flags:
            problems += 1
            print(f"  FAIL {path}: " + "; ".join(flags))
            if body != expected:
                for line in short_diff(path, expected, body):
                    print(f"       {line}")
        else:
            print(f"  ok   {path}")

    for page, text in args.expect or []:
        path = {"index": "index.html", "about": "about.html"}.get(page)
        if path is None:
            match = sorted((ROOT / "chapters").glob(f"{page}-*.html"))
            if not match:
                print(f"  FAIL --expect {page}: no such essay")
                problems += 1
                continue
            path = f"chapters/{match[0].name}"
        body = fetched.get(path)
        if body is None:
            body = fetch(path)
        if text in body:
            print(f'  ok   {path} contains "{text[:50]}"')
        else:
            print(f'  FAIL {path} does NOT contain "{text[:50]}"')
            problems += 1

    print("LIVE: PASS" if not problems else f"LIVE: FAIL ({problems} problem(s))")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
