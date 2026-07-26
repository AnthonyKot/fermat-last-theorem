"""Checks for essay 04: the valuation v_ell, the ring Z_ell, and free modules.

Every numerical claim essay 04 makes is recomputed here from definitions:

  * v_ell is additive on products and ultrametric on sums,
  * the absolute value |x|_ell = ell**(-v_ell(x)) is multiplicative and
    satisfies the strong triangle inequality,
  * the ell-adic digit expansion of a rational number is well defined and
    reconstructs the number modulo every power of ell,
  * the digit strings quoted in the essay are correct,
  * a matrix over Z_ell is invertible over Z_ell exactly when its
    determinant is a unit, which is a strictly stronger condition than
    being invertible over Q_ell.

Run: python3 checks/p_adic.py
"""

from fractions import Fraction
from itertools import product


def v(ell, x):
    """The ell-adic valuation of a rational number; +inf at zero."""
    if x == 0:
        return float("inf")
    x = Fraction(x)
    n, d = x.numerator, x.denominator
    e = 0
    while n % ell == 0:
        n //= ell
        e += 1
    while d % ell == 0:
        d //= ell
        e -= 1
    return e


def absval(ell, x):
    """|x|_ell, as an exact Fraction."""
    if x == 0:
        return Fraction(0)
    e = v(ell, x)
    return Fraction(1, ell**e) if e >= 0 else Fraction(ell ** (-e))


def residue(ell, x, n):
    """The image of x in Z/ell**n Z, for x with v_ell(x) >= 0."""
    x = Fraction(x)
    assert v(ell, x) >= 0, "not an ell-adic integer"
    m = ell**n
    return (x.numerator * pow(x.denominator, -1, m)) % m


def digits(ell, x, k):
    """The first k ell-adic digits of x, via a_{n+1} = a_n + ell**n b_n."""
    out = []
    a = 0
    for n in range(k):
        a_next = residue(ell, x, n + 1)
        b = (a_next - a) // ell**n
        assert 0 <= b < ell, f"digit out of range: {b}"
        out.append(b)
        a = a_next
    return out


def from_digits(ell, ds):
    """Partial sum of a digit string, as an ordinary integer."""
    return sum(b * ell**i for i, b in enumerate(ds))


def det2(m):
    (a, b), (c, d) = m
    return a * d - b * c


# ---------------------------------------------------------------- valuation

PRIMES = [2, 3, 5, 7, 11]
SAMPLE = sorted(
    {Fraction(n, d) for n in range(-18, 19) if n != 0 for d in range(1, 10)}
)

for ell in PRIMES:
    for x in SAMPLE:
        for y in SAMPLE:
            # additive on products
            assert v(ell, x * y) == v(ell, x) + v(ell, y)
            assert absval(ell, x * y) == absval(ell, x) * absval(ell, y)
            # ultrametric on sums, with equality when the valuations differ
            if x + y != 0:
                assert v(ell, x + y) >= min(v(ell, x), v(ell, y))
                assert absval(ell, x + y) <= max(absval(ell, x), absval(ell, y))
                if v(ell, x) != v(ell, y):
                    assert v(ell, x + y) == min(v(ell, x), v(ell, y))

# the ultrametric inequality is genuinely stronger than the triangle inequality
# only sometimes; check that the archimedean one can fail to be strengthened
assert absval(3, Fraction(1) + Fraction(2)) == max(absval(3, 1), absval(3, 2)) / 3
assert v(3, 1 + 2) == 1 > min(v(3, 1), v(3, 2)) == 0

# ------------------------------------------------------------------- digits

for ell in PRIMES:
    for x in SAMPLE:
        if v(ell, x) < 0:
            continue
        ds = digits(ell, x, 6)
        for n in range(1, 7):
            # the first n digits recover x modulo ell**n
            assert from_digits(ell, ds[:n]) % ell**n == residue(ell, x, n)

# the strings quoted in essay 04
assert digits(3, -1, 6) == [2, 2, 2, 2, 2, 2]
assert digits(3, Fraction(-1, 2), 6) == [1, 1, 1, 1, 1, 1]
assert digits(3, Fraction(1, 2), 6) == [2, 1, 1, 1, 1, 1]
assert digits(5, -1, 5) == [4, 4, 4, 4, 4]

# and the geometric series they encode: 1 + 3 + 9 + ... = -1/2 in Z_3
for n in range(1, 12):
    assert residue(3, Fraction(-1, 2), n) == from_digits(3, [1] * n) % 3**n
# 2 + 3 + 9 + ... = 1/2 in Z_3
for n in range(1, 12):
    assert residue(3, Fraction(1, 2), n) == from_digits(3, [2] + [1] * (n - 1)) % 3**n

# a rational with a denominator divisible by ell is not an ell-adic integer
for bad in [Fraction(1, 3), Fraction(2, 9), Fraction(-5, 3)]:
    assert v(3, bad) < 0

# ...but it is a 5-adic integer, and being an ell-adic integer for every ell
# except finitely many is what "rational" means
assert v(5, Fraction(1, 3)) == 0

# ------------------------------------------------------- free modules, GL_2

# essay 04's two matrices, over Z_3
scaling = ((3, 0), (0, 1))
shear = ((1, 1), (0, 1))

assert det2(scaling) == 3 and v(3, det2(scaling)) == 1  # not a unit in Z_3
assert det2(shear) == 1 and v(3, det2(shear)) == 0  # a unit in Z_3

# the inverse of the scaling matrix has an entry outside Z_3
inv_scaling = ((Fraction(1, 3), 0), (0, 1))
assert v(3, inv_scaling[0][0]) == -1
# ...while the shear's inverse is integral
inv_shear = ((1, -1), (0, 1))
assert all(v(3, e) >= 0 for row in inv_shear for e in row if e != 0)

# adjugate criterion: over Z_ell, M is invertible iff v_ell(det M) = 0.
# Verified exhaustively on all 2x2 matrices with entries in {0,...,8}: the
# adjugate is always integral, so invertibility is decided by the determinant.
for a, b, c, d in product(range(9), repeat=4):
    m = ((a, b), (c, d))
    det = det2(m)
    if det == 0:
        continue
    unit = v(3, det) == 0
    adj = ((d, -b), (-c, a))
    integral_inverse = all(v(3, Fraction(e, det)) >= 0 for row in adj for e in row if e != 0)
    assert unit == integral_inverse, m

print("PASS p_adic: valuation, absolute value, digits, GL_2(Z_ell) criterion")
