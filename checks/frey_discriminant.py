#!/usr/bin/env python3
"""Backs essay 22: the Frey curve y^2 = x(x - A)(x + B), where A = a^p, B = b^p and
a^p + b^p = c^p, has discriminant 16(abc)^{2p}.
Verified two independent ways:
  (1) 16 * prod (e_i - e_j)^2 over the roots 0, A, -B;
  (2) the standard Weierstrass b-invariant formula applied to the expanded cubic.
The two routes share no algebra, so agreement is a real check."""

def disc_from_roots(A, B):
    """16 * disc(monic cubic) with roots 0, A, -B."""
    e = [0, A, -B]
    d = 1
    for i in range(3):
        for j in range(i + 1, 3):
            d *= (e[i] - e[j]) ** 2
    return 16 * d

def disc_from_weierstrass(A, B):
    """Expand x(x-A)(x+B) = x^3 + a2 x^2 + a4 x + a6, then the standard formula."""
    a1 = a3 = 0
    a2 = B - A            # -(0 + A + (-B))
    a4 = -A * B           # 0*A + 0*(-B) + A*(-B)
    a6 = 0                # -0*A*(-B)
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6

def disc_from_minimal_model(A, B):
    """The integral model used at 2 when A=-1 mod 4 and B=0 mod 16.

    y^2 + xy = x^3 + ((B-A-1)/4)x^2 - (AB/16)x
    has discriminant (ABC)^2/2^8, where C=A+B.
    """
    assert A % 4 == 3 and B % 16 == 0
    a1, a3, a6 = 1, 0, 0
    a2 = (B - A - 1) // 4
    a4 = -(A * B) // 16
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6

def factor(n):
    n = abs(n); out = {}; d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: out[n] = out.get(n, 0) + 1
    return out

if __name__ == "__main__":
    # Triples with a + b = c, i.e. the exponent-1 case, where solutions DO exist.
    # Only the algebra of the construction is being checked, not the Fermat claim.
    print("exponent p = 1, so A = a and B = b:\n")
    print(f"{'(a,b,c)':>12} {'from roots':>14} {'from Weierstrass':>18} {'16(abc)^2':>14}  agree")
    for (a, b) in [(3, 5), (1, 1), (2, 7), (5, 12), (9, 16)]:
        c = a + b
        d1 = disc_from_roots(a, b)
        d2 = disc_from_weierstrass(a, b)
        d3 = 16 * (a * b * c) ** 2
        print(f"{str((a,b,c)):>12} {d1:>14} {d2:>18} {d3:>14}  {d1 == d2 == d3}")
        assert d1 == d2 == d3, (a, b, c)

    # Higher exponents: A = a^p, B = b^p. a^p + b^p = c^p need not hold -- and by
    # essays 01/02 it cannot for p >= 3 -- but the discriminant identity is pure
    # algebra in A and B, so it is checked with C defined as (A + B).
    print("\ngeneral p, with C := A + B (the identity is algebra, not arithmetic):\n")
    for (a, b, p) in [(3, 5, 5), (2, 3, 7), (1, 2, 11)]:
        A, B = a ** p, b ** p
        C = A + B
        d1, d2 = disc_from_roots(A, B), disc_from_weierstrass(A, B)
        assert d1 == d2 == 16 * (A * B * C) ** 2
        print(f"  a={a} b={b} p={p}:  both routes give 16*(A*B*C)^2  ->  {d1 == d2}")

    # At 2, the normalization A=-1 mod 4 and B=0 mod 16 makes the standard
    # integral change to a minimal model possible. Its discriminant is smaller
    # than the displayed model's by 2^12.
    print("\nminimal model at 2:\n")
    for A, B in [(3, 16), (7, 32), (-1, 32)]:
        C = A + B
        d_displayed = disc_from_weierstrass(A, B)
        d_minimal = disc_from_minimal_model(A, B)
        assert d_displayed == 16 * (A * B * C) ** 2
        assert d_minimal == (A * B * C) ** 2 // (2 ** 8)
        assert d_displayed == (2 ** 12) * d_minimal
        print(f"  A={A:>2} B={B:>2}: displayed/minimal = 2^12  ->  {d_displayed == 2**12 * d_minimal}")

    # the worked example printed in essay 22
    d = disc_from_roots(3, 5)
    f = factor(d)
    assert d == 230400 and f == {2: 10, 3: 2, 5: 2}, (d, f)
    print(f"\nessay 22 worked example: y^2 = x(x-3)(x+5)")
    print(f"  discriminant = {d} = 2^10 * 3^2 * 5^2")
    print(f"  bad primes contained in {{2, 3, 5}} = the primes dividing abc = 3*5*8")
    print("\nall assertions passed")
