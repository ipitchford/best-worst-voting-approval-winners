"""Exact all-ranks check of the four-cutoff inequality in the single-winner theorem.

This uses primal extreme points instead of the paper's dual multipliers.
At cutoffs 1, q, q+1, m-1 let the probability weights measure score gaps.
The two scalar conditions say that the weighted means of g and b are
nonpositive. We check that the weighted mean of f is then nonpositive,
where f is r times the per-ballot excess, r is the number of rivals in
the subset, and q is the number approved. The paper reduces the hard
case to all q approved rivals lying in the subset, r >= q and r > m-q.

Integer parameters are represented by a finite family of nonnegative
offsets. A polynomial with nonpositive coefficients is nonpositive at
all such offsets. All checks are symbolic and use exact integer arithmetic.
Requires Python 3.10 or later and SymPy (tested with SymPy 1.14.0).
The check relies on the manuscript's reduction of the ballot inequality to four cutoffs
(proof of Theorem 13); it verifies the resulting finite linear inequality for every number of
candidates. Failures raise SystemExit, so the script also checks under `python -O`.
"""
from itertools import combinations, product

import sympy as sp


S, T, U = sp.symbols('S T U')
VARIABLES = (S, T, U)


def has_certificate(conditions):
    """Rule out nonnegative weights/constraints and a strictly positive excess."""
    polys = [sp.Poly(p, *VARIABLES) for p in conditions]
    feasibility, excess = polys[:-1], polys[-1]

    def nonpositive(poly):
        return all(c <= 0 for c in poly.coeffs())

    # The value at zero is strictly negative and subsequent terms are nonpositive.
    if any(p.TC() < 0 and nonpositive(p) for p in feasibility):
        return True
    if nonpositive(excess):
        return True
    # Every feasible p is nonnegative. An upper bound on excess+p suffices.
    return any(nonpositive(excess + p) for p in feasibility)


def parameter_regions():
    """Exhaust all nonnegative integer S,T,U, retaining equality cases."""
    for difference, base, gap, first in product(
        (-1, 0, 1), (0, 1 + T), (1, 2 + U), (0, 1 + S)
    ):
        low, high = base, base + gap
        t, u = { -1: (high, low), 0: (low, low), 1: (low, high) }[difference]
        yield {S: first, T: t, U: u}


def extreme_points(g, b, f):
    """Enumerate potential violating vertices of the probability simplex with two cuts."""
    # Only index 1 (the cutoff q) has positive excess. A singleton at q
    # violates the g constraint. Every other violating vertex has two or
    # three support points including q.
    others = (0, 2, 3)
    for i in others:
        # A two-point vertex saturates at least one scalar constraint.
        for active, remaining in ((g, b), (b, g)):
            for direction in (1, -1):
                wq = -direction * active[i]
                wi = direction * active[1]
                yield (wq, wi, -(wq*remaining[1] + wi*remaining[i]),
                       wq*f[1] + wi*f[i])

    for i, j in combinations(others, 2):
        # A three-point vertex saturates both scalar constraints. The
        # cross product gives its unnormalised weights up to a common sign.
        for direction in (1, -1):
            wq = direction * (g[i]*b[j] - g[j]*b[i])
            wi = direction * (g[j]*b[1] - g[1]*b[j])
            wj = direction * (g[1]*b[i] - g[i]*b[1])
            yield (wq, wi, wj, wq*f[1] + wi*f[i] + wj*f[j])


def verify(equal):
    # ell=m-r counts the candidates outside the rival subset.
    # q=m-1 is covered separately in the manuscript. If r=q this leaves ell>=2.
    ell = (2 if equal else 1) + S
    q = ell + 1 + T
    r = q if equal else q + 1 + U
    m = r + ell
    cutoffs = (1, q, q + 1, m - 1)
    # Multiply the q scalar row by m, the m-1 row by 2, and excess by r.
    g = [(m + q - 1)*k - m*q if i < 2 else (m + q - 1)*(k - m)
         for i, k in enumerate(cutoffs)]
    b = [2*k - m for k in cutoffs]
    f = [-(q - 1)*r, q*(q - ell), -r*r + q*(q - ell + 1),
         -q if equal else -r - q]
    count = 0
    for conditions in extreme_points(g, b, f):
        if not has_certificate(conditions):
            for region in parameter_regions():
                local = [p.subs(region, simultaneous=True) for p in conditions]
                if not has_certificate(local):
                    raise SystemExit(f'CHECK FAILED: {equal} {conditions} {region}')
        count += 1
    return count


if __name__ == '__main__':
    for equal in (True, False):
        count = verify(equal)
        print(f'Verified all {count} signed vertex cases for r {"=" if equal else ">"} q.')
    print('ALL CHECKS PASSED')
