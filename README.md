# Recovering approval winners from ranked ballots

**Best–worst voting and the approval-compatibility questions of Terzopoulou, Lang and Zwicker**

Version 0.1.0 · DOI [10.5281/zenodo.24547593](https://doi.org/10.5281/zenodo.24547593) (all versions:
[10.5281/zenodo.24547592](https://doi.org/10.5281/zenodo.24547592)) · Author: Anonymous · Text CC0-1.0, code MIT ·
Release page: https://evidencepress.org/releases/best-worst-voting-approval-winners/

**Status: unrefereed research candidate.** The proofs and computations were checked by internal AI-assisted review,
a proof audit and clean replays only (see [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)). This is not peer review,
independent reproduction or formal verification.

## What this is about

Some organisations elect by approval voting: each voter ticks every candidate they find acceptable, and the candidates
with the most ticks win. Others ask voters to rank the candidates and award points by position; Borda counting is the
best-known such scoring rule. If the same sincere voters switched from ticking to ranking, each would put every
candidate they approved above every candidate they did not, but nothing fixes the order inside those two groups.

Could a scoring rule then reproduce the approval result, for some sincere choice of rankings? If not, switching the
ballot format can change the winner even when nobody changes their mind. Terzopoulou, Lang and Zwicker (Social Choice
and Welfare, 2026) showed that Borda can always make all approval winners win together, provided every ballot is
counted a fixed number of times (their device for letting a ballot be split between rankings), and that with three
candidates no other scoring rule can. They asked whether Borda is the only such rule for more candidates.

A small example: with three candidates and one voter approving x and y, best–worst voting (one point for first
place, minus one for last) on one ballot gives scores (1, 0, −1), so only one approval winner wins. Two copies ranked
x y z and y x z give (1, 1, −2): both approval winners win and z loses.

## What is new

1. **Best–worst voting recovers the approval winners exactly**, for any number m of candidates, with at most m − 1
   copies of each ballot, and one voter can force that many. The four-candidate rule (2, 1, 1, 0), which the original
   authors believed to work, is best–worst voting, so Borda is not unique.
2. **A polynomial-time test** of the property for any rational scoring rule, and complete lists of the rules that have
   it for four and five candidates and of the rational rules for six candidates. The four-candidate list completes a
   necessary condition stated by Terzopoulou, Lang and Zwicker; the five- and six-candidate lists are new.
3. **One designated winner.** Their conjectured inequalities decide when a single approval winner can be elected,
   whenever a ballot may be split (any scores) and with whole copies for rational scores.
4. **Where whole copies differ from splitting.** With irrational scores the conjecture can fail: in one
   eight-candidate, five-ballot election the designated candidate can win exactly when a parameter of the rule is
   rational, and the number of copies needed can be arbitrarily large.

## Limits

The results are about the existence of sincere rankings, not about what voters would actually submit, and they hold
for every possible electorate (worst case). The six-candidate classification covers rational rules (and split
ballots); irrational six-candidate rules are open, and there is no general formula for all numbers of candidates.
Borda already had the property, so the novelty lies in the second rule, the sharp copy count, the test and the lists.

## Contents

| Path | What it is |
|---|---|
| [manuscript.pdf](manuscript.pdf), [manuscript.tex](manuscript.tex) | The paper (14 pages); Section 10 describes the checks |
| [code/verify_endpoints.py](code/verify_endpoints.py) | Standard library. Checks the exact certificates in `data/` (3,600 inequalities at four candidates, 30,752 at five, 254,016 for each of three six-candidate corner rules), the two six-candidate witness profiles and the eight-candidate counterexample |
| [code/verify_rational_fpac.py](code/verify_rational_fpac.py) | SymPy 1.14.0. The 18 + 18 signed vertex cases of the one-winner criterion |
| [code/check_best_worst.py](code/check_best_worst.py) | Standard library. All one- and two-voter profiles for three to five candidates (44, 152, 560 profiles): least replication never exceeds m − 1 and reaches it |
| [data/endpoint_certificates.json](data/endpoint_certificates.json) | Rational certificates (SHA-256 06af0224c550e93d3be95437f35994cfc23c9582197be4bdc8be99fa92bc4070, printed in the paper) |
| [refs.bib](refs.bib) | Bibliography |
| [AI_INDEX.md](AI_INDEX.md), [RESEARCH_GATES.json](RESEARCH_GATES.json) | Machine-readable claim map; prior-art and limitation record |
| [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt) | Checking record |
| [MANIFEST.sha256](MANIFEST.sha256), [LICENSE.md](LICENSE.md), [CITATION.cff](CITATION.cff) | Hashes, licences, citation |

## Replay

From the package root (any Python 3.10 or later; seconds in total):

```sh
python3 -I -B -O code/verify_endpoints.py
python3 -m pip install sympy==1.14.0 && python3 -I -B -O code/verify_rational_fpac.py
python3 -I -B -O code/check_best_worst.py
```

Each prints `ALL CHECKS PASSED` and exits 0; any failed check exits non-zero, also under `-O`. All arithmetic is exact
(integers and rationals), so outputs are compared exactly on every platform; no tolerance is used. GitHub CI
([.github/workflows/replay.yml](.github/workflows/replay.yml)) runs all three on Linux, compares the printed lines with
the expected ones and runs a negative control (a changed certificate entry must fail).

## Cite

Anonymous (2026). *Recovering approval winners from ranked ballots: best–worst voting and the approval-compatibility
questions of Terzopoulou, Lang and Zwicker* (version 0.1.0). Evidence Press. https://doi.org/10.5281/zenodo.24547593
