#!/usr/bin/env python3
"""Backs essays 13 and 25: dim S_2(Gamma_0(N)) = genus X_0(N)
   = 1 + mu/12 - nu2/4 - nu3/3 - nu_inf/2.
Self-checking: asserts against the independently known list of genus-zero levels."""
from math import gcd
from fractions import Fraction as F

def primes_of(N):
    ps, n, d = [], N, 2
    while d * d <= n:
        if n % d == 0:
            ps.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: ps.append(n)
    return ps

def phi(n):
    r = n
    for p in primes_of(n): r -= r // p
    return r

def mu(N):                                  # [SL2(Z) : Gamma_0(N)]
    m = N
    for p in primes_of(N): m = m * (p + 1) // p
    return m

def nu2(N):                                 # elliptic points of order 2
    if N == 1: return 1
    if N % 4 == 0: return 0
    r = 1
    for p in primes_of(N):
        if p == 2: continue                 # factor 1 when N = 2 mod 4
        r *= 1 + (1 if p % 4 == 1 else -1)  # (-1/p)
    return r

def nu3(N):                                 # elliptic points of order 3
    if N == 1: return 1
    if N % 9 == 0: return 0
    r = 1
    for p in primes_of(N):
        if p == 3: continue
        r *= 1 + (1 if p % 3 == 1 else -1)  # (-3/p); p=2 gives factor 0
    return r

def nu_inf(N):                              # cusps
    return 1 if N == 1 else sum(phi(gcd(d, N // d)) for d in range(1, N + 1) if N % d == 0)

def dim_S2(N):
    return F(1) + F(mu(N), 12) - F(nu2(N), 4) - F(nu3(N), 3) - F(nu_inf(N), 2)

if __name__ == "__main__":
    print(f"{'N':>3} {'mu':>4} {'nu2':>4} {'nu3':>4} {'nu_inf':>7}   dim S2(Gamma_0(N))")
    for N in [1, 2, 3, 4, 5, 7, 11, 23, 37, 50]:
        print(f"{N:>3} {mu(N):>4} {nu2(N):>4} {nu3(N):>4} {nu_inf(N):>7}   {dim_S2(N)}")

    # every dimension must be a non-negative integer
    for N in range(1, 400):
        d = dim_S2(N)
        assert d.denominator == 1 and d >= 0, f"N={N}: got {d}"

    # cross-check: the genus-zero levels are classically 1-10, 12, 13, 16, 18, 25
    known0 = {1,2,3,4,5,6,7,8,9,10,12,13,16,18,25}
    got0 = {N for N in range(1, 400) if dim_S2(N) == 0}
    assert got0 == known0, f"genus-0 mismatch: {sorted(got0 ^ known0)}"

    # the two numbers essays 25 and 18 actually assert
    assert dim_S2(2) == 0, "essay 25's contradiction"
    assert dim_S2(11) == 1, "essay 18's conductor-11 example needs a 1-dim space"
    print("\nlevel 2:  1 + 3/12 - 1/4 - 0/3 - 2/2 =", dim_S2(2), " <- essay 25")
    print("level 11:", dim_S2(11), "-> a unique newform, essay 18's worked example")
    print("dim = 0 at levels:", sorted(got0))
    print("all assertions passed")
