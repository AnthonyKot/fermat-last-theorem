"""Toward the p >= 5 sharpening: irreducibility of rho-bar_(E,p) for Frey curves.

The open question is whether the Frey curve's *full rational 2-torsion*, on top of
semistability, pushes Mazur's threshold from p > 7 down to p >= 5. This script
does not settle it in general, and says so. What it establishes:

  A necessary condition for reducibility. If rho-bar_(E,p) is reducible then it is
  conjugate to upper triangular, so the characteristic polynomial of every
  Frobenius splits over F_p. With tr = a_l and det = l (essay 10), that means
      a_l^2 - 4l  is a square mod p
  at every good prime l. A single non-square PROVES irreducibility.

  Full rational 2-torsion pins a_l at small l. E[2] is rational, so it injects
  into E(F_l) at every good odd l, giving 4 | #E(F_l) = l + 1 - a_l, hence
  a_l = l + 1 (mod 4). Combined with Hasse, |a_l| <= 2 sqrt(l), this determines
  a_l almost completely for small l:
      l = 3:  a_3 = 0 mod 4, |a_3| <= 3  =>  a_3 = 0
      l = 5:  a_5 = 2 mod 4, |a_5| <= 4  =>  a_5 = +-2, so a_5^2 = 4
      l = 7:  a_7 = 0 mod 4, |a_7| <= 5  =>  a_7 in {0, +-4}

  Two clean consequences, each an elementary complete argument:
      p = 5, 3 good:  a_3^2 - 12 = 3 mod 5, a non-square  =>  irreducible
      p = 7, 5 good:  a_5^2 - 20 = 5 mod 7, a non-square  =>  irreducible
      p = 5, 7 good:  a_7^2 - 28 in {2, 3} mod 5, both non-squares => irreducible

  What is NOT proved. When the special prime divides abc it is a bad prime and the
  argument needs a different witness. Every curve tested is still settled by some
  other prime, but there is no uniform choice -- abc may be divisible by any
  finite set of primes -- so this is a generic-case argument plus computation, not
  the uniform theorem. Do not write "p >= 5" on the strength of it.

Run: python3 checks/frey_irreducibility.py
"""

import sys
from math import gcd, isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from frey_semistable import frey_minimal  # noqa: E402
from reduction_and_conductor import discriminant, primes_up_to, reduction  # noqa: E402


def squares_mod(p):
    return {x * x % p for x in range(p)}


def frey_triples(bound=400):
    """Frey-shaped triples: A = 3 mod 4, B = 0 mod 32, pairwise coprime."""
    out = []
    for A in range(3, bound, 4):
        for B in range(32, bound, 32):
            C = A + B
            if gcd(A, B) == 1 and gcd(A, C) == 1 and gcd(B, C) == 1:
                out.append((A, B, C))
    return out


TRIPLES = frey_triples()
assert len(TRIPLES) > 900

# ---- full rational 2-torsion forces 4 | #E(F_l), and Hasse then pins a_l ----

for A, B, C in TRIPLES[:120]:
    m = frey_minimal(A, B)
    d = discriminant(*m)
    for ell in primes_up_to(60):
        if ell == 2 or d % ell == 0:
            continue
        kind, a = reduction(m, ell)
        if kind != "good":
            continue
        assert (ell + 1 - a) % 4 == 0, (A, B, ell, a)      # E[2] is rational
        assert a * a <= 4 * ell, (A, B, ell, a)            # Hasse

# the pinned values at the three smallest useful primes
PINNED = {3: {0}, 5: {-2, 2}, 7: {0, -4, 4}}
for ell, expected in PINNED.items():
    seen = set()
    for A, B, C in TRIPLES:
        m = frey_minimal(A, B)
        if discriminant(*m) % ell == 0:
            continue
        kind, a = reduction(m, ell)
        if kind == "good":
            seen.add(a)
    assert seen <= expected, (ell, seen, expected)
    # and the pinning is forced, not merely observed:
    forced = {a for a in range(-2 * isqrt(ell) - 1, 2 * isqrt(ell) + 2)
              if (ell + 1 - a) % 4 == 0 and a * a <= 4 * ell}
    assert forced == expected, (ell, forced, expected)

# ---- the three uniform witnesses -------------------------------------------

WITNESS = [
    (5, 3, {0}),          # a_3 = 0
    (7, 5, {-2, 2}),      # a_5^2 = 4
    (5, 7, {0, -4, 4}),   # a_7^2 in {0, 16}
]
for p, ell, avals in WITNESS:
    sq = squares_mod(p)
    for a in avals:
        assert (a * a - 4 * ell) % p not in sq, (p, ell, a)

# ---- so: irreducible whenever the witness prime is good ---------------------

for p, ell, _ in WITNESS:
    sq = squares_mod(p)
    n = 0
    for A, B, C in TRIPLES:
        m = frey_minimal(A, B)
        if discriminant(*m) % ell == 0:
            continue
        kind, a = reduction(m, ell)
        if kind != "good":
            continue
        assert (a * a - 4 * ell) % p not in sq, (p, ell, A, B, a)
        n += 1
    assert n > 100, (p, ell, n)

# ---- and the remaining curves are settled case by case, not uniformly -------

for p in (5, 7):
    sq = squares_mod(p)
    special = [ell for q, ell, _ in WITNESS if q == p]
    stuck = []
    for A, B, C in TRIPLES:
        m = frey_minimal(A, B)
        d = discriminant(*m)
        if any(d % ell for ell in special):
            continue  # already handled by a uniform witness
        found = None
        for q in primes_up_to(300):
            if d % q == 0 or q == p:
                continue
            kind, a = reduction(m, q)
            if kind == "good" and (a * a - 4 * q) % p not in sq:
                found = q
                break
        if found is None:
            stuck.append((A, B))
    assert stuck == [], (p, stuck)

print("PASS frey_irreducibility: a_l pinned by rational E[2]; uniform witnesses at")
print("  (p,l) = (5,3), (7,5), (5,7); all remaining curves settled case by case.")
print("  NOT a uniform theorem -- see the module docstring.")
