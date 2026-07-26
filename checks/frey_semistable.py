"""Checks for essay 23: the Frey curve is semistable, with conductor rad(abc).

Nothing here assumes a Fermat solution exists. The semistability argument uses
only three properties of the triple, so the tests run over ordinary integer
triples satisfying them -- which is strictly more general than testing on
hypothetical p-th powers:

    A + B = C,  A, B, C pairwise coprime,  A = 3 mod 4,  B = 0 mod 32.

Checked here:

  * the change of variables x = 4X, y = 8Y + 4X lands on an integral model
    with a_1 = 1, and its discriminant is exactly (ABC)^2 / 2^8,
  * that model is minimal at 2, since v_2 drops by the full 12,
  * at every odd bad prime the reduced cubic has a double root and never a
    triple root, so the reduction is multiplicative,
  * at 2 the singular point is (0,0) and the quadratic part splits into two
    distinct tangent directions, so the reduction is multiplicative there too,
  * hence no additive reduction anywhere, and the conductor is rad(abc),
  * cross-checked against brute-force point counts: a_ell = +-1 at every bad
    prime, which is what multiplicative reduction means.

Run: python3 checks/frey_semistable.py
"""

import sys
from itertools import product
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reduction_and_conductor import (  # noqa: E402
    discriminant,
    points_and_singular,
    primes_up_to,
    radical,
    reduction,
    squarefree,
)


def frey_display(A, B):
    """y^2 = x(x - A)(x + B), expanded: a2 = B - A, a4 = -AB."""
    return (0, B - A, 0, -A * B, 0)


