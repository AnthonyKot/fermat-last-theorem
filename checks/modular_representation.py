"""Checks for essay 16: the level-11 Frobenius packet.

The Eichler--Shimura/Deligne construction itself is an imported theorem, not
something a finite script can prove.  This file checks the exact numerical
example used to make its conclusion visible:

  * the coefficients of f_11 = (eta(z)eta(11z))^2;
  * a_ell(f_11) = ell + 1 - #E(F_ell) for E: y^2+y=x^3-x^2;
  * the characteristic polynomial X^2-a_ell X+ell on both sides;
  * its reduction modulo several residual primes p, always keeping the
    auxiliary prime ell distinct from p and 11.

Run: python3 checks/modular_representation.py
"""

from math import comb

from reduction_and_conductor import E11, primes_up_to, reduction


PRECISION = 80


def eta_product_11(precision=PRECISION):
    """Return q prod_n (1-q^n)^2(1-q^(11n))^2 exactly."""
    product = [1] + [0] * (precision - 1)
    for degree in range(1, precision):
        exponent = 2 + (2 if degree % 11 == 0 else 0)
        factor = [(-1) ** j * comb(exponent, j) for j in range(exponent + 1)]
        updated = [0] * precision
        for old_degree, old_coefficient in enumerate(product):
            if old_coefficient == 0:
                continue
            for j, factor_coefficient in enumerate(factor):
                new_degree = old_degree + j * degree
                if new_degree >= precision:
                    break
                updated[new_degree] += old_coefficient * factor_coefficient
        product = updated
    return ([0] + product)[:precision]


f11 = eta_product_11()
assert f11[1:14] == [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4]

# Good-prime Frobenius packets, computed independently from the q-series and
# from brute-force point counts on the conductor-11 curve.
packets = {}
for ell in primes_up_to(47):
    if ell == 11:
        continue
    kind, curve_trace = reduction(E11, ell)
    assert kind == "good"
    form_trace = f11[ell]
    assert curve_trace == form_trace, (ell, curve_trace, form_trace)
    packets[ell] = (1, -form_trace, ell)  # coefficients of X^2-a_ell X+ell

# The residual polynomial is just the same packet reduced modulo p.  The
# determinant term ell mod p is the value of the mod-p cyclotomic character on
# Frobenius, as established in essays 03 and 10.
for residual_prime in (3, 5, 7):
    for ell, characteristic_polynomial in packets.items():
        if ell == residual_prime:
            continue
        reduced = tuple(c % residual_prime for c in characteristic_polynomial)
        assert reduced == (
            1,
            -f11[ell] % residual_prime,
            ell % residual_prime,
        )

if __name__ == "__main__":
    sample = ", ".join(
        f"a_{ell}={f11[ell]}" for ell in (2, 3, 5, 7, 13)
    )
    print("PASS modular_representation: form and curve give the same Frobenius packets")
    print(f"  {sample}")
    print("  and X^2-a_ell X+ell reduces coefficientwise modulo p")
