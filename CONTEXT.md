# CONTEXT — authoring notes for *No Such Form*

Internal guide for the essay series. Not published as a reader-facing page.

Working title: **No Such Form** — the last essay's punchline is that a required modular form has
nowhere to live. (Alternative considered: *The Ladder*. Decide before `index.html` ships.)

## Premise

A single argument, built one rung at a time, from Fermat's own descent to the 1995 contradiction.
Every essay adds exactly one object or one theorem, and every essay closes by saying what the final
contradiction now has and what it still owes. The series is finished when the ledger is empty.

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

## What is proved and what is stated (hard fence, stated in `about.html`)

- **Proved in full**: FLT for n = 4 and n = 3; the reduction to prime exponents p ≥ 5; the Frey curve
  construction; its discriminant and conductor; its semistability; the conductor of its mod p
  representation; dim S₂(Γ₀(2)) = 0; and the final contradiction given the black boxes below.
- **Stated with hypotheses, not proved**: the Modularity Theorem (Wiles–Taylor 1995 semistable case;
  Breuil–Conrad–Diamond–Taylor 2001 general case), Ribet's level-lowering theorem, Mazur's isogeny
  theorem, Néron–Ogg–Shafarevich, Eichler–Shimura, Langlands–Tunnell.
- **Sketched as anatomy, explicitly labelled**: Wiles's machinery (Part V). The reader learns what the
  objects are and what the strategy is. Three essays cannot prove a 109-page paper and must not
  pretend to. **The video does not cover this material at all** — greps for deformation, universal
  (deformation ring), Langlands, Tunnell, base change, R = T all come back genuinely empty, variants
  included. Part V is entirely ours, which is also why it is the likeliest place to overreach.

So: a complete, checkable derivation of *FLT from modularity*, plus a guided tour of why modularity is
true. That framing goes in About verbatim.

## Reader

Has undergraduate algebra: linear algebra through eigenvectors and the spectral theorem for commuting
self-adjoint operators; groups, rings, fields, ideals, quotients. Has seen complex analysis. Assumes
**no** algebraic number theory, **no** Galois theory beyond the definition of a field extension, **no**
algebraic geometry, **no** modular forms.

Consequence: the video's 18–38% stretch (vector spaces, linear transformations, eigenvalues) is *not
written*. The spectral theorem is recalled in essay 14 where it earns its keep.

## The four-rung template (every essay)

Exact headings (`<section class="rung">`, `<h2>` with a numbered pill):

1. **What we already have** — objects this essay stands on, cited *by essay number*, never a vague
   back-reference. If it isn't in an earlier essay it isn't available: say so and add it to the owed
   column.
2. **The construction** — the one new object or theorem, motivated before it is defined. One idea.
3. **What it buys** — an original worked example, plus the specific later essay that consumes this.
4. **Reading** — topic-level citations only (see Sourcing), flagged unverified.

Then the **ledger** (`<section class="ledger">`): two columns, *discharged here* and *still owed*. The
owed column is the previous essay's owed minus what this one discharged. `verify.sh` checks the chain.

Header, footer, prev/next nav copied verbatim between essays.

## The master ledger

Essay 25 needs exactly these. Every line must be discharged, and no essay may use a line before the
essay that discharges it.

