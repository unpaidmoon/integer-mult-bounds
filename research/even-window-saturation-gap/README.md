# No saturated even-window Gram systems at h >= 6

Scoped proof with exact finite corroboration, produced by Nick Petalas.

For a real or complex Gram line system of dimension `T >= 1`, suppose its
nonorthogonality adjacency `A` has `rank_F2 A=2k` and `1 in col A`. For every
`k >= 3`,

```text
v <= 2^k T - 1.
```

Thus a saturated system with `v=8T` at `h=6`, or `v=16T` at `h=8`, does not
exist. This answers [Matarener's PR5282, open question 1](https://github.com/CrocSwap/integer-mult-bounds/pull/5282).
The [proof](PROOF.md) establishes the stronger label-based statement even when
additional orthogonalities are permitted.

The new step is an equality obstruction. Saturation makes each affine
Lagrangian class an orthogonal basis. Summing those basis equations forces
`E_p + E_(p+w) = 2^(2-k) I` for orthogonal projections onto complementary label
classes. A nonzero projection cannot lie below a scalar smaller than one.

The prior cap `v <= 2^k T`, its label reduction and the Lagrangian counting
framework belong to DreamingOfClouds's [PR2244](https://github.com/CrocSwap/integer-mult-bounds/pull/2244).
PR5282 poses the equality question and supplies its historical decoder-screen
motivation. Those results are cited premises; no predecessor construction,
invoice or numerical result is audited or replayed here.

## Evidence and reproduction

The all-`k` theorem is a written proof. The standard-library verifier constructs
integer linear elimination certificates from independently enumerated RREF
generators. It returns the following finite data:

- `k=2`: 8 labels, 12 affine generators, 4 pair certificates, scalar `1`.
- `k=3`: 32 labels, 120 affine generators, 16 pair certificates, scalar `1/2`.
- `k=4`: 128 labels, 2160 affine generators, 64 pair certificates, scalar `1/4`.

It also checks a complementary-projection exception at `k=2`, 30 exact scalar
instances of the idempotent obstruction, and nine rejecting cases. The cases
remove or duplicate a generator, change the partner or scalar, or supply one
of five invalid dimension contracts. Checks use explicit exceptions and remain
active under optimized Python.

From the repository root, run:

```sh
~/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/even-window-saturation-gap/verify.py
~/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/even-window-saturation-gap/verify.py
~/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/even-window-saturation-gap
~/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/even-window-saturation-gap --check-source-history
```

Expected tokens are `PASS_EVEN_WINDOW_SATURATION_GAP`,
`PASS_REGISTERED_RESEARCH_PACKAGE`, and `PASS_RESEARCH_COMMIT_BYTES`.
CPython 3.12 or later suffices; the interpreter path above records the
local environment. The two registered checks each take less than one second
on the local macOS run. This is a runtime bound for these checks, not a claimed
speed improvement.

An optional `--receipt /absolute/path/outside-the-checkout.json` writes a
generated receipt containing the enumerated data, source hashes, package hashes
and interpreter version. Normal runs only print their result. The contextual
source documents, base commit, catalogue and selected record are pinned in
[SOURCES.json](SOURCES.json). No external library, solver or network is needed.

## Limits

This excludes equality, with an integer gap of one. It does not prove an
optimal dimension-independent density gap or exclude near-saturation as `T`
increases. The exception `k=2` is an algebra control, not an attaining exact
line-system construction. Arbitrary pairings and non-Gram decoder matrices are
outside the claim.

There is no native word, physical delivery, dirty restoration, complete current
signed invoice, supplier admission or new κ. PR5282's historical invoice is not
repriced. The selected frontier and all five retained assumptions are unchanged.
Independent human and formal proof-kernel review are unclaimed.

## Open next questions

The structured questions are in [TASK.json](TASK.json).

- Determine the optimal supremum of `v/T` at `h=6` or `h=8`. Begin with positive
  semidefinite deficits in the affine-basis equations. A quantitative deficit
  bound is missing; the integer gap here need not survive division by `T`.
- Test a concrete nonsaturated even-window system against a current complex
  caller. First specify its literal decoder, targets, paid children and
  restoration contract. Native realization, uniform closure and a complete
  signed invoice remain blockers.

## Implementation bounds

The verifier has no recursion or background processes. The RREF search is
restricted to `2 <= k <= 4`, with at most `256 * 2^16` candidates and at most
256 labels. Functions are below 60 lines and checks survive `-O`. Runtime
allocation is a Python deviation from the fixed-allocation rule. Live storage
is bounded by the finite RREF candidate and generator collections; no unbounded
input can expand the search. A systems-language fixed-buffer implementation
would be needed only if this verifier becomes a memory-constrained component.
Warnings-as-errors, syntax inspection and both registered commands are the
available local diagnostics; no dedicated Python linter or type checker is
installed on PATH. This package changes no shared build configuration.

## Credit

The complementary-label equality obstruction, proof and standalone verifier were
produced by Nick Petalas. Credit Matarener for PR5282's question and screen,
DreamingOfClouds for PR2244's line-count and label framework, and the decoder
lineage credited in those unchanged source documents. New work is Apache-2.0.
