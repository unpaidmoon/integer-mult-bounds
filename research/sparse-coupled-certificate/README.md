# Faster complete sparse coupled-recurrence certificates

This contribution was produced by Nick Petalas. Apache-2.0.

**Claim type: scoped implementation equivalence with finite conformance and
local performance evidence. No new κ.** Two lines in
scripts/certify_coupled_recurrence.py skip exact-zero elimination coefficients.
Both contraction alternatives, forcing solve, separate certificate verifier,
input validation, serialization and CLI remain intact.

The complete 64-type half-chain CLI is the benchmark workload. It is the
existing full-size test's recurrence, with one half-weight edge to the next
type and forcing one. Five alternating fresh-process pairs produce identical
complete certificate bytes. Measured timings and environment are recorded in
the PR's generated receipt, not inferred from a helper microbenchmark.
Dense and arbitrary-input speedups are not claimed.

[PROOF.md](PROOF.md) gives the all-accepted-input equivalence argument.
For a zero coefficient and a positive pivot, the original factor is zero,
so every omitted assignment leaves its rational value unchanged. The pivot
gate and every nonzero update keep their order and behavior.

## Evidence and reproduction

The opt-in checker authenticates the current producer and unchanged helper,
then reconstructs the exact old producer by removing exactly the two guard
lines and checking the historical digest. It compares full certificates on
286 fixture executions, including the complete two-type grid, sparse/dense sizes through
64, early/late noncontraction, a coupling failure and near-boundary input.
It cross-checks both producer outputs with both verifiers and checks input
preservation. Six malformed inputs, three false certificates and two source
mutations reject. The receipt enumerates contracting/noncontracting cases
and binds the actual package files.

From the repository root, with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/sparse-coupled-certificate/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/sparse-coupled-certificate/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/sparse-coupled-certificate
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B -m unittest discover -s tests -p 'test_research_coupled_recurrence.py' -v
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/sparse-coupled-certificate --check-source-history --check-modes
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B research/sparse-coupled-certificate/benchmark.py --output /absolute/external/directory/benchmark.json
```

Use a corresponding interpreter path elsewhere. The benchmark needs a fresh
external output path and runs on POSIX systems with os.getloadavg. It creates
all temporary files under that output's parent and cleans them. The default
scientific commands write no files and each has a 60-second cap. The success
markers are PASS_SPARSE_COUPLED_CERTIFICATE and PASS_REGISTERED_RESEARCH_PACKAGE.

## Scope and provenance

Base is canonical main 2485805a6d47f36ea83ddde6327d453ac82d44dc, priority
revision 8. The selected binding-only first example passes; selected κ remains
.003125804. No selected scientific cold replay, native/caller admission,
proof-kernel check or complete rounded multiplier is supplied. Independent
human and formal proof-kernel review are unclaimed.

The [canonical claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294807)
was updated before this implementation began. This originally posed
verifier-engineering target changes the replay-runtime card to the complete
bounded certificate CLI.

Live open PRs, claims and local reservations, recent account work, main-tree
README terms and merged/all-state object searches were checked. Bounded
coverage does not establish global novelty. The source-specific optimization
is not a re-audit of the predecessor theorem. Classical zero-elimination
skipping also appears in thakrarsagar's [PR736](https://github.com/CrocSwap/integer-mult-bounds/pull/736),
an optional cyclotomic-inverse adapter on a different consumer; its method
is credited and not claimed as a new algorithm here.

SOURCES.json pins the original producer as provenance, because that file is
the intended production edit. VERIFY.json declares both current live script
inputs. adapter.py additionally pins the exact current producer, exact old
producer and unchanged helper by SHA256. A source change invalidates this
finite conformance binding. The checks do not import or execute .pyc caches.
The benchmark compares exact old/current CLI sources, not the loader's speed.

The change touches one shared tool and adds this opt-in evidence package.
Frozen packages, upstream archives and selected-frontier files are unchanged.
Python allocation and the bounded authenticated comparison seam are documented
in PROOF.md. All five framework assumptions remain.

## Open next questions

Does a real coupled caller still spend most of its time in elimination after
this guard? First profile its complete actual matrix, with its density and
forcing preserved. No further optimization or consumer is reserved. This
package does not justify a broader sparse-storage or fraction-free rewrite.

## Credit

Ali Romman retains the complete constructive alternative, rational certificate
checker and coupled-update lineage. Nick Petalas's least-barrier fixture,
David Ganz / Dugongue's inverse interface, Jose Manuel's setup context and
their retained predecessors keep their credit. M-matrix theory and exact
Gaussian elimination are classical. thakrarsagar retains PR736's earlier
zero-update optimization on its different replay. The new contribution is
the production guard in this consumer, its complete conformance bridge and
the measured full-CLI improvement.
