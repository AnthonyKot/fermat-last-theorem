"""Checks for essay 24: the conductor of the Frey representation is 2.

Two computations, both independent of any particular triple.

1. Serre's level recipe evaluated symbolically. For the Frey curve
   Delta_min = 2^(-8) (abc)^(2p), so at an odd bad prime
       v_l(Delta_min) = 2p * v_l(abc) = 0  (mod p),
   while at 2
       v_2(Delta_min) = 2p * v_2(b) - 8 = -8  (mod p),
   which is non-zero for every p >= 3 since p does not divide 8. The recipe's
   product therefore runs over the single prime 2, whatever the solution was.
   Verified over many exponents and valuation patterns.

2. How far the 2-torsion irreducibility argument actually reaches. Mazur gives
   irreducibility for p > 7 on a semistable curve. Below that, full rational E[2]
   forces 4 | #E(F_l) at good odd l, so a_l = l + 1 mod 4, and Hasse bounds
   |a_l| <= 2 sqrt(l). For small l that leaves so few possible a_l that
   a_l^2 - 4l is a non-square mod p for ALL of them -- which proves the
   characteristic polynomial of Frobenius does not split, hence irreducibility.
   Enumerating every permitted a_l rather than sampling curves, the uniform
   witnesses are

       p = 5:  l = 3, 7      p = 7:  l = 5, 17

   and no others below 400. A witness works when it is a prime of good reduction,
   i.e. when it does not divide abc. So the argument covers p = 5 unless
   21 | abc, and p = 7 unless 85 | abc. That is a narrowing of the classical
   dependency, not its removal, and the script asserts the boundary rather than
   overstating it.

Run: python3 checks/frey_conductor.py
"""

import sys
from itertools import product
from math import isqrt, prod
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reduction_and_conductor import primes_up_to  # noqa: E402

PRIMES = [q for q in primes_up_to(400)]
EXPONENTS = [p for p in PRIMES if p >= 5]

# ===================== 1. the recipe gives exactly {2} ======================


def serre_level(p, v2_b, odd_valuations):
    """Product of primes l with v_l(Delta_min) not divisible by p.

    odd_valuations maps an odd prime l to v_l(abc), which is positive exactly at
    the odd bad primes.
    """
    level = []
    if (2 * p * v2_b - 8) % p != 0:
        level.append(2)
    for ell, v in odd_valuations.items():
        assert ell % 2 == 1 and v >= 1
        if (2 * p * v) % p != 0:
            level.append(ell)
    return prod(level) if level else 1


for p in EXPONENTS[:20]:
    # p never divides 8, so 2 always survives
    assert 8 % p != 0, p
    assert (-8) % p != 0, p
    for v2_b in range(1, 8):
        # v_2(Delta_min) must also be positive, which is essay 23's mod-32 point
        assert 2 * p * v2_b - 8 >= 2, (p, v2_b)
        for odd in (
            {3: 1},
            {5: 2},
            {3: 1, 7: 4},
            {11: 3, 13: 1, 17: 2},
            {q: 1 for q in (3, 5, 7, 11, 13, 19, 23)},
        ):
            assert serre_level(p, v2_b, odd) == 2, (p, v2_b, odd)

# every odd prime's valuation is a multiple of p, which is the whole mechanism
for p in EXPONENTS[:20]:
    for v in range(1, 12):
        assert (2 * p * v) % p == 0

# and the exponent at 2 is genuinely not a multiple of p
for p in EXPONENTS[:20]:
    for v2_b in range(1, 12):
        assert (2 * p * v2_b - 8) % p == (-8) % p != 0

# a contrast that shows where this would fail: if the model were NOT minimal at 2
# the displayed discriminant 16(abc)^(2p) has v_2 = 4 + 2p*v_2(b), and 4 - 8 = -4
# is still non-zero mod p, but the value of the exponent differs -- which is why
# essay 23 had to pin the minimal model before this computation could be trusted.
for p in EXPONENTS[:10]:
    assert (4 + 2 * p * 1) % p == 4 % p != 0

# ===================== 2. how far the E[2] argument reaches =================


def permitted_a(ell):
    """Values of a_ell allowed by full rational E[2] plus the Hasse bound."""
    return [
        a
        for a in range(-2 * isqrt(ell) - 2, 2 * isqrt(ell) + 3)
        if a * a <= 4 * ell and (ell + 1 - a) % 4 == 0
    ]


def uniform_witnesses(p, bound=400):
    sq = {x * x % p for x in range(p)}
    out = []
    for ell in primes_up_to(bound):
        if ell == 2 or ell == p:
            continue
        vals = permitted_a(ell)
        if vals and all((a * a - 4 * ell) % p not in sq for a in vals):
            out.append(ell)
    return out


assert permitted_a(3) == [0]                     # a_3 = 0 exactly
assert sorted(permitted_a(5)) == [-2, 2]         # a_5 = +-2
assert sorted(permitted_a(7)) == [-4, 0, 4]      # a_7 in {0, +-4}
assert sorted(permitted_a(17)) == [-6, -2, 2, 6]

assert uniform_witnesses(5) == [3, 7], uniform_witnesses(5)
assert uniform_witnesses(7) == [5, 17], uniform_witnesses(7)

# the residual cases, stated exactly
assert prod(uniform_witnesses(5)) == 21
assert prod(uniform_witnesses(7)) == 85

# above 7 Mazur already gives irreducibility on a semistable curve, so the
# witnesses there are a bonus rather than a necessity -- but they exist
for p in (11, 13):
    assert uniform_witnesses(p), p

# the non-square condition really is what proves irreducibility: if the char
# polynomial x^2 - a x + l splits mod p then rho-bar could be reducible, and it
# splits exactly when the discriminant is a square
for p in (5, 7):
    sq = {x * x % p for x in range(p)}
    for ell in uniform_witnesses(p):
        for a in permitted_a(ell):
            disc = (a * a - 4 * ell) % p
            assert disc not in sq
            # no root in F_p, confirming the polynomial is irreducible there
            assert all((x * x - a * x + ell) % p != 0 for x in range(p)), (p, ell, a)

print("PASS frey_conductor: Serre's recipe yields exactly {2} for every exponent and")
print("  valuation pattern tested; uniform E[2] witnesses are l=3,7 for p=5 and")
print("  l=5,17 for p=7, so the classical dependency narrows to 21|abc and 85|abc.")
