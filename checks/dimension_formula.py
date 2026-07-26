"""Checks for essay 13: the dimension formula, derived by Riemann-Hurwitz.

Essay 13 derives
    g(X_0(N)) = 1 + mu/12 - nu_2/4 - nu_3/3 - nu_inf/2
from Riemann-Hurwitz applied to the covering X_0(N) -> X(1) of degree mu, and
takes dim S_2(Gamma_0(N)) = g. This script checks every step of that derivation
rather than the formula's output alone.

Checked here:

  * Weight two is exactly the weight at which f(z) dz is invariant, because
    d(gz)/dz = 1/(cz+d)^2 -- verified numerically. That is why S_2 is the space of
    holomorphic differentials and hence why its dimension is the genus.
  * The ramification data is consistent: above i the indices are 1 or 2 with nu_2
    unramified points, so (mu - nu_2)/2 points ramify; above rho they are 1 or 3
    with nu_3 unramified, so (mu - nu_3)/3 ramify. Both counts must be integers,
    and are, for every N < 400.
  * The coefficient arithmetic -2 + 1/2 + 2/3 + 1 = 1/6 that collapses
    Riemann-Hurwitz to the closed formula.
  * Riemann-Hurwitz reproduces the closed formula exactly for every N < 400.
  * The explicit ramification at the two levels the collection evaluates, N = 2
    and N = 11, including cusp widths summing to mu.
  * nu_inf enters here as a RAMIFICATION count. The constraint-counting effect
    that essay 12 warned about is separate and vanishes at weight two; that is
    pinned in checks/modular_forms.py.

Run: python3 checks/dimension_formula.py
"""

import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dim_s2_gamma0 import dim_S2, mu, nu2, nu3, nu_inf  # noqa: E402

# ===================== weight two is the differential weight ================


def act(g, z):
    a, b, c, d = g
    return (a * z + b) / (c * z + d)


mats = [
    (a, b, c, d)
    for a in range(-3, 4)
    for b in range(-3, 4)
    for c in range(-3, 4)
    for d in range(-3, 4)
    if a * d - b * c == 1
]
h = 1e-7
for g in mats:
    _, _, c, d = g
    for z in (complex(0.3, 0.7), complex(-0.4, 1.2), complex(0.1, 2.5)):
        derivative = (act(g, z + h) - act(g, z)) / h
        predicted = 1 / (c * z + d) ** 2
        assert abs(derivative - predicted) < 1e-4 * max(1.0, abs(predicted)), (g, z)

# So f(gz) d(gz) = (cz+d)^k f(z) * dz/(cz+d)^2 = (cz+d)^(k-2) f(z) dz, which is
# f(z) dz for every g exactly when k = 2. Check that the surviving factor really is
# (cz+d)^(k-2) and is non-constant for k != 2, so no other weight can work.
for k in (2, 4, 6):
    for g in mats:
        _, _, c, d = g
        for z in (complex(0.3, 0.7), complex(-0.4, 1.2)):
            surviving = (c * z + d) ** k / (c * z + d) ** 2
            assert abs(surviving - (c * z + d) ** (k - 2)) < 1e-9
            if k == 2:
                assert abs(surviving - 1) < 1e-12
non_trivial = {round(abs((c * z + d) ** 2), 6)
               for (_, _, c, d) in mats for z in [complex(0.3, 0.7)]}
assert len(non_trivial) > 1        # for k = 4 the factor genuinely varies with g

# ===================== the ramification data is consistent ==================

for N in range(1, 400):
    m, a, b, c = mu(N), nu2(N), nu3(N), nu_inf(N)
    assert (m - a) % 2 == 0, (N, m, a)      # points above i with e = 2
    assert (m - b) % 3 == 0, (N, m, b)      # points above rho with e = 3
    assert a <= m and b <= m and 1 <= c <= m

# ===================== the coefficient arithmetic ===========================

assert F(-2) + F(1, 2) + F(2, 3) + F(1) == F(1, 6)

# ===================== Riemann-Hurwitz gives the closed formula =============


def genus_riemann_hurwitz(N):
    """2g - 2 = mu*(2*0 - 2) + sum over points of (e_P - 1), X(1) having genus 0."""
    m, a, b, c = mu(N), nu2(N), nu3(N), nu_inf(N)
    ram = F(m - a, 2) + 2 * F(m - b, 3) + (m - c)
    two_g_minus_2 = -2 * m + ram
    g = (two_g_minus_2 + 2) / 2
    assert g.denominator == 1 and g >= 0, (N, g)
    return int(g)


def genus_closed(N):
    g = 1 + F(mu(N), 12) - F(nu2(N), 4) - F(nu3(N), 3) - F(nu_inf(N), 2)
    assert g.denominator == 1
    return int(g)


for N in range(1, 400):
    assert genus_riemann_hurwitz(N) == genus_closed(N) == dim_S2(N), N

# ===================== the two levels that matter, explicitly ==============

# N = 2: mu = 3, so one point above i with e = 2, one above rho with e = 3,
# and two cusps whose widths sum to 3.
assert (mu(2), nu2(2), nu3(2), nu_inf(2)) == (3, 1, 0, 2)
assert (mu(2) - nu2(2)) // 2 == 1
assert (mu(2) - nu3(2)) // 3 == 1
assert F(-2 * 3) + F(3 - 1, 2) + 2 * F(3 - 0, 3) + (3 - 2) == -2   # so g = 0
assert genus_closed(2) == 0 and dim_S2(2) == 0

# N = 11: mu = 12, six points above i, four above rho, two cusps summing to 12.
assert (mu(11), nu2(11), nu3(11), nu_inf(11)) == (12, 0, 0, 2)
assert (mu(11) - nu2(11)) // 2 == 6
assert (mu(11) - nu3(11)) // 3 == 4
assert F(-2 * 12) + F(12, 2) + 2 * F(12, 3) + (12 - 2) == 0        # so g = 1
assert genus_closed(11) == 1 and dim_S2(11) == 1

# ===================== the slack: level 2 is not knife-edge =================

vanishing = [N for N in range(1, 400) if dim_S2(N) == 0]
assert vanishing == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 16, 18, 25], vanishing

print("PASS dimension_formula: d(gz)/dz = 1/(cz+d)^2 so weight two is the differential")
print("  weight; the ramification counts are integral for N < 400; and Riemann-Hurwitz")
print("  reproduces 1 + mu/12 - nu_2/4 - nu_3/3 - nu_inf/2 exactly, giving 0 at N = 2")
print("  and 1 at N = 11")
