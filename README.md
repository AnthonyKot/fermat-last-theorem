# No Such Form

Twenty-five essays building the proof of Fermat's Last Theorem one rung at a time, from Fermat's own
infinite descent to the contradiction that ends the problem: a weight-2 newform of level 2 must exist,
and the space it would occupy has dimension zero.

Third in a series built the same way, after [The Quantum Quartet](https://anthonykot.github.io/quantum-quartet/)
(four authors on early quantum mechanics) and The Bridge (a quantum-mechanics course carried forward to
quantum information).

Each essay follows four rungs — **What we already have → The construction → What it buys → Reading** —
and closes with a **ledger**: what it discharged, and what the final contradiction is still owed. The
series is finished when the ledger is empty. See [`about.html`](about.html) for exactly what is proved,
what is stated without proof, and what is only described.

## Reading it

A plain static site. Open `index.html`, or serve it:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/
```

## Status

Scaffold and the full 25-essay map are complete. Five essays are written — the two ends of the rope,
plus the first elliptic-curve construction:

| # | Essay | What it delivers |
|---|-------|------------------|
| 01 | Descent, and the exponent four | $x^4+y^4=z^2$ has no solution, proved in full; reduction to odd prime exponents |
| 02 | Unique factorisation, and where it runs out | $n=3$ first case in the Eisenstein integers; failure of unique factorisation; Kummer's regular primes |
| 06 | Elliptic curves, written correctly | General Weierstrass form, smoothness and discriminant; why integral models at $2$ and $3$ matter |
| 22 | The Frey curve | The construction, and $\Delta = 16(abc)^{2p}$ |
| 25 | Ribet, and the end | Level lowering stated; the level-2 arithmetic computed; the contradiction assembled conditionally |

The ends were written first deliberately: with the destination on paper, every construction in between
has to justify itself. Essays 03–05, 07–21, 23 and 24 are stubbed on the contents page, and essay 25 states
plainly that it is conditional until they exist.

## Verification

This collection was written without a personal library of the standard textbooks, so the usual safety
net — a checked page reference — is unavailable. Two substitutes carry it instead, both executable:

```bash
./verify.sh
```

- **Ledger checks.** Every essay must carry a ledger, and no essay's "What we already have" may cite an
  essay at or after its own number. Forward dependency is the one defect a careful read never catches,
  because each essay is internally correct.
- **Proof-register sync.** `data/ledger.json` is the source of truth for the public account of what is
  proved, stated, outlined, conditional or planned. `about.html` contains a committed generated block;
  every available item is tied to exactly one essay-ledger entry by `data-proof-id`, and verification
  fails if either side drifts.
- **Computed numbers.** Every numerical claim has a script in `checks/`, run by `verify.sh`, and where
  possible confirmed a second independent way:
  - `dim_s2_gamma0.py` — the dimension formula, cross-checked against the classical list of levels where
    it vanishes, and against the LMFDB dimension at level 11.
  - `frey_discriminant.py` — the discriminant identity, computed from root differences *and* from the
    Weierstrass $b$-invariants; the two routes share no algebra.
  - `kummer_regular_primes.py` — Bernoulli numbers and the irregular primes, asserted against the
    classical start of that sequence.
  - `weierstrass_models.py` — the two essay-06 discriminants and the change-of-coordinates identity,
    checked coefficient by coefficient.
- Plus the ported checks: computed count sync, link resolution, math-delimiter balance, prev/next
  contiguity, a scan forbidding section numbers for textbooks not owned, a check that every precise
  citation is logged in `SOURCES.md`, and an n-gram check against the reference transcript.

## Sources

Citations are tiered, and the tiers are enforced by `verify.sh`. Stable identifiers — LMFDB labels,
published-paper theorem numbers — are cited precisely. Textbooks not consulted directly are cited by
topic only and marked unverified. Encyclopaedias, blogs and lecture videos are used for orientation and
never cited. `SOURCES.md` logs every precise citation with the date it was checked.

No source text is reproduced anywhere. `resources/` and `sources/` are git-ignored and never pushed.

## Stack

- Plain HTML, one stylesheet (`static/style.css`), one small script (`static/theme.js`).
- No build step, no framework, no static-site generator.
- Math via [KaTeX](https://katex.org/) from CDN (`$…$` inline, `$$…$$` display), SRI hashes pinned.
- Light/dark theme honouring `prefers-color-scheme`, toggle persisted in `localStorage`.
- Print-friendly stylesheet.
- `.nojekyll` so GitHub Pages serves the files as-is.

## Structure

```
index.html               landing page + full 25-essay contents
about.html               method, scope fence, sourcing
chapters/NN-slug.html    one file per essay
static/style.css         shared styles (themes, ledger, print)
static/theme.js          theme toggle + KaTeX auto-render
checks/*.py              scripts backing every numerical claim
data/ledger.json         canonical proof-status register
scripts/render_status.py regenerates/checks About's proof-status block
verify.sh                all checks; exits non-zero on failure
CONTEXT.md               authoring notes: spine, ledger, style guide
SOURCES.md               Tier A citation ledger
```

## Deploying to GitHub Pages

The site is served from the repository root, so no build or workflow is needed.

1. Create an empty repository on GitHub (no README, no `.gitignore` — this repo has both).
2. Add it as a remote and push:

   ```bash
   git remote add origin git@github.com:<user>/<repo>.git
   git push -u origin main
   ```

3. In the repository, open **Settings → Pages**, set **Source** to *Deploy from a branch*, and choose
   branch `main` with folder `/ (root)`. Save.
4. The site appears at `https://<user>.github.io/<repo>/` within a minute or two.

`.nojekyll` is committed, so Jekyll does not process the files and directories are served verbatim. All
internal links are relative, so the site works correctly under the `/<repo>/` subpath without
configuration.
