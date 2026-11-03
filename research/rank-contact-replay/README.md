# Faster complete mapped-contact replay

The complete PR4841 mapped-contact distance caller takes 2.252 s rather than
8.199 s at the median of five alternating fresh-process pairs on the recorded
local machine, a **72.54% time reduction**. All ten runs succeed with identical
output hashes. This is a scoped implementation-equivalence proof with finite
conformance and local performance evidence. No new kappa is claimed.

The implementation, proof and experiments were produced by Nick Petalas.
David Ganz / Dugongue retains PR4841's compiler, geometric predicates, complete
small-domain checks, frozen graph and expected receipt. Cao Yifan's PR4610 and
Cinna Davis's PR4690/4672 retain the actual-word and contact-model lineage.
The full unchanged predecessor notice is an authenticated input.
Rank-nullity and binary elimination are classical. New work is Apache-2.0.

## Change and evidence

The original actual-change engine moves all 512 elements of each nine-dimensional
subspace for every axis. The replacement moves nine basis vectors and computes
an exact binary rank. A one-contact cache retains the original union rank and
the two immutable bases. [PROOF.md](PROOF.md) derives equality with literal
intersection without using the separate transvection-distance formula.

The complete caller retains every small check, 4,429 frames, 145 maps, all
1,240 chosen mapped edges, the same seed and every one of 79,360 sampled axes.
Its output is checked against the original authenticated JSON. The new engine
prepares exactly 1,240 contacts and executes every actual-change query.
No frozen predecessor file is edited.

The replacement conformance check covers 1,170,036 Lagrangian pair/axis cases
through width three, including the zero axis; 19,600 cases on all binary
two-planes; one equal-value cache replacement; and 4,608 wider cases through
width nine. Eleven invalid inputs, four changed-source controls and two
incorrect-output controls reject. Normal and optimized Python run the same
checks. This is verification of the replacement implementation, not a new
audit claim for the predecessor's construction.

The untimed profile attributes 16.799 of 18.866 profiled seconds to the
retained actual-change engine. Its generator performs 40,711,680 iterations.
The timing experiment includes interpreter startup, source authentication,
both complete caller phases, expected-output validation and JSON output.
Literal samples range from 8.028 to 8.284 s; rank samples range from 2.196 to
2.302 s. The medians are 8.198592292 and 2.251555958 s. Every side runs the
same source, flags and checks. The host has 18 logical CPUs, with observed
load averages 3.66/2.51/1.80 before measurement. Other work may run on this
shared machine, so the local percentage is not a hardware-independent promise.
The profile is excluded from the timing samples. It explains why removing
the enumeration can affect the complete path by this amount.

## Reproduce

From the repository root, using the Python 3.12 environment:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/rank-contact-replay/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/rank-contact-replay/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/rank-contact-replay
```

The direct commands print `PASS_RANK_CONTACT_REPLAY` in generated JSON. The
launcher must also print `PASS_REGISTERED_RESEARCH_PACKAGE`. Source pins are
in [SOURCES.json](SOURCES.json); all four live inputs are declared in
[VERIFY.json](VERIFY.json). Python's standard library suffices.

Run `replay.py` for the complete faster caller or add `--engine literal` for
the retained engine. To remeasure, choose an existing scratch directory and run:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/rank-contact-replay/benchmark.py --output "$TMPDIR/contact-benchmark.json"
```

The benchmark emits actual timings, exit status, complete work counts, output
hashes, environment and package-file hashes. It refuses to write inside the
package. Generated logs and receipts belong outside the checkout. Set TMPDIR
to the chosen scratch directory to place verification's temporary corruption
fixtures there too. CI runs conformance, not a speed threshold.

## Limits

The measured path is the entire retained `decoder/testformula.py --graph ...`
caller. It is one command of PR4841's larger package, not its whole five-command
compiler suite. Graph regeneration, new chart search, native implementation,
physical hosting, supplier admission, precision and outer funding were not run.
The five framework assumptions and selected frontier remain unchanged. No
independent human or formal proof-kernel acceptance is claimed.

## Open next questions

Can a basis-only contact ABI remove complete-subspace materialization too?
That could remove preparation work, but changes the caller interface. Start
with a bounded validated basis contract and measure the whole source caller.
It remains outside this first-improvement package.
