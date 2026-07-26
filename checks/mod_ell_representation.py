"""Checks for essay 10: the mod ell representation, its determinant, and traces.

Three things are verified, none of them requiring a Galois group to be built:

  * The Weil-pairing algebra behind det rho = the cyclotomic character. For the
    standard alternating form e(v, w) = zeta^(v ^ w) on (Z/n)^2, acting by
    M in GL_2(Z/n) multiplies the pairing by det M. Checked exhaustively over
    every invertible M for several n -- this is the identity that forces
    det rho(sigma) to be the exponent by which sigma acts on roots of unity.

  * Oddness. Complex conjugation inverts every root of unity, so its cyclotomic
    character value is -1, and therefore det rho-bar(c) = -1. Checked as the
    statement that the exponent -1 is the one sending zeta to its inverse.

  * The falsifiable consequence of reducibility. If rho-bar_{E,m} is reducible
    with a Galois-stable line on which the action is trivial -- which is exactly
    what a *rational* subgroup of order m gives -- then trace = 1 + ell and so
        a_ell = ell + 1  (mod m)   for every good prime ell,
    equivalently m divides #E(F_ell). Verified for two curves that have such a
    subgroup, and refuted for the same two curves at a prime where they do not,
    so the test has teeth rather than being vacuous.

Run: python3 checks/mod_ell_representation.py
"""

import sys
from itertools import product
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reduction_and_conductor import discriminant, primes_up_to, reduction  # noqa: E402

# ===================== the Weil pairing forces the determinant ==============


def det2(M, n):
    (a, b), (c, d) = M
    return (a * d - b * c) % n


def wedge(v, w, n):
    """The standard alternating form on (Z/n)^2: v ^ w = v0 w1 - v1 w0."""
    return (v[0] * w[1] - v[1] * w[0]) % n


def apply(M, v, n):
    (a, b), (c, d) = M
    return ((a * v[0] + b * v[1]) % n, (c * v[0] + d * v[1]) % n)

for n in (2, 3, 4, 5, 7, 9):
    invertible = [
        ((a, b), (c, d))
        for a, b, c, d in product(range(n), repeat=4)
        if gcd(det2(((a, b), (c, d)), n), n) == 1
    ]
    assert invertible, n
    # Exhaustive in the vectors for small n; for the larger moduli a fixed
    # spanning sample suffices, since the identity is bilinear.
    vecs = list(product(range(n), repeat=2))
    if n > 5:
        vecs = [(0, 1), (1, 0), (1, 1), (1, n - 1), (2 % n, 3 % n)]
    for M in invertible:
        dM = det2(M, n)
        for v, w in product(vecs, repeat=2):
            # e(Mv, Mw) = e(v, w)^(det M), read in the exponent
            assert wedge(apply(M, v, n), apply(M, w, n), n) == (dM * wedge(v, w, n)) % n

# a basis pairs to a primitive root of unity, so the exponent determines the
# character value: this is why det rho(sigma) is exactly the cyclotomic exponent
for n in (3, 5, 7, 11):
    e1, e2 = (1, 0), (0, 1)
    assert wedge(e1, e2, n) == 1  # e(P, Q) = zeta, a primitive n-th root

# ===================== oddness: complex conjugation ========================

# Conjugation sends zeta -> zeta^(-1), so its cyclotomic exponent is -1 and
# det rho-bar(c) = -1. In Z/n that exponent is n - 1, and it is the unique one
# that inverts every root of unity.
for n in (3, 5, 7, 11, 13):
    inverting = [k for k in range(n) if all((k * a) % n == (-a) % n for a in range(n))]
    assert inverting == [(-1) % n], (n, inverting)
    assert (-1) % n != 1 % n  # so the representation is genuinely odd, not trivial

# ===================== reducibility predicts the point counts ==============

E11 = (0, -1, 1, 0, 0)  # conductor 11; rational 5-torsion, from essays 07 and 09
E36 = (0, 0, 0, 0, 1)  # y^2 = x^3 + 1; rational 3-torsion, from essay 09


def congruence_holds(coeffs, m, limit=200):
    """Does a_ell = ell + 1 mod m at every good prime? Returns (n_ok, failures)."""
    delta = discriminant(*coeffs)
    ok, bad = 0, []
    for ell in primes_up_to(limit):
        if delta % ell == 0 or ell == m:
            continue
        kind, a = reduction(coeffs, ell)
        if kind != "good":
            continue
        if (a - (ell + 1)) % m == 0:
            ok += 1
        else:
            bad.append(ell)
    return ok, bad

# where a rational subgroup of that order exists, the congruence holds
for coeffs, m, label in ((E11, 5, "conductor-11 at 5"), (E36, 3, "y^2=x^3+1 at 3")):
    ok, bad = congruence_holds(coeffs, m)
    assert bad == [], (label, bad)
    assert ok >= 40, (label, ok)

# where it does not, the congruence fails -- so the test is not vacuous
for coeffs, m, label in ((E11, 3, "conductor-11 at 3"), (E36, 5, "y^2=x^3+1 at 5")):
    ok, bad = congruence_holds(coeffs, m)
    assert bad, (label, "congruence unexpectedly held everywhere")
    assert len(bad) > 20, (label, len(bad))

# the congruence is exactly essay 08's divisibility, restated
delta11 = discriminant(*E11)
for ell in primes_up_to(200):
    if delta11 % ell == 0 or ell == 5:
        continue
    kind, a = reduction(E11, ell)
    if kind != "good":
        continue
    assert ((ell + 1 - a) % 5 == 0) == ((a - (ell + 1)) % 5 == 0)

# ===================== the Frey curve's mod 2 representation is trivial =====

# Full rational 2-torsion (essay 09) means every point of E[2] is fixed by every
# automorphism, so rho-bar_{E,2} is the identity map: maximally reducible.
# In matrix terms the image is the trivial subgroup of GL_2(F_2).
trivial_image = [((1, 0), (0, 1))]
assert det2(trivial_image[0], 2) == 1
assert all(apply(trivial_image[0], v, 2) == v for v in product(range(2), repeat=2))

print("PASS mod_ell_representation: det from the Weil pairing, oddness, reducibility congruence")
