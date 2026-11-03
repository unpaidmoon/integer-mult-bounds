# A full rounded-native fiber already fits at radius three

This contribution was produced by Nick Petalas. Apache-2.0.

Scoped written proof with an exact finite certificate. For the fixed
112-owner rounded inverse of zxv's [PR5444](https://github.com/CrocSwap/integer-mult-bounds/pull/5444)
at three relative output bits, the least integer H admitting a full
4096-preimage fiber inside [-H,H]^112 is exactly **three**. The predecessor
gives radius sixteen as sufficient and explicitly leaves the finite-range
threshold open. The new result supplies a smaller attaining output and an
all-output lower bound. No new kappa is claimed.

    F(x) = 8x - M round_away(8 M^T x / 52),   x in Z^112
    maximum fiber: 4096 inputs
    minimum radius of a box containing such a fiber: 3

[PROOF.md](PROOF.md) proves that radius two is impossible: a maximal fiber
has sixteen full quotient cells, each inducing a width-four interval in
every owner. A radius-two box would force all cell midpoints to zero,
contradicting the injectivity of M on distinct quotient midpoints.

[WITNESS.json](WITNESS.json) gives a literal output y with entries 0,+4,-4,
M^T y=0 and y+2M1 divisible by eight. Its complete quotient set lies in
{-6,-2,2,6}^8. All 4096 reconstructed inputs have magnitude at most three.
Their exact radius counts are 16 at radius one, 1055 at radius two and
3025 at radius three. These counts concern this particular fiber, not
maxima over smaller input boxes.

## Reproduce

From the repository root, using standard-library CPython 3.12:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/rounded-native-fiber-radius/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/rounded-native-fiber-radius/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/rounded-native-fiber-radius
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/rounded-native-fiber-radius --check-source-history
```

Another CPython 3.12 executable may replace the local interpreter path.
Expected markers are PASS_ROUNDED_NATIVE_FIBER_RADIUS,
PASS_REGISTERED_RESEARCH_PACKAGE and PASS_RESEARCH_COMMIT_BYTES.
Every registered command has a 120-second timeout. The direct verifier
also runs from the eight-file package without Git, network or predecessors.
It writes no files. Its stdout receipt is generated and binds every
package file by SHA256; no receipt is handwritten.

The checker enumerates all 65536 candidate quotient tuples, checks every
accepted input with a literal forward map, counts distinct inputs and
checks all sixteen 256-point Cartesian cells and their owner midpoints.
Fifteen boundary, rejection and changed-scale controls remain active under
optimized execution. The all-output minimality claim rests on the written
proof; one finite fiber alone would not establish it.

## Scope, sources and credit

Base is canonical main 2485805a6d47f36ea83ddde6327d453ac82d44dc, priority
revision eight. The selected source-binding orientation passes; it is not
a selected scientific replay. The selected conditional kappa .003125804
and all five inherited framework assumptions are unchanged.

The uniform-transfer-audit card is explicitly changed to this original
finite-range precision/erasure side result in [TASK.json](TASK.json).
It does not discharge a selected assumption or change an actual caller.
[Advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294731).
Live open PRs, recent account contributions, handoffs, active Discussions,
local reservations, main README terms and distinctive merged searches were
checked. Sparse notes, arbitrary historical diffs and unpublished work remain
coverage limits. Empty searches are not proof of novelty.

Credit zxv for PR5444's fiber geometry, source lattice and code calculation,
relative-precision maximum and explicit finite-range question. Credit
Ali Romman/PR5323 for the same-grid recovery theorem, David Ganz/PR4929
and Dillon Amburgey/PR4933 for the fixed native matrix/geometry, Brian/PR5035
for the rounded kernel, and the retained native/controller/precision lineage.
Classical lattice, coding and rounding facts retain their classical status.
The new contribution is the minimum radius, midpoint exclusion and output
witness. MATRIX.json is an exact copy of the predecessor fixture; its bytes
and predecessor proof texts are pinned as provenance in SOURCES.json.
No predecessor scientific verifier or complete workload is imported or run.

PR6182 concerns fixed coordinate-parity recovery tags at four relative bits.
That tag interface is separate from this finite-range threshold question;
no counterpart tag count or altered-precision tag theorem is targeted here.

## Limits

The result uses the exact fixed matrix, origin-centered coordinate box,
integer inputs and half-away rounding. It does not classify smaller fibers,
other precision levels, repeated maps or restricted physical input sets.
Native realization, reversible recovery cost, source access, restoration,
precision/tape/stock costs and a favorable complete supplier invoice remain
open. No full multiplier, independent human review or formal proof-kernel
acceptance is claimed. Lean, Docker and the selected cold replay are unrun.

## Open next questions

- Determine a finite-range threshold for another row of PR5444's table.
  Begin with its equality geometry; no other precision is analyzed here.
- Bind this obstruction to one actual recovery site, including its lattice,
  permitted values and observations. That caller and its complete bill
  are the missing step toward a physical implication.

TASK.json records relevance, first steps and blockers for these questions.

## Code constraints

The verifier has no recursion, subprocess, network, dynamic imports or output
file path. Functions are below sixty lines. Fixed dimensions bound all loops:
65536 quotient tuples, at most 4096 input vectors, sixteen cells with 256
members, 112 owners with four entries and eight modes. Each file read is
capped at one MiB. Explicit exceptions enforce invariants under -O.

Power of Ten rule 3 deviation: CPython allocates managed integers and
containers while checking. Scope is this fixed one-shot verifier. At most
4096 input vectors of 112 small coordinates and 4096 eight-coordinate
quotients are retained, with bounded JSON serialization and eight capped
file reads. Normal and optimized checks exercise these capacities. A future
embedded or unbounded-input implementation needs a separate allocation model.
Rule 9 deviation: six rejecting controls use callbacks with only the named
local validation functions as targets. No external dispatch is allowed.
Warning-strict normal/optimized replay and in-memory compilation supply
diagnostics; no external type checker or linter is installed in this environment.
