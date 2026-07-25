#!/usr/bin/env python3
"""Backs essay 02: Kummer's regularity criterion.
p is regular iff p does not divide the numerator of B_{2i} for 1 <= i <= (p-3)/2.
Computes Bernoulli numbers exactly and derives the irregular primes.
Self-checking: asserts the classical start of the irregular-prime sequence."""
from fractions import Fraction as F
from math import comb

def bernoulli(n_max):
    """B_0..B_n_max by the standard recurrence sum_{j<=n} C(n+1,j) B_j = 0, n>=1."""
    B = [F(0)] * (n_max + 1)
    B[0] = F(1)
    for n in range(1, n_max + 1):
        s = sum(comb(n + 1, j) * B[j] for j in range(n))
        B[n] = -s / (n + 1)
    return B

def primes_upto(N):
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, N + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]

if __name__ == "__main__":
    LIMIT = 200
    B = bernoulli(LIMIT)

    irregular = {}
    for p in primes_upto(LIMIT):
        if p < 5:
            continue
        witnesses = [2 * i for i in range(1, (p - 3) // 2 + 1)
                     if B[2 * i].numerator % p == 0]
        if witnesses:
            irregular[p] = witnesses

    print("first Bernoulli numbers:")
    for n in [2, 4, 6, 8, 10, 12, 32]:
        print(f"  B_{n:<3} = {B[n]}")

    print(f"\nirregular primes below {LIMIT} (p divides numerator of B_2i, 1<=i<=(p-3)/2):")
    for p, ws in sorted(irregular.items()):
        print(f"  p = {p:<4} witnessed by B_{ws[0]}" + (f" (and B_{ws[1:]})" if len(ws) > 1 else ""))

    got = sorted(irregular)
    known = [37, 59, 67, 101, 103, 131, 149, 157]
    assert [p for p in got if p <= 157] == known, f"got {got}"
    assert 37 in irregular and irregular[37] == [32], f"37 should be witnessed by B_32, got {irregular.get(37)}"

    # 23 is REGULAR even though Z[zeta_23] is not a UFD (its class number is 3):
    # regularity asks p does not divide h_p, not that h_p = 1.
    assert 23 not in irregular, "23 must come out regular"
    print("\n23 is regular:", 23 not in irregular, "-- so Kummer's theorem covers p = 23")
    print("smallest irregular prime:", got[0], "-- the first exponent Kummer's method misses")
    print("all assertions passed")
