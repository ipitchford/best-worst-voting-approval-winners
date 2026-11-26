# AI index: Recovering approval winners from ranked ballots (v0.1.0)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1
states the question, what was known, what is new, related work and a roadmap; Section 9 gives open problems).
DOI 10.5281/zenodo.24547593 (concept 10.5281/zenodo.24547592). Status: unrefereed candidate; internal AI-assisted
review, a proof audit and exact computation only.

## Notation

m >= 3 candidates; approval ballots A; a ranking is compatible with A if A occupies its first |A| positions. Scores
v_1 >= ... >= v_m, v_1 > v_m. W = approval winners. Best–worst voting: (1, 0, ..., 0, -1), equivalently (2, 1, ..., 1, 0).
FUPAC / FPAC / CAC as in Terzopoulou, Lang and Zwicker (TLZ, Definitions 2 and 5): all of W co-winners after k-fold
replication / each y in W separately a winner after replication / each y in W a winner without replication and no
approval loser winning. "Split" variants use probability mixtures of compatible rankings. Gaps g_i = v_i - v_{i+1}.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A | A prescribed set can tie for first place iff a box meets a sum of base polytopes; interval criterion via sorting | Lemma 2, Corollary 3 (Lemma 4 used in Section 4) | written proof; Edmonds greedy / base polytope (Schrijver ch. 44) credited |
| B | Best–worst voting: for every profile and m >= 3, some k-fold replication with k <= m - 1 has compatible rankings whose winner set is exactly W; m - 1 is attained by one voter | Theorem 5, Example 6 | written proof (counting plus a network-flow/circulation argument); exhaustive check for m = 3, 4, 5 in check_best_worst.py |
| C | Best–worst voting has CAC | Corollary 7 | written proof |
| D | FUPAC is decidable in time polynomial in m and the bit size for rational scores | Theorem 8 | written proof |
| E | Every rule with FUPAC is reflection symmetric (contains TLZ Lemma 3) | Lemma 9 | written proof |
| F | m = 4: FUPAC iff (2+t, 1+t, 1, 0) up to affine change with rational 0 <= t <= 4 (split: real t); m = 5: (2+2t, 1+2t, 1+t, 1, 0) with rational 0 <= t <= 3 (split: real t) | Theorem 10 | necessity at m = 4 due to TLZ note 11; sufficiency (m = 4) and both halves (m = 5) new; exact certificates (3,600 and 30,752 inequalities) |
| G | m = 6 (rational, or split): FUPAC iff gaps (g1, g2, g3, g2, g1), g1 > 0, g3 <= 3g1 + 2g2, 2g2 + g3 <= 8g1; with g1 = 1 a quadrilateral with corners (0,0), (0,3), (5/4, 11/2), (4,0) in (g2, g3) | Theorem 12 | written proof: two witness profiles (functionals (-18, -12, 6), (-24, 6, 3)); exact certificates at three corners (254,016 inequalities each) |
| H | The TLZ scalar inequalities are sufficient for split FPAC for every real scoring vector and for FPAC for every rational one | Theorem 13, Corollary 14 | written proof; 18 + 18 signed vertex cases in verify_rational_fpac.py (relies on the reductions in the text) |
| I | For a one-parameter family of eight-candidate rules satisfying the inequalities, a five-ballot profile has a split completion electing y for every parameter, but a finite replication does so iff the parameter is rational; replication needed is unbounded | Theorem 15, Corollary 16 | written proof; budgets and auxiliary scores (30 versus at least 32) checked in verify_endpoints.py |

## Evidence

| Check | Program | Expected output | Arithmetic |
|---|---|---|---|
| Claims F, G (certificates, witnesses), I (eight-candidate checks) | [code/verify_endpoints.py](code/verify_endpoints.py) with [data/endpoint_certificates.json](data/endpoint_certificates.json) | certificate SHA-256 06af0224c550e93d3be95437f35994cfc23c9582197be4bdc8be99fa92bc4070; 3,600 / 30,752 / 254,016 x 3; witness and eight-candidate lines; ALL CHECKS PASSED | exact integers and fractions (standard library) |
| Claim H | [code/verify_rational_fpac.py](code/verify_rational_fpac.py) | 18 signed vertex cases for r = q and 18 for r > q; ALL CHECKS PASSED | SymPy 1.14.0, exact |
| Claim B for m = 3, 4, 5 | [code/check_best_worst.py](code/check_best_worst.py) | 44, 152, 560 profiles, largest least replication 2, 3, 4; ALL CHECKS PASSED | exact enumeration |

Negative control: changing one rational entry of the four-candidate certificate makes verify_endpoints.py exit 1
under python -O ([REPLAY_RECEIPT.md](REPLAY_RECEIPT.md); also run in CI).

Numbers quoted on the release page: one point / minus one point; at most m - 1 copies; four, five and six candidates;
two copies in the three-candidate example (scores (1, 0, -1) versus (1, 1, -2)); eight candidates and five ballots;
3,600 / 30,752 / 254,016 checks; corners (0,0), (0,3), (5/4, 11/2), (4,0).

## Limits

The results concern the existence of sincere completions, not what voters would submit, and are worst-case over all
profiles. The six-candidate classification covers rational rules and split ballots; irrational rules inside the
six-candidate region are open. No explicit description for every m (open problem (i)); least replication for other
FUPAC rules open; whether the rules of Theorems 10 and 12 make the winners exactly W is open. The certificates were
found with a floating-point LP solver and then checked exactly; only the exact checks are part of the proofs.

## Replay and records

Replay commands: [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI
[.github/workflows/replay.yml](.github/workflows/replay.yml). Review: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior art
and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json). Bibliography: [refs.bib](refs.bib). Licences:
[LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff). Hashes: [MANIFEST.sha256](MANIFEST.sha256).
