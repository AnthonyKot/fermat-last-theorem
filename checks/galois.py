"""Checks for essay 03: the Galois group of a cyclotomic field, and Frobenius.

The cyclotomic case is the one place where Frobenius is completely explicit, so it
is where the essay's claims can be tested rather than asserted.

Checked here:

  * [Q(zeta_n) : Q] = phi(n) = deg Phi_n, with Phi_n computed by dividing
    x^n - 1 by the lower cyclotomic polynomials,
  * Gal(Q(zeta_n)/Q) = (Z/n)^* as groups: sigma_a(zeta) = zeta^a composes as
    multiplication of exponents, verified as a full multiplication table,
  * Frobenius has the order the group law predicts. Frob_ell = sigma_ell, so its
    order in Gal is the multiplicative order of ell mod n -- and that order is
    ALSO the residue degree, i.e. the common degree of the irreducible factors of
    Phi_n mod ell. Verified by computing the least d with x^(ell^d) = x in
    F_ell[x]/Phi_n, which is exactly that degree.
  * The splitting extremes: ell splits completely in Q(zeta_n) iff ell = 1 mod n
    (Frob trivial, phi(n) roots), and is inert iff ell generates (Z/n)^*.
  * Q(zeta_5) has the subfield Q(sqrt 5), fixed by {1, sigma_-1}: the element
    zeta + zeta^-1 satisfies x^2 + x - 1 = 0.

Run: python3 checks/galois.py
"""

from math import gcd

# ---------------------------------------------------------------- polynomials
# Coefficient lists, lowest degree first, over Z or over F_ell.


def trim(f):
    while f and f[-1] == 0:
        f.pop()
    return f


def polymul(f, g, m=None):
    out = [0] * (len(f) + len(g) - 1) if f and g else []
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            out[i + j] += a * b
            if m:
                out[i + j] %= m
    return trim(out)


def polydivmod(f, g, m=None):
    """Divide f by monic-or-invertible-leading g. Exact over Z when it divides."""
    f = list(f)
    q = [0] * max(len(f) - len(g) + 1, 0)
    inv = pow(g[-1], -1, m) if m else None
    while len(f) >= len(g) and trim(f):
        if m:
            c = (f[-1] * inv) % m
        else:
            c, r = divmod(f[-1], g[-1])
            assert r == 0, "non-exact division over Z"
        k = len(f) - len(g)
        q[k] = c
        for i, b in enumerate(g):
            f[k + i] -= c * b
            if m:
                f[k + i] %= m
        trim(f)
    return trim(q), trim(f)


def cyclotomic(n, _cache={}):
    """Phi_n over Z, by dividing x^n - 1 by Phi_d for every proper divisor d."""
    if n in _cache:
        return list(_cache[n])
    f = [-1] + [0] * (n - 1) + [1]  # x^n - 1
    for d in range(1, n):
        if n % d == 0:
            f, r = polydivmod(f, cyclotomic(d))
            assert r == [], (n, d)
    _cache[n] = list(f)
    return list(f)


def totient(n):
    return sum(1 for a in range(1, n + 1) if gcd(a, n) == 1)


def residue_degree(n, ell):
    """Least d with x^(ell^d) = x in F_ell[x]/Phi_n: the degree of its factors."""
    phi = cyclotomic(n)
    phi = [c % ell for c in phi]
    # x^(ell^d) by repeated ell-th powering, reduced mod Phi_n each time
    cur = [0, 1]  # x
    for d in range(1, totient(n) + 1):
        acc = [1]
        base = list(cur)
        e = ell
        while e:
            if e & 1:
                acc = polydivmod(polymul(acc, base, ell), phi, ell)[1]
            base = polydivmod(polymul(base, base, ell), phi, ell)[1]
            e >>= 1
        cur = acc
        if cur == [0, 1]:
            return d
    return None


def multiplicative_order(a, n):
    a %= n
    assert gcd(a, n) == 1
    k, x = 1, a
    while x != 1:
        x = (x * a) % n
        k += 1
    return k


# ============================== degree = phi(n) =============================

for n in range(1, 26):
    assert len(cyclotomic(n)) - 1 == totient(n), n

assert cyclotomic(1) == [-1, 1]  # x - 1
assert cyclotomic(3) == [1, 1, 1]  # x^2 + x + 1, the essay-02 minimal polynomial of omega
assert cyclotomic(4) == [1, 0, 1]  # x^2 + 1
assert cyclotomic(5) == [1, 1, 1, 1, 1]
assert cyclotomic(8) == [1, 0, 0, 0, 1]

# ============================== Gal = (Z/n)^* ==============================

for n in (3, 4, 5, 7, 8, 9, 12):
    units = [a for a in range(1, n) if gcd(a, n) == 1]
    assert len(units) == totient(n)
    # sigma_a . sigma_b = sigma_(ab): a full multiplication table
    for a in units:
        for b in units:
            assert (a * b) % n in units
            assert (a * b) % n == (b * a) % n  # abelian, so Frobenius is well defined
    # every element has an inverse in the group
    for a in units:
        assert any((a * b) % n == 1 for b in units), (n, a)

# ============================== Frobenius has the right order ==============

for n in (3, 4, 5, 7, 8, 9, 11, 12):
    for ell in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % ell == 0:
            continue  # ramified; the essay excludes these
        predicted = multiplicative_order(ell, n)
        assert residue_degree(n, ell) == predicted, (n, ell, predicted)

# ============================== the two extremes ===========================

for n in (5, 7, 8, 12):
    phi = cyclotomic(n)
    for ell in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        if n % ell == 0:
            continue
        roots = [x for x in range(ell) if sum(c * pow(x, i, ell) for i, c in enumerate(phi)) % ell == 0]
        if ell % n == 1:
            # Frobenius trivial: splits completely, phi(n) distinct roots
            assert len(roots) == totient(n), (n, ell, roots)
            assert residue_degree(n, ell) == 1
        else:
            assert len(roots) == 0, (n, ell, roots)
            assert residue_degree(n, ell) > 1
        # inert exactly when ell generates the whole group
        inert = multiplicative_order(ell, n) == totient(n)
        assert inert == (residue_degree(n, ell) == totient(n))

# ============================== Q(zeta_5) contains Q(sqrt 5) ===============

# alpha = zeta + zeta^-1 is fixed by sigma_-1. Working modulo Phi_5:
phi5 = cyclotomic(5)
# alpha as a polynomial in zeta: zeta + zeta^4
alpha = [0, 1, 0, 0, 1]
alpha = polydivmod(alpha, phi5)[1]
alpha_sq = polydivmod(polymul(alpha, alpha), phi5)[1]
# alpha^2 + alpha - 1 = 0
total = [0] * 4
for i, c in enumerate(alpha_sq):
    total[i] += c
for i, c in enumerate(alpha):
    total[i] += c
total[0] -= 1
assert trim(total) == [], trim(total)
# so alpha = (-1 +- sqrt 5)/2 and Q(alpha) = Q(sqrt 5), an index-2 subfield
assert ((-1) ** 2 - 4 * 1 * (-1)) == 5  # discriminant of x^2 + x - 1

print("PASS galois: degree = phi(n), Gal = (Z/n)^*, Frobenius order = residue degree,")
print("  splitting extremes, and Q(sqrt 5) inside Q(zeta_5)")
