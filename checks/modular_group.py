"""Checks for essay 11: the modular group, its fundamental domain, and the counts.

Essay 13 will consume four numbers per level -- the index and the counts of
elliptic points and cusps -- so those are what this script pins, each by a route
independent of the closed formula it is checking.

Checked here:

  * The action preserves the upper half plane, via Im(gz) = Im(z)/|cz+d|^2,
    numerically over many matrices and points.
  * S: z -> -1/z and T: z -> z+1 generate SL_2(Z): every matrix with entries in
    [-3, 3] is reached by a word in S and T.
  * The reduction algorithm lands every point in the standard fundamental domain
    F = {|z| >= 1, |Re z| <= 1/2}, so F really is one.
  * i and rho = e^(2 pi i / 3) are elliptic, fixed by elements of order 2 and 3;
    and among the sampled points of F, no others are fixed by a non-identity
    element of small height. The sweep asserts it actually reached both, since a
    sample that missed one would pass the "no others" test for free.
  * The index [SL_2(Z) : Gamma_0(N)] = N prod (1 + 1/p) matches brute-force coset
    counting in SL_2(Z/N).
  * The elliptic counts have an arithmetic characterisation independent of the
    product formula: nu_2(N) is the number of solutions of x^2 + 1 = 0 mod N, and
    nu_3(N) the number of solutions of x^2 + x + 1 = 0 mod N. Verified for
    N < 200 against the formulas essay 13 will use.
  * All four counts are cross-checked jointly by the genus: 1 + mu/12 - nu_2/4
    - nu_3/3 - nu_inf/2 must be a non-negative integer for every N, which a wrong
    count would generically break.

Run: python3 checks/modular_group.py
"""

import cmath
import sys
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dim_s2_gamma0 import dim_S2, mu, nu2, nu3, nu_inf  # noqa: E402

S = (0, -1, 1, 0)
T = (1, 1, 0, 1)


def mat(g, h):
    a, b, c, d = g
    e, f, i, j = h
    return (a * e + b * i, a * f + b * j, c * e + d * i, c * f + d * j)


def act(g, z):
    a, b, c, d = g
    return (a * z + b) / (c * z + d)


# ===================== the action preserves H ===============================

pts = [complex(x / 4, y / 4) for x in range(-6, 7) for y in range(1, 9)]
# the grid misses rho, so the elliptic points are added explicitly -- without them
# the "no other fixed point" sweep below never reaches rho and passes vacuously
pts += [complex(0, 1), cmath.exp(2j * cmath.pi / 3), cmath.exp(2j * cmath.pi / 3) + 1,
        complex(0, 2), complex(0.5, 3 ** 0.5 / 2)]
mats = [
    (a, b, c, d)
    for a, b, c, d in product(range(-3, 4), repeat=4)
    if a * d - b * c == 1
]
assert len(mats) > 100
for g in mats:
    a, b, c, d = g
    for z in pts:
        w = act(g, z)
        assert w.imag > 0, (g, z)
        # Im(gz) = Im(z)/|cz+d|^2, exactly
        assert abs(w.imag - z.imag / abs(c * z + d) ** 2) < 1e-9, (g, z)

# ===================== S and T generate ====================================

reached = {(1, 0, 0, 1)}
frontier = [(1, 0, 0, 1)]
for _ in range(9):
    nxt = []
    for g in frontier:
        for h in (S, T, (1, -1, 0, 1), (0, 1, -1, 0)):
            p = mat(g, h)
            if max(abs(x) for x in p) <= 6 and p not in reached:
                reached.add(p)
                nxt.append(p)
    frontier = nxt
small = {g for g in mats if max(abs(x) for x in g) <= 3}
assert small <= reached, sorted(small - reached)[:4]

# ===================== the fundamental domain ==============================


