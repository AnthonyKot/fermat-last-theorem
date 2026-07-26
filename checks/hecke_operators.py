"""Checks for essay 14: Hecke operators and Fourier coefficients.

Everything is done with exact integer q-series.  The script checks the part of
Hecke theory the essay proves rather than the analytic input it explicitly
imports (the Petersson inner product and self-adjointness).

Checked here:

  * the coefficient formula

        a_r(T_n f) = sum_{d | gcd(r,n)} d^(k-1) a_(rn/d^2)(f);

  * the Hecke relations, including T_m T_n = T_mn for coprime m,n and the
    prime-power recurrence;
  * Delta is a simultaneous eigenform at level 1;
  * (eta(z)eta(11z))^2 is an eigenform for T_ell at the good primes
    ell = 2,3,5,7, with eigenvalue a_ell;
  * its good coefficients are multiplicative and satisfy the prime-power
    recurrence, while applying the good-prime formula at the bad prime 11
    fails -- the boundary essay 15 has to address.

Run: python3 checks/hecke_operators.py
"""

from math import comb, gcd


PREC = 400


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def hecke(coeffs, n, weight, out_prec):
    """Return T_n(sum a_r q^r), truncated before q^out_prec."""
    out = [0] * out_prec
    for r in range(1, out_prec):
        out[r] = sum(
            d ** (weight - 1) * coeffs[r * n // (d * d)]
            for d in divisors(gcd(r, n))
        )
    return out


def add_scaled(target, source, scalar):
    return [x + scalar * y for x, y in zip(target, source)]


def eta_product(exponents, precision=PREC):
    """q times a product of (1-q^d)^e_d, with exact coefficients."""
    out = [1] + [0] * (precision - 1)
    for d in range(1, precision):
        exponent = exponents(d)
        if not exponent:
            continue
        factor = [((-1) ** j) * comb(exponent, j) for j in range(exponent + 1)]
        new = [0] * precision
        for i, value in enumerate(out):
            if not value:
                continue
            for j, factor_value in enumerate(factor):
                degree = i + j * d
                if degree >= precision:
                    break
                new[degree] += value * factor_value
        out = new
    return ([0] + out)[:precision]


# ===================== the operator relations ==============================

# An arbitrary series makes this a test of the operators, not of a special
# modular form.  Enough coefficients are supplied for every truncation below.
raw = [0] + [r * r - 3 * r + 7 for r in range(1, 2000)]
for weight in (2, 4, 12):
    for m, n in ((2, 3), (3, 4), (4, 5), (5, 6)):
        assert gcd(m, n) == 1
        # To compute T_m(T_n f) through q^24, first compute T_n f far
        # enough for the largest coefficient T_m will inspect.
        tn = hecke(raw, n, weight, 25 * m)
        lhs = hecke(tn, m, weight, 25)
        rhs = hecke(raw, m * n, weight, 25)
        assert lhs == rhs, (weight, m, n, lhs, rhs)

    # The full relation also covers a common divisor:
    # T_m T_n = sum_{d|(m,n)} d^(k-1) T_(mn/d^2).
    for m, n in ((2, 2), (4, 2), (4, 6), (6, 6)):
        tn = hecke(raw, n, weight, 25 * m)
        lhs = hecke(tn, m, weight, 25)
        rhs = [0] * 25
        for d in divisors(gcd(m, n)):
            rhs = add_scaled(
                rhs,
                hecke(raw, m * n // (d * d), weight, 25),
                d ** (weight - 1),
            )
        assert lhs == rhs, (weight, m, n, lhs, rhs)


# ===================== two eigenforms from essay 12 ========================

# Delta = q prod(1-q^n)^24, level 1 and weight 12.
delta = eta_product(lambda _d: 24)
assert delta[1:9] == [1, -24, 252, -1472, 4830, -6048, -16744, 84480]
for ell in (2, 3, 5, 7):
    transformed = hecke(delta, ell, 12, 25)
    expected = [delta[ell] * a for a in delta[:25]]
    assert transformed == expected, ("Delta", ell, transformed, expected)

# f_11 = q prod(1-q^n)^2(1-q^(11n))^2, level 11 and weight 2.
f11 = eta_product(lambda d: 2 + (2 if d % 11 == 0 else 0))
assert f11[1:14] == [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4]
for ell in (2, 3, 5, 7):
    transformed = hecke(f11, ell, 2, 30)
    expected = [f11[ell] * a for a in f11[:30]]
    assert transformed == expected, ("f11", ell, transformed, expected)

# The coefficient of q is a_n, so the eigenvalue is a_n once a_1 = 1.
for n in (2, 3, 5, 6, 7, 10):
    assert hecke(f11, n, 2, 2)[1] == f11[n]

# Multiplicativity and the prime-power recurrence at primes away from level 11.
for m in range(1, 35):
    for n in range(1, 35):
        if m * n >= PREC or gcd(m, n) != 1 or gcd(m * n, 11) != 1:
            continue
        assert f11[m * n] == f11[m] * f11[n], (m, n)

for ell in (2, 3, 5, 7):
    for exponent in (1, 2):
        left = f11[ell ** (exponent + 1)]
        right = (
            f11[ell] * f11[ell**exponent]
            - ell * f11[ell ** (exponent - 1)]
        )
        assert left == right, (ell, exponent, left, right)

# At ell = 11 the prime-to-level formula is the wrong operator.  It agrees in
# the first coefficient by accident (that identity is general) but not as a
# q-series.  Essay 15 introduces the bad-prime operator/newform statement.
wrong_at_11 = hecke(f11, 11, 2, 20)
assert wrong_at_11 != [f11[11] * a for a in f11[:20]]

print("PASS hecke_operators: the q-coefficient formula satisfies the Hecke relations;")
print("  Delta and the level-11 eta product are eigenforms at every tested good prime,")
print("  with eigenvalue a_ell, multiplicative coefficients, and the prime-power recurrence")
print("  (the prime-to-level formula correctly fails when misapplied at ell = 11)")
