# Packed exact Gaussian products in the complete order-17 replay

A new signed integer matrix kernel reduces the measured complete four-command
PR6208 replay median from 198.08 ms to 181.89 ms, an 8.17% reduction. This is
a scoped implementation proof and a local performance result. There is no
new Clifford theorem, multiplication bound or selected-frontier change.

The opt-in runner replaces only exact matrix multiplication in the primary
checker. Its matrix, polynomial, Pauli, Bell and seven hypothesis checks stay
intact. The separately written checker stays unchanged. All frozen files retain
their bytes. [PROOF.md](PROOF.md) proves signed extraction and the resource
bounds. [SOURCES.json](SOURCES.json) binds the five live inputs at canonical
main 2485805a6d47f36ea83ddde6327d453ac82d44dc.

## Evidence and limits

Five alternating bundles per side complete 40 commands with zero failures and
identical complete stdout hashes. Baseline range is 192.84–215.58 ms; packed
range is 176.45–201.92 ms. All five matched pairs favor the new kernel. The
overlapping ranges reflect shared-machine noise. An earlier five-pair run of
the same arithmetic kernel also improved the median by 6.80%, with disjoint
ranges. The final receipt binds the published kernel, runner and benchmark
hashes; its generated JSON is retained in the PR body. Timings are local to
CPython 3.12.15 on macOS arm64 and are not a cross-platform guarantee.

A separate profile identifies exact multiplication as about half the original
primary cost. The new primary still spends time constructing and canonicalizing
Pauli matrices; the independent checker and process startup are also unchanged.
The benchmark includes all four processes, imports, authentication and output
capture. It excludes the additional equivalence/regression checks introduced
here. No speedup of the generic registered package command is claimed.

The coverage check compares every one of 85 literal matrix products, with
21760 Gaussian output entries, and complete primary stdout. It also runs the
actual packed CLI and unchanged independent checker. Additional controls cover
16275 signed vector pairs, 71 matrix cases, 11 invalid inputs, five changed
sources and negative lower-tail borrowing. These are checks of the new
implementation, rather than a new scientific acceptance claim for PR6208.

## Reproduce

From the repository root, using the existing Python 3.12 environment:

```sh
PY=~/git/integer-mult-bounds/.venv/bin/python3.12
"$PY" -B scripts/research_package.py --package research/packed-order17-replay
"$PY" -I -B -W error research/packed-order17-replay/verify.py
"$PY" -I -O -B -W error research/packed-order17-replay/verify.py
"$PY" -B scripts/check_research_commit.py --package research/packed-order17-replay --check-source-history
"$PY" -B research/packed-order17-replay/benchmark.py --output /absolute/external/path/benchmark.json
```

The benchmark refuses to overwrite a receipt. Each registered command is
bounded to 120 seconds. Only the standard library is required. For the faster
scientific suite itself, run run_replay.py normally and with -O, then run
research/order-seventeen-clifford/independent.py normally and with -O, using
the same interpreter and -I -B -W error flags. The original checks remain
available through their original entry points.

## Open next questions

Does this bounded packed kernel help another actual Gaussian-rational checker
with larger numerator components? First profile that complete consumer and
measure its packing width. This package supplies no evidence for another
consumer, native realization or supplier invoice. Stop if the complete-path
gain falls within noise. The structured question is in [TASK.json](TASK.json).

## Credit

The implementation, scoped proof and experiments were produced by Nick Petalas.
apoursh / Armin Pourshafeie retains PR6208's construction and both original
checkers. Nick Petalas retains PR6192's rank cap and Bell method; Ross Richardson
retains the earlier cubic and Pauli-character lineage. Kronecker substitution
is standard and is not claimed as a new mathematical method. Apache-2.0.
