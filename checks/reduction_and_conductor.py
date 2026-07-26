"""Checks for essay 08: reduction types, a_ell, and the conductor.

Everything is computed from a general Weierstrass model by brute force over
F_ell, with no elliptic-curve library:

  * the discriminant of a general integral model, from the b-invariants,
  * the bad primes are exactly the primes dividing the discriminant,
  * a_ell = ell + 1 - #E(F_ell) at primes of good reduction, checked against
    the Hasse bound and against the LMFDB newform coefficients of 11.2.a.a,
  * at a bad prime, the singular point of the reduced curve is located by
    partial derivatives, and a_ell = ell - #E^ns(F_ell) separates additive
    reduction (a_ell = 0) from multiplicative reduction (a_ell = +-1),
  * the two curves essay 08 works out land on the reduction types and
    conductors that LMFDB records for 11.a3 and 36.a4.

Run: python3 checks/reduction_and_conductor.py
"""

from itertools import product


def discriminant(a1, a2, a3, a4, a6):
    """Delta of y^2 + a1 xy + a3 y = x^3 + a2 x^2 + a4 x + a6."""
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4**3 - 27 * b6 * b6 + 9 * b2 * b4 * b6


def points_and_singular(coeffs, ell):
    """Affine F_ell-points of the reduced model, and its singular points.

    The affine equation is F(x, y) = y^2 + a1 xy + a3 y - x^3 - a2 x^2
    - a4 x - a6, so F_x = a1 y - 3x^2 - 2 a2 x - a4 and F_y = 2y + a1 x + a3.
    On a Weierstrass model the point at infinity is never singular.
    """
    a1, a2, a3, a4, a6 = (c % ell for c in coeffs)
    affine, singular = [], []
    for x, y in product(range(ell), repeat=2):
        f = (y * y + a1 * x * y + a3 * y - x**3 - a2 * x * x - a4 * x - a6) % ell
        if f:
            continue
        affine.append((x, y))
        fx = (a1 * y - 3 * x * x - 2 * a2 * x - a4) % ell
        fy = (2 * y + a1 * x + a3) % ell
        if fx == 0 and fy == 0:
            singular.append((x, y))
    return affine, singular


def reduction(coeffs, ell):
    """Reduction type at ell, and a_ell, from the point counts."""
    affine, singular = points_and_singular(coeffs, ell)
    delta = discriminant(*coeffs)
    if not singular:
        assert delta % ell != 0, f"smooth reduction but ell | Delta at {ell}"
        n = len(affine) + 1  # the point at infinity
        return "good", ell + 1 - n
    assert delta % ell == 0, f"singular reduction but ell does not divide Delta at {ell}"
    assert len(singular) == 1, f"expected one singular point at {ell}, got {singular}"
    n_ns = (len(affine) - 1) + 1  # drop the singular point, keep infinity
    a = ell - n_ns
    assert a in (0, 1, -1), f"bad a_ell at {ell}: {a}"
    if a == 0:
        return "additive", 0
    return ("split multiplicative" if a == 1 else "non-split multiplicative"), a


def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = [False] * len(sieve[i * i :: i])
    return [i for i, p in enumerate(sieve) if p]


def radical(n):
    n, r = abs(n), 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            r *= d
            while n % d == 0:
                n //= d
        d += 1
    return r * n if n > 1 else r


def squarefree(n):
    return radical(n) == abs(n)


# ============================== the conductor-11 curve, LMFDB 11.a3 ==========

E11 = (0, -1, 1, 0, 0)  # y^2 + y = x^3 - x^2
assert discriminant(*E11) == -11, discriminant(*E11)

# essay 06's short model of the same curve, whose discriminant is 6^12 * (-11)
short = -16 * (4 * (-432) ** 3 + 27 * 8208**2)
assert short == 6**12 * (-11) == -23944605696
# minimality in the sense of definition: Delta_min divides every model's Delta
assert short % discriminant(*E11) == 0
assert short // discriminant(*E11) == 6**12

# the bad primes are exactly the primes dividing Delta
bad11 = [p for p in primes_up_to(200) if discriminant(*E11) % p == 0]
assert bad11 == [11], bad11

# a_ell at the good primes. These are the coefficients of newform 11.2.a.a
# actually logged in SOURCES.md, so they are an external cross-check and not
# merely a record of this script's own output.
LMFDB_11 = {2: -2, 3: -1, 5: 1, 7: -2, 13: 4}
for ell, expected in LMFDB_11.items():
    kind, a = reduction(E11, ell)
    assert kind == "good", (ell, kind)
    assert a == expected, (ell, a, expected)

