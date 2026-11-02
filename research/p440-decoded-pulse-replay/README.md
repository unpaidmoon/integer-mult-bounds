# Decode-once execution of the complete pivot-440 replay

This contribution was produced by Nick Petalas. Apache-2.0.

Scoped exact implementation improvement with a local performance measurement.
The complete PR1431 independent forward-pulse replay takes **15.91% less wall
time** in the recorded five-pair comparison. Its median falls from 5.886 s to
4.949 s. Every timed process completes the original caller and checks its saved
mathematical receipt. All ten stdout hashes agree. No new mathematical
obstruction, construction or kappa is claimed.

The new opt-in command is [fast.py](fast.py). The frozen
[predecessor package](../complex-p440-window-shocks/README.md) is unchanged.
Hanson Sun's PR1431 supplies the mathematics, enumeration and independent
caller. This contribution changes how its fixed gates execute.

## Exact change and retained coverage

The original pulse interpreter reconstructs the same rational coefficient
each time it visits a gate. The new interpreter prepares one exact `Fraction`
per gate, retains every original gate field, and appends that coefficient.
It preserves the original state recurrence, every gate visit, every pulse cut,
zero removal and operation order. The complete original `main` still runs.
Preparation and source loading are inside the timed process.

For one prepared gate, its saved coefficient equals the source's `amount(g)`
by construction. Starting with equal states, both interpreters add the same
pulses before a cut. Both then perform the same add or scale using that exact
coefficient and remove precisely the zero coordinates. Induction over all cuts,
including the terminal pulse cut, proves equal returned states. No sign,
integrality or nonzero-state hypothesis is needed. The window enumerator reads
only original fields, so its domain, order and response serialization agree.
This proof concerns the fixed interpreter contract, not the predecessor's
mathematical obstruction theorem.

The complete source caller retains 2,757 nonzero windows, one zero window,
1,611 projective directions, all 5,177,758 classified span cases and the full
704-column dirty-input identity. It also retains the missing-close,
wrong-coefficient and omitted-fourth-window rejection controls. The source
checks the full window and direction digests and compares its complete result
with `INDEPENDENT.json`; comparing stdout alone is not the equality test.

The new verifier additionally compares both interpreters on every word of
length zero through two from a 17-gate alphabet, three initial states and
every pulse cut. It rejects changed source bytes, an unknown gate, a zero
denominator and both gate-capacity violations. The normal and optimized
registered commands execute both complete callers, including all source
controls. The generated stdout receipt binds all eight package files.

## Measurement

[BENCHMARK.json](BENCHMARK.json) is the unedited generated timing receipt.
[benchmark.py](benchmark.py) runs five alternating baseline/prepared pairs in
fresh CPython processes. Both sides load the same source and execute the same
complete independent caller. Every subprocess must exit successfully, emit no
stderr and produce the matching success output. The receipt binds the source
manifest, implementation and harness hashes. Timing is opt-in; CI checks its
source bindings and correctness without imposing a machine-dependent speed
threshold.

| Complete independent caller | Median | Observed range |
| --- | ---: | ---: |
| Original gate decoding | 5.886 s | 5.676 to 5.942 s |
| Prepared coefficients | 4.949 s | 4.797 to 5.208 s |

Environment was CPython 3.12.15 on macOS 27.0.1 arm64. The machine reports
18 logical CPUs; the pre-run load averages were 2.61, 2.50 and 1.92. Other
research processes can run concurrently, so the samples alternate and the
claim is local to this measurement. The ranges do not overlap. There were
ten successful complete callers and zero errors.

A separate instrumented profile put 21.961 of 22.601 seconds in
`direct_windows`, chiefly its 2,760 `run` calls. It observed 5,419,435
`amount` calls. Profiling overhead is excluded from reported timings. Rational
state arithmetic and full gate traversal remain; the change does not remove
their cost. No timing claim covers the primary verifier, predecessor test
suite, other pivots or a full supplier replay.

## Reproduce

From the repository root, with the CPython 3.12 standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/p440-decoded-pulse-replay/fast.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/p440-decoded-pulse-replay/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/p440-decoded-pulse-replay/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/p440-decoded-pulse-replay
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/p440-decoded-pulse-replay --check-source-history
```

Add `--baseline` to `fast.py` to run the unmodified interpreter. Run
`benchmark.py` with the same interpreter and flags to print a fresh timing
receipt. Another CPython 3.12 installation can replace the absolute path.
Use a scratch path outside the checkout for redirected output.

The repository runner authenticates all four declared live inputs in
[SOURCES.json](SOURCES.json). Direct execution authenticates the interpreter
bytes and runs the source's word-hash and complete saved-receipt checks.
The selected record and original task catalogue are historical provenance.
The research base is `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority
revision 8. The selected-binding positive control passed; selected conditional
kappa stays `781451/250000000`.

## Bounds and limitations

This is one opt-in execution adapter, with no changes to shared code or frozen
sources. It does not discharge native, compiler, ownership, precision/tape or
analytic-recovery assumptions. No complete multiplication theorem follows.
Independent human and formal proof-kernel review are unclaimed. Lean, Docker,
selected supplier cold replay and a separate static analyzer were not run.

New functions are under 60 lines. Preparation and execution accept at most
8,192 gates; the actual pulse sequences have 1,963 gates. The source word has
1,844 B gates and 6,800 cleanup gates, of which the caller selects 119. The
private interpreter receives only prepared source gates or the finite control
domain. Its state has at most 704 coordinates on the actual word. No recursion,
network access or file writes occur in the implementation or verifier.
Subprocess timeouts are 120 seconds and every return code is checked.

Managed Python allocation is a bounded deviation from static memory allocation.
The fixed gate and coordinate domains bound live collections. Executing
authenticated source bytes and rebinding two names in one private module is a
bounded deviation from avoiding dynamic execution and dispatch. This preserves
the predecessor's complete caller without copying or editing it and bypasses
bytecode-cache reads. The changed-source control exercises that boundary.
The five immediately executed rejection callbacks are a bounded dispatch
deviation. Warning-strict normal and optimized runs and in-memory syntax checks
provide diagnostics. A larger domain, shared module or concurrent use of one
module instance requires a new contract; this package supplies none.

## Open next questions

- Can sparse zero-state handling reduce the remaining exact pulse cost? Begin
  with a profile of the prepared complete caller and cancellation, scale-zero,
  dirty-state and pulse-boundary tests. No such shortcut is supplied here.
- Should a maintained successor adopt this prepared execution? Begin with one
  explicit caller and retain all four pinned inputs and full receipt checks.
  The frozen source integration and broader workload measurements remain open.

Structured relevance, first steps and blockers are in [TASK.json](TASK.json).

## Credit

Credit Hanson Sun / bbMisk for [PR1431](https://github.com/CrocSwap/integer-mult-bounds/pull/1431),
its exact window theorem, source interpreter, independent integer-rank caller
and saved receipts. `run` adapts that interpreter by saving each coefficient;
the new adapter, differential controls, harness and measurements are produced
by Nick Petalas. Marius-Paul Dumitrean / PR1337, Rohan Arun / PR1297, Jeremy
Kothe / PR1274 and the retained construction lineage keep their credit. Source
[notices](../complex-p440-window-shocks/NOTICE.md) and licenses remain applicable
and unchanged. Their mathematical results are predecessors, not new results of
this contribution.