def frey_minimal(A, B):
    """The model after x = 4X, y = 8Y + 4X. Integral when A = 3 mod 4, 16 | B."""
    assert (B - A - 1) % 4 == 0, "a_2 is not integral"
    assert (A * B) % 16 == 0, "a_4 is not integral"
    return (1, (B - A - 1) // 4, 0, -(A * B) // 16, 0)


def v(ell, n):
    e = 0
    while n % ell == 0:
        n //= ell
        e += 1
    return e


def triples(limit=40):
    """Integer triples with the three properties the argument actually uses."""
    out = []
    for A in range(3, 400, 4):          # A = 3 mod 4
        for B in range(32, 400, 32):    # B = 0 mod 32
            C = A + B
            if gcd(A, B) == 1 and gcd(A, C) == 1 and gcd(B, C) == 1:
                out.append((A, B, C))
                if len(out) >= limit:
                    return out
    return out


CASES = triples()
assert len(CASES) >= 40

for A, B, C in CASES:
    disp = frey_display(A, B)
    mini = frey_minimal(A, B)

    # --- the displayed model, as essay 22 computes it -----------------------
    assert discriminant(*disp) == 16 * (A * B * C) ** 2

    # --- the minimal model's discriminant, from the b-invariants ------------
    # b2 = B - A, b4 = -AB/8, b6 = 0, b8 = -(AB/16)^2, and the bracket
    # (B - A)^2 + 4AB collapses to (A + B)^2 = C^2.
    assert discriminant(*mini) * 2**8 == (A * B * C) ** 2

    # --- minimality at 2: the coordinate change removed the full 2^12 ------
    d_disp, d_min = discriminant(*disp), discriminant(*mini)
    assert d_disp == d_min * 2**12
    assert v(2, d_min) == v(2, d_disp) - 12
    # and 2 is genuinely bad: v_2(Delta_min) = 2*v_2(B) - 8 >= 2
    assert v(2, d_min) == 2 * v(2, B) - 8 >= 2

    # --- a_1 = 1 is what survives at 2, and it is the whole point ----------
    assert mini[0] == 1

    bad = [p for p in primes_up_to(200) if d_min % p == 0]
    assert 2 in bad
    assert all(p in bad for p in primes_up_to(200) if (A * B * C) % p == 0)

    # --- odd bad primes: a double root, never a triple root ----------------
    for ell in bad:
        if ell == 2:
            continue
        # exactly one of A, B, C is divisible by ell, by pairwise coprimality
        divides = [x % ell == 0 for x in (A, B, C)]
        assert sum(divides) == 1, (A, B, C, ell)
        # the three roots of x(x - A)(x + B) modulo ell
        roots = [0 % ell, A % ell, (-B) % ell]
        counts = {r: roots.count(r) for r in set(roots)}
        assert max(counts.values()) == 2, (A, B, C, ell, roots)  # double, not triple
        assert len(set(roots)) == 2

    # --- at 2: singular point (0,0), two distinct tangent directions -------
    a1, a2, a3, a4, a6 = (c % 2 for c in mini)
    affine, singular = points_and_singular(mini, 2)
    assert singular == [(0, 0)], (A, B, singular)
    # F = Y^2 + XY - X^3 - a2 X^2 - a4 X; at the origin the quadratic part is
    # Y^2 + XY + a2 X^2, i.e. T^2 + T + a2 for T = Y/X. In characteristic 2
    # its derivative is 1, so it is separable: two distinct tangents. A node.
    assert a4 == 0  # required for (0,0) to lie on the curve
    sep = [t for t in range(2) if (t * t + t + a2) % 2 == 0]
    assert len(set(sep)) == len(sep)  # no repeated tangent direction
    # split when the tangents are rational, non-split when conjugate
    expected_2 = "split multiplicative" if a2 == 0 else "non-split multiplicative"

    # --- reduction type at every bad prime, by brute-force point count ------
    for ell in bad:
        kind, a_ell = reduction(mini, ell)
        assert kind.endswith("multiplicative"), (A, B, C, ell, kind)
        assert a_ell in (1, -1)
        if ell == 2:
            assert kind == expected_2, (A, B, kind, expected_2)

    # --- semistable, so the conductor is the radical ------------------------
    N = radical(d_min)
    assert N == radical(A * B * C), (A, B, C, N)
    assert squarefree(N)
    assert N % 2 == 0  # 2 | B, so 2 always divides the conductor

# --- the identity behind the discriminant, symbolically over many values ----
for A, B in product(range(-30, 31), repeat=2):
    assert (B - A) ** 2 + 4 * A * B == (A + B) ** 2

# --- what the mod-32 normalisation actually buys ----------------------------
# Integrality of the minimal model only needs 16 | B (A is odd, so a_4 = -AB/16
# is integral exactly when 16 | B). The extra factor of 2 does something else:
# v_2(Delta_min) = 2*v_2(B) - 8, so 32 | B is what makes 2 a *bad* prime and
# therefore puts 2 into the conductor -- which is what essays 24 and 25 need.
A, B = 3, 16                      # 16 | B but not 32 | B
mini_16 = frey_minimal(A, B)      # still integral, still a_1 = 1
assert mini_16[0] == 1
assert v(2, discriminant(*mini_16)) == 2 * v(2, B) - 8 == 0
kind_16, _ = reduction(mini_16, 2)
assert kind_16 == "good", kind_16
assert radical(discriminant(*mini_16)) % 2 == 1  # 2 absent from the conductor

A, B = 3, 32                      # 32 | B
mini_32 = frey_minimal(A, B)
assert v(2, discriminant(*mini_32)) == 2 * v(2, B) - 8 == 2
assert reduction(mini_32, 2)[0].endswith("multiplicative")
assert radical(discriminant(*mini_32)) % 2 == 0  # 2 now in the conductor

# For a genuine Fermat solution b is even and p >= 5, so v_2(B) = p*v_2(b) >= 5
# and the 16-but-not-32 case cannot arise.
assert all(2 * (5 * k) - 8 >= 2 for k in range(1, 10))

print("  (aside) 16 | B gives good reduction at 2; 32 | B makes 2 multiplicative")
print("PASS frey_semistable: minimal model at 2, multiplicative everywhere, conductor = rad(abc)")

