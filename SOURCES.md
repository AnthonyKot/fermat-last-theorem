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
| 2026-07-26 | Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 24 (*Modular forms and L-functions*, dated 12/7/2023) | definition 24.28; §24.7; definitions 24.30, 24.31 and the following discussion | $a_p=p+1-\#E(\mathbb{F}_p)$ at good primes and $L_p(T)$ at bad ones, so $a_p\in\{0,\pm1\}$ there; the reduced singular cubic has one singular point, $E^{\mathrm{ns}}$ is a group and $a_p:=p-\#E^{\mathrm{ns}}(\mathbb{F}_p)$, with the triple root giving additive reduction and $a_p=0$ and the double root multiplicative reduction and $a_p=\pm1$ by whether the tangent slopes are rational; **semistable means no additive reduction at any prime**; for semistable $E$ the conductor is the product of the primes dividing $\Delta_{\min}$; **$N_E$ is square-free iff $E$ is semistable**, with $f_\ell=1$ at multiplicative primes, $f_\ell\geq2$ at additive primes and $f_\ell=2$ there for $\ell>3$, while $2$ and $3$ admit exponents up to $2^8$ and $3^5$ | 08 |
| 2026-07-26 | Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 24 (*Modular forms and L-functions*) | theorem 24.8, and the definitions of $\nu_2$, $\nu_3$, $\nu_\infty$ preceding it; remark 24.9 | $\dim M_k(\Gamma)$ and $\dim S_k(\Gamma)$ in terms of the genus $g(X(\Gamma))$ together with $\nu_2$, $\nu_3$ and $\nu_\infty$, with **$\dim S_2(\Gamma)=g(\Gamma)$**; $\nu_2(\Gamma)$ defined as the number of $\Gamma$-inequivalent $\mathrm{SL}_2(\mathbb{Z})$-translates of $i$ fixed by some $\gamma\in\Gamma$ other than $\pm I$, and $\nu_3$ likewise via $\rho=e^{2\pi i/3}$; $\nu_\infty$ the number of cusp orbits. **Verified 2026-07-26 against the PDF text**: the theorem gives $\dim S_k$ only for $k>2$ and states $\dim S_2(\Gamma)=g(\Gamma)$ as a separate line -- substituting $k=2$ into the $k>2$ formula returns $g-1$, so weight two is a separate case and not a vanishing coefficient. Remark 24.9 says a reader who knows some algebraic geometry may suspect a relationship between $S_2(\Gamma_0(N))$ and the regular differentials on $X_0(N)$ since their dimensions coincide, and confirms it. The lecture gives no proof of the dimension formulas (it cites Diamond--Shurman) and **never mentions Riemann--Hurwitz or the valence formula** -- checked by searching the whole file -- so essay 13's derivation is not following this source | 11, 13 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 24](https://math.mit.edu/classes/18.783/2023/LectureNotes24.pdf) (*Modular forms and L-functions*, dated 12/7/2023) | theorem 24.11; corollaries 24.12–24.15; remark 24.16; definition 24.18; lemma 24.19; theorems 24.20–24.21 | The lattice definition of $T_n$ and the relations $T_{mn}=T_mT_n$ for coprime indices and $T_{\ell^{r+1}}=T_{\ell^r}T_\ell-\ell^{k-1}T_{\ell^{r-1}}$; the exact coefficient formula $a_r(T_\ell f)=a_{\ell r}+\ell^{k-1}a_{r/\ell}$ and $a_1(T_nf)=a_n(f)$; at level $N$ these formulas and Hermitian behavior are clean for $(n,N)=1$, while primes dividing $N$ require modified operators; the Petersson product, simultaneous diagonalisation of commuting Hermitian operators, the one-dimensional level-one eigenbasis, and the two general-level failures repaired by the newspace: bad-prime operators and good-Hecke eigenspaces that need not be one-dimensional | 14, 15 |
| 2026-07-26 | [LMFDB elliptic curve](https://www.lmfdb.org/EllipticCurve/Q/36/a/4) | `36.a4` | The curve $y^2=x^3+1$ has conductor $36=2^2\cdot3^2$, minimal discriminant $-432=-2^4\cdot3^3$, $j=0$, and **additive** reduction at both $2$ (Kodaira IV) and $3$ (Kodaira III), with conductor exponent $2$ at each — so $\operatorname{rad}(\Delta_{\min})=6\neq36$ | 08 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.785, Fall 2021, Lecture 1](https://math.mit.edu/classes/18.785/2021fa/LectureNotes1.pdf) (*Absolute values and discrete valuations*, dated 9/8/2021) | definitions 1.2, 1.6, 1.7, 1.10; lemma 1.4; theorems 1.8, 1.9 | The absolute-value axioms, with condition 4 ($\lvert x+y\rvert\leq\max$) defining **nonarchimedean**; nonarchimedean iff $\lvert 1+\cdots+1\rvert\leq1$ for all $n$; equivalence of absolute values; the $p$-adic valuation $v_p(\pm\prod q^{e_q})=e_p$ with $v_p(0)=\infty$ and $\lvert x\rvert_p=p^{-v_p(x)}$; a valuation as a homomorphism with $v(x+y)\geq\min(v(x),v(y))$; **Ostrowski** — every nontrivial absolute value on $\mathbb{Q}$ is equivalent to some $\lvert\cdot\rvert_p$, $p\leq\infty$; the product formula $\prod_{p\leq\infty}\lvert x\rvert_p=1$. This is the *primary* treatment; Lecture 8 only recalls the axioms | 04 |
| 2026-07-26 | [Andrew Sutherland, MIT 18.785, Fall 2021, Lecture 8](https://math.mit.edu/classes/18.785/2021fa/LectureNotes8.pdf) | §8.1 and §8.1.1; definitions 8.1, 8.3, 8.7–8.9, 8.16; propositions 8.11, 8.17; example 8.13 | The absolute-value axioms and the non-archimedean strengthening $\lvert x+y\rvert\leq\max(\lvert x\rvert,\lvert y\rvert)$; ultrametric spaces are totally disconnected, every point of a ball is a centre, balls are disjoint or nested, and every open ball is closed; Cauchy sequences, completeness and the completion; directed sets, inverse systems and inverse limits; the valuation ring of a completion is $\varprojlim A/\pi^nA$; $\mathbb{Q}_p$ is the completion of $\mathbb{Q}$ for $\lvert x\rvert_p=p^{-v_p(x)}$ and $\mathbb{Z}_p\cong\varprojlim\mathbb{Z}/p^n\mathbb{Z}$ — **two equivalent definitions**; every $p$-adic integer has a unique digit expansion and every digit string occurs | 04 |

| 2026-07-26 | [Andrew Sutherland, MIT 18.783, Fall 2023, Lecture 25](https://math.mit.edu/classes/18.783/2023/LectureNotes25.pdf) (*Fermat's Last Theorem*, dated 12/12/2023) | §25.2, §25.4; conjecture 25.1; theorems 25.2, 25.4–25.8; corollary 25.3 | **Settles the irreducibility threshold.** $\bar\rho_{E,\ell}$ is irreducible iff $E$ admits no rational $\ell$-isogeny, and **Mazur's isogeny theorem gives this for $\ell\notin\{2,3,5,7,11,13,17,19,37,43,67,163\}$**, where $19,43,67,163$ need CM. The FLT argument may then take $\ell>163$ because FLT was already known for $\ell\leq163$. Chronology: Dirichlet and Legendre complete $n=5$ in **1825**, Lamé addresses $n=7$ in **1839**, Kummer 1847 for regular primes, computers to $4\times10^6$ by 1993; Euler's 1753 $n=3$ proof has a **fixable** error. $\Delta_{\min}(E_{a,b,c})=2^{-8}(abc)^{2\ell}$ assuming $\ell>3$; normalisation $a\equiv3\pmod4$, $b\equiv0\pmod2$; $E_{a,b,c}$ has no additive reduction anywhere, so it is semistable with squarefree conductor $\prod_{\ell\mid abc}\ell$. **Serre's optimal level**: $N(\bar\rho_{E,\ell})$ is the product of primes $p$ with $v_p(\Delta_{\min})\not\equiv0\bmod\ell$ — the mechanism that drops the Frey level to $2$. Theorem 25.2 is Ribet in the form needed; 25.4 Taylor–Wiles (semistable $\Rightarrow$ modular); 25.5 Langlands–Tunnell; **25.6 no semistable curve over $\mathbb{Q}$ admits a rational 15-isogeny**, proved via $X_0(15)$ having 8 rational points, 4 non-cuspidal, all of conductor $50=2\cdot5^2$; 25.7 the 3–5 trick; 25.8 the assembled proof. Serre's conjecture (25.1) proved by Khare–Wintenberger 2008 | 22, 24, 25, and Part V |
| 2026-07-26 | [Samir Siksek, *Modularity, Level Lowering, Frey Curves and Fermat's Last Theorem*](https://samirsiksek.github.io/siksek.github.io/sarajevo/talk1.pdf) (Sarajevo lectures, talk 1, dated 11 July 2016) | slides 4, 8, 11–15 | **Settles the threshold.** Slide 13, Theorem (Mazur): $E/\mathbb{Q}$ has no $p$-isogenies if $p$ satisfies *at least one* of — $p>163$, **or $p\geq5$ and $\#E(\mathbb{Q})[2]=4$ and the conductor of $E$ is squarefree**. Hence "by Mazur, for $p\geq5$, the Frey curve does not have $p$-isogenies". Slide 11: the normalisation $\gcd(a,b,c)=1$, $2\mid b$, $a^p\equiv-1\pmod4$, and for $Y^2=X(X-u)(X-v)$ the identity $\Delta=16u^2v^2(u-v)^2$, giving $\Delta=+16a^{2p}b^{2p}c^{2p}$ — a **third independent confirmation of the positive sign**. Slide 12: $\Delta_{\min}=a^{2p}b^{2p}c^{2p}/2^8$ and $N=\prod_{\ell\mid abc}\ell$. Slide 8, Ribet (simplified): for $p\geq3$, $E$ with no $p$-isogenies and modular, there is a newform of level $N_p=N/\prod_{q\|N,\;p\mid\mathrm{ord}_q(\Delta)}q$; slide 14 evaluates $N_p=2$. Slide 4: **there are no newforms at levels 1–10, 12, 13, 16, 18, 22, 25, 28, 60** — note this is a statement about *newforms*, wider than $\dim S_2(\Gamma_0(N))=0$, since 22, 28 and 60 have positive genus | 09, 22, 23, 24, 25 |

**Why Lecture 24 carries both modular forms and elliptic-curve reduction — it is not a mis-numbering.**
Three essays cite Lecture 24 for what look like two unrelated subjects: essay 11 for theorem 24.8, the
dimensions of $M_k(\Gamma)$ and $S_k(\Gamma)$; essays 06 and 08 for definitions 24.28–24.31 and §24.7,
covering minimal models, reduction types and the conductor. Both are correct, and the PDF settles it: the
footer on the page carrying §24.6, §24.7 and definition 24.29 reads *18.783 Fall 2023, Lecture #24, Page
10*, while theorem 24.8 sits on page 3 of the same file. The map of that one lecture, titled *Modular
forms and L-functions*:

| pages | contents | cited by |
|---|---|---|
| 1–3 | Taylor–Wiles (24.1) and BCDT (24.2); modular and cusp forms (24.3, 24.5, 24.6); **theorem 24.8**, the dimension formulas, with $\dim S_2(\Gamma)=g(\Gamma)$ | 11, 13, 18 |
| 3–7 | Hecke operators (24.2–24.4): theorem 24.11, corollaries 24.12–24.13, theorem 24.14, corollary 24.15, remark 24.16; Petersson definition 24.18, simultaneous-diagonalisation lemma 24.19, and theorems 24.20–24.21 | 14, 15 |
| 9–10 | $L$-functions of cusp forms and of elliptic curves: definition 24.24, theorems 24.25, 24.27, **definition 24.28** | 17 |
| 10–12 | **§24.7, definitions 24.29–24.30**: minimal models, the three reduction types, semistable | 06, 08 |
| 13–14 | **definition 24.31** the conductor; theorem 24.33 modularity; theorem 24.37 Eichler–Shimura | 08, 16, 18 |

The reason the two subjects share a lecture is structural rather than accidental: §24.6 defines the
$L$-function of an elliptic curve by an Euler product whose bad-prime factors depend on the reduction
type, so §24.7 has to supply reduction types, minimal models and the conductor immediately afterwards.
Reduction theory appears inside a modular-forms lecture **because the $L$-function needs it**. Do not
"fix" these pointers.

**Notation trap: Sutherland's $\ell$ and $p$ are the reverse of ours.** In 18.783 Lecture 25, $\ell$ is
the *residual* prime (the one the representation is mod, which for FLT is the Fermat exponent) and $p$
ranges over auxiliary primes of reduction. This collection fixes the opposite in essay 04: $p$ is the
Fermat exponent, $\ell$ is auxiliary. **Every quotation from that lecture must swap the letters.** It
already caused one error: Serre's optimal-level recipe was written into essays 05 and 23 in the source's
letters, inverting the convention both essays had just restated. In our letters it is
$N(\bar\rho_{E,p})=\prod\ell$ over the $\ell$ with $v_\ell(\Delta_{\min})\not\equiv0\pmod p$.

**Page-level evidence, so re-verification is one page read.** Four essays now cite Lecture 25 §25.3 and
three cite §25.4, so the pointers are load-bearing and worth pinning precisely. Read directly from the
PDF: **page 3** carries §25.3's opening, the $\ell$-torsion field, the representation on $E[\ell]$, and
the decomposition-group construction — $p\mathcal{O}_K=\mathfrak{p}_1\cdots\mathfrak{p}_r$, transitivity,
$D_\mathfrak{p}$, the isomorphism $\varphi:D_\mathfrak{p}\to\mathrm{Gal}(\mathbb{F}_\mathfrak{p}/\mathbb{F}_p)$,
and $\mathrm{Frob}_\mathfrak{p}:=\varphi^{-1}(\pi_p)$; it explicitly defers the factorisation into
distinct primes to its own Lecture 20. **Page 4** carries the conjugacy remark, the characteristic
polynomial $\lambda^2-(\operatorname{tr}A_p)\lambda+\det A_p$ with $\operatorname{tr}\equiv a_p$ and
$\det\equiv p$, the Tate module $T_\ell(E):=\varprojlim E[\ell^n]$ with multiplication-by-$\ell$
connecting maps, and $\rho_{E,\ell}:G_{\mathbb{Q}}\to\mathrm{GL}_2(\mathbb{Z}_\ell)$. **Pages 5–6**
carry §25.4: oddness from complex conjugation on the torus, the definition of irreducible, Mazur's
exceptional list with $19,43,67,163$ as the CM cases, and Serre's optimal level. So one long overview
section really does carry all of it, and the decomposition-group material sits inside the
elliptic-curves course because that lecture is an FLT overview drawing on the number-theory course.

**One disagreement, resolved against the source.** Lecture 25 §25.2 displays
$\Delta(E_{a,b,c})=-16(abc)^{2\ell}$. The sign is wrong: $\Delta=16\prod_{i<j}(e_i-e_j)^2$ for
$y^2=f(x)$ with $f$ monic of degree three, and that product is a square. Checked three independent
ways — the short-form identity $\Delta=-16(4A^3+27B^2)$ on the control curve $y^2=x^3-x$ (giving
$+64$, matching $16\prod=64$), the root-difference product, and the $b$-invariant expansion, the
latter two in `checks/frey_discriminant.py`. Essay 22 therefore keeps $\Delta=+16(abc)^{2p}$, and this
is exactly what the compute-it-yourself rule exists to catch.

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
