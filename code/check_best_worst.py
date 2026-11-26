"""Exhaustive independent best-worst stress test on all profiles of one or two voters.

For 3, 4 and 5 candidates, every profile of one or two approval ballots is replicated k = 1, 2, ...
times and all compatible best-worst completions are enumerated; the smallest k whose winners are
exactly the approval winners is recorded. Theorem 5 predicts k <= m - 1, attained. Failures raise
an exception, so the script also checks under `python -O`. Standard library only.
"""
from itertools import combinations_with_replacement, product
from collections import Counter


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def winners(scores):
    return frozenset(i for i, score in enumerate(scores) if score == max(scores))


def check(m):
    all_c = frozenset(range(m))
    ballots = [frozenset(i for i in all_c if mask & (1 << i)) for mask in range(2**m)]
    zero = (0,) * m
    possibilities = {}
    for ballot in ballots:
        first = ballot or all_c
        last = (all_c - ballot) or all_c
        one = {tuple(int(i == f) - int(i == l) for i in range(m))
               for f, l in product(first, last) if f != l}
        poss = {zero}
        for k in range(1, m):
            poss = {add(y, z) for y, z in product(poss, one)}
            possibilities[ballot, k] = poss
    freq = Counter()
    for n in (1, 2):
        for profile in combinations_with_replacement(ballots, n):
            target = winners(tuple(sum(i in a for a in profile) for i in range(m)))
            for k in range(1, m):
                options = [possibilities[a, k] for a in profile]
                if any(winners(tuple(map(sum, zip(*vs)))) == target for vs in product(*options)):
                    freq[k] += 1
                    break
            else:
                raise AssertionError((m, profile))
    return dict(sorted(freq.items()))


if __name__ == '__main__':
    for size in (3, 4, 5):
        result = check(size)
        if max(result) != size - 1:
            raise SystemExit(f'CHECK FAILED: largest factor {max(result)} for {size} candidates')
        print(f'{size} candidates, {sum(result.values())} profiles by smallest replication factor: {result}')
    print('ALL CHECKS PASSED')
