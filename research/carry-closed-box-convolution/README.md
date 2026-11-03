# Remove index padding from carry-graded box convolution

A changed carry grade permits index stride N instead of 2N-1 in PR524's
box-convolution packing. For D axes and volume N, choose T>D coprime to N.
The exact signed convolution uses four integer products, each with fewer
than 2NT coefficient slots. Power-of-two boxes admit T<=D+2.

Claim type: scoped constructive proof with exact finite corroboration.
This contribution was produced by Nick Petalas. No new kappa is claimed.

The first retained improvement is the twelve-axis binary box. Its product
extent is 106495 slots, saving 81896 slots against PR524's 188391-slot layout.
The checker enumerates the actual slot maxima and executes the four new
integer products. This is a representation saving, not a runtime measurement.

The new step is to choose the grade weights backwards with last weight zero.
Adding two packed input indices then counts every coordinate carry, including
the final overflow into the grade digit. The total carry count is between
zero and D, so T>D rejects every overflow. [PROOF.md](PROOF.md) proves the
identity for arbitrary positive radices, signed coefficients and singleton
axes. The finite checker corroborates it without importing predecessor code.

## Reproduce

From the repository root, using CPython 3.12 and its standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/carry-closed-box-convolution/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/carry-closed-box-convolution/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/carry-closed-box-convolution
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/carry-closed-box-convolution --check-source-history
```

Any CPython 3.12 path can replace the absolute interpreter path. Direct replay
prints `PASS_CARRY_CLOSED_BOX_CONVOLUTION` in a generated JSON receipt with
actual enumeration counts and SHA256 hashes. It writes no files. Both normal
and optimized registered commands must pass. Source inputs are authenticated
but their scientific suites are not replayed as this contribution.

The checker covers all coordinate pairs for axes in 1..3, dimensions 1..5,
and volume at most 100; complete signed coefficient arrays in {-1,0,1} on
six stated small shapes; 48 deterministic ragged signed products; and the
4096-output separable large fixture. Four further products exercise maximum
volume, dimension and coefficient limits, including either input being zero.
Arithmetic controls expose missing final
carry, undersized modulus, wrong recurrence, lost signed cross terms and
missing grade-wrap extraction. Invalid axes, volume, modulus and coefficients
must reject. The receipt gives enumerated counts rather than inferred totals.

## Limits and implementation bounds

The executable accepts 1..16 axes, volume <=4096, T<=64 and coefficient
magnitudes <=65536. The written theorem is uncapped. Arithmetic is exact and
checks stay active under `-O`. There is no recursion, evaluator, subprocess,
network access or global mutable state. All functions fit within 60 lines.

Power of Ten rule 3 has a managed-runtime deviation. Python integers, tuples
and byte buffers allocate during execution. Each input buffer is at most
262144 coefficient slots and each product buffer at most 524287 slots, with
at most six bytes per slot under the executable caps. There are four integer
products. Coordinate storage has at most 4096 rows of at most 16 integers.
The checker uses larger aggregate iteration counts only over the explicitly
bounded finite domains described above. Runtime/library allocator overhead
is not a measured memory bound. A fixed-allocation native implementation
would need its own proof and tests before use as a physical supplier.

No strict total-memory or fixed-tape runtime claim is made. Warning-strict
normal and optimized execution and source/pin checks are the available
Python diagnostics; Ruff and mypy were unavailable in the retained interpreter.
The software checks are finite corroboration of the proof, not a proof kernel.

T>D and coprimality are sufficient, not necessary. Arbitrary radices can
require a large T, so this does not improve every box. Byte alignment adds
up to seven coefficient bits per slot; the claim compares coefficient slots.
Physical packing, extraction, movement, arbitrary dirty restoration, table
construction, the full weighted tensor solve and its outer invoice remain
unpriced. The selected frontier and its five framework assumptions are
unchanged. No selected cold replay, Lean, Docker, rounded multiplier,
independent human review or formal proof-kernel acceptance was run.

## Open next questions

- Can a smaller admissible grade modulus preserve stride N for a useful
  general-radix family? Start with the attainable total-carry counts and the
  backward congruences. The coprime sufficient condition is not optimal.
- Can this layout be installed in one literal weighted Gaussian caller with
  complete packing, extraction, movement and precision costs? Start with one
  actual recentered tile and preserve its input/output ordering. No complete
  physical caller or favorable outer invoice is supplied here.

Structured questions and blockers are in [TASK.json](TASK.json).

## Credit and overlap

Credit Chafik Boukhalfa / chafreaky, PR524 at
`9161fb1ff1c71bd8255e32d57ab5164aa8109376`, for the mixed-radix carry filter,
signed product convention, weighted tensor motivation and retained Gaussian
lineage. Credit Ross Richardson / PR918 for the fixed-layout modulus scope.
The rank-filtered convolution literature cited by PR524 retains its credit.
Predecessor files and notices are unchanged. New work is Apache-2.0.

The uniform-transfer-audit card is explicitly changed to a representation side
result. It does not resolve a selected framework assumption. Live open PRs,
active Discussions, merged formula/object searches, recent account work and
local reservations were checked before the
[advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19291929).
Cached sparse-note coverage was incomplete and is not a novelty certificate.
The concurrent unsigned radix carry-capacity claim studies normalization of
coefficient digits, whereas this construction changes coordinate-index grades.
