#!/usr/bin/env python3
"""Finite evidence for essay 18's conductor-11 modularity example.

This script checks, with exact arithmetic:

  * E: y^2+y=x^3-x^2 has discriminant and semistable conductor 11;
  * dim S_2(Gamma_0(11)) = 1;
  * the curve trace equals the eta-product coefficient at every good prime < 180;
  * at 11 both sides have the split-multiplicative polynomial 1-T;
  * c_4 = 16 and j(E) = c_4^3/Delta = -4096/11.

It checks one finite example.  It does not prove the Modularity Theorem,
the equivalence of its formulations, or the period construction.

Run: python3 checks/modularity_theorem.py
"""

from fractions import Fraction

from dim_s2_gamma0 import dim_S2
from reduction_and_conductor import (
    E11,
    discriminant,
    primes_up_to,
    radical,
    reduction,
)
from two_l_functions import f11


BOUND = 180


# The minimal discriminant has one bad prime; the curve is split multiplicative
# there, so in this semistable example the conductor is its radical.
delta = discriminant(*E11)
assert delta == -11
assert radical(delta) == 11
kind_11, curve_a11 = reduction(E11, 11)
assert kind_11 == "split multiplicative"
assert curve_a11 == f11[11] == 1
assert (1, -curve_a11) == (1, -1)  # local polynomial 1-T

# Essay 13's independently implemented genus formula makes the level-11
# weight-two cusp space one-dimensional.
assert dim_S2(11) == 1

# The two coefficient constructions agree at every tested good prime.
tested_good_primes = []
for ell in primes_up_to(BOUND - 1):
    if ell == 11:
        continue
    kind, curve_trace = reduction(E11, ell)
    assert kind == "good"
    assert curve_trace == f11[ell], (ell, curve_trace, f11[ell])
    tested_good_primes.append(ell)

# General Weierstrass invariants for E11=(a1,a2,a3,a4,a6).
a1, a2, a3, a4, _a6 = E11
b2 = a1 * a1 + 4 * a2
b4 = 2 * a4 + a1 * a3
c4 = b2 * b2 - 24 * b4
j_invariant = Fraction(c4**3, delta)
assert b2 == -4 and b4 == 0 and c4 == 16
assert j_invariant == Fraction(-4096, 11)


if __name__ == "__main__":
    print("PASS modularity_theorem: finite level-11 evidence")
    print(f"  conductor 11, dim S_2(Gamma_0(11)) = 1, {len(tested_good_primes)} good primes checked")
    print("  bad local polynomial at 11: 1-T; j(E) = -4096/11")
    print("  this does not prove modularity, its equivalent formulations, or the period construction")
