"""Exact checks for the simultaneous-recovery classifications and the real-score counterexample.

Run from the package root:  python code/verify_endpoints.py
Needs Python 3.10 or later and the standard library only. Every check raises an
error on failure, so the script also checks under `python -O`.

1. Endpoint certificates (Theorems 10 and 12 of the manuscript). For each certified score vector
   and each nonempty pair (R, S) of candidate sets, inequality (4) of the manuscript
       |S| L_A(R) - |R| U_A(S) <= sum_j alpha_j |class_j & A|
   is checked for every labelled ballot A (a missing key means alpha = 0). The extrema
   L_A, U_A are obtained by enumerating every ranking compatible with A, independently of the symmetry reduction used to find
   the coefficients alpha. Also checked: sum_j |class_j| alpha_j = 0 and alpha_j >= 0 on the
   two classes outside S.
2. Six-candidate facet witnesses (Theorem 12): the two profiles whose interval functional
   equals 6(g3 - 3 g1 - 2 g2) and 3(2 g2 + g3 - 8 g1) on reflection-symmetric vectors.
3. Eight-candidate real-score counterexample (Theorem 15): score budgets and auxiliary scores.
"""
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CERT_FILE = ROOT / 'data' / 'endpoint_certificates.json'


class CheckFailed(Exception):
    pass


def check(condition, message):
    if not condition:
        raise CheckFailed(message)


def subsets_of(universe):
    items = sorted(universe)
    return [frozenset(i for k, i in enumerate(items) if mask >> k & 1) for mask in range(1 << len(items))]


def compatible_rankings(m, ballot):
    rest = [i for i in range(m) if i not in ballot]
    for top in itertools.permutations(sorted(ballot)):
        for bottom in itertools.permutations(rest):
            yield top + bottom


def extrema_table(m, scores):
    universe = frozenset(range(m))
    subsets = subsets_of(universe)
    table = {}
    for ballot in subsets:
        rankings = list(compatible_rankings(m, ballot))
        position = [{c: p for p, c in enumerate(order)} for order in rankings]
        for subset in subsets[1:]:
            totals = [sum(scores[pos[c]] for c in subset) for pos in position]
            table[ballot, subset] = (min(totals), max(totals))
    return subsets, table


def verify_certificate(scores, weights):
    m = len(scores)
    universe = frozenset(range(m))
    subsets, extrema = extrema_table(m, scores)
    checked = 0
    for R, S in itertools.product(subsets[1:], repeat=2):
        key = f'{m},{len(R)},{len(S)},{len(R & S)}'
        alpha = [Fraction(a) for a in weights.get(key, ['0'] * 4)]
        classes = [R & S, R - S, S - R, universe - (R | S)]
        check(sum(len(g) * a for g, a in zip(classes, alpha)) == 0, f'class sum for {key}')
        check(alpha[1] >= 0 and alpha[3] >= 0, f'sign condition for {key}')
        for ballot in subsets:
            lhs = len(S) * extrema[ballot, R][0] - len(R) * extrema[ballot, S][1]
            rhs = sum(len(g & ballot) * a for g, a in zip(classes, alpha))
            check(lhs <= rhs, f'inequality (4) fails: scores={scores} R={sorted(R)} S={sorted(S)} A={sorted(ballot)}')
            checked += 1
    return checked


def symmetric_vector(gaps):
    """Scores (v_1..v_m) with v_m = 0 from gaps g_1..g_{m-1}."""
    return tuple(sum(gaps[i:]) for i in range(len(gaps) + 1))


def interval_functional(m, scores, ballots, R, S):
    """|S| L(R) - |R| U(S) summed over the profile, with extrema from enumeration."""
    total = 0
    for ballot in ballots:
        lows, highs = [], []
        for order in compatible_rankings(m, ballot):
            pos = {c: p for p, c in enumerate(order)}
            lows.append(sum(scores[pos[c]] for c in R))
            highs.append(sum(scores[pos[c]] for c in S))
        total += len(S) * min(lows) - len(R) * max(highs)
    return total


