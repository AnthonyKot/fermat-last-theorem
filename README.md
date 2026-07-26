# No Such Form

Twenty-five essays building the proof of Fermat's Last Theorem one rung at a time, from Fermat's own
infinite descent to the contradiction that ends the problem: a weight-2 newform of level 2 must exist,
and the space it would occupy has dimension zero.

Third in a series built the same way, after [The Quantum Quartet](https://anthonykot.github.io/quantum-quartet/)
(four authors on early quantum mechanics) and The Bridge (a quantum-mechanics course carried forward to
quantum information).

Each essay follows four rungs — **What we already have → The construction → What it buys → Reading** —
and closes with a three-part **ledger**: what it proves, what it explicitly assumes, and what remained
owed at that point. The required debt is now empty; assumed results remain visible as assumptions.
See [`about.html`](about.html) for the generated proof boundary.

## Reading it

A plain static site. Open `index.html`, or serve it:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/
```

## Status

Scaffold and the full 25-essay map are complete. Twenty-two essays are written — the two ends of the
rope, the elliptic-curve and modular-form bridges through the Modularity Theorem, and the
semistability check:

| # | Essay | What it delivers |
|---|-------|------------------|
| 01 | Descent, and the exponent four | $x^4+y^4=z^2$ has no solution, proved in full; reduction to odd prime exponents |
| 02 | Unique factorisation, and where it runs out | Both cases for $n=3$ proved in the Eisenstein integers; failure of unique factorisation; Kummer's regular primes |
| 03 | The absolute Galois group | $G_{\mathbb{Q}}$ as an inverse limit of finite Galois groups; $\mathrm{Gal}(\mathbb{Q}(\zeta_n)/\mathbb{Q})\cong(\mathbb{Z}/n)^\times$ with $\mathrm{Frob}_\ell=\sigma_\ell$ |
| 04 | A new pair of sunglasses: the $p$-adics | $v_\ell$ and the ultrametric inequality; $\mathbb{Z}_\ell$ built twice; free modules and $\mathrm{GL}_2(\mathbb{Z}_\ell)$ |
| 05 | Galois representations | Continuous $\rho$ into $\mathrm{GL}_2(K)$, reducibility and semisimplicity; the conductor stated; traces of Frobenius identify a semisimple $\rho$ |
| 06 | Elliptic curves, written correctly | General Weierstrass form, smoothness and discriminant; why integral models at $2$ and $3$ matter |
| 07 | The group law | Chord-and-tangent addition and an order-five example; associativity and complex uniformization stated |
| 08 | Reduction and the conductor | Good, multiplicative and additive reduction; $a_\ell$; semistable ⟺ square-free conductor |
| 09 | Division points and the Tate module | $E[2]$ and $E[3]$ by hand; the Frey curve's full rational $2$-torsion; $T_\ell(E)$ free of rank $2$ |
| 10 | The representation attached to a curve | $\rho_{E,\ell}$ from the Tate module; $\det=\chi_\ell$ so every $\bar\rho$ is odd; reducible $\iff$ a rational subgroup |
| 11 | The modular group | $\mathbb{H}$, $\Gamma_0(N)$, the fundamental domain, and the four counts $\mu$, $\nu_2$, $\nu_3$, $\nu_\infty$ |
| 12 | Modular forms | $q$-expansions and cusp forms; $E_4^3-E_6^2=1728\Delta$; the level-$11$ form exhibited and matched to essay 08's point counts |
| 13 | The dimension formula | Weight-two forms as differentials; Riemann–Hurwitz gives $\dim S_2(\Gamma_0(N))$ and the level-$2$ space vanishes |
| 14 | Hecke operators | The $q$-coefficient formula; eigenvalues are Fourier coefficients; multiplicativity and the prime-power recurrence |
| 15 | Newforms, and the meaning of the level | The level-$22$ oldspace and bad-prime $U_2$ computed; Atkin–Lehner–Li imported to define normalized newforms and exact level |
| 16 | The representation attached to a form | The modular-Jacobian route from a weight-$2$ newform to $\rho_{f,\lambda}$; Eichler–Shimura imported; the level-$11$ Frobenius packets matched exactly |
| 17 | Two $L$-functions, one shape | The good and bad newform Euler factors derived from their separate Hecke relations; curve factors defined by reduction type; analytic continuation and the functional equation imported off the FLT chain |
| 18 | The Modularity Theorem | Conductor equals exact newform level; local factors, $L$-functions and Galois representations match; semistable and general theorems stated precisely |
| 22 | The Frey curve | The construction, and $\Delta = 16(abc)^{2p}$ |
| 23 | Semistable, and therefore modular | A minimal model at $2$; multiplicative reduction at every bad prime; conductor $\mathrm{rad}(abc)$ |
| 24 | The Frey representation | $N(\bar\rho_{E,p})=2$: odd primes drop out because $p$ divides their valuation, $2$ survives because $p\nmid8$; irreducibility for every $p\geq5$ |
| 25 | Ribet, and the end | Level lowering stated; the level-2 arithmetic computed; the FLT contradiction derived from the published assumption roster |

The ends were written first deliberately: with the destination on paper, every construction in between
has to justify itself. Writing order follows dependency rather than page number, which is why 04 and 08
arrived before 03 and 05 — essay 08 reads the discriminant one prime at a time, so it wanted the
valuation to link back to rather than a declared debt. Essays 19–21 are stubbed on
the contents page as an optional anatomy of Wiles's machinery. Essay 18 now registers modularity as
the accepted theorem that closes the continuity gap.
Essay 25 states its remaining conditions explicitly.

## Verification

This collection was written without a personal library of the standard textbooks, so the usual safety
net — a checked page reference — is unavailable. Two substitutes carry it instead, both executable:

```bash
./verify.sh          # everything local
./verify.sh --live   # local checks, then byte-compare the PUBLISHED site and register
```

- **Ledger checks.** Every essay must carry proved/assumed/owed columns, and no essay's "What we
  already have" may cite an essay at or after its own number. Every registered item must appear in the
  column dictated by its canonical proof mode, with matching mode and FLT-chain/background badges.
  Consecutive essays must carry forward the same set of owed L-labels; a label may disappear only
  when the new essay's claim summary explicitly records its proof or accepted registration.
  Claim summaries that close a ledger line are tagged as `proved`, `mixed`, or `imported`; verification
  rejects the old ambiguous “Discharges” label and checks the tag against the canonical register.
- **Proof-register sync.** `data/ledger.json` is the source of truth for the public account of what is
  proved, assumed, outlined, conditional or planned, whether it is required by the FLT chain, and
  which required imports the completion policy accepts. `about.html` contains a committed generated
  block; verification fails if either side drifts.
- **Computed numbers.** Every numerical claim has a script in `checks/`, run by `verify.sh`, and where
  possible confirmed a second independent way:
  - `dim_s2_gamma0.py` — the dimension formula, cross-checked against the classical list of levels where
    it vanishes, and against the LMFDB dimension at level 11.
  - `hecke_operators.py` — the exact Hecke coefficient formula and operator relations on arbitrary
    series; the level-one $\Delta$ and level-$11$ eta product as eigenforms at good primes; and a
    deliberate failure check when the prime-to-level formula is misapplied at $11$.
  - `newforms_and_level.py` — the two degeneracy copies of the level-$11$ form span the level-$22$
    cusp space and share all tested good eigenvalues; the bad-prime matrix
    $U_2=\left(\begin{smallmatrix}-2&1\\-2&0\end{smallmatrix}\right)$ is computed from exact
    $q$-series and has nonreal eigenvalues, while the level-$22$ newspace has dimension zero.
  - `two_l_functions.py` — the level-$11$ eta product is expanded exactly; its good traces are
    compared with independent point counts; the quadratic good-prime and linear bad-prime rules
    reconstruct every coefficient below $180$.
  - `modularity_theorem.py` — finite level-$11$ evidence: conductor and cusp-space dimension,
    forty matching good-prime traces, the bad polynomial $1-T$, and $j(E)=-4096/11$. The script
    explicitly does not claim to check modularity.
  - `frey_discriminant.py` — the discriminant identity, computed from root differences *and* from the
    Weierstrass $b$-invariants; the two routes share no algebra.
  - `kummer_regular_primes.py` — Bernoulli numbers and the irregular primes, asserted against the
    classical start of that sequence.
  - `weierstrass_models.py` — the two essay-06 discriminants and the change-of-coordinates identity,
    checked coefficient by coefficient.
  - `group_law.py` — exact general-Weierstrass addition on essay 07's order-five subgroup.
  - `p_adic.py` — $v_\ell$ and $|\cdot|_\ell$ in exact rational arithmetic: additivity, the ultrametric
    inequality and its equality case over thousands of pairs, every digit string recomputed from
    congruences, and the $\mathrm{GL}_2(\mathbb{Z}_3)$ determinant criterion checked against the
    adjugate exhaustively.
  - `representations.py` — $\mathrm{GL}_2(\mathbb{F}_\ell)$ enumerated for $\ell\leq7$: the
    diagonalisable matrices with a given characteristic polynomial form one conjugacy class, and the
    identity versus the Jordan block shows why the trace theorem needs semisimplicity. Also identifies
    the conductor-$11$ curve's mod $5$ semisimplification as $\mathbf{1}\oplus\bar\chi$.
  - `galois.py` — cyclotomic polynomials built from scratch, $\mathrm{Gal}(\mathbb{Q}(\zeta_n)/\mathbb{Q})$
    as a multiplication table, and the Frobenius claim tested the only way it can be: the least $d$ with
    $x^{\ell^d}=x$ in $\mathbb{F}_\ell[x]/\Phi_n$ equals the multiplicative order of $\ell$ mod $n$.
  - `frey_conductor.py` — Serre's level recipe evaluated symbolically over many exponents and valuation
    patterns, always yielding exactly $\{2\}$; and the irreducibility witnesses computed by enumerating
    every $a_\ell$ the constraints permit, giving $\ell=3,7$ for $p=5$ and $\ell=5,17$ for $p=7$.
  - `frey_irreducibility.py` — progress on the collection's open question. Rational $E[2]$ forces
    $4 \mid \#E(\mathbb{F}_\ell)$, which with Hasse pins $a_3=0$, $a_5=\pm2$, $a_7\in\{0,\pm4\}$;
    since reducibility would force $a_\ell^2-4\ell$ to be a square mod $p$, each pinned value is a
    witness. Gives $\bar\rho_{E,5}$ and $\bar\rho_{E,7}$ irreducible whenever the witness prime is
    good. Not the uniform theorem, and the script says so.
  - `mod_ell_representation.py` — the pairing identity $e(Mv,Mw)=e(v,w)^{\det M}$ over every invertible
    matrix for several moduli, the uniqueness of $-1$ as the root-of-unity-inverting exponent, and the
    reducibility congruence $a_\ell\equiv\ell+1$ tested on two curves at two primes each, passing in
    the two cases with a rational subgroup and failing in the two without.
  - `torsion.py` — an exact rational group law for general Weierstrass models: the $2$-division cubic,
    no rational $2$-torsion for the conductor-$11$ curve versus all of it for six Frey curves, $\psi_3$
    and the order of $(0,\pm1)$ on $y^2=x^3+1$, and the coordinate description of the Tate module.
  - `frey_semistable.py` — runs essay 23's whole argument over forty triples with the three properties
    it actually uses: integrality of the minimal model, $\Delta_{\min}=(ABC)^2/2^8$, the double-root
    analysis at odd primes, the separable tangent cone at $2$, and — independently, by point counting —
    $a_\ell=\pm1$ at every bad prime.
  - `reduction_and_conductor.py` — point counts over $\mathbb{F}_\ell$ with no elliptic-curve library:
    bad primes from the discriminant, $a_\ell$ against the LMFDB newform coefficients, the Hasse bound,
    and both reduction types located two independent ways — by point count and by the tangent
    directions at the singular point.
- **Generated site facts.** The contents tally, About status, assumption total, each chapter's owed
  L-label roster, and every previous/next link are regenerated together. The footer contains stable
  source/deployment links, not a guessed commit hash: a commit cannot truthfully contain its own hash.
- **Published-artifact check.** `./verify.sh --live` cache-busts every public URL and requires every
  served HTML file plus `data/ledger.json` to equal this verified checkout byte for byte. It therefore
  catches local-only work, unpushed commits, failed builds, stale caches and partial deployments.
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
data/ledger.json         canonical proof-status, role, debt and completion policy
scripts/render_status.py regenerates/checks status, counts, navigation and deployment footers
scripts/check_live.py    byte-compares the published pages and register with this checkout
verify.sh                local checks; --live also verifies the deployed artifact
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
