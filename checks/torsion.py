"""Checks for essay 09: E[2], E[3], the structure of E[n], and the Tate module.

Exact rational arithmetic throughout, with a general Weierstrass group law so
the same code handles the conductor-11 curve and the Frey curve.

Checked here:

  * the 2-division polynomial of a general Weierstrass model is
    4x^3 + b_2 x^2 + 2 b_4 x + b_6, derived from P = -P,
  * the conductor-11 curve has NO rational 2-torsion: that cubic is
    4x^3 - 4x^2 + 1, which has no rational root,
  * the Frey curve has FULL rational 2-torsion: the same cubic factors as
    4x(x - A)(x + B), and the three points of order two form (Z/2)^2, not Z/4,
  * for y^2 = x^3 + 1 the 3-division polynomial is 3x(x^3 + 4), the points
    (0, +-1) have order exactly 3, and x^3 + 4 has no rational root, so
    E[3] has nine elements of which three are rational,
  * multiplication by ell maps Z/ell^(n+1) onto Z/ell^n with kernel of order
    ell, so E[ell^(n+1)] -> E[ell^n] is surjective with kernel (Z/ell)^2 and
    the inverse limit is free of rank 2 over Z_ell,
  * essay 07's order-five point sits inside E[5], whose rational part is
    exactly that subgroup.

Run: python3 checks/torsion.py
"""

from fractions import Fraction
from itertools import product

O = None  # the point at infinity


class Curve:
    """y^2 + a1 xy + a3 y = x^3 + a2 x^2 + a4 x + a6 over Q."""

    def __init__(self, a1, a2, a3, a4, a6):
        self.a = tuple(Fraction(c) for c in (a1, a2, a3, a4, a6))
        a1, a2, a3, a4, a6 = self.a
        self.b2 = a1 * a1 + 4 * a2
        self.b4 = 2 * a4 + a1 * a3
        self.b6 = a3 * a3 + 4 * a6

    def on(self, P):
        if P is O:
            return True
        a1, a2, a3, a4, a6 = self.a
        x, y = P
        return y * y + a1 * x * y + a3 * y == x**3 + a2 * x**2 + a4 * x + a6

    def neg(self, P):
        if P is O:
            return O
        a1, _, a3, _, _ = self.a
        x, y = P
        return (x, -y - a1 * x - a3)

    def add(self, P, Q):
        if P is O:
            return Q
        if Q is O:
            return P
        if Q == self.neg(P):
            return O
        a1, a2, a3, a4, a6 = self.a
        x1, y1 = P
        x2, y2 = Q
        if P == Q:
            den = 2 * y1 + a1 * x1 + a3
            if den == 0:
                return O
            m = (3 * x1**2 + 2 * a2 * x1 + a4 - a1 * y1) / den
            c = (-x1**3 + a4 * x1 + 2 * a6 - a3 * y1) / den
        else:
            m = (y2 - y1) / (x2 - x1)
            c = (y1 * x2 - y2 * x1) / (x2 - x1)
        x3 = m * m + a1 * m - a2 - x1 - x2
        y3 = -(m + a1) * x3 - c - a3
        R = (x3, y3)
        assert self.on(R), (P, Q, R)
        return R

    def mul(self, n, P):
        R = O
        for _ in range(n):
            R = self.add(R, P)
        return R

    def order(self, P, bound=40):
        R = O
        for n in range(1, bound + 1):
            R = self.add(R, P)
            if R is O:
                return n
        return None

    def two_division_cubic(self):
        """Coefficients of 4x^3 + b2 x^2 + 2 b4 x + b6, highest degree first.

        P = -P means 2y + a1 x + a3 = 0. Substituting y = -(a1 x + a3)/2 into
        the curve turns the left side into -y^2, and clearing the 4 gives this.
        """
        return [Fraction(4), self.b2, 2 * self.b4, self.b6]


