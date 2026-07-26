"""Checks for essay 12: q-expansions, cusp forms, and the level-11 form exhibited.

Power series with exact integer coefficients throughout. Nothing here needs a
modular-forms library; a form is a sequence of integers and the claims about it
are claims about that sequence.

Checked here:

  * The weight factor (cz+d)^k satisfies the cocycle condition
    j(gh, z) = j(g, hz) j(h, z), which is what makes the definition consistent;
    and -I forces k even for Gamma_0(N), since it gives f = (-1)^k f.
  * At level 1, weight 12: Delta = q prod (1-q^n)^24 has the Ramanujan
    coefficients 1, -24, 252, -1472, 4830, -6048, and the identity
        E_4^3 - E_6^2 = 1728 Delta
    holds exactly as power series, with E_4 and E_6 built from sigma_3 and
    sigma_5. That is a genuine constraint linking three independently defined
    series.
  * The form essay 11's dimension count predicted at level 11 is exhibited:
    (eta(z) eta(11z))^2 = q prod (1-q^n)^2 (1-q^(11n))^2, whose coefficients at
    primes are EXACTLY the a_ell that essay 08 obtained by counting points on
    y^2 + y = x^3 - x^2 over F_ell -- including at the bad prime 11.
  * That series is normalised (a_1 = 1) and its coefficients are multiplicative,
    a_mn = a_m a_n for coprime m, n, which is the property essay 14 will explain.

Run: python3 checks/modular_forms.py
"""

import sys
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reduction_and_conductor import primes_up_to, reduction  # noqa: E402

PREC = 40


def mul(a, b, n=PREC):
    out = [0] * n
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if i + j >= n:
                break
            out[i + j] += x * y
    return out


def power(a, e, n=PREC):
    out = [0] * n
    out[0] = 1
    for _ in range(e):
        out = mul(out, a, n)
    return out


def euler_factor(m, n=PREC):
    """prod_{k>=1} (1 - q^(m k)), truncated."""
    out = [0] * n
    out[0] = 1
    for k in range(1, n // m + 1):
        f = [0] * n
        f[0] = 1
        if m * k < n:
            f[m * k] = -1
        out = mul(out, f, n)
    return out


def shift(a, s, n=PREC):
    return ([0] * s + a)[:n]


def sigma(k, n):
    return sum(d**k for d in range(1, n + 1) if n % d == 0)


# ===================== the weight factor is a cocycle =======================


def j(g, z, k):
    _, _, c, d = g
    return (c * z + d) ** k


def matmul(g, h):
    a, b, c, d = g
    e, f, i, l = h
    return (a * e + b * i, a * f + b * l, c * e + d * i, c * f + d * l)


def act(g, z):
    a, b, c, d = g
    return (a * z + b) / (c * z + d)


mats = [
    (a, b, c, d)
    for a in range(-2, 3)
    for b in range(-2, 3)
    for c in range(-2, 3)
    for d in range(-2, 3)
    if a * d - b * c == 1
]
pts = [complex(x / 3, y / 3) for x in range(-3, 4) for y in range(1, 5)]
for k in (2, 4, 12):
    for g in mats:
        for h in mats:
            for z in pts:
                lhs = j(matmul(g, h), z, k)
                rhs = j(g, act(h, z), k) * j(h, z, k)
                assert abs(lhs - rhs) < 1e-6 * max(1.0, abs(lhs)), (g, h, z, k)

# -I is in Gamma_0(N) for every N, and forces even weight
minus_I = (-1, 0, 0, -1)
for k in (1, 2, 3, 4):
    factor = j(minus_I, complex(0, 1), k)      # (0*z - 1)^k = (-1)^k
    assert abs(factor - (-1) ** k) < 1e-12
assert (-1) ** 3 == -1 and (-1) ** 2 == 1      # odd k forces f = -f, hence f = 0

# ===================== level 1, weight 12 ==================================

Delta = shift(power(euler_factor(1), 24), 1)
assert Delta[1:7] == [1, -24, 252, -1472, 4830, -6048], Delta[1:7]

E4 = [1] + [240 * sigma(3, n) for n in range(1, PREC)]
E6 = [1] + [-504 * sigma(5, n) for n in range(1, PREC)]
assert E4[:4] == [1, 240, 2160, 6720]
assert E6[:4] == [1, -504, -16632, -122976]

lhs = [a - b for a, b in zip(power(E4, 3), mul(E6, E6))]
assert lhs == [1728 * c for c in Delta], (lhs[:6], [1728 * c for c in Delta][:6])

# Delta is a cusp form: it vanishes at the cusp, i.e. a_0 = 0
assert Delta[0] == 0
# while E_4 and E_6 do not
assert E4[0] == 1 and E6[0] == 1

# ===================== level 11, weight 2: the form itself ==================

f11 = shift(mul(power(euler_factor(1), 2), power(euler_factor(11), 2)), 1)
assert f11[0] == 0                                  # a cusp form
assert f11[1] == 1                                  # normalised
assert f11[1:14] == [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4], f11[1:14]

# the coefficients logged in SOURCES.md from LMFDB newform 11.2.a.a
LMFDB = [1, -2, -1, 2, 1, 2, -2, 0, -2, -2, 1, -2, 4]
assert f11[1:14] == LMFDB

# and they equal the point counts of essay 08's curve, at EVERY prime in range
E11 = (0, -1, 1, 0, 0)
checked = 0
for ell in primes_up_to(PREC - 1):
    kind, a = reduction(E11, ell)
    assert f11[ell] == a, (ell, f11[ell], a, kind)
    checked += 1
assert checked >= 10, checked

# including the bad prime, where a_ell came from a different formula entirely
assert reduction(E11, 11)[0] == "split multiplicative"
assert f11[11] == 1

# ===================== multiplicativity, previewing essay 14 ===============

for m in range(1, PREC):
    for n in range(1, PREC):
        if m * n >= PREC or gcd(m, n) != 1:
            continue
        assert f11[m * n] == f11[m] * f11[n], (m, n, f11[m * n], f11[m] * f11[n])

# Delta's coefficients are multiplicative too -- tau(6) = tau(2) tau(3)
assert Delta[6] == Delta[2] * Delta[3] == -24 * 252

print("PASS modular_forms: the weight factor is a cocycle and -I forces even weight;")
print("  E_4^3 - E_6^2 = 1728 Delta exactly; and (eta(z)eta(11z))^2 has a_1 = 1,")
print(f"  multiplicative coefficients, and matches the point counts at {checked} primes")
