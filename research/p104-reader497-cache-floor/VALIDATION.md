# Validation and limits

Prepared for @CubeJerry with substantial OpenAI Codex assistance, 2026-10-30.
Environment: Linux x86_64, CPython 3.12.14, standard library only. No solver,
predecessor Python module, network request or Git command is used by verify.py.

## Executed scientific checks

From the repository root:

```sh
python3.12 -W error -B scripts/research_package.py --package research/p104-reader497-cache-floor
```

The warning-strict direct verifier first generated the committed receipt with
`--output` pointing outside the package. The registered command above then
recomputed and compared every canonical receipt byte
in ordinary and optimized (`-O`) interpreters. Both direct modes reported
`PASS_P104_READER497_CACHE_FLOOR recipes=126 geometric=52964 controls=13 no_new_kappa`.
The runner reported `PASS_REGISTERED_RESEARCH_PACKAGE`.

Coverage:

- Frozen input SHA256 and Git blob checks, nine literal source anchors, complete
  reader-use scan within the selected interval, and actual binary intersections.
- Closure enumeration of all 2,825 subspaces of the six-dimensional source
  universe; all 52,964 comparable contact triples; exactly 126 dimension recipes.
- Six exact integer concave-order comparisons per recipe, unique equality, and
  a positive rank-four gap whenever the root meeting has dimension below six.
- Independently emitted local events and a rational linear interpreter on four
  independent values: 126 representative schedules, 2,006 events, every MOVE
  rank, input preservation, correct receiver output, ownership and cleanup.
- General-proof corroboration at `u=2,...,10`, `1<=s<u`: 10,791 recipes and
  186,780 exact inequalities. This finite check is not the all-dimension proof;
  the latter is the explicit concavity argument in PROOF.md, section 4.
- Thirteen rejection controls, each required to fail for its specified reason:
  root sign; V capture; B capture; cleanup; cache MOVE omission; ownership;
  ascending owned MOVE; source event; source dimension cap; free cache invoice;
  impossible historical delivery; convex tariff; changed source incidence.
- A separate changed-incidence positive control gives ranks `(1,1,2,3,6)` and
  capped differences `(0,0,-1,-1,-1,0)`. It satisfies the local identity and
  contradicts an incorrectly generalized incidence-free obstruction. It is
  explicitly not a changed-source construction on PR6167.

## Committed snapshot and portable replay

The completed scientific snapshot passed these standard repository checks:

```sh
python3.12 -B scripts/check_research_commit.py --package research/p104-reader497-cache-floor --check-source-history --check-modes
python3.12 -B scripts/export_research_package.py export --package research/p104-reader497-cache-floor --ref HEAD --output /tmp/reader497-tested.tar
python3.12 -B scripts/export_research_package.py check /tmp/reader497-tested.tar
```

The displayed archive location is portable; the executed archive was in the
session scratch directory. Both byte/history/mode preflight and export integrity
passed: eight package files plus four declared inputs. The PR6167 head's word
blob was also read directly from Git and equals the pinned `f2d3f98964f939e5ca652f9b1453a0604f15f829`.

The checked archive was extracted into a fresh directory with no Git repository.
Using the absolute CPython 3.12 path and an empty `PATH`, direct checks with
`-W error -I -B` and `-W error -I -O -B` passed in 2.912 and 3.474 seconds.
These are local observations, not speedup claims. Exported files were marked
read-only; all 13 SHA256 values, including the export receipt, stayed unchanged.

In a separate disposable extraction, appending a byte to the frozen word
was rejected as `input SHA256` before parsing. Restoring the source and changing
one paid rank in the certificate was rejected as `complete certificate bytes`.
Both tests used the actual optimized CLI and required the specific error text.
No frozen source in the repository was edited. Later changes were confined to
this validation record and task/handoff metadata; the scientific files stayed
byte-identical. Final publication checks use the complete final tree.

## Provenance and interpretation

The source-bound selected orientation command
`python3 -B scripts/research_selected_baseline.py` passed
`PASS_RESEARCH_BASELINE_BINDINGS_ONLY` after materializing its declared sparse
inputs. That is metadata/source binding, not a selected scientific replay.

Base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8;
PR6167 source head `564a076b113621a93edc4e39968ee4e4a8c9caf0`.
SOURCES.json gives exact immutable input hashes. TASK.json records the random
draw, three candidates, bounded live-overlap coverage, local claim and canonical
main checkpoints. Public Discussion5645 explicitly releases reader497/frame520.
The browser was signed out and the connected GitHub toolset supplied no
Discussion posting operation, so no public coordination post is claimed.

This is a scoped proof and exact certificate, not a finite search failure and
not a full multiplication theorem. No full predecessor/selected cold replay,
native phase replay, physical caller admission, compiler/outer replay, rounded
error analysis, Lean, Docker or hosted CI run is claimed. Independent human
and proof-kernel review remain open. The five selected framework assumptions
remain: native all-columns, owned erasure, uniform compiler, precision/tape,
and analytic recovery. **No new κ.**
