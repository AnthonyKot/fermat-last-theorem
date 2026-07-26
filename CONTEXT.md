# CONTEXT — authoring notes for *No Such Form*

Internal guide for the essay series. Not published as a reader-facing page.

Working title: **No Such Form** — the last essay's punchline is that a required modular form has
nowhere to live. (Alternative considered: *The Ladder*. Decide before `index.html` ships.)

## Premise

A single argument, built one rung at a time, from Fermat's own descent to the 1995 contradiction.
Every essay adds exactly one object or one theorem, and every essay closes by saying what the final
contradiction now has and what it still owes. The series is finished when the required debt is empty;
explicit imports remain visible as assumptions.

## The reference video

`resources/transcript.txt` — auto-generated captions of the 8-hour lecture the plan came from
(`youtube.com/watch?v=9f-hGSh8lF0`), 74,788 words, one line, **no timestamps**, no punctuation, proper
nouns badly mangled (Wiles → "walls", Galois → "galwa"/"gallo", Frey → "fray", Ribet → "ribbit",
Frobenius → "probenius", Hecke → "heap"/"hackiff", Mazur → "mazour", Néron–Ogg–Shafarevich → "naron
arc chef thorich", Eichler–Shimura → "equil shimmerra", eigen → "igen").

**How it is used:** the video fixes *what* the series covers and *in what order*. It is never cited —
no timestamps exist to cite, and a mangled auto-caption is not a citable source. `resources/` is
git-ignored. Verification queries against it are done with word-offset percentages, and the mangling
means **a term coming up "absent" in a grep proves nothing** until phonetic variants are checked; that
mistake was made once already and produced a coverage map claiming the video never mentions Galois
theory, Hecke operators, Frey, or Ribet.

**Verified coverage map** (word-offset % → essay), from grepping variants and reading the passages:

| Video % | Content | Essay |
|---|---|---|
| 0–4 | framing; gcd properties as descent tooling | 01 |
| 4–18 | n = 4 and n = 3, by **elementary number theory** | 01, 02 |
| 18–38 | vector spaces, linear transformations, eigenvalues ("igen value") | *prerequisite — not written* |
| 38–48 | groups, rings, fields, unique factorization domains, degree of extension | 02, 03 |
| 48–52 | **G_Q**, the absolute Galois group; modules over a ring | 03, 04 |
| 52–56 | **Frobenius elements**; p-adic numbers and valuations | 04 |
| 56–63 | elliptic curves, group law | 06, 07 |
| 63–70 | division points E[2], E[3], E[n] ≅ (Z/n)²; **Tate module**; discriminant, reduction | 08, 09 |
| 70–74 | conductor; representations from the Tate module | 09, 10 |
| 74–82 | ℍ, modular group, fundamental domain, cusps, modular forms, q-expansions, Eisenstein/cusp decomposition, **valence formula** | 11, 12, 13 |
| 82–88 | Hecke forms, multiplicativity of coefficients, L-functions via Euler product | 14, 17 |
| 88–92 | newforms, level, Shimura, modularity | 15, 16, 18 |
| 92–96 | conductor ↔ level, Wiles's theorem (**black box**) | 18 |
| 96–97 | **Ribet's level lowering**, with full hypotheses | 25 |
| 97–99 | Frey curve, semistability, **Mazur's isogeny theorem**, **Néron–Ogg–Shafarevich** | 22, 23, 24 |
| 99–100 | dimension of S₂(Γ₀(2)) computed = 0; the contradiction | 25 |

**Three findings from the transcript that changed this spine** — each is a correction to my own first
draft, which was built from the plan summary alone:

1. **p-adic numbers are a topic, not an aside.** The video spends ~52–56% on valuations and the p-adic
   viewpoint. My first spine used Z_p in the Tate-module essay without ever introducing it — a genuine
   forward dependency, exactly the defect the ledger exists to catch, found in my own plan. Now
   essay 04.
2. **Mazur's isogeny theorem and Néron–Ogg–Shafarevich are in the video and were missing from the plan
   summary.** They are not optional colour: Mazur's theorem is *how* irreducibility of the Frey
   representation is obtained (finitely many possible primes, all excluded ⟹ irreducible for p ≥ 5),
   and Néron–Ogg–Shafarevich is *how* the representation's conductor is computed from the curve's
   reduction. Without them, essay 24 has no method, only an assertion. Now named in 10 and 24.
3. **The dimension formula is arithmetic, not Riemann–Hurwitz.** The video goes valence formula →
   explicit genus/dimension formula in the index and the counts ν₂, ν₃, ν_∞. That is the better route
   here: fully computable, no Riemann-surface machinery, and `checks/` can verify it against many
   levels. My first spine derived it geometrically. Changed in 13.

The video also **confirms** two things the plan summary got loose (see Corrections): it states Ribet's
hypotheses properly, and it does treat irreducibility as a theorem. Those corrections apply to the
*summary*, not to the video.

## What is proved and what is stated (hard fence)

`data/ledger.json` is the only source of truth for the public proof boundary. It keeps three questions
orthogonal: whether a claim is available or planned; whether it is proved, stated, outlined,
conditional or described; and whether it is required by the FLT chain or is background. Every
available record is tied to exactly one essay-ledger item by `data-proof-id`. `about.html` is generated
from it; never edit the generated block to change scope.

The completion policy names every required result that the collection deliberately imports rather
than proves. **Do not list them here.** That list went stale by hand twice — once at six entries and
once at seven — which is exactly the failure the generated block exists to prevent. The authoritative
roster is rendered on `about.html` from `data/ledger.json`, by name, with essay links and a marker for
the ones whose essay is unwritten; read it there. To see it without a browser:

```bash
python3 -c "import json;d=json.load(open('data/ledger.json'));print(*d['completion_policy']['accepted_assumption_ids'],sep=chr(10))"
```

Those results are **stated with their usable hypotheses, not proved**. The validator requires the
policy's allowlist to equal exactly the required records whose proof mode is `stated`, and requires
every stated record to carry a `short` label so it can be published by name rather than merely
counted; a new assumption cannot slip in without a deliberate edit to the canonical policy.

**Keep the chain's assumptions as narrow as what it spends.** Two entries were deliberately narrowed
rather than accepted wholesale, and the same test applies to every future one — *does the closing
argument consume all of this, or only part of it?*

- **The conductor exponents were split.** The Frey curve is semistable, so every bad prime is
  multiplicative and only $f_\ell=1$ there is load-bearing. The additive exponents, the $\ell>3$
  threshold and the special treatment of $2$ and $3$ are `background`: essay 08's contrast curve needs
  them, the chain does not.
- **Global minimal-model existence was demoted to `background`.** The chain never needs the general
  theorem; it needs one curve's minimal model. That trade — a permanent trust obligation for a
  dischargeable debt — is always worth making, and the reverse never is. **Essay 23 has since
  discharged it**: the substitution $x=4X$, $y=8Y+4X$ exhibits the Frey curve's minimal model and
  proves it minimal at $2$, so `23-frey-minimal-model` is now proved and available, and the chain's
  assumption set did not grow when essay 23 landed.

### Assumed and owed are not the same kind of thing

They behave differently on purpose, and the difference must not be smoothed away:

| | *Still owed* | *Assumed here* |
|---|---|---|
| Direction | a forward promise | a standing trust obligation |
| Over the collection | **shrinks**, and must reach empty | **accumulates**, and never empties |
| Discharged by | a later essay **resolving** it — proving it, or being the essay that states an accepted assumption | nothing — it is permanent by construction |
| Scope shown | per essay, because it changes essay to essay | per essay for what that essay adds |
| Global view | the release gate in `verify.sh` | the allowlist plus About's generated block |

**A required assumption is therefore listed in both places, and that is not a contradiction — but say
which is which.** An accepted import like modularity is *permanently assumed* (it will never be
proved), while the collection still *owes the essay that states it*. What leaves the owed column is the
missing essay, not the missing proof. Word owed-column lines accordingly, and never list an
already-available accepted assumption as owed: `25-small-exponents` is external classical work, so
nothing can ever discharge it, and filing it as owed would keep the release gate from closing for ever.

### The third state: proved, conditional on an assumption made elsewhere

The schema originally had only *proved* and *assumed*, and results of the form "this follows from a
theorem imported in an earlier essay" had nowhere to sit. Filed as assumed they broke the column's own
definition — they *are* discharged by something, namely the upstream import — and they inflated the
roster, putting two entries under one root. Two records had drifted into exactly that state:
`09-torsion-general` (from essay 07's uniformization) and `23-modularity-applied` (from essay 18's
Modularity Theorem).

Both are now `register: proved` with a **`depends_on`** naming the upstream assumption. Consequences,
all enforced by `render_status.py`:

- `depends_on` may appear only on a proved record, and every id in it must exist and be an assumption;
- **the root import must carry at least the role of everything hanging off it.** A chain-required proof
  may not depend on a background assumption. That check immediately caught a real leak:
  `07-uniformization` was `background` while the chain-required `09-torsion-general` derived from it, so
  the chain rested on something the roster never listed. Uniformization is now `required_for_flt`;
- the allowlist therefore counts **root imports only** — 13, not 15 — and About names each one.

Expect this state to recur: every essay downstream of uniformization or modularity will want it. When it
does, use `depends_on` rather than adding an assumption. It also makes narrowing cheap later: if
uniformization is ever proved or demoted, everything hanging off it follows automatically.

⚠ **The owed column is free prose and the validator does not check it.** `render_status.py` pins every
*registered* item to the right column, but a hand-written line in an owed list can drift out of date
with nothing to catch it. Two such lines had already drifted in essay 23. When editing an owed column,
re-derive it from the register rather than from the previous essay's list.

So **the assumed column does not carry forward, and should not.** Repeating every inherited assumption
in all eight ledgers would duplicate About's job and grow without bound. But because the set only ever
grows, the accumulating view is the one that needs teeth, and that is where the allowlist lives: it is
a hand-edited constant that must exactly equal the required stated records, so adding an assumption is
always a visible, deliberate edit to the policy. The per-essay column answers *what did this essay ask
me to take on trust*; the allowlist answers *what does the finished proof rest on*.

The rest of the non-negotiable boundary is:

- Langlands–Tunnell and complex uniformization are imported as background, not dependencies of the
  closing FLT chain;
- Wiles's machinery in Part V is **described as anatomy**, not proved. The reader learns what the
  objects are and what the strategy is. Three essays cannot prove a 109-page paper and must not
  pretend to;
- the second case for $n=3$ remains **outlined** unless essay 02 is expanded into a genuine proof;
- an item moves into the **proved** register only when its essay exists and supplies the promised
  derivation.

Part V is not in the video at all: greps for deformation, universal (deformation ring), Langlands,
Tunnell, base change and $R=T$ all come back genuinely empty, variants included. It is entirely ours,
which is also why it is the likeliest place to overreach.

The completed target remains a checkable derivation of FLT from the explicitly named imported
results, plus a guided tour of the background around them. Completion means that no required record is
planned, outlined, conditional or otherwise unresolved. It does not relabel an import as a proof.

## Reader

Has undergraduate algebra: linear algebra through eigenvectors and the spectral theorem for commuting
self-adjoint operators; groups, rings, fields, ideals, quotients. Has seen complex analysis. Assumes
**no** algebraic number theory, **no** Galois theory beyond the definition of a field extension, **no**
algebraic geometry, **no** modular forms.

Consequence: the video's 18–38% stretch (vector spaces, linear transformations, eigenvalues) is *not
written*. The spectral theorem is recalled in essay 14 where it earns its keep.

The contents page carries an orientation band for every Part. Parts I–V name external prerequisites;
Part VI deliberately names internal reading dependencies instead. Treat those bands as a contract, not
marketing copy: if an essay needs vocabulary or technique beyond its band's floor, either introduce it
in place or update the band before publication. Part VI explicitly marks Part V as explanatory rather
than logically required.

## The four-rung template (every essay)

Exact headings (`<section class="rung">`, `<h2>` with a numbered pill):

1. **What we already have** — objects this essay stands on, cited *by essay number*, never a vague
   back-reference. If it isn't in an earlier essay it isn't available: say so and add it to the owed
   column.
2. **The construction** — the one new object or theorem, motivated before it is defined. One idea.
3. **What it buys** — an original worked example, plus the specific later essay that consumes this.
4. **Reading** — topic-level citations only (see Sourcing), flagged unverified.

Then the **ledger** (`<section class="ledger">`): three columns, *proved here*, *assumed here* and
*still owed*. A registered item carries canonical mode and role badges. Proved items alone receive a
green check; outlined and conditional results remain owed. The middle column is named *assumed*, not
*imported*, on purpose: everything in it is an unproved result taken from the literature — a live trust
obligation — and never merely a pointer to an earlier essay of this collection. Provenance from an
earlier essay belongs in Rung 1, not in the ledger. The owed column is the previous essay's debt minus
what this essay proves or explicitly assumes.
`verify.sh` checks the structure now and will check exact carry-forward equality when the middle
essays exist.

Header, footer, prev/next nav copied verbatim between essays.

## The master ledger

Essay 25 needs exactly these. Every line must be resolved by a proof or a declared import, and no essay
may use a line before the essay that makes it available.

| # | Ledger line | Discharged in |
|---|---|---|
| L1 | FLT reduces to exponents p prime, p ≥ 5 | 01; 02 proves the first case for n = 3 but still owes the second-case descent |
| L2 | G_Q exists; Frobenius elements; traces of Frobenius determine a semisimple representation | 03, 05 |
| L3 | Z_p and the p-adic valuation v_ℓ | 04 |
| L4 | Elliptic curves over Q form a group; discriminant, reduction types, conductor | 06, 07, 08 |
| L5 | Semistable ⟺ squarefree conductor ⟺ multiplicative reduction at all bad primes | 08 |
| L6 | E[n] ≅ (Z/n)²; T_p(E) free of rank 2 over Z_p | 09 |
| L7 | ρ̄_{E,p} : G_Q → GL₂(F_p) exists, tr ρ̄(Frob_ℓ) ≡ a_ℓ | 10 |
| L8 | Mazur's isogeny theorem ⟹ irreducibility of ρ̄_{E,p} for **p > 7**, E semistable | 10 (stated) |
| L9 | Néron–Ogg–Shafarevich: unramified at ℓ ⟺ good reduction at ℓ | 10 (stated) |
| L10 | dim S₂(Γ₀(N)) from the valence formula, index, and ν₂, ν₃, ν_∞ | 13 |
| L11 | Hecke eigenbasis exists; eigenvalues = Fourier coefficients | 14 |
| L12 | Newforms; the level of a newform | 15 |
| L13 | Eichler–Shimura: weight-2 newform → ρ_{f,p} | 16 (stated) |
| L14 | Modularity Theorem (semistable case) | 18 (stated) |
| L15 | Frey curve construction from a solution | 22 |
| L16 | Frey curve is semistable; conductor = rad(abc) | 23 |
| L17 | Conductor of ρ̄_{Frey,p} is 2 | 24 |
| L18 | Ribet: level lowering to the representation's conductor | 25 (stated) |
| L19 | dim S₂(Γ₀(2)) = 0 | 25 |

## Sourcing discipline — web-assisted, tiered

No textbooks are owned. Book 2's rule (every `§` checked against a real copy) is unavailable for
books — but the web supplies a citation form that is **strictly better than a book section number**,
because it uses *stable identifiers* that do not drift between editions. That was the whole reason
book 2 banned recalled `§` pointers. Labels and paper theorem numbers don't have that failure mode.

### Tier A — citable precisely, but only after being fetched in this session

- **LMFDB** (`lmfdb.org`) — elliptic curves and newforms by label: `11.2.a.a`, isogeny class `11.a`.
  Authoritative and computational. This is the primary reference for every numerical claim about a
  specific curve or form. Cite the label, not a URL fragment.
- **Published papers**, by theorem/proposition number: Wiles, *Modular elliptic curves and Fermat's
  Last Theorem*, Annals 1995; Ribet, *On modular representations of Gal(Q̄/Q) arising from modular
  forms*, Inventiones 1990; Serre's 1987 Duke paper; Mazur 1978. Theorem numbers in a published paper
  are stable in a way book sections are not.
- **Darmon–Diamond–Taylor, *Fermat's Last Theorem*** (survey, freely available) — the canonical
  readable account of the whole proof. **This is what Part V needs**: it is the difference between
  Part V being an informed sketch and being vibes. Fetch it before drafting 19–21.
- **Named open lecture notes** with a stable URL and a version date (Milne on elliptic curves and
  modular functions; Sutherland's MIT 18.783). Cite author + notes title or course offering + topic
  + the date fetched. Use numbered pointers only when the URL and citation pin a specific version;
  treat rolling, unversioned notes as topic-level pointers.

### Tier B — orientation only, never cited

Wikipedia, blogs, forums, Q&A sites, and the video transcript. Use them to find out *what to look up*
and *what the standard name of a thing is*. They never appear in a Reading rung.

### Tier C — textbooks we do not own

Silverman, Diamond–Shurman, Cornell–Silverman–Stevens. **Topic-level only, forever**, unless a copy
lands in `sources/`: "Silverman, *The Arithmetic of Elliptic Curves*, on reduction types and the
conductor". No section numbers.

### The hard rules

- **A search result is not a source.** Only cite what `WebFetch` actually returned in this session
  and you actually read. A search snippet is Tier B. This is the same failure as a recalled `§`
  number wearing a URL.
- **Every Tier A citation is logged in `SOURCES.md`** — date fetched, URL, label or theorem number,
  and the one thing it confirmed. An unlogged citation is treated as unverified and fails `verify.sh`.
- Theorem *attributions* with years are always allowed (checkable, not edition-dependent).
- **Never reproduce prose from anything** — papers, notes, LMFDB, or the transcript. State results in
  our own words; the content of a theorem is free, its author's sentences are not.
- **Two passes, as in book 2.** Verification pass: sources open, pin every pointer and number.
  Writing pass: sources closed, write from understanding. With a paper's sentence in the context
  window the path of least resistance is to reproduce it.

### The two internal verifications (these still carry the book)

1. **Internal dependency check.** Every theorem an essay uses must be stated in an earlier essay.
   `verify.sh` parses each ledger, confirms the owed column carries forward, confirms no essay uses a
   line before the essay that makes it available, and confirms essay 25's owed column is empty. Catches forward
   dependency, which no per-essay read catches because each essay is internally fine. Already caught
   one at the planning stage (p-adics).
2. **Numerical self-check, now cross-validated.** Compute it ourselves in `checks/` *and* confirm
   against LMFDB — two independent routes. Already done for essay 18's worked example: brute-force
   point counting on y² + y = x³ − x², an η-product q-expansion, and LMFDB `11.2.a.a` all give
   a₂ = −2, a₃ = −1, a₅ = 1, a₇ = −2, a₁₃ = 4; and `checks/dim_s2_gamma0.py` independently gives
   dim S₂(Γ₀(11)) = 1, matching LMFDB's dimension for that space. A claim verified by two independent
   computations plus a database is stronger than anything a page number could give.

`sources/` stays in place, git-ignored, with a README listing wanted texts, so Tier C can be upgraded
if copies arrive.

## Spine — 25 essays, six parts

### PART I — THE OLD METHOD, AND WHY IT STOPS (5)

| # | Slug | Construction | Notes |
|---|------|--------------|-------|
| 01 | descent-and-n4 | Infinite descent; Pythagorean parametrization; **FLT for n = 4, proved** | Fermat's own method, in full. The gcd lemmas the video front-loads are stated here as tooling, where they are used. Fixes the exponent reduction: any n ≥ 3 has an odd prime factor or is divisible by 4. |
| 02 | unique-factorization-and-n3 | **First case for n = 3 proved; second case outlined**; then unique factorization as a *structure*: UFDs, the failure in Z[ζ₂₃], class numbers, regular primes, Kummer's partial result | The pivot of Part I. The video proves n = 3 by elementary number theory and introduces UFDs separately; we keep both and connect them. Until the second-case descent is expanded, L1 remains open. See Deviations #2. |
| 03 | galois-and-g-q | Field extensions and degree, the Galois correspondence, Q̄, **G_Q** as a profinite group, **Frobenius elements** at primes | Why G_Q resists direct study: not finite, no presentation. Motivates 05 instead of asserting it. |
| 04 | p-adics-and-modules | The p-adic valuation v_ℓ, Z_p and Q_p, "small means highly divisible"; modules over a ring, free modules and rank | **Not in my first draft; the transcript forced it.** Needed for T_p(E) ≅ Z_p² (09), GL₂(Z_p) (10), the finite-at-p condition (24), and the valuation computation (23). Discharges L3. |
| 05 | galois-representations | Continuous ρ : G_Q → GL₂(K); ramified/unramified primes; conductor of a representation; irreducibility; **traces of Frobenius determine a semisimple ρ** | The linearization move. The trace fact is load-bearing — it makes "these two representations are isomorphic" *checkable* in 18, so it lives here. Discharges L2. |

### PART II — ELLIPTIC CURVES (5)

| # | Slug | Construction | Notes |
|---|------|--------------|-------|
| 06 | elliptic-curves | General Weierstrass form, smoothness, the discriminant, the point at infinity; why short integral form loses information at 2 and 3 | Corrections #1, #2. Short form exists over Q, but its integral arithmetic can be bad at 2 and 3; the Frey argument happens at 2. Get the distinction right here or pay in 23. |
| 07 | the-group-law | Chord-and-tangent addition, E(Q) abelian, associativity (stated), E(C) ≅ C/Λ | The torus is not decoration: it is what makes a modular parametrization X₀(N) → E conceivable in Part IV. |
| 08 | reduction-and-conductor | Minimal integral models; reduction mod ℓ; good, multiplicative, additive reduction; a_ℓ = ℓ + 1 − #E(F_ℓ); the conductor; **semistable ⟺ conductor squarefree** | Discharges L4, L5. Check: brute-force a_ℓ for a small curve. |
| 09 | torsion-and-tate-module *(written)* | E[2] and E[3] explicitly, then E[n] ≅ (Z/n)² in characteristic 0; the **Tate module** T_p(E), free of rank 2 **over Z_p**; det = cyclotomic character | The video's route — compute two small cases, then generalize — is the right one; keep it. Name the ring (Corrections #3). Rank 2 is why the representations are 2×2. Discharges L6. |
| 10 | elliptic-representation | ρ_{E,p} : G_Q → GL₂(Z_p) from the action on T_p(E); reduction to ρ̄_{E,p}; tr ρ(Frob_ℓ) = a_ℓ; **Mazur's isogeny theorem**; **Néron–Ogg–Shafarevich** | Discharges L7; states L8, L9. Both named theorems were absent from the plan summary and are the *methods* 24 needs. Introduce here so 24 can cite rather than assert. |

### PART III — MODULAR FORMS (5)

| # | Slug | Construction | Notes |
|---|------|--------------|-------|
| 11 | the-modular-group | ℍ, SL₂(Z) by fractional linear transformations, the fundamental domain, Γ₀(N), index, cusps, elliptic points | Geometry first, functions second. The counts defined here are exactly what 13 plugs in. |
| 12 | modular-forms | Weight-k modularity, holomorphy at the cusps, q-expansions, Eisenstein series, cusp forms, the decomposition M_k = ⟨E_k⟩ ⊕ S_k | Concrete: write actual q-expansions. |
| 13 | valence-and-dimension | The **valence formula** (weighted zeros/poles = k/12), then **dim S₂(Γ₀(N)) = 1 + μ/12 − ν₂/4 − ν₃/3 − ν_∞/2** | Discharges L10. Arithmetic route, not Riemann–Hurwitz (finding #3). Built 12 essays early and **without mentioning level 2** — the reader must not see the ending from here. Check: tabulate the formula for many N. |
| 14 | hecke-operators | T_n on S_k(Γ₀(N)); they commute; self-adjoint under the Petersson product; **spectral theorem ⟹ simultaneous eigenbasis**; a₁ = 1 ⟹ eigenvalues *are* the Fourier coefficients; multiplicativity | Where the prerequisite spectral theorem is cashed. Be precise: clean simultaneous diagonalizability needs gcd(n, N) = 1, and the clean statement needs 15 (Corrections #4). Discharges L11. |
| 15 | newforms-and-level | Oldforms, degeneracy maps, Atkin–Lehner, **newforms** as the honest basis, the level | Discharges L12. Without this, "the level" in Ribet's theorem is undefined. |

### PART IV — THE TWO WORLDS ARE ONE (3)

| # | Slug | Construction | Notes |
|---|------|--------------|-------|
| 16 | modular-representation | **Eichler–Shimura**: a weight-2 newform of level N gives ρ_{f,p} with tr ρ_f(Frob_ℓ) = a_ℓ(f), via J₀(N) | States L13. Stated, not proved — say so. Both worlds now emit the same kind of object. |
| 17 | two-l-functions | L(E, s) as an Euler product in the a_ℓ; L(f, s) from the coefficient sequence, its Euler product resting on multiplicativity (14); analytic continuation and functional equation | Merges the plan's two L-function threads. The video's framing — the Riemann zeta Euler product works because of unique factorization, and Hecke coefficients are multiplicative the same way — is a good one and connects back to 02. |
| 18 | modularity-theorem | The clues assembled (a_ℓ ↔ Fourier coefficients, conductor ↔ level), Taniyama–Shimura–Weil, then the **Modularity Theorem**: semistable (Wiles–Taylor 1995), general (BCDT 2001) | Discharges L14. Check: the conductor-11 curve against the level-11 newform's q-expansion, both computed independently and compared — the most convincing paragraph in the book for a 20-line script. |

### PART V — WILES'S MACHINE (anatomy, 3)

Not in the video at all. Opens with a standing banner: these three essays describe, they do not prove.

| # | Slug | Construction | Notes |
|---|------|--------------|-------|
| 19 | deformations | Mazur's deformation theory: lifting a fixed ρ̄ to characteristic 0, deformation conditions, the universal deformation ring R | The reframing that made modularity attackable: parametrize *all* lifts instead of chasing one. |
| 20 | r-equals-t | The Hecke algebra T as the modular side; the surjection R → T; "R = T ⟹ every lift is modular"; Taylor–Wiles patching and the numerical criterion, named not derived | The heart of the 1995 paper at the level of what the two objects are and why equality is the theorem. |
| 21 | the-mod-3-seed | Why the argument needs a residually modular starting point; **Langlands–Tunnell** supplies mod 3 (solvable base change, projective image in S₄); the **3–5 switch** when ρ̄_{E,3} is reducible | The step popular accounts omit: the proof needs somewhere to start, and that start is a different theorem from a different field. |

### PART VI — THE CONTRADICTION (4)

| # | Slug | Construction | Notes |
|---|------|--------------|-------|
| 22 | the-frey-curve | Assume a primitive solution aᵖ + bᵖ = cᵖ, p prime ≥ 5; normalize (coprimality, aᵖ ≡ −1 mod 4, bᵖ ≡ 0 mod 32); build **y² = x(x − aᵖ)(x + bᵖ)**; compute the discriminant 16(abc)^{2p} | Discharges L15. **Frey 1986**, following Hellegouarch (DDT p. 8) — not 1984 as the plan summary has it. Turn a solution into a curve whose properties are absurdly good. DDT's convention aᵖ + bᵖ = cᵖ adopted so the citable source and the essay agree. |
| 23 | semistable-and-modular | ℓ-adic valuations of the discriminant ⟹ multiplicative reduction at every bad prime ⟹ **semistable**, conductor = rad(abc) ⟹ **modular** by 18 | Discharges L16. The valuation computation is done in full — elementary, and the one place a reader can check Wiles's hypothesis is met. Uses 04. |
| 24 | the-frey-representation | ρ̄ = ρ̄_{Frey,p}: **irreducible** via Mazur's isogeny theorem (10), unramified outside 2 and p via **Néron–Ogg–Shafarevich** (10), finite at p, and **conductor exactly 2** | Discharges L17. Corrections #5 lives here: the *curve's* conductor is rad(abc); it is the *representation's* conductor that is 2. Level lowering exists to close exactly that gap. |
| 25 | ribet-and-the-end | **Ribet's level-lowering theorem** (1990) with its hypotheses; applied: modular of level rad(abc) ⟹ modular of level 2, so a weight-2 newform of level 2 exists. But μ = 3, ν₂ = 1, ν₃ = 0, ν_∞ = 2 gives 1 + 3/12 − 1/4 − 0 − 1 = 0, so **dim S₂(Γ₀(2)) = 0**. No such form. Hence no such representation, no such curve, no such solution. ∎ | Imports L18 and proves the L19 computation once essay 13 supplies its formula; the required debt then empties without disguising Ribet as proved. Closes with what the proof does *not* give: no effective bounds, no explanation of *why*, and the ABC-shaped questions still open. Note the slack — levels 1, 2, 3, 4 all give 0 — so the contradiction is not knife-edge. |

**Part I is complete** (01–05), and so is Part II (06–10). The collection now has an unbroken
reading path from Fermat's descent to the representation attached to a curve, with no forward
references anywhere in essays 01–10. Everything remaining is Part III onward plus essay 24.

## Sequencing notes (writing order is not reading order)

- **Write 01, 02, 22, 25 first.** The descent and the endgame are the two ends of the rope and are
  nearly independent of the middle. Having 25 drafted early keeps every construction essay honest
  about what it is *for* — the failure mode of expositions like this is beautiful machinery with no
  memory of the target.
- **Essay 09 is written. Deviation recorded:** the spine assigned "det = cyclotomic character" to 09,
  but a determinant is a statement about a *representation*, which does not exist until essay 10. The
  Weil pairing and the resulting oddness of $\bar\rho$ therefore move to **essay 10**, where they are
  also what supplies Ribet's "odd" hypothesis. Essay 09 keeps $E[2]$, $E[3]$, $E[n]\cong(\mathbb{Z}/n)^2$
  and the Tate module, and it stays one idea.
- ✅ **Essay 05 inherited the corrected continuity definition** (done). Essay 03 originally said a
  continuous map out of $G_{\mathbb{Q}}$ is one determined at a finite level. That is true only for a
  **discrete** target, so it holds for $\bar\rho\to\mathrm{GL}_2(\mathbb{F}_\ell)$ and is **false**
  for $\rho_{E,\ell}\to\mathrm{GL}_2(\mathbb{Z}_\ell)$ — which is continuous with open, hence
  infinite, image for a non-CM curve, so it factors through no finite quotient. The corrected statement
  uses both towers: $\rho$ is continuous exactly when every layer
  $G_{\mathbb{Q}}\to\mathrm{GL}_2(\mathbb{Z}/\ell^n)$ is determined at a finite level, while $\rho$
  itself need not be. *Finite level on each layer, not finite overall.* Essay 05 states it in that
  form and points at the single-layer case as the reason $\bar\rho$ is easier.
- **Writing order from here: 24, then 11 → 12 → 13, then 14 → 15 → 16 → 18,
  then 17, 19–21 and 02's second case.** This replaces an earlier note that put 24 next, which was
  wrong: essay 24 is about the *representation's* conductor, and the representation does not exist
  until essay 10, which needs essay 09's Tate module. 24 cannot precede them.
- **Essay 09 comes first, and it earns its place twice.** It needs only 04, 06 and 07, all written.
  And it is where the Frey curve's **full rational 2-torsion** is established — $x(x-a^p)(x+b^p)$ has
  three rational roots, so $E[2]\subset E(\mathbb{Q})$ — which is exactly the extra structure that may
  sharpen Mazur's threshold from $p>7$ to $p\geq5$. That is registered as
  `09-frey-full-2-torsion` so the connection is structural rather than a remark.
- **A late Part IV is about meaning, not the ledger.** Essay 25's input (A) says a weight-2 newform of
  level $\operatorname{rad}(abc)$ has the same Galois representation. That assumption is allowlisted,
  but the *sentence* is a string of undefined terms until 12, 15 and 16 exist. An allowlisted
  assumption still needs its vocabulary built; do not treat 14–18 as optional because the register
  already accounts for them.

- **Then 13.** It is the only formula essay 25 evaluates. Discharging that debt early makes the
  closing arithmetic self-contained and gives the middle of the book a visible payoff.
- **Then 03, 04, 05, 09, 10, 24.** Essay 05 remains the highest-dependency node: 10, 16, 18, 19, 21
  and 24 all speak its language. Write the abstract sequence to the minimum depth those consumers
  demonstrably require, while still meeting the reading-order contract.
- **Then complete 11–12 and 14–18.** Essay 13 is intentionally allowed to arrive early in writing
  order, but it remains essay 13 in reading order. Finish the modular-forms bridge before removing
  essay 23's modularity debt.
- **Part V last.** It is the likeliest place to overreach and has no video support to lean on. If an
  essay starts growing lemmas, cut it back.
### Two decisions taken in advance (Part III scope control)

Both were settled before drafting, because writing the course version and then finding the chain used a
tenth of it is how a five-essay Part becomes nine.

1. **Essay 14 proves the coefficient step and imports the eigenbasis.** The chain needs exactly one
   thing from Hecke theory: that $a_\ell(f)$ is meaningful, i.e. that for a normalised eigenform the
   eigenvalues *are* the Fourier coefficients. That is short and illuminating, so it is proved
   (`14-hecke-coefficients`). The apparatus behind existence — Petersson inner product,
   self-adjointness, multiplicity one — is a course, is never evaluated by the closing argument, and is
   imported as `14-eigenbasis` for $\gcd(n,N)=1$. Do not write the course.
2. **Essay 13 imports the valence formula and proves the dimension formula from it.** Valence follows
   from a contour integral around the fundamental domain: provable at this level, genuinely beautiful,
   and a whole essay. Part III is already the riskiest stretch, so it is imported
   (`13-valence-formula`) and 13 derives $\dim S_2(\Gamma_0(N))$ from it and essay 11's counts. The
   evidence for the result is not the proof anyway: `checks/dim_s2_gamma0.py` verifies it across every
   level below 400, against the classical genus-zero list and against LMFDB at level 11. That is a
   deliberate decision and it cost one allowlist entry, not a discovery made halfway through drafting.

### Part III is where this collection would die

Five essays of real analysis with no visible Fermat content, and the reader must hold on until 16 pays
it off. Two standing rules, not suggestions:

- **Keep the $X_0(11)$ thread running through every Part III essay.** The pieces already point at each
  other: $\dim S_2(\Gamma_0(11))=1$ from `checks/dim_s2_gamma0.py`, the newform `11.2.a.a`, the curve
  `11.a3`, its $a_\ell$ computed by hand in essay 08, and its $5$-torsion from essay 07. One concrete
  object the reader already knows, reappearing in each essay, is worth more than any amount of
  motivation in the abstract.
- **Put the payoff sentence in every Part III essay, not only at the end of the Part.** Each essay says
  which line of Ribet's hypotheses it is building toward.

- **`checks/` scripts get written with the essay, not after.** A numerical claim without its script is
  unverified, and this book has no other verification for numbers.

## Deviations from the video (deliberate)

Recorded so they are not "fixed" later by someone re-watching.

1. **The linear-algebra stretch (18–38%) is not written.** Prerequisite. The spectral theorem is
   recalled in 14 where it is used. Writing it out would put ~6 essays of standard material before
   anything Fermat-specific.
2. **Essay 02 adds the Kummer story.** The video proves n = 3 elementarily and treats UFDs separately;
   greps for cyclotomic, Kummer, regular primes, class number all come back genuinely empty. We
   connect them, because "the obvious generalization fails, and the failure is measured by the class
   number" is the honest reason the rest of the book exists.
3. **The conductor sits in 08**, with reduction types, not among the Part IV clues. Semistability —
   Wiles's hypothesis — is a statement about the conductor and is needed in 23.
4. **The two L-function threads merge** into 17, adjacent to the theorem they motivated.
5. **Part V is added wholesale** (see above).
6. **Traces-determine-semisimple-representations is promoted** into 05; it is used implicitly whenever
   two representations are called isomorphic.

## Corrections to the plan summary (keep these straight)

These correct the *written plan summary*, which is lossy. Where the video gets it right, that is noted.

1. **"Smooth cubic with at least one rational point."** The substantive condition is smoothness. For a
   general genus-1 curve, a rational point is what permits the Weierstrass form; once in Weierstrass
   form the point at infinity is there by construction. State it in that order.
2. **Short form exists over Q, but is not enough for integral arithmetic.** Characteristic zero permits
   y² = x³ + ax + b over Q, but the coordinate changes divide by 2 and 3. Reduction at those primes
   therefore requires the general integral form y² + a₁xy + a₃y = x³ + a₂x² + a₄x + a₆.
   Non-optional: the Frey curve's semistability argument happens at 2.
3. **Name the Tate module's ring.** T_p(E) is free of rank 2 **over Z_p**. "Free module of rank 2"
   without the ring is empty, and the point is that GL₂(Z_p) is where ρ lands.
4. **Simultaneous diagonalization of Hecke operators has hypotheses.** The clean statement is for T_n
   with gcd(n, N) = 1; eigenvalue-equals-Fourier-coefficient needs a₁ = 1 plus newform theory.
   "Behave perfectly under all Hecke operators simultaneously" overstates it at level N > 1.
5. **Conductor 2 belongs to the representation, not the curve.** The Frey curve's conductor is
   rad(abc), which is large. It is the conductor of **ρ̄_{Frey,p}** that is 2, because ρ̄ is unramified
   outside 2 and p and finite at p. Collapsing the two makes level lowering look unnecessary when
   closing that gap is its whole function. *The video keeps these distinct.*
6. **Irreducibility is a theorem, not an observation.** Ribet needs ρ̄ irreducible; Mazur's isogeny
   theorem supplies it. The summary lists "irreducible" as a property one notices.
7. **The irreducibility threshold — SETTLED (2026-07-26).** Both the plan summary and the video say
   p ≥ 5, and that is wrong. The correct shape is not a threshold at all: **Mazur's isogeny theorem
   gives a finite exceptional list.** Sutherland's 18.783 Fall 2023 Lecture 25, §25.4, states that
   ρ̄_{E,ℓ} is irreducible iff E admits no rational ℓ-isogeny, and that no elliptic curve over Q has
   one for
   ℓ ∉ {2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163}, the last four requiring CM. Two routes close
   the gap:
   - **Semistable refinement (DDT p. 8):** for a semistable curve the list collapses to ℓ ≤ 7, so the
     Frey representation is irreducible for **ℓ > 7** and the argument runs for p ≥ 11. *This is the
     route the essays take* — tightest, and the Frey curve is semistable anyway.
   - **Sutherland's route:** take ℓ > 163, legitimate because FLT was known for all exponents ≤ 163.
     Cheaper in machinery, much more expensive in imported results.
   Either way **p = 5 and p = 7 are outside the Frey argument**, since both are in Mazur's list. The
   **live sub-question: does full rational 2-torsion sharpen this to p ≥ 5?** Plausible and probably
   true. The Frey curve has E[2] ⊂ E(Q), so a reducible ρ̄_{E,p} yields a rational cyclic subgroup of
   order 2p or 4p, hence a non-cuspidal rational point on X₀(2p) or X₀(4p); ruling those out for p ≥ 5
   would close it. Note **X₀(10) has genus 0**, so the 2p level alone cannot settle p = 5 — the
   argument has to live at 4p. **Four source attempts have failed to produce a Tier A statement:** DDT
   gives only the semistable ℓ > 7, Sutherland's Lecture 25 puts 5 and 7 *inside* Mazur's list,
   Freitas–Siksek is about totally real fields with only its abstract reachable, and the numdam page
   carries no numbered statements. Search snippets do assert p ≥ 5, but a snippet is Tier B and
   uncitable under our own rule — which is exactly the rule's purpose.
   **Progress made, 2026-07-26 — a generic-case argument, derived here, not sourced.**
   `checks/frey_irreducibility.py`. Reducibility of $\bar\rho_{E,p}$ forces the characteristic
   polynomial of every Frobenius to split over $\mathbb{F}_p$, so with $\operatorname{tr}=a_\ell$ and
   $\det=\ell$ it forces $a_\ell^2-4\ell$ to be a square mod $p$ at every good $\ell$. **One
   non-square proves irreducibility.** And full rational $E[2]$ pins $a_\ell$ at small $\ell$: the
   $2$-torsion is rational, so it injects into $E(\mathbb{F}_\ell)$ at good odd $\ell$, giving
   $4\mid\#E(\mathbb{F}_\ell)$ and hence $a_\ell\equiv\ell+1\pmod4$; with Hasse that leaves
   $a_3=0$, $a_5=\pm2$, $a_7\in\{0,\pm4\}$. Three uniform witnesses follow:

   | $p$ | witness $\ell$ | pinned value | $a_\ell^2-4\ell \bmod p$ | non-square? |
   |---|---|---|---|---|
   | 5 | 3 | $a_3=0$ | 3 | yes |
   | 7 | 5 | $a_5^2=4$ | 5 | yes |
   | 5 | 7 | $a_7^2\in\{0,16\}$ | 2 or 3 | both yes |

   So **$\bar\rho_{E,5}$ and $\bar\rho_{E,7}$ are irreducible whenever the witness prime is good**,
   by an elementary argument with no modular curves in it. Verified over 1000 Frey-shaped semistable
   triples; every curve whose witness prime is bad is still settled by some other prime.
   **What this is not.** It is not the uniform theorem. When the witness prime divides $abc$ it is bad,
   and no finite set of witnesses can cover every $abc$. So this is the generic case plus computation.
   Two consequences to handle if it is ever promoted to a shipped claim:
   `08-hasse` and `08-torsion-injects` are currently `background`, and the `depends_on` role rule would
   correctly refuse to let a chain result rest on them — they would need promoting, exactly as
   `07-uniformization` did.

   **So the dependency stays declared.** An *undeclared* dependency is the failure mode; a
   conservatively *declared* one costs one line on About and can be deleted the moment a real citation
   appears. Do not write p ≥ 5 before then. To close it: get Mazur 1978 itself, or any paper stating
   the X₀(4p) argument over Q by theorem number.
   **Consequence, now recorded rather than implicit:** the collection depends on classical work it does
   not contain — Dirichlet and Legendre for n = 5 (1825), Lamé for n = 7 (1839). That is the register
   record `25-small-exponents`, which is why the chain's assumption count is 8 and not 7. Leaving it
   out was the one genuinely hidden dependency in the collection.
8. **Ribet lowers the level at primes ℓ ≠ p.** The condition at p (finite at p, weight 2) is separate
   and must be stated as such. *The video states the full hypotheses.*
9. **Chronology.** **Frey 1986, following Hellegouarch** (DDT p. 8) — the summary's ~1984 is wrong.
   Then Serre's conjectures 1987; Ribet 1990; Wiles's 1993 announcement, gap, Taylor–Wiles completion
   published 1995; general modularity BCDT 2001. **Ribet precedes Wiles** — level lowering is why
   Wiles's target mattered, not a consequence of it. The summary's ordering ("Ribet's theorem states…"
   after Wiles) inverts this.
10. **The normalization is stronger than "b even".** DDT: aᵖ ≡ −1 (mod 4) and bᵖ ≡ 0 (mod 32). The
    second is automatic once b is even and p ≥ 5, since then 2ᵖ | bᵖ — but state and spend it. It
    permits the integral minimal model at 2 with
    $\Delta_{\min}=2^{-8}(abc)^{2p}$; without that bridge, essay 22's displayed discriminant appears
    to change silently in essay 23.
11. **Use *semistable* consistently**, one word.

## Tech stack (unchanged from books 1 and 2)

- Plain HTML, one shared `static/style.css`, one small `static/theme.js`. No build step.
- `data/ledger.json` is the canonical proof-status register. `scripts/render_status.py --write`
  refreshes the committed About block; serving and deployment still require no build.
- KaTeX from CDN with SRI hashes **copied byte-for-byte from book 2's chapters**.
- Light/dark theme honouring `prefers-color-scheme`, toggle persisted in `localStorage`.
- Relative links only; `.nojekyll`; GitHub Pages from repo root.
- `checks/` — scripts backing every numerical claim, run by `verify.sh`.
- `resources/` — git-ignored; the transcript. `sources/` — git-ignored, empty, README lists wanted texts.

## verify.sh — what it must check

Port book 2's checks (count sync, link resolution, math-delimiter balance, prev/next contiguity,
quotation scan, no tracked PDFs), then add:

1. **Current ledger structure** — every written essay has proved/assumed/owed columns; every
   registered item is in the column dictated by its mode and carries canonical mode/role badges; and
   no essay's *What we already have* names an essay number ≥ its own.
2. **Proof-register sync** — every available `data/ledger.json` item maps to exactly one essay-ledger
   entry, and About's generated scope block matches the canonical data.
3. **Full-chain release gate, once the middle exists** — each essay's *still owed* must equal the
   previous debt minus its proofs and declared imports, and essay 25's owed column must be empty. This is not honestly
   checkable across the current jumps from 02 to 22 to 25, so the current script does not claim to.
4. **No book section numbers** — grep Reading rungs for `§`, `Ch.` + digit, `p.` + digit; fail on a
   hit. LMFDB labels and paper theorem numbers are permitted (Tier A) and must not be caught by this
   check, so match on the Tier C author names specifically.
5. **Every Tier A citation is logged** — extract LMFDB labels and paper theorem references from the
   essays and fail on any that is absent from `SOURCES.md`.
6. **No transcript prose** — the transcript is git-ignored but present; check no essay shares long
   n-grams with it.
7. Run every script in `checks/` and fail on non-zero exit.

## Status

Spine formulated (25 essays, 19 ledger lines) and checked against the transcript. Sourcing is
web-assisted and tiered; LMFDB and the DDT survey are both fetched and logged in `SOURCES.md`.

**Scaffolded and committed:** `index.html` with the full
25-essay contents (6 linked, 19 stubs), `about.html`, `static/`, `.nojekyll`, `.gitignore` excluding
`resources/` and `sources/`, `README.md` with GitHub Pages instructions, `verify.sh` — passing.

**Written:** 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 22, 23, 25 — the two ends of the rope, the valuation, the
elliptic-curve bridge through the representation, and the semistability check.
**Unwritten:** 11–21, 24.

⚠ **Essay 10 was written before 03 and 05, and it is the first essay whose declared debts are its own
vocabulary rather than peripheral.** It uses $G_{\mathbb{Q}}$ only as a group of field automorphisms,
which needs no machinery and carries the construction, the determinant and the oddness. But
`10-trace-formula` had to be *stated* rather than derived, because $\mathrm{Frob}_\ell$ is built in
essay 03. **Essay 10's stated trace formula: what can and cannot retire it.** The record
`10-trace-formula` bundles two claims, and they have different fates. Do not write an instruction to
"convert it when 05 lands" — an instruction that cannot be satisfied fails the same way as none.

- **The determinant half is done.** Essay 03 proves $\chi(\mathrm{Frob}_\ell)=\ell$ in the
  cyclotomic family, which is exactly what essay 10 asserted as
  $\det\bar\rho(\mathrm{Frob}_\ell)\equiv\ell$ once $\det\rho=\chi$ was derived there.
- **The trace half is not essay 05's business at all.** Deriving
  $\operatorname{tr}\bar\rho_{E,p}(\mathrm{Frob}_\ell)\equiv a_\ell$ needs two facts about elliptic
  curves over finite fields: that reduction $E[p]\to\tilde{E}[p]$ is injective at a good prime for
  $p\neq\ell$, and that the Frobenius *endomorphism* of $\tilde{E}$ satisfies
  $x^2-a_\ell x+\ell$ — which comes from $\#\tilde{E}(\mathbb{F}_\ell)=\deg(1-\phi)$ and the degree
  map being a quadratic form. That is essay **08**'s territory, not representation theory. Essay 05
  supplies ramification, conductors and continuity; none of it touches this.
- **So the retrofit belongs to 08.** `08-torsion-injects` already exists as a background record and is
  half of what is needed; the Frobenius endomorphism and the degree form are not in the collection at
  all. Retiring `10-trace-formula` means adding them to essay 08 and promoting
  `08-torsion-injects` to the chain — at which point the `depends_on` role rule applies, exactly as it
  did for `07-uniformization`.

Essay 03 also supplies the reason traces are the right invariant at all: $\mathrm{Frob}_\ell$ is a
*conjugacy class*, so only conjugation-invariant quantities can be read off it — which retro-justifies
essay 10's phrasing and is the hook essay 05 needs for `05-traces-determine`.

**L3, L4 and L5 are now discharged.** Essay 04 supplies $v_\ell$, $\mathbb{Z}_\ell$ and free modules;
essay 08 supplies reduction types, the conductor, and semistable ⟺ square-free conductor. Essay 23's
valuation argument is therefore unblocked and is the natural next essay: it needs only 04, 08 and 22,
all written, plus a declared import of modularity from 18.

**Check scripts, all passing:** `dim_s2_gamma0.py`, `frey_discriminant.py`,
`group_law.py`, `kummer_regular_primes.py`, `p_adic.py`, `reduction_and_conductor.py`,
`weierstrass_models.py`.

### Open items for the next pass

1. ~~Resolve the p > 7 threshold~~ — **done**, see Corrections #7. Mazur gives a finite exceptional
   list, not a threshold; the essays take the semistable refinement (ℓ > 7, so p ≥ 11); and the
   dependency on classical n = 5 and n = 7 is now an explicit register record. Essay 24 should cite
   Lecture 25 §25.4 for the list and DDT p. 8 for the semistable collapse.
1b. **Sutherland 18.783 Fall 2023 Lecture 25 is the single best source for Part V and essays 24–25**,
   fetched and logged. Numbered items to use: **theorem 25.2** Ribet in exactly the form the endgame
   needs; **25.4** Taylor–Wiles (semistable ⟹ modular) in modularity-lifting form; **25.5**
   Langlands–Tunnell; **25.6** no semistable curve over Q admits a rational 15-isogeny, proved
   concretely via X₀(15) having 8 rational points of which 4 are non-cuspidal, all of conductor
   50 = 2·5² and hence not semistable — that is a *provable* essay-21 centrepiece rather than a
   citation; **25.7** the 3–5 trick; **25.8** the assembled proof; **conjecture 25.1** Serre's
   modularity conjecture, proved by Khare–Wintenberger in 2008. Also **Serre's optimal level recipe**:
   N(ρ̄_{E,ℓ}) is the product of primes p with v_p(Δ_min) ≢ 0 mod ℓ. For the Frey curve
   Δ_min = 2^{-8}(abc)^{2ℓ}, so every odd bad prime has v_p ≡ 0 mod ℓ and drops out, leaving level 2.
   **That is the mechanism essay 24 owes** — currently 24 plans to assert conductor 2 via
   Néron–Ogg–Shafarevich; this recipe explains *why* it is 2.
1c. **Lecture 25 §25.2 prints Δ(E_{a,b,c}) = −16(abc)^{2ℓ}; the sign is wrong.** Δ = 16∏(eᵢ−eⱼ)²,
   a positive multiple of a square. Verified three ways (see `SOURCES.md`). Essay 22 keeps
   +16(abc)^{2p}. Do not "correct" the essay to match the source.
2. **Part V is unblocked** — DDT is fetched. Its citable structure so far: §1.2 and §1.5 (modular
   curves), §1.8 (Shimura–Taniyama), theorem 2.15 in §2.2 (ramification of the Frey representation),
   §3.2 (Serre's conjectures). Read the chapter openings for the deformation-theory and R = T sections
   before drafting 19–21.
3. **Essay 02's second case** is an outline, and `about.html` says so. Either complete it or leave the
   fence — but do not quietly upgrade the claim.
4. When 03, 05, 09–21, 23, 24 land, essay 25's four declared inputs (A)–(D) must become
   back-references and its ledger must close. `verify.sh`'s forward-dependency check will enforce the
   direction; the closing itself needs a human look.
5. **Sutherland's 18.783 Fall 2023 Lecture 24 covers far more of Parts III–IV than expected**, and is
   fetched and logged. It is titled *Modular forms and L-functions*, not anything about reduction —
   the minimal-model and conductor material sits at its end, in §24.7 and definitions 24.29–24.31.
   Numbered items usable later, all in that one lecture: **theorem 24.8** gives
   $\dim M_k(\Gamma)$ and $\dim S_k(\Gamma)$ with $\dim S_2(\Gamma)=g(\Gamma)$ (**essay 13** — note it
   is the genus form, so essay 13 still owes the arithmetic route to the genus); definition 24.5,
   24.6 and theorem 24.11, corollaries 24.12–24.13, theorem 24.14, corollary 24.15 and remark 24.16
   cover modular forms, cusp forms and Hecke operators including the $\gcd(n,N)=1$ restriction
   (**essays 12, 14**, and remark 24.16 confirms Corrections #4); definition 24.24, theorem 24.25 and
   theorem 24.27 give the $L$-function of a cusp form, its continuation and functional equation, and
   the newform Euler product, with definition 24.28 the elliptic-curve $L$-function (**essay 17**);
   theorem 24.1 is Taylor–Wiles for semistable curves and theorem 24.33 is BCDT (**essay 18**);
   theorem 24.37 is Eichler–Shimura in the Carayol form (**essay 16**). Read these before drafting
   Part III, and log each in `SOURCES.md` as it is used.
