# Executed validation and coverage

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.

## Mathematical evidence

The result is a written scoped proof, corroborated by exact standard-library
arithmetic. It is not a claim that finitely many runs prove an infinite theorem.
Both implementations were written in this contribution by the same AI-assisted
contributor; separate algorithms do not constitute independent human review.

Environment: Linux x86_64, CPython 3.12.14, no third-party dependencies.
Source base: `2485805a6d47f36ea83ddde6327d453ac82d44dc`. Exact source pins and
the unchanged retained PR6246 proof are in SOURCES.json.

Executed successfully:

```sh
python3.12 -B scripts/research_package.py --package research/cubic-equal-step-classification
```

All four registered commands use isolated Python, warnings as errors and no
bytecode writes. `verify.py` and `crosscheck.py` each passed in normal and
optimized (`-O`) mode, checking their complete committed JSON receipts.
The wrapper returned `PASS_REGISTERED_RESEARCH_PACKAGE`. There are no
assert-based validation guards in either checker.

| Coverage | Exact completed domain |
|---|---|
| Polynomial algebra | Three power-sum recurrences and their zero bases; one spacing factorization; eight cleared-denominator coefficient identities |
| Dyadic classification | Both rational branches for every r=3..1024, 2,044 decompositions |
| Spacing corroboration | Every d=k/8, -32<=k<=256, k!=0, for r=3..40: 10,944 cases |
| Literal symbolic programs | All fifteen eligible r<=257, every retained child, repair, inverse repair and full inverse; 8,540 family events |
| Literal dirty values | All 27 triples from {-3/2,0,5/4} at r=3,4,16,33,65,129,257: 189 cases, 56,916 events including inverses |
| Large new-branch cases | s=1,2,3,4,5,7,11,17,31,64,128; exact coefficients and repair/inverse from the symbolic deferred boundary; original exponential-length prefixes are not executed |
| Separate coefficient path | 510 exact systems for both branches at r=3..257; 1,020 nonmonic rescalings; literal power sums checked against binary-block concatenation |
| Separate large cases | s=1,2,5,7,11,17,31,64,128, defect derived by binary-block concatenation and weights by generic Gaussian elimination |
| Positive scope controls | PR6212's unequal-direction r14 repair and centered directions -35,0,35 at r50; both outside the classified direction family |

The primary's fourteen pinned-reason controls reject domain/zero-spacing
errors, odd denominators, incorrect fitted spacing, a changed weight,
missing or mistimed restoration, an omitted final query, a missing original
child, forbidden output feedback and duplicate JSON keys. In particular,
moving the first query before its initial shear preserves the final source
but fails the output: endpoint source restoration alone is insufficient.

The separate implementation checks four incorrect spacings against the actual
fourth coefficient, rejects singular zero spacing, and detects the non-dyadic
91/11 coefficient in the credited r14 rational two-query repair. Its nonmonic
tests use both dyadic units and odd nonunits: a nonunit rescaling cannot rescue
an excluded normalized coefficient. These algebraic form tests do not claim
that every nonprimitive row is a physically admissible source frame.

## Proof review and scope

Self-review checked the normalization step, division only by nonzero S1 and d,
the p=3 denominator case, modulo-three sufficiency, chronological query locations,
literal inverses, source-shear visit counts and complete symbolic price list.
The centered r50 example prompted explicit wording that zero must be at an end
of the progression. It is retained as a scope-positive control. The new r33
and r129 count cases are compared against all three pinned predecessors.

The initial metadata check rejected a list-valued `TASK.evidence`, then rejected
a non-enumerated `outcome`; both fields were corrected to the documented schema.
These were packaging failures, not mathematical counterexamples. No failed
scientific case was removed to obtain a pass.

## Source history and transport

The committed-byte preflight passed for all eleven package files and both
declared input files, including owner-execute modes and base-source ancestry:

```sh
python3.12 -B scripts/check_research_commit.py --package research/cubic-equal-step-classification --check-source-history --check-modes
```

The official exporter and its `check --check-inputs` mode passed. The exported
tree contains no Git repository. Both direct checkers passed in normal and
optimized Python using the absolute interpreter path with an empty PATH,
isolated imports and warnings as errors. The fourteen exported files,
including the export manifest, were marked read-only. Every file's bytes and
mode remained unchanged. Normal and optimized stdout matched byte for byte
for each implementation.

Eighteen actual corrupted-export executions rejected with the specified
diagnostic. Each test used a fresh copy; no committed input was edited:

| Mutation | Executions | Required diagnostic |
|---|---:|---|
| Append one newline to each PR6212 and PR6215 proof | 2 inputs × 2 scripts × 2 modes = 8 | Primary `SOURCE_BYTES`, cross-check `INPUT_BYTES` |
| Append one newline to the retained PR6246 proof | 2 scripts × 2 modes = 4 | Primary `PREDECESSOR_BYTES`, cross-check `RETAINED_PROOF_BYTES` |
| Replace the retained PR6246 head in SOURCES.json | Primary in 2 modes | `PREDECESSOR_DECLARATION` |
| Replace a RESULT.json integer-one event count with boolean true | Primary in 2 modes | `RECEIPT_MISMATCH` |
| Replace CROSSCHECK.json's first exponent 1 with boolean true | Cross-check in 2 modes | `CROSSCHECK_RECEIPT_MISMATCH` |

The boolean mutations verify type-sensitive canonical JSON comparison rather
than Python's `True == 1` equality. The initial external export-test harness
failed while cleaning a copied read-only root after the first source mutation;
restoring that temporary root's write permission fixed cleanup. The full
unchanged test set was then rerun and all eighteen rejections completed. No
success receipt from the failed harness attempt is relied on.

These transport checks authenticate the tested package and explicit inputs;
they do not establish the mathematics or cover undeclared dependencies.
Only base provenance is covered by the source-history check. PR6246's pending
original history is not asserted as an ancestor: its exact proof bytes and
original Git blob are retained and authenticated separately.

Only this package is added to the canonical base. Publication verification
compares the complete remote Git tree with the tested local tree; the exact
published commit and the fresh verification result are in the PR description.

## Not executed or not claimed

No selected-supplier cold replay, native/physical caller replay, rounded program,
full multiplier, external solver, wider arity search, Lean/Docker run or hosted
scientific CI was run. No independent human or proof-kernel acceptance is claimed.
There is no physical cost inequality, supplier admission or new kappa.
The five inherited selected assumptions remain unchanged. Exact events are
priced symbolically; unknown backend costs are not treated as zero.
