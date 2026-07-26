#!/usr/bin/env python3
"""Checks for essay 15: oldforms, bad-prime operators, and exact level.

The Atkin--Lehner--Li newform theorem is explicitly imported by the essay; this
script checks the concrete calculation that motivates the import.

Starting with

    f(q) = (eta(z) eta(11z))^2 in S_2(Gamma_0(11)),

we raise the level to 22 using the two degeneracy maps f(q) and f(q^2).
Everything below uses exact integer q-series.

Checked here:

  * dim S_2(Gamma_0(11)) = 1 and dim S_2(Gamma_0(22)) = 2;
  * f(q) and f(q^2) are linearly independent, so they span the whole level-22
    space and its new subspace has dimension zero;
  * every tested T_ell with ell coprime to 22 acts on both copies by the same
    eigenvalue a_ell, so the good-Hecke eigenspace is genuinely two-dimensional;
  * at the bad prime 2, U_2(sum b_n q^n) = sum b_(2n) q^n and, in the ordered
    basis (f(q), f(q^2)),

          U_2 = [[-2, 1],
                 [-2, 0]];

  * this matrix has characteristic polynomial X^2 + 2X + 2 and nonreal
    eigenvalues, so U_2 is not Hermitian and cannot inherit essay 14's spectral
    theorem argument.

Run: python3 checks/newforms_and_level.py
"""

from math import comb

from dim_s2_gamma0 import dim_S2


PREC = 900


def eta_product_11(precision=PREC):
    """Return q prod_n (1-q^n)^2(1-q^(11n))^2 through q^(precision-1)."""
    out = [1] + [0] * (precision - 1)
    for degree in range(1, precision):
        exponent = 2 + (2 if degree % 11 == 0 else 0)
        factor = [(-1) ** j * comb(exponent, j) for j in range(exponent + 1)]
        new = [0] * precision
        for i, value in enumerate(out):
            if value == 0:
                continue
            for j, factor_value in enumerate(factor):
                target = i + j * degree
                if target >= precision:
                    break
                new[target] += value * factor_value
        out = new
    return ([0] + out)[:precision]


def degeneracy(coeffs, d):
    """V_d f(q) = f(q^d)."""
    out = [0] * len(coeffs)
    for n in range(1, len(out)):
        if n % d == 0:
            out[n] = coeffs[n // d]
    return out


def good_hecke_prime(coeffs, ell, weight, out_precision):
    """Prime-to-level T_ell coefficient formula."""
    out = [0] * out_precision
    for n in range(1, out_precision):
        out[n] = coeffs[ell * n]
        if n % ell == 0:
            out[n] += ell ** (weight - 1) * coeffs[n // ell]
    return out


def bad_u(coeffs, ell, out_precision):
    """Bad-prime U_ell coefficient shift."""
    return [0] + [coeffs[ell * n] for n in range(1, out_precision)]


f = eta_product_11()
v2f = degeneracy(f, 2)
assert f[1:14] == [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4]

# The level-11 line produces two independent level-22 vectors.  Their first
# nonzero coefficients occur at q and q^2 respectively.
assert f[1] == 1 and v2f[1] == 0 and v2f[2] == 1
assert dim_S2(11) == 1
assert dim_S2(22) == 2
old_dimension = 2
new_dimension = int(dim_S2(22)) - old_dimension
assert new_dimension == 0

# Good operators commute with the degeneracy map.  Thus both copies have the
# same good eigenvalues and the good eigenspace does not split.
for ell in (3, 5, 7, 13, 17, 19, 23, 29):
    assert 22 % ell != 0
    out_precision = 25
    tf = good_hecke_prime(f, ell, 2, out_precision)
    tv2f = good_hecke_prime(v2f, ell, 2, out_precision)
    assert tf == [a * f[ell] for a in f[:out_precision]], ell
    assert tv2f == [a * f[ell] for a in v2f[:out_precision]], ell

# At level 22 the prime 2 is bad, so its operator is U_2, not the good-prime
# T_2 formula.  The level-11 identity T_2 f = a_2 f gives
# U_2 f = a_2 f - 2 V_2 f, while U_2(V_2 f) = f.
out_precision = 100
u2f = bad_u(f, 2, out_precision)
u2v2f = bad_u(v2f, 2, out_precision)
assert u2f == [
    f[2] * f[n] - 2 * v2f[n] for n in range(out_precision)
]
assert u2v2f == f[:out_precision]

# Columns are the images of f and V_2 f in that ordered basis.
u2_matrix = ((-2, 1), (-2, 0))
trace = u2_matrix[0][0] + u2_matrix[1][1]
determinant = (
    u2_matrix[0][0] * u2_matrix[1][1]
    - u2_matrix[0][1] * u2_matrix[1][0]
)
assert (trace, determinant) == (-2, 2)
assert trace * trace - 4 * determinant == -4

print("PASS newforms_and_level: dim S_2(Gamma_0(22)) = 2, and the two degeneracy")
print("  images f(q), f(q^2) span it, so its newspace has dimension 0; every tested")
print("  good T_ell has the same eigenvalue on both copies, while")
print("  U_2 = [[-2,1],[-2,0]] has characteristic polynomial X^2+2X+2")
print("  and is not Hermitian -- exactly the boundary imported newform theory repairs")
