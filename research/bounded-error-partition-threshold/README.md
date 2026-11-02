# A sharp bounded-error threshold for rational-frame cut certificates

This contribution was produced by Nick Petalas. Apache-2.0.

**Claim type: scoped proof with exact finite corroboration.** Allowing errors
does not evade a weighted partition certificate if simultaneous success is
strictly greater than `1/q`, for independent uniform inputs over an alphabet
of size `q`. Arbitrary nonlinear pointwise gates are allowed. For common-flag
rational frames, success above this threshold still requires `s >= Wm`.

The threshold is sharp. For every `q >= 2`, `W >= 2` and `m >= 1`, an
invertible identity circuit with a prescribed swap endpoint has success
exactly `1/q` and rank mass `Wm-1`. All frames are diagonal. An exact swap
circuit costs `Wm` with the same terminal frames.

Independent random coins preserve the obstruction when every fixed-coin
branch has the deficient budget. Expected cost alone is different: mixing
these two circuits gives success greater than `1/q` and expected cost less
than `Wm`. [PROOF.md](PROOF.md) supplies the quantifiers, successful-input
fiber argument, exact matrices and attaining gate words.

This is an originally posed change of correctness model, motivated by Jose
Manuel / jmbarrancoml's [PR1757](https://github.com/CrocSwap/integer-mult-bounds/pull/1757).
Its zero-error results are cited, not audited or replayed. The new step is the
successful-input fiber bound, sharp threshold and distinction between
branchwise and expected budgets. Classical subset counting retains its credit.

## Reproduce

Use CPython 3.12 and the standard library, from the repository root:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/bounded-error-partition-threshold/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/bounded-error-partition-threshold/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/bounded-error-partition-threshold
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/bounded-error-partition-threshold --check-source-history
```

Any absolute CPython 3.12 path can replace this interpreter. The direct check
prints `PASS_BOUNDED_ERROR_PARTITION_THRESHOLD` in a generated JSON receipt
binding all six package files by SHA256. It writes no files and imports no
predecessor implementations. The runner prints `PASS_REGISTERED_RESEARCH_PACKAGE`.

The new finite checks enumerate 2,002 map/demand cases and 111,744 vertex
classes across the declared binary and ternary topologies. They include
nonlinear ternary maps and count their actual successful-input fibers. They execute both attaining words,
charge every physical edge and test randomized mixtures by literal seed/input
enumeration. The 48 framed fixtures execute 1,668 input tuples. Literal random
mixtures execute another 1,668 seed/input cases. Ten invalid-contract controls
reject and five boundary controls pass. Exact counts appear in the generated
receipt. The universal result rests on the written proof, not these finite checks.

## Limits and relation to the frontier

This error-tolerance obstruction is a changed scope under `bit-new-register-model`,
not a new supplier, kappa or multiplication theorem. An error allowance below
`1-1/q` alone cannot open a partition-excluded mechanism. Fixed topology,
independent uniform inputs, distinct designated sinks and complete wire charging
remain essential. Input-dependent topology and uncharged data-dependent advice
are excluded. Coins are independent of inputs. The theorem concerns simultaneous
exact symbol recovery, not numerical distance or individual receiver error.

An arbitrary rational rank metric need not admit a sufficient partition
certificate. Non-common-flag geometry is not universally excluded. Nonuniform
inputs, physical realization, native tariffs, dirty ownership, precision/tape,
stock, compiler and analytic recovery need separate work. No selected cold
replay, native replay or proof-kernel build was run. Independent human and
formal proof-kernel review are unclaimed. Selected PR6030 is unchanged.

## Open next questions

- For a named producer's actual nonuniform distribution, what is the maximum
  mass of a successful transcript fiber? Start with that distribution and one
  deficient cut. A justified distribution and its acquisition costs are missing.
- Can a proposed approximate supplier provide a useful partition certificate
  and simultaneous symbol-success contract? First extract its complete graph,
  endpoints and all wires. Numerical error and physical recovery remain separate.

Structured questions and the stopping decision are in [TASK.json](TASK.json).
The work stops at this first verified threshold result.

## Sources and verification bounds

Base main is `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision eight.
[SOURCES.json](SOURCES.json) pins predecessor statements as provenance, with no
runtime scientific dependencies. Credit Navinor / PR825 for common flags,
Jose Manuel / PR1757 for outgoing transcripts and weighted partitions, and
ywz65 / PR2507 for designated demands and disposable workspace. Their retained
finite-shear and circuit lineages remain credited. The six-frame zero-error
theorem PR5944 and fixed-support Hurwitz success theorem address different
boundaries and are not targets here.

The verifier has fixed finite domains, explicit exceptions and functions below
sixty lines. It has no recursion, subprocesses, network, generated code or input
callbacks. Warning-strict normal and optimized replay supply the available
standard-library diagnostics. Power of Ten rule three deviation: Python
allocates integers, fractions, tuples and dictionaries during verification.
Fixed domains bound live states to 125 input tuples and at most nine circuit
vertices. A fixed-allocation port is outside this bounded checker. Dimensions,
ports and tables are validated at entry.
