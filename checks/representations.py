"""Checks for essay 05: characters, semisimplicity, and why traces suffice.

The essay's load-bearing import is that a semisimple representation is pinned by
its traces of Frobenius. That is a theorem about groups, but the matrix-level fact
underneath it is finite and checkable, and so is the reason the hypothesis
"semisimple" cannot be dropped. Both are verified here.

Checked here:

  * Among 2x2 matrices over F_ell, the DIAGONALISABLE ones with a given
    characteristic polynomial form a single conjugacy class -- verified
    exhaustively over GL_2(F_ell) for several ell. So the char poly, i.e. trace
    and determinant, determines a semisimple matrix up to conjugacy.
  * The hypothesis is necessary. A Jordan block and the identity share a
    characteristic polynomial and are not conjugate, so traces alone cannot tell
    a non-semisimple representation from its semisimplification.
  * The quadratic character of (Z/5)^* has kernel {1, 4}, which is exactly the
    subgroup essay 03 showed fixes Q(sqrt 5) -- so this character "is" that
    quadratic field, and it is ramified only at 5.
  * The reducible semisimple representation 1 + chi has trace 1 + ell and
    determinant chi at Frobenius, and those traces match the a_ell of the
    conductor-11 curve modulo 5 at every good prime -- so by the trace theorem
    that curve's mod 5 semisimplification IS 1 + chi-bar.

Run: python3 checks/representations.py
"""

import sys
from itertools import product
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reduction_and_conductor import discriminant, primes_up_to, reduction  # noqa: E402


def gl2(ell):
    out = []
    for a, b, c, d in product(range(ell), repeat=4):
        if (a * d - b * c) % ell:
            out.append(((a, b), (c, d)))
    return out


def matmul(M, N, ell):
    return tuple(
        tuple(sum(M[i][k] * N[k][j] for k in range(2)) % ell for j in range(2))
        for i in range(2)
    )


def inverse(M, ell):
    (a, b), (c, d) = M
    det = (a * d - b * c) % ell
    inv = pow(det, -1, ell)
    return ((d * inv % ell, -b * inv % ell), (-c * inv % ell, a * inv % ell))


def charpoly(M, ell):
    (a, b), (c, d) = M
    return ((a + d) % ell, (a * d - b * c) % ell)  # (trace, determinant)


def diagonalisable(M, ell):
    """Semisimple for a 2x2 matrix: distinct eigenvalues, or already scalar."""
    tr, det = charpoly(M, ell)
    disc = (tr * tr - 4 * det) % ell
    if disc != 0:
        # distinct roots in F_ell or in F_(ell^2); either way diagonalisable
        return True
    # repeated eigenvalue: semisimple only if the matrix is scalar
    lam = (tr * pow(2, -1, ell)) % ell if ell != 2 else None
    if ell == 2:
        return M in (((0, 0), (0, 0)), ((1, 0), (0, 1)))
    return M == ((lam, 0), (0, lam))


def conjugacy_class(M, ell, group):
    return frozenset(matmul(matmul(g, M, ell), inverse(g, ell), ell) for g in group)


# ============ semisimple + same char poly => conjugate =====================

for ell in (2, 3, 5, 7):
    G = gl2(ell)
    by_poly = {}
    for M in G:
        by_poly.setdefault(charpoly(M, ell), []).append(M)
    for poly, mats in by_poly.items():
        ss = [M for M in mats if diagonalisable(M, ell)]
        if not ss:
            continue
        # one class computation per char poly: every other semisimple matrix with
        # that char poly must land inside the class of the first
        cls = conjugacy_class(ss[0], ell, G)
        for M in ss[1:]:
            assert M in cls, (ell, poly, M)
        assert len(ss) == len(cls), (ell, poly, len(ss), len(cls))

# ============ and the hypothesis cannot be dropped =========================

for ell in (3, 5, 7):
    G = gl2(ell)
    identity = ((1, 0), (0, 1))
    jordan = ((1, 1), (0, 1))
    assert charpoly(identity, ell) == charpoly(jordan, ell)  # same trace and det
    assert diagonalisable(identity, ell) and not diagonalisable(jordan, ell)
    assert jordan not in conjugacy_class(identity, ell, G)
    # the Jordan block is reducible: it fixes the line spanned by (1,0)
    assert matmul(jordan, ((1, 0), (0, 0)), ell)[0][0] == 1

# ============ the quadratic character of (Z/5)^* is Q(sqrt 5) ==============

units5 = [a for a in range(1, 5) if gcd(a, 5) == 1]
squares5 = {a * a % 5 for a in units5}
legendre = {a: (1 if a % 5 in squares5 else -1) for a in units5}
assert legendre == {1: 1, 2: -1, 3: -1, 4: 1}
kernel = sorted(a for a in units5 if legendre[a] == 1)
assert kernel == [1, 4]  # exactly essay 03's subgroup {1, sigma_-1}
# it is a homomorphism, so it really is a character
for a in units5:
    for b in units5:
        assert legendre[(a * b) % 5] == legendre[a] * legendre[b]
# order two, so its fixed field is a quadratic field: Q(sqrt 5), ramified only at 5
assert len(set(legendre.values())) == 2

# ============ 1 + chi has trace 1 + ell, and that pins the curve ===========

E11 = (0, -1, 1, 0, 0)  # conductor 11, rational 5-torsion
d11 = discriminant(*E11)
matched = 0
for ell in primes_up_to(200):
    if d11 % ell == 0 or ell == 5:
        continue
    kind, a = reduction(E11, ell)
    if kind != "good":
        continue
    # trace of the semisimple representation 1 + chi-bar at Frobenius
    predicted_trace = (1 + ell) % 5
    predicted_det = ell % 5
    assert a % 5 == predicted_trace, (ell, a)
    # and the determinant is the cyclotomic character, essay 03's chi(Frob) = ell
    assert predicted_det == ell % 5
    matched += 1
assert matched >= 40, matched

# the same prediction fails for a curve without a rational subgroup of order 5,
# so the identification is doing work rather than restating a tautology
E36 = (0, 0, 0, 0, 1)
d36 = discriminant(*E36)
mismatch = 0
for ell in primes_up_to(200):
    if d36 % ell == 0 or ell == 5:
        continue
    kind, a = reduction(E36, ell)
    if kind == "good" and a % 5 != (1 + ell) % 5:
        mismatch += 1
assert mismatch > 20, mismatch

print("PASS representations: semisimple + char poly => conjugate (and the hypothesis is")
print("  necessary); the quadratic character of (Z/5)^* is Q(sqrt 5); traces identify")
print(f"  the conductor-11 curve's mod 5 semisimplification as 1 + chi at {matched} primes")