def verify_six_candidate_witnesses():
    m = 6
    # Witness A: candidates a,b = 0,1; c..f = 2..5. Three ballots {c,d,e,f}; four ballots {a,b,i}.
    wa = [frozenset({2, 3, 4, 5})] * 3 + [frozenset({0, 1, i}) for i in (2, 3, 4, 5)]
    Ra, Sa = frozenset({0, 1}), frozenset(range(6))
    # Witness B: candidate y = 0. Four ballots C minus {y}; one ballot {y,i} for each i.
    wb = [frozenset(range(1, 6))] * 4 + [frozenset({0, i}) for i in range(1, 6)]
    Rb, Sb = frozenset({0}), frozenset(range(6))
    for profile in (wa, wb):
        approvals = {sum(c in A for A in profile) for c in range(m)}
        check(len(approvals) == 1, 'witness profile must give every candidate the same approval count')
    # Note: with S = C the interval criterion compares L(R)/|R| with U(C)/|C| = mean score.
    forms = []
    for profile, R, S, expected in ((wa, Ra, Sa, (-18, -12, 6)), (wb, Rb, Sb, (-24, 6, 3))):
        coeffs = []
        for basis in ((1, 0, 0, 0, 1), (0, 1, 0, 1, 0), (0, 0, 1, 0, 0)):
            coeffs.append(interval_functional(m, symmetric_vector(basis), profile, R, S))
        # The functional must be linear on ordered symmetric vectors: test at further points.
        for g in ((1, 2, 3, 2, 1), (3, 1, 7, 1, 3), (2, 5, 1, 5, 2), (1, 0, 4, 0, 1)):
            value = interval_functional(m, symmetric_vector(g), profile, R, S)
            check(value == sum(c * x for c, x in zip(coeffs, g[:3])), f'linearity at gaps {g}')
        check(tuple(coeffs) == expected, f'witness functional {coeffs} != {expected}')
        forms.append(tuple(coeffs))
    return forms


def verify_single_winner_witness():
    """Theorem 15: evaluate both projections under every compatible ranking of each ballot."""
    P = (14, 12, 12, 12, 3, 2, 1, 0)
    Q = (39, 32, 32, 32, 6, 3, 0, 0)
    D = tuple(11 * q - 32 * p + 32 for p, q in zip(P, Q))
    check(D == (13, 0, 0, 0, 2, 1, 0, 32), 'auxiliary vector D')
    for scores in (P, Q):
        check(all((7 + q) * sum(scores) <= 8 * (q * scores[0] + 7 * scores[q]) for q in range(2, 8)),
              'scalar conditions for P and Q')
    ballots = [frozenset(v) for v in ((0,), (0,), (1, 2, 3, 4), (1, 5, 6, 7), (2, 3, 4, 5, 6, 7))]
    check({sum(i in A for A in ballots) for i in range(8)} == {2}, 'every candidate has two approvals')
    max_P = max_Q = forced_D = rival_min_D = 0
    for A in ballots:
        rankings = list(compatible_rankings(8, A))
        top = min(order.index(0) for order in rankings)
        best = [order for order in rankings if order.index(0) == top]
        check(P[top] == max(P[order.index(0)] for order in rankings), 'best position under P')
        check(Q[top] == max(Q[order.index(0)] for order in rankings), 'best position under Q')
        check(all(P[order.index(0)] < P[top] for order in rankings if order.index(0) != top),
              'strict drop below the best position')
        max_P += P[top]
        max_Q += Q[top]
        forced_D += D[top]
        rival_min_D += min(D[order.index(1)] for order in best)
    check(8 * max_P == 5 * sum(P) and 8 * max_Q == 5 * sum(Q), 'score budgets equal the means')
    check((forced_D, rival_min_D) == (30, 32), 'auxiliary scores 30 versus at least 32')


def main():
    raw = CERT_FILE.read_bytes()
    print(f'certificate file sha256 {hashlib.sha256(raw).hexdigest()}')
    certs = json.loads(raw)
    expected = {'6,5,1,0': 3600, '8,7,4,1,0': 30752,
                '5,4,4,1,1,0': 254016, '10,9,5,5,1,0': 254016, '40,36,31,9,4,0': 254016}
    for key, count in expected.items():
        scores = tuple(int(x) for x in key.split(','))
        n = verify_certificate(scores, certs[key])
        check(n == count, f'unexpected number of checks for {key}')
        print(f'{len(scores)} candidates, scores ({key}): {n:,} exact ballot inequalities verified')
    forms = verify_six_candidate_witnesses()
    print(f'Six-candidate facet witnesses: functionals {forms[0]} and {forms[1]} on (g1, g2, g3) verified')
    verify_single_winner_witness()
    print('Eight candidates: both score budgets attained and auxiliary scores 30 versus at least 32 verified')
    print('ALL CHECKS PASSED')


if __name__ == '__main__':
    try:
        main()
    except CheckFailed as exc:
        print(f'CHECK FAILED: {exc}', file=sys.stderr)
        sys.exit(1)
