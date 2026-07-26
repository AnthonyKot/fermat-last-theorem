#!/usr/bin/env python3
"""Independent coefficient checks for essay 06's two Weierstrass models."""


def discriminant(a1, a2, a3, a4, a6):
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = (
        a1 * a1 * a6
        + 4 * a2 * a6
        - a1 * a3 * a4
        + a2 * a3 * a3
        - a4 * a4
    )
    delta = -b2 * b2 * b8 - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6
    return (b2, b4, b6, b8), delta


def poly_add(*polys):
    result = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def poly_scale(poly, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items()}


def poly_mul(left, right):
    result = {}
    for (lx, ly), lc in left.items():
        for (rx, ry), rc in right.items():
            monomial = (lx + rx, ly + ry)
            result[monomial] = result.get(monomial, 0) + lc * rc
    return {m: c for m, c in result.items() if c}


def poly_pow(poly, exponent):
    result = {(0, 0): 1}
    for _ in range(exponent):
        result = poly_mul(result, poly)
    return result


# y^2 + y = x^3 - x^2
invariants, delta = discriminant(0, -1, 1, 0, 0)
assert invariants == (-4, 0, 1, -1)
assert delta == -11

# The singular comparison y^2 = x^3 + x^2.
singular_invariants, singular_delta = discriminant(0, 1, 0, 0, 0)
assert singular_invariants == (4, 0, 0, 0)
assert singular_delta == 0

# Y^2 = X^3 - 432X + 8208
_, short_delta = discriminant(0, 0, 0, -432, 8208)
assert short_delta == -23_944_605_696
assert short_delta == 6**12 * delta

# Verify:
# Y^2 - (X^3 - 432X + 8208)
#   = 46656(y^2 + y - x^3 + x^2)
# after X = 36x - 12 and Y = 216y + 108.
x = {(1, 0): 1}
y = {(0, 1): 1}
one = {(0, 0): 1}
X = poly_add(poly_scale(x, 36), poly_scale(one, -12))
Y = poly_add(poly_scale(y, 216), poly_scale(one, 108))
left = poly_add(
    poly_pow(Y, 2),
    poly_scale(poly_pow(X, 3), -1),
    poly_scale(X, 432),
    poly_scale(one, -8208),
)
right = poly_scale(
    poly_add(
        poly_pow(y, 2),
        y,
        poly_scale(poly_pow(x, 3), -1),
        poly_pow(x, 2),
    ),
    46656,
)
assert left == right

print("general model: b-invariants", invariants, "discriminant", delta)
print("short model: discriminant", short_delta, "= 6^12 * (-11)")
print("coordinate-change identity: verified coefficient by coefficient")
