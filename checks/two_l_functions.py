#!/usr/bin/env python3
"""Checks for essay 17: the level-11 curve and newform Euler factors.

This script uses exact integer arithmetic to check one example:

  * f_11 = q product_n (1-q^n)^2(1-q^(11n))^2;
  * a_ell(f_11) = ell + 1 - #E(F_ell) at every good prime ell < 180 for
    E: y^2+y=x^3-x^2;
  * the good-prime quadratic recurrence and the bad-prime linear rule at 11;
  * multiplicative reconstruction of every coefficient a_n for 1 <= n < 180;
  * the common bad local polynomial 1-T, since a_11=1 on both sides.

It checks this finite level-11 example.  It does not prove analytic
continuation, the general newform Euler-product theorem, or modularity.

Run: python3 checks/two_l_functions.py
"""

from math import comb

from reduction_and_conductor import E11, primes_up_to, reduction


BOUND = 180
PRECISION = BOUND + 1


def eta_product_11(precision=PRECISION):
    """Return exact coefficients of q prod_n (1-q^n)^2(1-q^(11n))^2."""
    product = [1] + [0] * (precision - 1)
    for degree in range(1, precision):
        exponent = 2 + (2 if degree % 11 == 0 else 0)
        factor = [(-1) ** j * comb(exponent, j) for j in range(exponent + 1)]
        updated = [0] * precision
        for old_degree, old_coefficient in enumerate(product):
            if old_coefficient == 0:
                continue
            for j, factor_coefficient in enumerate(factor):
                target = old_degree + j * degree
                if target >= precision:
                    break
                updated[target] += old_coefficient * factor_coefficient
        product = updated
    return ([0] + product)[:precision]


def factor_prime_powers(n):
    """Return the pairs (ell, r) in n = product ell^r."""
    factors = []
    ell = 2
    while ell * ell <= n:
        if n % ell:
            ell += 1
            continue
        exponent = 0
        while n % ell == 0:
            n //= ell
            exponent += 1
        factors.append((ell, exponent))
        ell += 1
    if n > 1:
        factors.append((n, 1))
    return factors


def local_prime_power_coefficient(ell, exponent, trace):
    """Coefficient of T^exponent in the reciprocal local polynomial."""
    if ell == 11:
        # The bad polynomial is 1-a_11 T, so its reciprocal has a_11^r.
        return trace**exponent
    previous, current = 1, trace
    if exponent == 0:
        return previous
    if exponent == 1:
        return current
    for _ in range(2, exponent + 1):
        previous, current = current, trace * current - ell * previous
    return current


f11 = eta_product_11()
assert f11[1:14] == [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4]

# Compute every prime trace from the curve, then compare it with the independently
# expanded eta product.  The only bad prime is treated by reduction type.
curve_traces = {}
for ell in primes_up_to(BOUND - 1):
    kind, curve_trace = reduction(E11, ell)
    if ell == 11:
        assert kind == "split multiplicative"
    else:
        assert kind == "good"
    assert curve_trace == f11[ell], (ell, curve_trace, f11[ell])
    curve_traces[ell] = curve_trace

# At 11 both constructions have a_11=1, hence local polynomial 1-T.
assert curve_traces[11] == f11[11] == 1
bad_local_polynomial = (1, -curve_traces[11])
assert bad_local_polynomial == (1, -1)

# Reconstruct each Dirichlet coefficient from its local prime-power choices,
# multiplying the coefficients for distinct primes.
reconstructed = [0] * BOUND
reconstructed[1] = 1
for n in range(2, BOUND):
    value = 1
    for ell, exponent in factor_prime_powers(n):
        value *= local_prime_power_coefficient(
            ell, exponent, curve_traces[ell]
        )
    reconstructed[n] = value
    assert value == f11[n], (n, value, f11[n])

# The local polynomials displayed in the essay.
displayed = {
    2: (1, 2, 2),
    3: (1, 1, 3),
    5: (1, -1, 5),
    7: (1, 2, 7),
    11: (1, -1),
}
for ell, expected in displayed.items():
    if ell == 11:
        actual = (1, -curve_traces[ell])
    else:
        actual = (1, -curve_traces[ell], ell)
    assert actual == expected, (ell, actual, expected)


if __name__ == "__main__":
    print("PASS two_l_functions: the level-11 curve and eta product have matching")
    print(f"  prime traces and local rules, reconstructing every a_n for 1 <= n < {BOUND}")
    print("  the bad factor at 11 is 1-T because both sides have a_11=1")
    print("  this checks the example, not analytic continuation or the general theorem")
