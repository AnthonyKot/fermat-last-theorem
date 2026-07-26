#!/usr/bin/env python3
"""Render every repeated site fact from its canonical source.

Serving the site still has no build step: generated HTML is committed. During
authoring, use --write after changing data/ledger.json. verify.sh uses --check
and fails when committed status, inventory, or navigation has drifted.
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
INDEX = ROOT / "index.html"
COUNT_START = "<!-- essay-count:start -->"
ABOUT_COUNT_START = "<!-- about-essay-count:start -->"
ABOUT_COUNT_END = "<!-- about-essay-count:end -->"
ASSUM_START = "<!-- assumption-count:start -->"
ASSUM_END = "<!-- assumption-count:end -->"
FINALE = ROOT / "chapters" / "25-ribet-and-the-end.html"
COUNT_END = "<!-- essay-count:end -->"
STAMP_START = "<!-- build-stamp:start -->"
STAMP_END = "<!-- build-stamp:end -->"
REPO = "https://github.com/AnthonyKot/fermat-last-theorem"


WORDS = {
    0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
    7: "Seven", 8: "Eight",
    9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
    15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen",
    20: "Twenty", 21: "Twenty-one", 22: "Twenty-two", 23: "Twenty-three",
    24: "Twenty-four", 25: "Twenty-five",
}


def essay_files() -> list[Path]:
    return sorted((ROOT / "chapters").glob("[0-9][0-9]-*.html"))


def essay_title(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    match = re.search(r"<h1>(.*?)</h1>", source, re.S)
    if not match:
        raise ValueError(f"{path.relative_to(ROOT)} has no h1")
    return re.sub(r"\s+", " ", match.group(1)).strip()


def joined_html(parts: list[str]) -> str:
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def written_links(prefix: str) -> str:
    return joined_html(
        [f'<a href="{prefix}{path.name}">{int(path.name[:2]):02d}</a>' for path in essay_files()]
    )


def owed_count(items: list[dict], policy: dict) -> int:
    accepted_ids = set(policy["accepted_assumption_ids"])
    return sum(
        item["role"] == "required_for_flt"
        and not closes_required_debt(item, accepted_ids)
        for item in items
    )


def write_essay_count() -> bool:
    """Generate the contents page's written-essay tally from the files on disk.

    This paragraph was hand-maintained, went stale for four consecutive essays,
    and shipped saying "Eight" when twelve existed. A count on a page is a
    promise to update it; generating it is the only way to keep the promise.
    """
    files = essay_files()
    nums = [int(f.name[:2]) for f in files]
    links = ", ".join(
        f'<a href="chapters/{f.name}">{n:02d}</a>' for f, n in zip(files[:-1], nums[:-1])
    )
    last = f'<a href="chapters/{files[-1].name}">{nums[-1]:02d}</a>'
    para = (
        f"    {COUNT_START}<p><strong>{WORDS[len(files)]} of the twenty-five essays are written</strong>"
        f" — {links} and {last} — and the remaining {25 - len(files)} are listed above as stubs."
        f"</p>{COUNT_END}"
    )
    text = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(COUNT_START) + r".*?" + re.escape(COUNT_END), re.S)
    if not pattern.search(text):
        raise ValueError("index.html is missing the essay-count markers")
    new = pattern.sub(lambda _m: para.strip(), text, count=1)
    if new != text:
        INDEX.write_text(new, encoding="utf-8")
        return True
    return False


def about_essay_count(items: list[dict], policy: dict) -> str:
    files = essay_files()
    written = {int(path.name[:2]) for path in files}
    missing = [n for n in range(1, 26) if n not in written]
    missing_text = joined_html([f"{n:02d}" for n in missing])
    debts = owed_count(items, policy)
    if missing:
        remaining = (
            f"The {WORDS[len(missing)].lower()} unwritten "
            f'essay{"" if len(missing) == 1 else "s"} '
            f'{"is" if len(missing) == 1 else "are"} {missing_text}.'
        )
    else:
        remaining = "No essays remain unwritten."
    return (
        f"{ABOUT_COUNT_START}<p><strong>{WORDS[len(files)]} of twenty-five essays are written:</strong> "
        f"{written_links('chapters/')}."
        f" {remaining}"
        f" The canonical proof register currently records {debts} required "
        f'item{"" if debts == 1 else "s"} still owed, so the chain does not yet close. '
        f'The <a href="index.html">contents page</a> gives the reading order and the contribution '
        f"of every written and planned essay.</p>{ABOUT_COUNT_END}"
    )


def write_about_essay_count(items: list[dict], policy: dict) -> bool:
    text = ABOUT.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(ABOUT_COUNT_START) + r".*?" + re.escape(ABOUT_COUNT_END), re.S
    )
    if not pattern.search(text):
        raise ValueError("about.html is missing the about-essay-count markers")
    new = pattern.sub(lambda _m: about_essay_count(items, policy), text, count=1)
    if new != text:
        ABOUT.write_text(new, encoding="utf-8")
        return True
    return False


def check_about_essay_count(items: list[dict], policy: dict) -> str:
    text = ABOUT.read_text(encoding="utf-8")
    expected = about_essay_count(items, policy)
    pattern = re.compile(
        re.escape(ABOUT_COUNT_START) + r".*?" + re.escape(ABOUT_COUNT_END), re.S
    )
    match = pattern.search(text)
    if not match:
        raise ValueError("about.html has no generated essay status; run --write")
    if match.group(0) != expected:
        raise ValueError("about.html's essay status has drifted; run --write")
    return f"{WORDS[len(essay_files())]} ({len(essay_files())})"


def write_assumption_count(policy: dict) -> bool:
    """Put the live root-assumption total into the closing essay's fence.

    Essay 25 briefly claimed its argument rested on three things "and nothing
    else", with a fourth listed in the table directly below it. A count in the
    closing essay is the claim most likely to rot, so it is generated.
    """
    n = len(policy["accepted_assumption_ids"])
    body = (f'{ASSUM_START}<strong>The finished proof would rest on {n} assumed results in total</strong>'
            f' — see <a href="../about.html">About</a> for the roster.{ASSUM_END}')
    text = FINALE.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(ASSUM_START) + r".*?" + re.escape(ASSUM_END), re.S)
    if not pattern.search(text):
        raise ValueError("essay 25 is missing the assumption-count markers")
    new = pattern.sub(lambda _m: body, text, count=1)
    if new != text:
        FINALE.write_text(new, encoding="utf-8")
        return True
    return False


def check_assumption_count(policy: dict) -> str:
    n = len(policy["accepted_assumption_ids"])
    text = FINALE.read_text(encoding="utf-8")
    m = re.search(re.escape(ASSUM_START) + r"<strong>The finished proof would rest on (\d+) assumed", text)
    if not m:
        raise ValueError("essay 25 has no generated assumption count; run --write")
    if int(m.group(1)) != n:
        raise ValueError(f"essay 25 says {m.group(1)} assumed results; the register has {n}")
    return f"{n} in essay 25"


def check_essay_count() -> str:
    """The generated tally must match the files on disk."""
    files = essay_files()
    text = INDEX.read_text(encoding="utf-8")
    m = re.search(
        re.escape(COUNT_START) + r"<p><strong>([A-Za-z-]+) of the twenty-five essays are written",
        text,
    )
    if not m:
        raise ValueError("index.html has no generated essay count; run --write")
    if m.group(1) != WORDS[len(files)]:
        raise ValueError(
            f"index.html says {m.group(1)} essays are written; {len(files)} files on disk"
        )
    linked = set(re.findall(r'href="chapters/(\d\d)-', text))
    if linked != {f.name[:2] for f in files}:
        raise ValueError("index.html's essay links do not match the files on disk")
    return f"{m.group(1)} ({len(files)})"


def public_pages() -> list[Path]:
    return sorted(ROOT.glob("*.html")) + essay_files()


def git(*args: str) -> str:
    import subprocess

    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def deployment_footer() -> str:
    """A stable footer with no guessed deployment revision.

    A commit cannot contain its own hash. The old footer therefore named the
    parent while calling it the build revision, which was structurally capable
    of being stale. Exact deployment identity now belongs to check_live.py,
    which compares the served artifact with this checkout byte for byte.
    """
    return (
        f'{STAMP_START}<p class="build-stamp">'
        f'<a href="{REPO}">Source</a> · '
        f'<a href="{REPO}/deployments">deployment history</a>'
        f"</p>{STAMP_END}"
    )


def write_deployment_footers() -> int:
    footer = deployment_footer()
    pattern = re.compile(re.escape(STAMP_START) + r".*?" + re.escape(STAMP_END), re.S)
    changed = 0
    for path in public_pages():
        text = path.read_text(encoding="utf-8")
        if STAMP_START not in text:
            raise ValueError(f"{path} has no build-stamp markers")
        new = pattern.sub(lambda _m: footer, text, count=1)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def check_deployment_footers() -> str:
    """Every page carries the stable source/deployment links."""
    expected = deployment_footer()
    for path in public_pages():
        text = path.read_text(encoding="utf-8")
        if text.count(STAMP_START) != 1 or text.count(STAMP_END) != 1:
            raise ValueError(
                f"{path.relative_to(ROOT)} must carry exactly one deployment footer"
            )
        pattern = re.compile(re.escape(STAMP_START) + r".*?" + re.escape(STAMP_END), re.S)
        if pattern.search(text).group(0) != expected:
            raise ValueError(
                f"{path.relative_to(ROOT)} has a stale deployment footer; run --write"
            )
    return f"{len(public_pages())} page(s)"


def chapter_nav(index: int, files: list[Path]) -> str:
    previous = files[index - 1] if index else None
    following = files[index + 1] if index + 1 < len(files) else None
    if previous is None:
        left = '<a href="../index.html"><span class="dir">←</span> Contents</a>'
    else:
        left = (
            f'<a href="{previous.name}"><span class="dir">← Previous written essay</span> '
            f'{int(previous.name[:2]):02d} · {essay_title(previous)}</a>'
        )
    if following is None:
        right = '<a class="next" href="../index.html"><span class="dir">Contents →</span></a>'
    else:
        right = (
            f'<a class="next" href="{following.name}"><span class="dir">Next written essay →</span> '
            f'{int(following.name[:2]):02d} · {essay_title(following)}</a>'
        )
    return f'<nav class="chapter-nav">\n      {left}\n      {right}\n    </nav>'


def write_navigation() -> int:
    files = essay_files()
    pattern = re.compile(r'<nav class="chapter-nav">.*?</nav>', re.S)
    changed = 0
    for index, path in enumerate(files):
        text = path.read_text(encoding="utf-8")
        found = pattern.findall(text)
        if len(found) != 1:
            raise ValueError(
                f"{path.relative_to(ROOT)} must carry exactly one chapter navigation block"
            )
        new = pattern.sub(lambda _m: chapter_nav(index, files), text, count=1)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def check_navigation() -> str:
    files = essay_files()
    pattern = re.compile(r'<nav class="chapter-nav">.*?</nav>', re.S)
    for index, path in enumerate(files):
        text = path.read_text(encoding="utf-8")
        found = pattern.findall(text)
        if len(found) != 1 or found[0] != chapter_nav(index, files):
            raise ValueError(
                f"{path.relative_to(ROOT)} has stale prev/next navigation; run --write"
            )
    return f"{len(files)} written essays"

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
    revisions = raw.get("register_revisions", [])
    if not isinstance(revisions, list):
        raise ValueError("register_revisions must be a list")
    for rev in revisions:
        missing = {"commit", "date", "owed", "assumptions", "note"} - rev.keys()
        if missing:
            raise ValueError(f"register_revisions entry missing {sorted(missing)}")
        for field in ("owed", "assumptions"):
            if not (isinstance(rev[field], list) and len(rev[field]) == 2):
                raise ValueError(f"{rev['commit']}: {field} must be [before, after]")
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
        # Every assumption must be publishable by name, not merely counted: a
        # reader who sees the roster can argue with the classification, while a
        # reader who sees only a number can do nothing but trust it.
        if item["register"] == "stated" and not item.get("short"):
            raise ValueError(f"{item['id']} is a stated record and needs a 'short' label for the roster")
        # A third state: proved, but conditional on an assumption made elsewhere.
        # Without this, such a record has to masquerade as an assumption, which
        # double-counts the roster and puts two entries under one root import.
        if "depends_on" in item:
            if item["register"] != "proved":
                raise ValueError(f"{item['id']}: depends_on is only for proved records")
            if not item["depends_on"]:
                raise ValueError(f"{item['id']}: depends_on must be non-empty")
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

    for item in items:
        for dep in item.get("depends_on", []):
            if dep not in ids:
                raise ValueError(f"{item['id']} depends on unknown record {dep}")
            upstream = next(x for x in items if x["id"] == dep)
            if upstream["register"] != "stated":
                raise ValueError(f"{item['id']} depends on {dep}, which is not an assumption")
            # the root import must carry at least the role of everything hanging off it
            if item["role"] == "required_for_flt" and upstream["role"] != "required_for_flt":
                raise ValueError(
                    f"{item['id']} is on the FLT chain but depends on {dep}, which is only background"
                )

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

    # The check above runs register -> page. Without the reverse direction a record
    # that is deleted from the register leaves its ledger entry standing on the page,
    # still telling readers something is assumed after it stopped being assumed --
    # which is how essay 25 went on claiming FLT for n = 5 and n = 7 as an import
    # for three commits after essay 24 closed that threshold.
    for path in sorted((ROOT / "chapters").glob("*.html")):
        for orphan in re.findall(r'data-proof-id="([^"]+)"', path.read_text(encoding="utf-8")):
            if orphan not in ids:
                raise ValueError(
                    f"{path.name} carries a ledger item for {orphan}, "
                    "which is not in the register"
                )
    return items, policy, revisions


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


def dep_note(item: dict, items: list[dict]) -> str:
    """Name the upstream assumption a conditional proof rests on."""
    deps = item.get("depends_on")
    if not deps:
        return ""
    by_id = {x["id"]: x for x in items}
    names = ", ".join(
        html.escape(by_id[d].get("short", d), quote=False) for d in deps
    )
    return f' <span class="scope-dep">conditional on: {names}</span>'


def render_items(items: list[dict], allitems: list[dict] | None = None) -> list[str]:
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
                f'{ROLE_LABELS[item["role"]]}</span>'
                + (dep_note(item, allitems) if allitems else ""),
                f"          {text} <span class=\"scope-essays\">({refs})</span>",
                "       </li>",
            ]
        )
    lines.append("      </ul>")
    return lines


def counts_at(sha: str) -> tuple[int, int] | None:
    """(owed, accepted) computed from data/ledger.json as it stood at a commit."""
    try:
        blob = git("show", f"{sha}:data/ledger.json")
    except Exception:  # noqa: BLE001
        return None
    try:
        raw = json.loads(blob)
    except json.JSONDecodeError:
        return None
    items = raw.get("proof_register") or []
    accepted = set(raw.get("completion_policy", {}).get("accepted_assumption_ids") or [])
    owed = sum(
        1
        for i in items
        if i.get("role") == "required_for_flt" and not closes_required_debt(i, accepted)
    )
    return owed, len(accepted)


def trajectory(upto: str = "HEAD") -> list[str]:
    """Every commit where either counter moved, oldest first.

    The counts have moved for three different reasons -- essays landing, a
    re-granulation of the register, and assumptions being narrowed or discharged --
    and reading them one snapshot at a time made ordinary movement look like
    error. Computed from git rather than recorded by hand, so it cannot drift.
    """
    shas = git("log", upto, "--format=%h", "--", "data/ledger.json").split()
    rows, prev = [], None
    for sha in reversed(shas):
        got = counts_at(sha)
        if got is None or got == prev:
            continue
        subject = git("log", "-1", "--format=%s", sha)
        rows.append((sha, got, subject))
        prev = got
    if not rows:
        return []
    lines = ['      <details class="scope-revisions">',
             "        <summary>How the two counts have moved</summary>",
             '        <table><thead><tr><th>commit</th><th>owed</th><th>assumed</th>'
             "<th>what changed</th></tr></thead><tbody>"]
    for sha, (owed, acc), subject in rows:
        lines.append(
            f'          <tr><td><a href="{REPO}/commit/{sha}"><code>{sha}</code></a></td>'
            f"<td>{owed}</td><td>{acc}</td>"
            f"<td>{html.escape(subject[:72], quote=False)}</td></tr>"
        )
    lines += ["        </tbody></table>",
              '        <p class="scope-note">Computed from the register at each commit, not recorded by'
              " hand. Owed falls as essays land and rises when the register is made finer; assumed rises"
              " when an essay names a new import and falls when one is discharged or narrowed.</p>",
              "      </details>"]
    return lines


def render_revisions(revisions: list[dict]) -> list[str]:
    """Log every change to what the counters count, so the series stays readable."""
    if not revisions:
        return []
    lines = ['      <details class="scope-revisions">',
             "        <summary>How these numbers have been counted</summary>",
             '        <ul>']
    for rev in revisions:
        ob, oa = rev["owed"]
        ab, aa = rev["assumptions"]
        moved = []
        if ob != oa:
            moved.append(f"owed {ob}&nbsp;&rarr;&nbsp;{oa}")
        if ab != aa:
            moved.append(f"assumed {ab}&nbsp;&rarr;&nbsp;{aa}")
        shift = "; ".join(moved) or "counts unchanged"
        lines.append(
            f'          <li><a href="{REPO}/commit/{rev["commit"]}"><code>{rev["commit"]}</code></a>'
            f' · {rev["date"]} · <strong>{shift}</strong><br>'
            f'{html.escape(rev["note"], quote=False)}</li>'
        )
    lines += ["        </ul>", "      </details>"]
    return lines


def render_roster(items: list[dict]) -> list[str]:
    """Name every assumption in a count, so the classification can be argued with."""
    lines = ['      <ul class="scope-roster">']
    for item in items:
        pending = "" if item["availability"] == "available" else ' <span class="roster-planned">not yet written</span>'
        lines.append(
            f'        <li>{html.escape(item["short"], quote=False)}'
            f' <span class="scope-essays">({essay_refs(item["essays"])})</span>{pending}</li>'
        )
    lines.append("      </ul>")
    return lines


def render_block(items: list[dict], policy: dict, revisions: list[dict], upto: str = "HEAD") -> str:  # noqa: C901
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

    # Two separate headline counts. "What the finished proof rests on" and "what
    # the exposition rests on" are different claims: the Hasse bound or the
    # existence of Q_ell do not weaken "FLT follows from modularity", while
    # Mazur's isogeny theorem does. A single undifferentiated count buries that.
    chain_assumed = [i for i in items if i["role"] == "required_for_flt" and i["register"] == "stated"]
    bg_assumed = [i for i in items if i["role"] == "background" and i["register"] == "stated"]
    n_owed_chain = len(owed)

    lines = [
        START,
        '    <div class="scope-counts">',
        '      <p class="scope-headline">The finished proof would rest on '
        f'<strong>{len(chain_assumed)}</strong> assumed result'
        f'{"" if len(chain_assumed) == 1 else "s"}.</p>',
        '      <p class="scope-note">These are the results the FLT chain consumes and does not prove. '
        "Each is named in the completion policy, which the validator pins to this register, so "
        "adding one is a deliberate edit rather than a side effect. This is the only number against "
        "which the phrase <em>a derivation of Fermat's Last Theorem from named assumptions</em> is "
        "defensible.</p>",
        *render_roster(chain_assumed),
        '      <p class="scope-headline">The exposition additionally assumes '
        f'<strong>{len(bg_assumed)}</strong> background result'
        f'{"" if len(bg_assumed) == 1 else "s"}.</p>',
        '      <p class="scope-note">Stated for orientation, and deliberately kept off the chain.'
        " Doubting any of them leaves the closing argument intact.</p>",
        *render_roster(bg_assumed),
        '      <p class="scope-note">Both rosters come from one <code>role</code> field per record, so'
        " re-classifying an assumption is a one-word edit and the validator immediately re-pins the"
        " completion policy to match. Three of the calls above are judgements rather than obvious facts,"
        " and are the ones worth disagreeing with: <em>associativity</em> is on the chain because the"
        " group law is what defines torsion and reduction, <em>complex uniformization</em> is off it"
        " because nothing in the closing argument evaluates a lattice, and the <em>discriminant"
        " criterion</em> is on it because essay 08 reads bad reduction straight off"
        " $\\Delta_{\\min}$. Essays 09 and 23 may move any of the three.</p>",
        '      <p class="scope-note">Every figure above counts <strong>records in '
        "<code>data/ledger.json</code></strong>, one per claim, at whatever granularity the register "
        "currently uses. That granularity has changed, so counts from different dates are not "
        "comparable; each change is logged below rather than applied silently.</p>",
        *render_revisions(revisions),
        *trajectory(upto),
        '      <p class="scope-note"><strong>Not yet settled:</strong> '
        f'{n_owed_chain} required item{"" if n_owed_chain == 1 else "s"} remain'
        f'{"s" if n_owed_chain == 1 else ""} owed, listed below. Until that list is empty the'
        " collection is an argument in progress, not a completed derivation.</p>",
        "   </div>",
        "",
        "   <h3>Proved in the written essays</h3>",
        '    <p class="scope-note">This list is generated from <code>data/ledger.json</code>. An item',
        "     appears here only when it is both available and marked proved.</p>",
        *render_items(proved, items),
        "",
        "   <h3>Explicitly assumed, not proved here</h3>",
        '    <p class="scope-note">These available inputs are named in the completion policy. They',
        "     close a dependency without being presented as proofs.</p>",
        *render_items(imported),
        "",
        "   <h3>Still owed by the FLT chain</h3>",
        '    <p class="scope-note">An item remains here while its essay is unwritten, its treatment is',
        "     only outlined or conditional, or it has not yet reached its declared imported state.</p>",
        *render_items(owed),
        "",
        "   <h3>Background outside the closing debt</h3>",
        '    <p class="scope-note">These claims support orientation or historical context. Their proof',
        "     status remains visible, but they do not determine whether the FLT chain closes.</p>",
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

    items, policy, revisions = load_register()
    before = ABOUT.read_text(encoding="utf-8")
    after = replace_block(before, render_block(items, policy, revisions))

    if args.write:
        if before != after:
            ABOUT.write_text(after, encoding="utf-8")
            print("updated about.html from data/ledger.json")
        else:
            print("about.html already up to date")
        if write_essay_count():
            print("updated index.html's essay count")
        if write_about_essay_count(items, policy):
            print("updated about.html's essay count")
        if write_assumption_count(policy):
            print("updated essay 25's assumption count")
        navigated = write_navigation()
        print(
            f"navigation regenerated on {navigated} page(s)"
            if navigated
            else "chapter navigation already current"
        )
        footers = write_deployment_footers()
        print(
            f"deployment footer regenerated on {footers} page(s)"
            if footers
            else "deployment footers already current"
        )
        return 0

    if before != after:
        # The trajectory is computed from git history, so a commit that contains
        # a data/ledger.json change cannot also contain a row naming its own hash.
        # Accept the render as of HEAD's parent; the next authoring render adds
        # that historical row.
        try:
            lagged = replace_block(before, render_block(items, policy, revisions, upto="HEAD^"))
        except Exception:  # noqa: BLE001
            lagged = None
        if lagged is None or before != lagged:
            print("about.html is out of date; run: python3 scripts/render_status.py --write")
            return 1
        print("about.html trails HEAD by one trajectory row, which is expected after a ledger commit")
    try:
        counted = check_essay_count()
    except ValueError as exc:
        print(f"essay count: {exc}")
        return 1
    print(f"contents-page essay count agrees with the files on disk: {counted}")
    try:
        about_counted = check_about_essay_count(items, policy)
    except ValueError as exc:
        print(f"About essay count: {exc}")
        return 1
    print(f"About essay count agrees with the files and register: {about_counted}")
    try:
        assumed = check_assumption_count(policy)
    except ValueError as exc:
        print(f"assumption count: {exc}")
        return 1
    print(f"closing essay's assumption total agrees with the register: {assumed}")
    try:
        navigation = check_navigation()
    except ValueError as exc:
        print(f"chapter navigation: {exc}")
        return 1
    print(f"chapter navigation is generated and current: {navigation}")
    try:
        footers = check_deployment_footers()
    except ValueError as exc:
        print(f"deployment footer: {exc}")
        return 1
    print(f"deployment footer contains no mutable revision: {footers}")
    accepted_ids = set(policy["accepted_assumption_ids"])
    outstanding = sum(
        item["role"] == "required_for_flt"
        and not closes_required_debt(item, accepted_ids)
        for item in items
    )
    print(
        "proof register and about.html agree; "
        f"{outstanding} required item(s) still owed; "
        f"{len(accepted_ids)} accepted assumption record(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
