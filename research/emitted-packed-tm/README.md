# Complete emitted packed TM backend

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped simulation proof with exact finite corroboration.
The package completes the emitted constant-overhead backend left open in
David Ganz / Dugongue's [PR4538](https://github.com/CrocSwap/integer-mult-bounds/pull/4538).
It joins packed input initialization, simultaneous observation, finite dispatch,
signed head motion, fixed-window raw output and genuine halt into ordinary
bounded-word RAM instructions. No host TM-step or access macro remains in the
emitted program. Shared code and predecessor packages are unchanged.

The new dense fixture initializes 256 tape cells in 128 packed data words.
This is an exact storage count for that fixture, not a runtime benchmark.
The all-input statement rests on the induction in [PROOF.md](PROOF.md).
For k tapes, alphabet size A, N initial symbols, m output symbols and T steps,
its complete successful-instruction upper bound is

```text
19 + 4 lambda + 5 log2(B) + 4k + 26N
   + (T+1)(45k + 3k A^k + 1) + 22m.
```

Here lambda=floor(log2(n+2)), c is the fixed symbol-field width and B is the
largest power of two at most floor(lambda/(8c)), with B=1 below that cutoff.
The input includes the scale n; it is not execution fuel. At most
2k ceil((N+T+m+1)/B) tape words are touched, plus the fixed control bank.
The proof states the nonwrapping word-width condition and distinguishes
that word footprint from the address span and emitted code.

## Evidence and reproduction

The new-emitter checks cover 294 cases: 277 halting runs, 17 nonhalting
prefixes, 1,907 literal TM transitions and 419,591 successful RAM instructions.
Every state boundary is compared with a separate signed-coordinate TM model,
including the entire finite possibly affected tape interval. Packed block
sizes 1,2,4,8,16, both zero crossings, multi-block excursions, four tapes,
all supported alphabets, simultaneous cross-copy, nonzero output-tape choices,
zero output and terminal halt are exercised. All fixtures retain arbitrary
unused high bits and one exterior word.

Twelve additional paired fixtures compare new-emitter outputs with the pinned
unpacked compiler from PR4538. Its scientific tests and counts are not replayed
or claimed as new coverage. Six actual emitted-code mutations are rejected,
as are eight invalid machine specifications. The source bytes are authenticated
before scientific execution. [SOURCES.json](SOURCES.json) pins those inputs and
historical catalogue/selected-record provenance.

Run from the repository root with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/emitted-packed-tm/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/emitted-packed-tm/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/emitted-packed-tm
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/emitted-packed-tm --check-source-history
```

Expected markers are PASS_EMITTED_PACKED_TM, PASS_REGISTERED_RESEARCH_PACKAGE
and PASS_RESEARCH_COMMIT_BYTES. Another host's CPython 3.12 path can replace the
shown interpreter. VERIFY.json registers both direct modes with 180-second
limits. The direct verifier prints a generated JSON receipt bound to every
package file's SHA256. Optional `--receipt /absolute/new/external/file.json`
saves the same receipt and refuses to overwrite. Nothing is generated in the
checkout. An official package export retains the three declared predecessor
inputs at their repository paths for the paired comparison.

## Interface and limits

compiler.py exposes Machine, compile_machine and width_bound. The returned
immutable instruction tuple is the actual finite program. ram.py executes only
primitive instructions. The prototype reference interpreter is for this
research certificate; it is not the installed RamStd.step formalization.

The emitter accepts one through four tapes, alphabets of size one through four,
one through sixteen states, and at most one million emitted instructions.
Its input is a well-formed length-prefixed list of a scale, output extent,
then each tape length and symbols. Tape fields begin blank; arbitrary dirty
future blank fields require initialization. The output is exactly m raw
symbols, including zeros. The program preserves its final simulated tapes but
does not erase its control or tape storage. A surrounding cleanup or integer
codec has its own costs. No arbitrary-bit codec, access fusion or tabulation is
silently included.

A particular caller must justify its scale, execution/address envelope, width,
input presentation, output interpretation and any cleanup. No complete
multiplication machine or selected supplier is materialized. Native costs,
dirty-helper restoration, rounded arithmetic, stock, precision, analytic
recovery and all five inherited framework assumptions remain open.
No new kappa, selected-frontier change, unconditional multiplication theorem,
Lean proof or independent human/proof-kernel acceptance is claimed.

## Provenance and overlap

The question source is PR4538, whose representation and unpacked compiler are
credited. Classical packing and simulation methods are not new results here.
Retain the RamStd/Problem 1.8 formalization and Szymon Torunczyk compositional
simulation lineage credited there, together with its native, physical, precision,
compiler and analytic predecessors. Nick Petalas's older PR4883 supplies a
local retained-read access improvement, which this complete emitter does not
yet integrate. Dugongue's PR4541 gives a stronger tabulated asymptotic transfer
as an operational model; PR4724 gives a portfolio construction. Neither is
replaced by this constant-overhead emitted backend.

Canonical base is 2485805a6d47f36ea83ddde6327d453ac82d44dc, priority revision 8.
Selected conditional kappa is .003125804. The selected source-binding first
command passed; no predecessor scientific suite was run as the deliverable.
The uniform-transfer-audit card explicitly changes to this model-transfer side
result. [TASK.json](TASK.json) records the precise scope and next questions.
The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19292016)
was posted before implementation.

Overlap checks covered live open PRs, 319 account PRs since October 23, active
Discussions, recent handoffs, merged packed-backend terms and main README
searches. The cached helper searched 97 of 8,722 main notes; arbitrary code
diffs and unpublished work remain outside that coverage. No novelty conclusion
rests on an absent search match.

## Open next questions

- Can PR4883's retained-read slabs survive the complete dispatcher's clobbers?
  Start by retaining one cache per distinct tape and checking every live cell.
  This could reduce access instructions; cache preservation is the blocker.
- Can a materialized multiplication caller instantiate this backend's actual
  scale, word width and IO contract? Start with its complete finite machine and
  polynomial tape/time envelope. The absent full caller and separately charged
  conversion/cleanup prevent an application claim here.

## Verification bounds

The verifier has no recursion and executes each fixture within the displayed
instruction envelope, capped at ten million successful instructions. Generated
programs are capped at one million instructions. Each new fixture has at most
four tapes, 128 initialized symbols per tape and at most 80 simulated steps;
the two-tape dense fixture has 128 symbols per tape. Alphabet products have at
most 256 tuples, and the directed machines have at most sixteen states. All
functions are below sixty physical lines. Explicit require checks remain
enabled under -O. Warning-strict normal/optimized execution, source compilation
and the package/publication checks provide the recurring diagnostics.

Power of Ten rule 3 has a managed-runtime deviation. Python tuples, integers,
dictionaries and JSON allocate during compilation/replay. The fixed caps above,
512-bit RAM words and one live compiled fixture bound this use; the verifier
does not claim allocation-free operation. A fixed-array interpreter is the
follow-up if that property becomes a caller requirement. Rule 8 has a narrow
source-loading deviation: exactly the hash-authenticated PR4538 Python source
is compiled into an isolated namespace for twelve paired fixtures. It runs no
predecessor test entry point. Ordinary local imports and dataclass construction
are the only other runtime registration. Rule 9 permits the two fixed source
comparison targets compile_tm and VM in that namespace. No input selects an
arbitrary callable. The emitted program itself uses only the enumerated direct
RAM operations; it contains none of this host source loading.