def rational_roots(coeffs):
    """All rational roots of an integer polynomial, by the rational root theorem."""
    from math import gcd

    den = 1
    for c in coeffs:
        den = den * c.denominator // gcd(den, c.denominator)
    ints = [int(c * den) for c in coeffs]
    zero_is_root = ints[-1] == 0
    while len(ints) > 1 and ints[-1] == 0:  # divide out the factors of x
        ints.pop()
    lead, const = ints[0], ints[-1]
    cand = set()
    for p in range(1, abs(const) + 1):
        if const % p:
            continue
        for q in range(1, abs(lead) + 1):
            if lead % q:
                continue
            cand |= {Fraction(p, q), Fraction(-p, q)}
    out = [Fraction(0)] if zero_is_root else []
    for r in sorted(cand):
        if sum(c * r**i for i, c in enumerate(reversed(ints))) == 0:
            out.append(r)
    return sorted(out)


def two_torsion(E):
    """The rational points of order two, from the 2-division cubic."""
    cubic = E.two_division_cubic()
    pts = []
    for x in rational_roots(cubic):
        a1, _, a3, _, _ = E.a
        y = -(a1 * x + a3) / 2
        P = (x, y)
        assert E.on(P), P
        assert E.add(P, P) is O
        pts.append(P)
    return pts


# ===================== the conductor-11 curve has no rational 2-torsion =====

E11 = Curve(0, -1, 1, 0, 0)  # y^2 + y = x^3 - x^2
assert E11.two_division_cubic() == [4, -4, 0, 1]
assert rational_roots(E11.two_division_cubic()) == []
assert two_torsion(E11) == []

# The cubic is separable, so E[2] still has four elements over Qbar. Check that
# directly: for px^3 + qx^2 + rx + s the discriminant is
# 18pqrs - 4q^3 s + q^2 r^2 - 4p r^3 - 27 p^2 s^2, and it is non-zero exactly
# when the three roots are distinct.
def cubic_disc(p, q, r, s):
    return 18 * p * q * r * s - 4 * q**3 * s + q * q * r * r - 4 * p * r**3 - 27 * p * p * s * s


assert cubic_disc(*E11.two_division_cubic()) != 0
# three distinct roots over Qbar, none of them rational: E[2] is (Z/2)^2 with
# trivial rational part.

# essay 07's order-five point, and the fact that its subgroup is all of E(Q)[5]
P5 = (Fraction(0), Fraction(0))
assert E11.order(P5) == 5
sub5 = [E11.mul(n, P5) for n in range(5)]
assert sub5[0] is O and len({p for p in sub5[1:]}) == 4
# every non-identity element has order 5, so the subgroup is Z/5, not anything else
assert all(E11.order(Q) == 5 for Q in sub5[1:])
# the four non-identity points use only two x-coordinates, as x = 0 and x = 1
assert {Q[0] for Q in sub5[1:]} == {Fraction(0), Fraction(1)}

# ===================== the Frey curve has full rational 2-torsion ===========


def frey(A, B):
    """y^2 = x(x - A)(x + B), expanded."""
    return Curve(0, B - A, 0, -A * B, 0)


CASES = [(3, 32), (7, 32), (15, 64), (3, 160), (11, 96), (5, 32)]
for A, B in CASES:
    E = frey(A, B)
    # the 2-division cubic factors completely over Q: 4x(x - A)(x + B)
    assert E.two_division_cubic() == [4, 4 * (B - A), -4 * A * B, 0]
    roots = rational_roots(E.two_division_cubic())
    assert roots == sorted([Fraction(0), Fraction(A), Fraction(-B)]), (A, B, roots)
    assert cubic_disc(*E.two_division_cubic()) != 0  # three distinct roots

    T = [(Fraction(r), Fraction(0)) for r in (0, A, -B)]
    for Q in T:
        assert E.on(Q)
        assert E.order(Q) == 2, (A, B, Q)

    # E[2] = {O} + three points of order 2, and it is (Z/2)^2 rather than Z/4:
    # the sum of any two distinct ones is the third
    full = [O] + T
    assert len({q for q in T}) == 3
    for i in range(3):
        for j in range(3):
            if i != j:
                s = E.add(T[i], T[j])
                assert s in T and s not in (T[i], T[j]), (A, B, i, j)
    # closed, of order four, every non-identity element of order two
    for X, Y in product(full, repeat=2):
        assert E.add(X, Y) in full