| # | Ledger line | Discharged in |
|---|---|---|
| L1 | FLT reduces to exponents p prime, p ≥ 5 | 01, 02 |
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
  modular functions; Sutherland's MIT 18.783). Cite author + notes title + topic + the date fetched.

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
   line before its discharging essay, and confirms essay 25's owed column is empty. Catches forward
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
| 02 | unique-factorization-and-n3 | **FLT for n = 3, proved** elementarily; then unique factorization as a *structure*: UFDs, the failure in Z[ζ₂₃], class numbers, regular primes, Kummer's partial result | The pivot of Part I. Video proves n = 3 by elementary number theory and introduces UFDs separately; we keep both and connect them — the naive generalization dies at p = 23, and *why* it dies is the first sign arithmetic needs structure. Completes L1. See Deviations #2. |
| 03 | galois-and-g-q | Field extensions and degree, the Galois correspondence, Q̄, **G_Q** as a profinite group, **Frobenius elements** at primes | Why G_Q resists direct study: not finite, no presentation. Motivates 05 instead of asserting it. |
| 04 | p-adics-and-modules | The p-adic valuation v_ℓ, Z_p and Q_p, "small means highly divisible"; modules over a ring, free modules and rank | **Not in my first draft; the transcript forced it.** Needed for T_p(E) ≅ Z_p² (09), GL₂(Z_p) (10), the finite-at-p condition (24), and the valuation computation (23). Discharges L3. |
| 05 | galois-representations | Continuous ρ : G_Q → GL₂(K); ramified/unramified primes; conductor of a representation; irreducibility; **traces of Frobenius determine a semisimple ρ** | The linearization move. The trace fact is load-bearing — it makes "these two representations are isomorphic" *checkable* in 18, so it lives here. Discharges L2. |

### PART II — ELLIPTIC CURVES (5)

| # | Slug | Construction | Notes |
|---|------|--------------|-------|
| 06 | elliptic-curves | General Weierstrass form, smoothness, the discriminant, the point at infinity; why y² = x³ + ax + b is not enough over Q | Corrections #1, #2. The short form fails at 2 and 3 and the Frey argument happens at 2. Get it right here or pay in 23. |
| 07 | the-group-law | Chord-and-tangent addition, E(Q) abelian, associativity (stated), E(C) ≅ C/Λ | The torus is not decoration: it is what makes a modular parametrization X₀(N) → E conceivable in Part IV. |
| 08 | reduction-and-conductor | Reduction mod ℓ; good, multiplicative, additive reduction; a_ℓ = ℓ + 1 − #E(F_ℓ); the conductor; **semistable ⟺ conductor squarefree** | Discharges L4, L5. Check: brute-force a_ℓ for a small curve. |
| 09 | torsion-and-tate-module | E[2] and E[3] explicitly, then E[n] ≅ (Z/n)² in characteristic 0; the **Tate module** T_p(E), free of rank 2 **over Z_p**; det = cyclotomic character | The video's route — compute two small cases, then generalize — is the right one; keep it. Name the ring (Corrections #3). Rank 2 is why the representations are 2×2. Discharges L6. |
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
| 25 | ribet-and-the-end | **Ribet's level-lowering theorem** (1990) with its hypotheses; applied: modular of level rad(abc) ⟹ modular of level 2, so a weight-2 newform of level 2 exists. But μ = 3, ν₂ = 1, ν₃ = 0, ν_∞ = 2 gives 1 + 3/12 − 1/4 − 0 − 1 = 0, so **dim S₂(Γ₀(2)) = 0**. No such form. Hence no such representation, no such curve, no such solution. ∎ | Discharges L18, L19; ledger empties. Closes with what the proof does *not* give: no effective bounds, no explanation of *why*, and the ABC-shaped questions still open. Note the slack — levels 1, 2, 3, 4 all give 0 — so the contradiction is not knife-edge. |

## Sequencing notes (write order, by dependency)

- **Write 01, 02, 22, 25 first.** The descent and the endgame are the two ends of the rope and are
  nearly independent of the middle. Having 25 drafted early keeps every construction essay honest
  about what it is *for* — the failure mode of expositions like this is beautiful machinery with no
  memory of the target.
- **05 is the highest-dependency node.** 10, 16, 18, 19, 21, 24 all speak in the vocabulary of Galois
  representations. Write it early and carefully; a wobble propagates everywhere.
- **13 before 14.** The dimension formula is arithmetic/geometry, the Hecke theory operator algebra;
  they are independent, and doing 13 first makes 25's punchline a *recall* rather than a new theorem
  arriving at the moment of maximum drama.
