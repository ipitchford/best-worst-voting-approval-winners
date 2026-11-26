# Replay receipt (v0.1.0, 26 November 2026)

Release replay by the publisher from a fresh copy of the approved candidate (code, data, requirements.txt), macOS
arm64, working directory the package root. Interpreters as printed inside the run (see [ENVIRONMENT.txt](ENVIRONMENT.txt)):
CPython 3.12.11 with SymPy 1.14.0; CPython 3.14.7 (uv shim) for the two standard-library scripts.

| Program | Flags | Exit | Output |
|---|---|---|---|
| code/verify_endpoints.py | -I -B -O | 0 | certificate sha256 06af0224c550e93d3be95437f35994cfc23c9582197be4bdc8be99fa92bc4070; 3,600; 30,752; 254,016 x 3; facet witnesses (-18, -12, 6) and (-24, 6, 3); eight-candidate line; ALL CHECKS PASSED |
| code/verify_rational_fpac.py | -I -B -O | 0 | 18 signed vertex cases for r = q and 18 for r > q; ALL CHECKS PASSED |
| code/check_best_worst.py | -I -B -O | 0 | m = 3: 44 profiles {1: 39, 2: 5}; m = 4: 152 {1: 116, 2: 28, 3: 8}; m = 5: 560 {1: 393, 2: 122, 3: 40, 4: 5}; ALL CHECKS PASSED |
| Negative control | verify_endpoints.py with one entry of the (6,5,1,0) certificate (class 4,1,3,0) changed from 12 to 11, -I -B -O | 1 | `CHECK FAILED: class sum for 4,1,3,0` |

stderr was empty for all passing runs. The output matches the lead's clean replay of 24 November 2026. After the
replay only the title-page DOI line of manuscript.tex, the rebuilt PDF and the release records changed; the code,
certificate data and requirements are byte-identical to the approved candidate.

Comparison policy for other platforms: exact (integer and rational arithmetic only).