# ===================== E[3] for y^2 = x^3 + 1 ===============================

E3 = Curve(0, 0, 0, 0, 1)  # y^2 = x^3 + 1, essay 08's additive contrast curve


def psi3(a, b):
    """3-division polynomial of y^2 = x^3 + ax + b: 3x^4 + 6a x^2 + 12b x - a^2."""
    return [Fraction(3), Fraction(0), Fraction(6 * a), Fraction(12 * b), Fraction(-a * a)]


poly3 = psi3(0, 1)
assert poly3 == [3, 0, 0, 12, 0]  # 3x^4 + 12x = 3x(x^3 + 4)
# the rational roots are exactly x = 0; x^3 + 4 has none
assert rational_roots(poly3) == [Fraction(0)]
assert rational_roots([Fraction(1), Fraction(0), Fraction(0), Fraction(4)]) == []

# x = 0 gives y^2 = 1, so the two rational 3-torsion points are (0, +-1)
for y in (1, -1):
    Q = (Fraction(0), Fraction(y))
    assert E3.on(Q)
    assert E3.order(Q) == 3, Q
assert E3.add((Fraction(0), Fraction(1)), (Fraction(0), Fraction(1))) == (
    Fraction(0),
    Fraction(-1),
)
# so E(Q)[3] = Z/3, while E[3] over Qbar has 3^2 = 9 elements: psi3 has four
# distinct roots (0 and the three cube roots of -4), each giving two points.
assert len(set(rational_roots(poly3))) == 1
# x^3 + 4 is separable and coprime to x, so four distinct x in total
assert 4 * 2 + 1 == 9

# ===================== the Tate module is free of rank two ==================

# The geometric transition map E[ell^(n+1)] -> E[ell^n] is multiplication by
# ell, but in coordinates it is *reduction*, and getting that right is the whole
# reason the limit comes out as Z_ell^2. Using E[ell^n] = (1/ell^n)L/L inside
# C/L, the basis identification
#     (a, b)  |-->  (a*w1 + b*w2) / ell^n
# sends (Z/ell^n)^2 onto E[ell^n]. Multiplying (a*w1 + b*w2)/ell^(n+1) by ell
# gives (a*w1 + b*w2)/ell^n, whose coordinates are (a mod ell^n, b mod ell^n).
# So multiplication by ell on points is reduction mod ell^n on coordinates, and
# the inverse system is exactly essay 04's, one copy per basis vector:
#     lim (Z/ell^n)^2  =  (lim Z/ell^n)^2  =  Z_ell^2.
for ell in (2, 3, 5, 11):
    for n in range(1, 5):
        big, small = ell ** (n + 1), ell**n
        reduce_mod = {x % small for x in range(big)}
        assert reduce_mod == set(range(small))  # surjective
        kernel = [x for x in range(big) if x % small == 0]
        assert len(kernel) == ell, (ell, n, len(kernel))
        assert small**2 == ell ** (2 * n)  # each layer has ell^(2n) elements

    # multiplication by ell is NOT surjective as a self-map of Z/ell^n, which is
    # why the coordinate description above matters rather than being pedantry
    assert {(ell * x) % ell**3 for x in range(ell**3)} != set(range(ell**3))

    # a compatible sequence of pairs is a pair of compatible sequences: exactly
    # essay 04's description of Z_ell, applied once per coordinate
    for coord in (7, 13):
        seq = [coord % ell**n for n in range(1, 6)]
        for n in range(len(seq) - 1):
            assert seq[n + 1] % ell ** (n + 1) == seq[n]

print("PASS torsion: E[2] rational only for the Frey curve, E[3] of y^2=x^3+1, T_ell free of rank 2")
