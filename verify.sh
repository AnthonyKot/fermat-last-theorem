#!/usr/bin/env bash
# No Such Form — standing verification. Run from anywhere: ./verify.sh
#
# Ports the checks from The Bridge (count sync, links, math delimiters, prev/next
# contiguity, quotation scan, no tracked PDFs) and adds the four this book needs,
# because it has no owned source texts to check pointers against:
#   * every written essay carries a ledger and no essay uses a result too early
#   * the generated public proof status matches the canonical ledger data
#   * no Tier C textbook section numbers anywhere
#   * every Tier A citation is logged in SOURCES.md
#   * no long n-grams shared with the reference transcript
# Counts are COMPUTED, never typed. Exits non-zero on any hard failure.
set -u
cd "$(dirname "$0")"
fail=0

echo "== count sync (computed, not typed) =="
files=$(ls chapters/*.html 2>/dev/null | wc -l | tr -d ' ')
links=$(grep -oE 'href="chapters/[0-9][^"]*\.html"' index.html | sort -u | wc -l | tr -d ' ')
echo "  $files essay files on disk; $links distinct essay links on the contents page"
if [ "$files" != "$links" ]; then echo "  FAIL: contents page ($links) != essay files ($files)"; fail=1; fi

echo "== HTML well-formed: no math leaking into the tag parser =="
# A raw "<" inside math is swallowed by the HTML tokenizer as a tag name, which
# silently destroys the rest of the sentence. Source review does not catch it;
# only parsing does. Two spans in essay 04 were lost this way. Two guards:
# normalise every angle bracket in math to \lt / \gt, and parse for bogus tags.
python3 - <<'PY' || fail=1
import glob, re, sys
from html.parser import HTMLParser
KNOWN = {"meta","title","link","script","header","div","a","nav","button","main","p","h1","h2","h3",
         "span","section","ul","ol","li","em","strong","table","thead","tbody","tr","th","td","br",
         "footer","code","hr","sup","sub","abbr","figure","figcaption","blockquote","b","i",
         "details","summary"}
MATH = re.compile(r'\$\$(.+?)\$\$|(?<!\$)\$([^$\n]+?)\$(?!\$)', re.S)
bad = 0
for f in sorted(glob.glob("*.html") + glob.glob("chapters/*.html")):
    t = open(f).read()
    if not t.lstrip().lower().startswith("<!doctype html>"):
        print(f"  MISSING DOCTYPE in {f}: KaTeX refuses to render in quirks mode")
        bad += 1
    for m in MATH.finditer(t):
        body = m.group(1) or m.group(2)
        if "<" in body or ">" in body:
            line = t[: m.start()].count("\n") + 1
            print(f"  RAW ANGLE BRACKET in math {f}:{line}: use \\lt or \\gt -> ${body.strip()[:50]}$")
            bad += 1
    class P(HTMLParser):
        def handle_starttag(s, tag, attrs):
            if tag not in KNOWN:
                print(f"  BOGUS TAG <{tag}> in {f}:{s.getpos()[0]} (math or entity leaked into markup)")
                globals().__setitem__("bad", globals()["bad"] + 1)
    P().feed(t)
print("  OK" if not bad else f"  {bad} problem(s)")
sys.exit(1 if bad else 0)
PY

echo "== links resolve + math delimiters balance =="
python3 - <<'PY' || fail=1
import re, os, glob, sys
bad = 0
for f in glob.glob("*.html") + glob.glob("chapters/*.html"):
    base = os.path.dirname(f); t = open(f).read()
    dd = t.count("$$"); s = t.count("$") - 2 * dd
    if dd % 2 or s % 2:
        print(f"  MATH imbalance {f}: $$={dd} inline$={s}"); bad += 1
    for m in re.findall(r'(?:href|src)="([^"]+)"', t):
        if m.startswith("http") or m.startswith("#"): continue
        if not os.path.exists(os.path.normpath(os.path.join(base, m.split('#')[0]))):
            print(f"  BROKEN link {f} -> {m}"); bad += 1
print("  OK" if not bad else f"  {bad} problem(s)")
sys.exit(1 if bad else 0)
PY

echo "== prev/next chain contiguity over the WRITTEN essays =="
python3 - <<'PY' || fail=1
import re, os, sys
idx = open("index.html").read()
order = re.findall(r'href="chapters/([0-9][^"#]*\.html)"', idx)
seen = set(); order = [x for x in order if not (x in seen or seen.add(x))]
CONTENTS = "../index.html"
def norm(h):
    if not h: return None
    return "CONTENTS" if h.endswith("index.html") else os.path.basename(h)
prob = 0
for i, name in enumerate(order):
    p = os.path.join("chapters", name)
    if not os.path.exists(p):
        print(f"  {name}: listed on contents but file missing"); prob += 1; continue
    m = re.search(r'<nav class="chapter-nav">(.*?)</nav>', open(p).read(), re.S)
    if not m:
        print(f"  {name}: no chapter-nav"); prob += 1; continue
    nav = m.group(1)
    nx = re.search(r'<a class="next" href="([^"]+)"', nav)
    nxh = nx.group(1) if nx else None
    pvh = next((a for a in re.findall(r'<a[^>]*href="([^"]+)"', nav) if a != nxh), None)
    exp_prev = order[i-1] if i > 0 else CONTENTS
    exp_next = order[i+1] if i < len(order)-1 else CONTENTS
    if norm(pvh) != norm(exp_prev): print(f"  {name}: prev={pvh}  expected {exp_prev}"); prob += 1
    if norm(nxh) != norm(exp_next): print(f"  {name}: next={nxh}  expected {exp_next}"); prob += 1
print(f"  {len(order)} written essays in contents order, chain contiguous" if not prob
      else f"  {prob} chain problem(s)")
sys.exit(1 if prob else 0)
PY

echo "== ledger: every essay carries one, and no forward dependencies =="
python3 - <<'PY' || fail=1
import re, os, glob, sys, json
prob = 0
essays = sorted(glob.glob("chapters/*.html"))

# An essay counts as SETTLED once it exists and every required record assigned to
# it is resolved -- proved and available, or an accepted assumption and available.
reg = json.load(open("data/ledger.json"))
accepted = set(reg["completion_policy"]["accepted_assumption_ids"])
written = {int(os.path.basename(p)[:2]) for p in essays}
outstanding = set()
for item in reg["proof_register"]:
    if item["role"] != "required_for_flt":
        continue
    resolved = item["availability"] == "available" and (
        item["register"] == "proved" or item["id"] in accepted
    )
    if not resolved:
        outstanding.update(item["essays"])
SETTLED = written - outstanding
for f in essays:
    n = int(os.path.basename(f)[:2])
    t = open(f).read()
    if '<section class="ledger">' not in t:
        print(f"  {os.path.basename(f)}: no ledger section"); prob += 1; continue
    led = t.split('<section class="ledger">', 1)[1]
    expected_columns = (
        'class="col proved-here"',
        'class="col assumed-here"',
        'class="col owed"',
    )
    if any(column not in led for column in expected_columns):
        print(f"  {os.path.basename(f)}: ledger missing a proved/imported/owed column"); prob += 1
    # backwards debt: the owed column must not name an essay that is at or
    # before this one AND has nothing left outstanding. An earlier-numbered
    # essay may legitimately be named if it is unwritten, or if it still carries
    # an unresolved required item (essay 02's outlined second case, for
    # instance). Nine essays had drifted here, because the owed column is prose
    # the validator did not read.
    if 'class="col owed"' in led:
        owed = led.split('class="col owed"', 1)[1].split("</div>", 1)[0]
        for ref in re.findall(r'essays? ((?:\d\d(?:[,\s]+(?:and\s+)?)?)+)', owed):
            for num in re.findall(r'\d\d', ref):
                k = int(num)
                if k <= n and k in SETTLED:
                    print(f"  {os.path.basename(f)}: owed column names essay {num}, "
                          f"which is at/before {n:02d} and has nothing outstanding")
                    prob += 1
    # forward dependency: "What we already have" must not cite a later essay
    m = re.search(r'Rung 1</span>\s*What we already have(.*?)</section>', t, re.S)
    if m:
        for ref in re.findall(r'(\d\d)-[a-z0-9-]+\.html', m.group(1)):
            if int(ref) >= n:
                print(f"  {os.path.basename(f)}: Rung 1 cites essay {ref} (>= own number {n:02d})")
                prob += 1
print("  ledgers present, no forward dependencies" if not prob else f"  {prob} ledger problem(s)")
sys.exit(1 if prob else 0)
PY

echo "== generated proof status agrees with the canonical ledger data =="
python3 scripts/render_status.py --check || fail=1

echo "== no Tier C textbook section numbers (no owned copies to verify against) =="
hits=$(grep -rInE '(Silverman|Diamond|Shurman|Washington|Cornell|Stevens)[^<]{0,80}(§|Ch\.? ?[0-9]|p\.? ?[0-9]|section ?[0-9])' chapters/*.html *.html 2>/dev/null)
if [ -n "$hits" ]; then echo "  FAIL: precise citation to an unowned textbook:"; echo "$hits"; fail=1
else echo "  none (textbooks cited by topic only, as required)"; fi

echo "== every Tier A citation is logged in SOURCES.md =="
python3 - <<'PY' || fail=1
import re, glob, sys, os
src = open("SOURCES.md").read() if os.path.exists("SOURCES.md") else ""
missing = 0
for f in sorted(glob.glob("chapters/*.html")):
    t = open(f).read()
    # LMFDB labels like 11.2.a.a, individual curves like 11.a3, or classes like 11.a
    for lab in set(re.findall(r'<code>(\d+\.\d+\.[a-z]+\.[a-z]+|\d+\.[a-z]+\d+|\d+\.[a-z]+)</code>', t)):
        if lab not in src:
            print(f"  {os.path.basename(f)}: LMFDB label {lab} not logged in SOURCES.md"); missing += 1
    # DDT theorem/section references
    for thm in set(re.findall(r'theorem (\d+\.\d+)', t)):
        if thm not in src:
            print(f"  {os.path.basename(f)}: theorem {thm} not logged in SOURCES.md"); missing += 1
print("  all Tier A citations logged" if not missing else f"  {missing} unlogged citation(s)")
sys.exit(1 if missing else 0)
PY

echo "== no prose shared with the reference transcript =="
python3 - <<'PY' || fail=1
import re, glob, os, sys
tp = "resources/transcript.txt"
if not os.path.exists(tp):
    print("  transcript absent, skipped"); sys.exit(0)
def words(s):
    return re.sub(r'[^a-z ]', ' ', re.sub(r'<[^>]+>', ' ', s.lower())).split()
tw = words(open(tp).read())
N = 12
grams = {tuple(tw[i:i+N]) for i in range(len(tw)-N+1)}
bad = 0
for f in sorted(glob.glob("chapters/*.html")):
    ew = words(open(f).read())
    for i in range(len(ew)-N+1):
        g = tuple(ew[i:i+N])
        if g in grams:
            print(f"  {os.path.basename(f)}: shares {N} words with transcript: {' '.join(g)[:90]}")
            bad += 1; break
print(f"  no {N}-word overlap with the transcript" if not bad else f"  {bad} overlap(s)")
sys.exit(1 if bad else 0)
PY

echo "== self-assessment scan (an essay must not grade itself) =="
hits=$(grep -rniE "cleanest|clearest|sharpest|in the whole book|of its thesis|worth saying|this book cannot|the rest of this book" chapters/*.html)
if [ -n "$hits" ]; then echo "  triage (mathematical superlative = ok; verdict about the essay = fix):"; echo "$hits"
else echo "  none"; fi

echo "== numerical checks =="
for s in checks/*.py; do
  [ -e "$s" ] || continue
  if python3 "$s" >/dev/null 2>&1; then echo "  PASS $s"
  else echo "  FAIL $s"; python3 "$s" 2>&1 | tail -5; fail=1; fi
done

echo "== no copyrighted PDFs or transcripts tracked by git =="
tracked=$(git ls-files 2>/dev/null | grep -Ei '\.(pdf|epub)$|^resources/|^sources/' )
if [ -n "$tracked" ]; then echo "  FAIL: should not be tracked:"; echo "$tracked"; fail=1
else echo "  none tracked"; fi

echo "----------"
if [ "$fail" = 0 ]; then echo "VERIFY: PASS"; else echo "VERIFY: FAIL"; fi
exit $fail
