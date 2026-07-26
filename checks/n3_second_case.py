#!/usr/bin/env python3
"""Exact arithmetic checks for essay 02's Eisenstein-integer descent.

The essay is the proof.  This script guards the expansion and unit bookkeeping
where a sign or coefficient error would invalidate the descent.
"""

from math import gcd


def mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Multiply a+b*w and c+d*w using w^2=-1-w."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def power(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    result = (1, 0)
    for _ in range(exponent):
        result = mul(result, value)
    return result


def norm(value: tuple[int, int]) -> int:
    a, b = value
    return a * a - a * b + b * b


LAMBDA = (1, -1)
OMEGA = (0, 1)


for m in range(-40, 41):
    for n in range(-40, 41):
        gamma = (m, n)
        c = m**3 + n**3 - 3 * m * n**2
        d = 3 * m * n * (m - n)
        assert power(gamma, 3) == (c, d)

        base = mul(LAMBDA, power(gamma, 3))
        omega_base = mul(OMEGA, base)
        omega2_base = mul(OMEGA, omega_base)
        assert sum(base) == 3 * d
        assert sum(omega_base) == 3 * (c - d)
        assert sum(omega2_base) == -3 * c

        # lambda does not divide m+n*w exactly when m+n is nonzero mod 3.
        if (m + n) % 3:
            assert c % 3
            assert sum(omega_base) % 9
            assert sum(omega2_base) % 9

        q = norm(gamma)
        assert q >= max(abs(m), abs(n), abs(m - n))
        assert norm(power(gamma, 3)) == q**3


# The rational 3-adic calculation: for coprime x,y with 3 | x+y and 3 not
# dividing xy, the quadratic factor has exactly one factor of 3.
for x in range(-120, 121):
    for y in range(-120, 121):
        if not x or not y or gcd(x, y) != 1 or x % 3 == 0 or y % 3 == 0:
            continue
        if (x + y) % 3:
            continue
        quadratic = x * x - x * y + y * y
        assert quadratic % 3 == 0
        assert quadratic % 9 != 0
        assert gcd(abs(x + y), quadratic) == 3


# Independent bounded search: no nonzero primitive integer solution is missed
# by the sign conventions used to move the 3-divisible term to the right.
bound = 500
cubes = {n**3: n for n in range(-bound, bound + 1)}
for x in range(-bound, bound + 1):
    for y in range(-bound, bound + 1):
        if not x or not y:
            continue
        z = cubes.get(x**3 + y**3)
        assert z is None or x * y * z == 0

print("  Eisenstein cube expansion and all three unit classes agree exactly")
print("  rational gcd and 3-adic lemmas checked on every primitive pair in range")
print(f"  no nonzero solution with |x|, |y|, |z| <= {bound}")