def reduce_to_domain(z, limit=200):
    """Translate into |Re z| <= 1/2, invert while |z| < 1. Standard algorithm."""
    for _ in range(limit):
        n = round(z.real)
        if n:
            z = z - n
            continue
        if abs(z) < 1 - 1e-12:
            z = -1 / z
            continue
        return z
    raise AssertionError("did not reduce")


for z in pts:
    w = reduce_to_domain(z)
    assert abs(w) >= 1 - 1e-9, (z, w)
    assert abs(w.real) <= 0.5 + 1e-9, (z, w)
    assert w.imag > 0

# ===================== the two elliptic points =============================

i_pt = complex(0, 1)
rho = cmath.exp(2j * cmath.pi / 3)

assert abs(act(S, i_pt) - i_pt) < 1e-12                 # S fixes i
assert mat(S, S) == (-1, 0, 0, -1)                      # order 2 in PSL_2(Z)
ST = mat(S, T)
assert abs(act(ST, rho) - rho) < 1e-12                  # ST fixes rho
assert mat(ST, mat(ST, ST)) == (-1, 0, 0, -1)           # order 3 in PSL_2(Z)

# and no other point of the sampled domain is fixed by a small non-identity element
fixed = set()
for g in mats:
    if g in ((1, 0, 0, 1), (-1, 0, 0, -1)):
        continue
    for z in pts:
        w = reduce_to_domain(z)
        if abs(act(g, w) - w) < 1e-9:
            fixed.add((round(w.real, 6), round(w.imag, 6)))
for pt in fixed:
    near_i = abs(complex(*pt) - i_pt) < 1e-4
    near_rho = min(abs(complex(*pt) - rho), abs(complex(*pt) - (rho + 1))) < 1e-4
    assert near_i or near_rho, pt
# and the sweep must actually have REACHED both, or it proves nothing about them
assert any(abs(complex(*pt) - i_pt) < 1e-4 for pt in fixed), "sweep never reached i"
assert any(min(abs(complex(*pt) - rho), abs(complex(*pt) - (rho + 1))) < 1e-4 for pt in fixed), \
    "sweep never reached rho"

# ===================== the index, by coset counting ========================


def index_bruteforce(N):
    G = [(a, b, c, d) for a, b, c, d in product(range(N), repeat=4) if (a * d - b * c) % N == 1]
    H = [g for g in G if g[2] % N == 0]
    assert len(G) % len(H) == 0
    return len(G) // len(H)


for N in range(2, 26):
    assert index_bruteforce(N) == mu(N), (N, index_bruteforce(N), mu(N))

# ===================== the elliptic counts, arithmetically =================

for N in range(1, 200):
    roots2 = sum(1 for x in range(N) if (x * x + 1) % N == 0)
    roots3 = sum(1 for x in range(N) if (x * x + x + 1) % N == 0)
    assert roots2 == nu2(N), (N, roots2, nu2(N))
    assert roots3 == nu3(N), (N, roots3, nu3(N))

# ===================== the joint consistency check =========================

for N in range(1, 400):
    g = 1 + Fraction(mu(N), 12) - Fraction(nu2(N), 4) - Fraction(nu3(N), 3) - Fraction(nu_inf(N), 2)
    assert g.denominator == 1 and g >= 0, (N, g)

# the two levels this collection actually evaluates
assert (mu(11), nu2(11), nu3(11), nu_inf(11)) == (12, 0, 0, 2)
assert dim_S2(11) == 1                      # and LMFDB records one newform, 11.2.a.a
assert (mu(2), nu2(2), nu3(2), nu_inf(2)) == (3, 1, 0, 2)
assert dim_S2(2) == 0                       # the contradiction essay 25 needs

print("PASS modular_group: action preserves H, S and T generate, F is a fundamental domain,")
print("  i and rho are the only fixed points among those sampled (and both were reached),")
print("  index matches coset counting over 2.1M tuples, and")
print("  nu_2, nu_3 match root counts of x^2+1 and x^2+x+1 for N < 200")