# the Hasse bound, at every good prime below 200
for ell in primes_up_to(200):
    if ell == 11:
        continue
    kind, a = reduction(E11, ell)
    assert kind == "good"
    assert a * a <= 4 * ell, (ell, a)

# essay 07 found a rational point of order 5 on this curve. Reduction at a
# good prime is injective on torsion of order coprime to ell, so 5 should
# divide #E(F_ell) at every good ell other than 5 -- and it does, at ell = 5
# as well, which the theorem does not promise.
for ell in primes_up_to(200):
    if ell == 11:
        continue
    _, a = reduction(E11, ell)
    assert (ell + 1 - a) % 5 == 0, (ell, ell + 1 - a)
assert 5 + 1 - reduction(E11, 5)[1] == 5  # #E(F_5) = 5 exactly

# the bad prime: multiplicative, so the curve is semistable
kind, a11 = reduction(E11, 11)
assert kind == "split multiplicative", kind
assert a11 == 1  # and LMFDB's newform has a_11 = 1
affine, singular = points_and_singular(E11, 11)
assert singular == [(8, 5)], singular  # the node located in the essay
assert len(affine) - 1 + 1 == 10 == 11 - 1  # #E^ns(F_11) = ell - 1, split case

# Independent confirmation that the singularity is a NODE with tangents defined
# over F_11, which is what "split" means. Translate the singular point to the
# origin and read off the quadratic part of
#   F(x, y) = y^2 + y - x^3 + x^2.
# With x = 8 + X and y = 5 + Y over F_11, the constant and linear terms vanish
# (that is what singular means) and the quadratic part should be Y^2 - X^2.
x0, y0 = 8, 5
for X in range(11):
    for Y in range(11):
        x, y = x0 + X, y0 + Y
        assert (y * y + y - x**3 + x * x) % 11 == (
            (Y * Y - X * X - X**3) % 11
        ), (X, Y)  # the full expansion, degree 3 included
# so the reduced curve at the node is Y^2 = X^2 + X^3, whose quadratic part
# Y^2 - X^2 = (Y - X)(Y + X) gives two distinct tangent lines with slopes in
# F_11. A node, and a split one.
tangent_slopes = sorted({s for s in range(11) if (s * s - 1) % 11 == 0})
assert tangent_slopes == [1, 10], tangent_slopes  # Y = X and Y = -X
assert len(tangent_slopes) == 2  # distinct => node, not cusp
assert a11 == 1  # and split, consistent with the slopes being rational

# semistable, so the conductor is the radical of the minimal discriminant
N11 = radical(discriminant(*E11))
assert N11 == 11 and squarefree(N11)

# ============================== y^2 = x^3 + 1, LMFDB 36.a4 ==================

E36 = (0, 0, 0, 0, 1)  # y^2 = x^3 + 1
assert discriminant(*E36) == -432 == -(2**4) * 3**3

bad36 = [p for p in primes_up_to(200) if discriminant(*E36) % p == 0]
assert bad36 == [2, 3], bad36

# additive at both, matching LMFDB's Kodaira symbols IV at 2 and III at 3
for ell in (2, 3):
    kind, a = reduction(E36, ell)
    assert kind == "additive", (ell, kind)
    assert a == 0

# mod 3 the cubic is a perfect cube, which is the triple root the essay shows
assert all((x**3 + 1 - (x + 1) ** 3) % 3 == 0 for x in range(3))

# so the curve is NOT semistable, and its conductor is not squarefree:
# LMFDB gives N = 36 = 2^2 * 3^2, with conductor exponent 2 at each bad prime
N36 = 36
assert N36 == 2**2 * 3**2
assert not squarefree(N36)
assert radical(N36) == 6 and radical(discriminant(*E36)) == 6
# the radical of the discriminant is 6, strictly smaller than the conductor:
# for an additive curve the conductor is NOT the radical
assert radical(discriminant(*E36)) != N36

# a good prime of this curve, for contrast
kind, a5 = reduction(E36, 5)
assert kind == "good" and a5 == 0  # #E(F_5) = 6

# ============================== the two directions of L5 ====================

# On the evidence of the two curves above, computed independently here and
# recorded by LMFDB: multiplicative at every bad prime <-> squarefree conductor.
assert reduction(E11, 11)[0].endswith("multiplicative") and squarefree(11)
assert reduction(E36, 2)[0] == "additive" and not squarefree(36)

if __name__ == "__main__":
    print("PASS reduction_and_conductor: bad primes, a_ell vs LMFDB, reduction types, conductors")
