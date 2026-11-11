# Linear drift in a repeated rounded native cycle

This contribution is produced by Nick Petalas.

For the unchanged fixed-grid native cycle `29→0→2→341→29` of
[JoyboyBrian's PR5492](https://github.com/CrocSwap/integer-mult-bounds/pull/5492),
let C be one rounded traversal. On coordinates `(1,10,39,44)`, take

```text
x = (3+2i, 1, 3i, 3+i)
d = (-4+4i, 4+4i, 4+4i, 4-4i).
```

All other 508 coordinates are zero. The new exact identity is

```text
C^(24k)(x) = x + k d,     k >= 0.
```

Thus this rounded identity cycle has infinite order and Euclidean defect
`8 sqrt(2) k` after `24k` traversals. At grid spacing `h=2^-g`, the same
witness has defect `8 sqrt(2) k h`. A fixed grid therefore admits no absolute
error bound independent of the number of traversals.

A second consequence concerns exact correction. If the unchanged rounded
payload and a tag are the decoder's only inputs, correction for every signed
integer input and paths of length `0,24,...,24K` needs at least `K+1` tag
states, hence at least `ceil(log2(K+1))` bits in a fixed-width tag. The proof
allows an arbitrary deterministic decoder, not only additive corrections.
Supplying the path length separately supplies additional side information.
A fixed bounded input domain is outside this storage lower bound.

This is a **scoped proof with an exact finite certificate**. The universal
iteration statement follows from a proved integral-shift covariance lemma
and a checked 24-step orbit, rather than extrapolation from a long run.
[PROOF.md](PROOF.md) gives the circuit, shift certificate and decoder argument.
It also states the diagnostic's complete claim boundary.

## Reproduce

From the repository root, with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/native-loop-linear-drift/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/native-loop-linear-drift/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/native-loop-linear-drift
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/native-loop-linear-drift --check-source-history
```

The direct verifier prints generated JSON with status
`PASS_NATIVE_LOOP_LINEAR_DRIFT`. Its normal and optimized modes check the
same finite domain:

- All 96 edges of the new orbit with two implementations, one on four
  coordinates and one on the full 512-coordinate bank.
- Eight exact even-difference tests establishing the shift certificate,
  plus 128 signed covariance fixtures, including 80-bit inputs.
- 2,401 complete small pair inputs against a separate component formula
  and exact inverse, 769 consecutive iterate formulas, and 33 distinct
  originals producing one identical final payload.
- Four rejecting controls and two positive controls, including a periodic
  input. The theorem asserts existence of drift, not drift on every input.

No predecessor executable or scientific receipt is replayed. The unchanged
recipe data are authenticated before use. Optional `--receipt /absolute/path`
writes a new hash-bound receipt outside the checkout and refuses overwrite;
`--check-receipt /absolute/path` recomputes it. No receipt is handwritten or
committed. [VALIDATION.md](VALIDATION.md) records local execution and limits.
The direct commands also work in the official Git-free package export.

## Scope and credit

PR5492 supplies the actual signed native recipes, ideal identity loop,
one-traversal defect and source binding. The new contribution is the drift
orbit, integral-shift certificate, infinite-order proof and correction-state
lower bound. Credit JoyboyBrian; Tekalign's P104 reversible lifting;
Cao Yifan's round-three word; ywz65's native adapters; the coherent-frame
additivity work; and the retained P104/native/controller/geometry lineage.
Sricharan Vagvala's PR1631 supplies a related orbit-based rounding obstruction
for a different shear-equivariance contract, and Sagar Thakrar's PR1537
constructs exact paid infinite-order returns. Neither studies this rounded
identity cycle. Reversible lifting, floor translation and the pigeonhole
principle are classical. No literature-priority claim is made.

The cycle joins occurrences on different supplier roles. It is a frame
consistency diagnostic, not a chronological supplier subword. Width one
already establishes this scoped obstruction; other tensor widths, every
initial input, dynamic grids and changed edge maps are unclaimed. Every
finite reverse word still restores its input exactly.

The result supplies no paid replacement, full physical implementation,
new kappa or selected-frontier change. Native pricing, owned erasure,
compiler closure, complete precision/tape and analytic recovery remain
open. Source pins are in [SOURCES.json](SOURCES.json); the current source-binding
orientation passed for selected PR6030 at canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. Independent
human and formal proof-kernel review are unclaimed. New work is Apache-2.0.

## Open next questions

1. Bind an equivalent drift segment to an actual chronological caller with
   its full entry and restored exit. Start from one named caller; no such
   embedding is supplied by this diagnostic.
2. Specify a changed rounded-edge ABI that removes the drift, with an explicit
   storage, erasure and scalar-ADD contract. Price the complete physical and
   recursive bill before claiming a supplier improvement.

The structured questions and blockers are in [TASK.json](TASK.json). Research
stops at this first verified result. Minimal drift periods and other cycles
were not investigated.
