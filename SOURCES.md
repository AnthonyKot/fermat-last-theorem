# SOURCES — Tier A citation ledger

Every precise citation in the essays is logged here: what was fetched, when, and what it confirmed.
An essay citation absent from this table is treated as unverified and fails `verify.sh`.

Tier definitions are in `CONTEXT.md`. Briefly: **A** = fetched this session, citable precisely
(LMFDB labels, paper theorem numbers, named open notes). **B** = orientation only, never cited
(Wikipedia, blogs, forums, the video transcript). **C** = textbooks not owned, topic-level only.

## Verified

| Date | Source | Identifier | What it confirmed | Used in |
|---|---|---|---|---|
| 2026-07-25 | LMFDB newform page | `11.2.a.a` | Level 11, weight 2, trivial character orbit `11.a`, **space dimension 1**; coefficients a₁…a₁₃ = 1, −2, −1, 2, 1, 2, −2, 0, −2, −2, 1, −2, 4; associated to elliptic curve isogeny class `11.a` | 18 |
| 2026-07-26 | [LMFDB elliptic-curve isogeny class](https://www.lmfdb.org/EllipticCurve/Q/11/a/) | `11.a3`, class `11.a` | The model $y^2+y=x^3-x^2$ has label `11.a3`, discriminant $-11$ and conductor $11$; class `11.a` is attached to newform `11.2.a.a`; `11.a2`, not `11.a3`, is the $\Gamma_0(11)$-optimal curve | 06, 18, 25 |
| 2026-07-25 | Darmon–Diamond–Taylor, *Fermat's Last Theorem* (rev. 9 Sept 2007), Introduction | p. 3 | Fermat's n = 4 proof establishes the stronger claim that x⁴ + y⁴ = z² has no solution in coprime integers with xyz ≠ 0; such solutions correspond to rational points on v² = u³ − 4u. **The reduction: every integer n ≥ 3 is divisible either by an odd prime or by 4.** Euler proved ℓ = 3 in 1753 by a 3-descent on x³ + y³ = 1, and **his argument seems to have contained a gap**. ℓ = 5 settled ~100 years later | 01, 02 |
| 2026-07-25 | Darmon–Diamond–Taylor, Introduction | p. 6 | Kummer's regularity criterion: ℓ is regular iff ℓ does not divide the numerator of B_{2i} for 1 ≤ i ≤ (ℓ−3)/2, via h_ℓ = h⁺·h⁻ and an explicit formula for h⁻ | 02 |
| 2026-07-25 | Darmon–Diamond–Taylor, Introduction | p. 7 | Regularity holds heuristically for ~61% of primes; **it is still unknown whether infinitely many regular primes exist**, though infinitely many irregular ones is not hard. FLT verified for all odd prime exponents below four million. Faltings 1985 (Mordell) gives finitely many solutions per exponent, and FLT for a density-one set of exponents | 02, 25 |
| 2026-07-25 | Darmon–Diamond–Taylor, Introduction | p. 8 | **Mazur:** an elliptic curve over Q with square-free conductor has no rational cyclic subgroup of order ℓ when ℓ > 7. **Frey's insight is 1986** (following Hellegouarch), curve E : y² = x(x − a^ℓ)(x + b^ℓ), semistable, i.e. square-free conductor. **Normalization: a^ℓ ≡ −1 (mod 4) and b^ℓ ≡ 0 (mod 32).** Ramification of the ℓ-division field restricted to 2 and ℓ — precise statement at **DDT theorem 2.15, §2.2** | 22, 23, 24 |
| 2026-07-25 | Darmon–Diamond–Taylor, Introduction | p. 9 | **Mazur ⟹ ρ̄_{E,ℓ} irreducible for ℓ > 7** (using semistability); with Serre, surjective for ℓ > 7. Serre's conjectures at **DDT §3.2**; Shimura–Taniyama at **§1.8**; X₀(ℓ), X₁(ℓ) at **§1.2, §1.5**. Serre's conjecture predicted weight 2 **level 2** forms, which **do not exist because X₀(2) has genus 0**. Ribet reduced FLT to Shimura–Taniyama; Wiles proved it for semistable curves | 18, 24, 25 |
| 2026-07-26 | [Darmon–Diamond–Taylor, *Fermat's Last Theorem*](https://wstein.org/edu/2011/581g/misc/Darmon-Diamond-Taylor-Fermats_Last_Theorem.pdf) | §2.2, immediately before theorem 2.15 | For $A\equiv-1\pmod4$ and $B\equiv0\pmod{16}$, the displayed Frey model has an integral minimal Weierstrass model with $\Delta_{\min}=2^{-8}(ABC)^2$. Applied to $A=a^p$, $B=b^p$, $C=c^p$, this is $2^{-8}(abc)^{2p}$ | 22, 23 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 1](https://math.mit.edu/classes/18.783/2023/LectureNotes1.pdf) | definitions 1.1, 1.5; example 1.12 | An elliptic curve over a field is a smooth projective genus-one curve with a distinguished rational point; smoothness of a plane projective curve is detected by its partial derivatives; a nonsingular short Weierstrass cubic has genus one | 06 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 2](https://math.mit.edu/classes/18.783/2023/LectureNotes2.pdf) | §§2.1–2.3 | The general Weierstrass equation and its point at infinity; chord-and-tangent addition, the short-form formulas, and verification of the group axioms, with associativity requiring a separate argument | 06, 07 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 14](https://math.mit.edu/classes/18.783/2023/LectureNotes14.pdf) | definition 14.1; §14.4 | A lattice in $\mathbf C$, the complex torus $\mathbf C/L$, and the Weierstrass $\wp$-function construction that leads from a lattice to a cubic | 07 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 15](https://math.mit.edu/classes/18.783/2023/LectureNotes15.pdf) | theorem 15.1; corollary 15.12 | The map from $\mathbf C/L$ to the associated complex elliptic curve is a group isomorphism, and every elliptic curve over $\mathbf C$ arises from a lattice | 07 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 24](https://math.mit.edu/classes/18.783/2023/LectureNotes24.pdf) | discussion before and definition 24.29 | A short integral equation is always bad at 2 although a general integral equation for the same curve may be good there; global minimal models are defined in general Weierstrass form | 06, 08 |

## Cross-checks (computed independently, not cited)

| Claim | Independent routes | Agreement |
|---|---|---|
| a_p of the conductor-11 curve = coefficients of the level-11 newform | (1) brute-force point count of y² + y = x³ − x² over F_p; (2) η-product q-expansion of (η(z)η(11z))²; (3) LMFDB `11.2.a.a` | all three agree on p = 2, 3, 5, 7, 13, 17, 19, 23, 29, 31 |
| dim S₂(Γ₀(N)) formula | (1) `checks/dim_s2_gamma0.py` from μ, ν₂, ν₃, ν_∞; (2) classical genus-zero level list {1–10, 12, 13, 16, 18, 25}; (3) LMFDB dimension for level 11 | exact match; dim S₂(Γ₀(2)) = 0 and dim S₂(Γ₀(11)) = 1 |

## Wanted before drafting

| Needed for | Source | Why |
|---|---|---|
| Part V (19–21) | Darmon–Diamond–Taylor, *Fermat's Last Theorem* (survey) | The only freely available account covering deformation rings, R = T, and Langlands–Tunnell at the level Part V needs. Without it Part V is guesswork. **Blocking for 19–21.** |
| 25 | Ribet, Inventiones 1990 | Exact hypotheses of level lowering, by theorem number |
| 18 | Wiles, Annals 1995 | Exact statement of the semistable modularity theorem, by theorem number |
| 24 | Mazur 1978 | Exact statement of the isogeny theorem and its list of primes |
| 10, 24 | Néron–Ogg–Shafarevich criterion | Standard statement; find in Silverman (Tier C, topic-level) or open notes (Tier A) |
| 22 | Frey 1986 | The original construction, for the historical note |
