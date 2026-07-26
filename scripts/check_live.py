#!/usr/bin/env python3
"""Assert the PUBLISHED site matches this checkout. Reads no local HTML.

Every previous live check in this project was a hand-rolled curl pipeline, and
every one of them got disputed. The failure mode is real: a check that reads the
filesystem keeps passing while the site keeps not changing. So this fetches the
github.io URLs and nothing else.

What it asserts, per page:
  * HTTP 200;
  * the served build stamp names HEAD or HEAD's parent. It cannot be HEAD alone:
    committing the stamp changes the hash, so the generator records HEAD at
    generation time, which becomes the parent once committed. Anything older
    means the deploy has not caught up or the generator was not re-run;
  * every page serves the SAME stamp, so a partial deploy is visible;
  * the HTML parses with no tag outside the known set, catching math or entities
    that leaked into markup on the way through the CDN.

Usage:
    python3 scripts/check_live.py            # all pages
    python3 scripts/check_live.py 24 25      # just those essays
    python3 scripts/check_live.py --expect 25 "Two assumptions"
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://anthonykot.github.io/fermat-last-theorem"
STAMP = re.compile(r'Built from <a href="[^"]+/commit/([0-9a-f]+)"><code>\1</code></a> · ([^<·]+) ·')
KNOWN = {
    "meta", "title", "link", "script", "header", "div", "a", "nav", "button", "main", "p",
    "h1", "h2", "h3", "span", "section", "ul", "ol", "li", "em", "strong", "table", "thead",
    "tbody", "tr", "th", "td", "br", "footer", "code", "hr", "sup", "sub", "abbr", "figure",
    "figcaption", "blockquote", "b", "i", "details", "summary",
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


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


def pages(selection: list[str]) -> list[str]:
    chapters = sorted(p.name for p in (ROOT / "chapters").glob("*.html"))
    if selection:
        wanted = set(selection)
        chapters = [c for c in chapters if c[:2] in wanted]
        return [f"chapters/{c}" for c in chapters]
    return ["index.html", "about.html"] + [f"chapters/{c}" for c in chapters]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("essays", nargs="*", help="two-digit essay numbers; default is every page")
    ap.add_argument("--expect", nargs=2, action="append", metavar=("PAGE", "TEXT"),
                    help='assert TEXT appears in a page ("index", "about" or an essay number)')
    args = ap.parse_args()

    head, parent = git("rev-parse", "--short", "HEAD"), git("rev-parse", "--short", "HEAD^")
    allowed = {head, parent}
    print(f"HEAD {head}, parent {parent} — a served stamp must be one of these")

    stamps: dict[str, str] = {}
    problems = 0
    for path in pages(args.essays):
        try:
            body = fetch(path)
        except RuntimeError as exc:
            print(f"  FAIL {path}: {exc}")
            problems += 1
            continue
        m = STAMP.search(body)
        if not m:
            print(f"  FAIL {path}: no build stamp served")
            problems += 1
            continue
        sha, when = m.group(1), m.group(2).strip()
        stamps[path] = sha
        checker = TagCheck()
        checker.feed(body)
        flags = []
        if sha not in allowed:
            flags.append(f"stamp {sha} is neither HEAD nor its parent — deploy is behind")
        if checker.bogus:
            flags.append(f"bogus tags {sorted(set(checker.bogus))}")
        if flags:
            problems += len(flags)
            print(f"  FAIL {path}: " + "; ".join(flags))
        else:
            print(f"  ok   {path}  {sha} · {when}")

    if len(set(stamps.values())) > 1:
        print(f"  FAIL stamps disagree across pages: {sorted(set(stamps.values()))}")
        problems += 1

    for page, text in args.expect or []:
        path = {"index": "index.html", "about": "about.html"}.get(page)
        if path is None:
            match = sorted((ROOT / "chapters").glob(f"{page}-*.html"))
            if not match:
                print(f"  FAIL --expect {page}: no such essay")
                problems += 1
                continue
            path = f"chapters/{match[0].name}"
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
