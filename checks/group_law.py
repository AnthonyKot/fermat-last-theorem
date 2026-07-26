#!/usr/bin/env python3
"""Exact group-law checks for essay 07's order-five example."""

from fractions import Fraction


O = None
A1, A2, A3, A4, A6 = map(Fraction, (0, -1, 1, 0, 0))


def on_curve(point):
    if point is O:
        return True
    x, y = point
    return y * y + A1 * x * y + A3 * y == (
        x**3 + A2 * x**2 + A4 * x + A6
    )


def negate(point):
    if point is O:
        return O
    x, y = point
    return x, -y - A1 * x - A3


def add(left, right):
    if left is O:
        return right
    if right is O:
        return left
    if right == negate(left):
        return O

    x1, y1 = left
    x2, y2 = right
    if left == right:
        denominator = 2 * y1 + A1 * x1 + A3
        if denominator == 0:
            return O
        slope = (3 * x1**2 + 2 * A2 * x1 + A4 - A1 * y1) / denominator
        intercept = (-x1**3 + A4 * x1 + 2 * A6 - A3 * y1) / denominator
    else:
        slope = (y2 - y1) / (x2 - x1)
        intercept = (y1 * x2 - y2 * x1) / (x2 - x1)

    x3 = slope**2 + A1 * slope - A2 - x1 - x2
    y3 = -(slope + A1) * x3 - intercept - A3
    result = (x3, y3)
    assert on_curve(result)
    return result


def multiple(n, point):
    result = O
    for _ in range(n):
        result = add(result, point)
    return result


P = (Fraction(0), Fraction(0))
expected = [
    O,
    P,
    (Fraction(1), Fraction(-1)),
    (Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(-1)),
    O,
]

assert all(on_curve(point) for point in expected)
assert [multiple(n, P) for n in range(6)] == expected
assert negate(P) == expected[4]

# Check the complete addition table of the five displayed points. This is a
# finite consistency check, not a proof of associativity for every elliptic curve.
subgroup = expected[:5]
for i, left in enumerate(subgroup):
    for j, right in enumerate(subgroup):
        assert add(left, right) == subgroup[(i + j) % 5]

print("multiples of P=(0,0):", expected)
print("order of P: 5")
print("five-by-five subgroup addition table: verified")