- **Part V last.** It is the likeliest place to overreach and has no video support to lean on. If an
  essay starts growing lemmas, cut it back.
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
2. **y² = x³ + ax + b is not the right form over Q.** The short form needs char ≠ 2, 3; arithmetic over
   Q must handle reduction at 2 and 3, so the general form y² + a₁xy + a₃y = x³ + a₂x² + a₄x + a₆ is
   required. Non-optional: the Frey curve's semistability argument happens at 2.
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
7. **The irreducibility threshold is p > 7, not p ≥ 5.** ⚠ Both the plan summary and the video say
   p ≥ 5. DDT (p. 8–9) is precise: Mazur shows a semistable elliptic curve over Q has no rational
   cyclic subgroup of order ℓ for **ℓ > 7**, and that is what gives irreducibility of ρ̄_{E,ℓ}. The
   exponents p = 5 and p = 7 are **not** covered by that route and are instead covered by the
   nineteenth-century results (Dirichlet and Legendre for 5, Lamé for 7), so the Frey-curve argument
   proper runs for p ≥ 11. **Do not write "p ≥ 5" into essay 24 without resolving this**, and verify
   against Mazur 1978 and Ribet 1990 directly before drafting. Flagged, not yet settled.
8. **Ribet lowers the level at primes ℓ ≠ p.** The condition at p (finite at p, weight 2) is separate
   and must be stated as such. *The video states the full hypotheses.*
9. **Chronology.** **Frey 1986, following Hellegouarch** (DDT p. 8) — the summary's ~1984 is wrong.
   Then Serre's conjectures 1987; Ribet 1990; Wiles's 1993 announcement, gap, Taylor–Wiles completion
   published 1995; general modularity BCDT 2001. **Ribet precedes Wiles** — level lowering is why
   Wiles's target mattered, not a consequence of it. The summary's ordering ("Ribet's theorem states…"
   after Wiles) inverts this.
10. **The normalization is stronger than "b even".** DDT: aᵖ ≡ −1 (mod 4) and bᵖ ≡ 0 (mod 32). The
    second is automatic once b is even and p ≥ 5, since then 2ᵖ | bᵖ — but state it, because the
    mod-32 condition is what the reduction type at 2 actually uses.
11. **Use *semistable* consistently**, one word.

## Tech stack (unchanged from books 1 and 2)

- Plain HTML, one shared `static/style.css`, one small `static/theme.js`. No build step.
- KaTeX from CDN with SRI hashes **copied byte-for-byte from book 2's chapters**.
- Light/dark theme honouring `prefers-color-scheme`, toggle persisted in `localStorage`.
- Relative links only; `.nojekyll`; GitHub Pages from repo root.
- `checks/` — scripts backing every numerical claim, run by `verify.sh`.
- `resources/` — git-ignored; the transcript. `sources/` — git-ignored, empty, README lists wanted texts.

## verify.sh — what it must check

Port book 2's checks (count sync, link resolution, math-delimiter balance, prev/next contiguity,
quotation scan, no tracked PDFs), then add:

1. **Ledger chain** — each essay's *still owed* = previous owed − this essay's discharged; essay 25's
   owed column empty.
2. **No forward dependencies** — no essay's *What we already have* names an essay number ≥ its own.
3. **No book section numbers** — grep Reading rungs for `§`, `Ch.` + digit, `p.` + digit; fail on a
   hit. LMFDB labels and paper theorem numbers are permitted (Tier A) and must not be caught by this
   check, so match on the Tier C author names specifically.
4. **Every Tier A citation is logged** — extract LMFDB labels and paper theorem references from the
   essays and fail on any that is absent from `SOURCES.md`.
5. **No transcript prose** — the transcript is git-ignored but present; check no essay shares long
   n-grams with it.
6. Run every script in `checks/` and fail on non-zero exit.

## Status

Spine formulated (25 essays, 19 ledger lines) and checked against the transcript. Sourcing upgraded to
web-assisted tiers; the LMFDB pipeline is tested and working. One check script written and passing
(`checks/dim_s2_gamma0.py`). Nothing written, nothing scaffolded.
