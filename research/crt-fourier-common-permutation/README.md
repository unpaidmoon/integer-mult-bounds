# Exact common-permutation criterion for CRT Fourier tensorization

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped algebraic proof with exact finite corroboration.
For pairwise-coprime cyclic axes `s_i`, put `N=product_i s_i` and `M_i=N/s_i`.
A single address permutation identifies both indices of the length-N standard
Fourier kernel with the tensor of the standard axis kernels exactly when
**every `M_i` is a square unit modulo `s_i`**. This remains necessary when
arbitrary nonlinear permutations are allowed. Every valid map is

```text
f(x) = sum_i M_i v_i x_i mod N,     M_i v_i^2 = 1 mod s_i.
```

[PROOF.md](PROOF.md) proves the classification and its exact product count.
Axes `(13,17)` have four common maps, including `102x+26y mod 221`.
Axes `(3,5)` and `(3,7)` admit none. Ordinary two-map Good–Thomas
factorization still works on all three grids. No new kappa is claimed.

## Connection to the current problem

David Ganz / Dugongue's [PR5564](https://github.com/CrocSwap/integer-mult-bounds/pull/5564)
supplies prime-free native coprime grids and distinguishes their two CRT
address conventions. This originally posed question changes that interface
by demanding exactly the same permutation on both Fourier indices, while
retaining standard local roots. It settles which grids permit that demand.
It does not audit the predecessor or assert that its distinct-map contract
needs replacement. The result is a side interface theorem relevant to
transform-layout design, not a change to the binding recursive invoice.

Nonlinear reindexing cannot fix a failed square test. Different input/output
permutations or changed local roots remain available. Their physical costs
must be charged separately. No permutation-cost saving is claimed here.

## Reproduce

CPython 3.12 and the standard library suffice. From the repository root:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/crt-fourier-common-permutation/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/crt-fourier-common-permutation/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/crt-fourier-common-permutation
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/crt-fourier-common-permutation --check-source-history --check-modes
```

Other machines may substitute their CPython 3.12 path. The direct marker is
`PASS_CRT_FOURIER_COMMON_PERMUTATION`. Stdout is a generated JSON receipt
bound to all six package files and both exact source inputs. No receipt is
handwritten. Direct replay needs no Git, network, predecessor executable or
output directory, and writes no files. Materialize `research/native-coprime-grid`
in a sparse checkout before replay. The official package export includes
both inputs and supports the same direct commands without Git.

Local normal and optimized runs agree on 105 coprime shapes, 7,313 cyclic
candidates, 147 constructed common maps and 887,566 literal phase entries
for those maps. There are sixty excluded shapes. The tiny domains enumerate
all 1,592 permutations, accepting nine, all additive. The four `(13,17)`
maps receive another 195,364 phase checks. Three distinct-map scope controls
cover 1,066 phase entries, and fourteen invalid-input or semantic controls
reject. Full phase tests use exact congruences modulo N. Only the written
proof makes the all-axis-size and arbitrary-bijection claims.

Both registered commands ran locally in about one second each on CPython
3.12.15, macOS arm64, far below their 120-second bounds. These are local
check timings, not a performance-improvement or portable-runtime claim.

## Scope and credit

Base canonical main is `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority
revision 8, selected conditional kappa `.003125804`. The
[advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294771)
records the original interface question. TASK.json changes the
`uniform-transfer-audit` card to this side result. No selected assumption is
discharged. Live open PRs, handoffs, active Discussions, recent account work,
main README formulas and several merged/all-state object searches were
checked. Sparse/cache coverage and unpublished work remain limits; empty
searches are not a novelty proof.

Credit David Ganz / Dugongue for PR5564's native interface, two address
conventions and context; ToikY for the guard-safe band, Jose Manuel for the
tensor caller, Tekalign for the earlier CRT streams, and Cinna Davis,
Chafik Boukhalfa, unpaidmoon and the retained native/tensor/CRT lineage.
The cited setup and source statements are authenticated inputs, not scientific
claims re-verified as this contribution. CRT, finite cyclic characters,
congruence-preserving bilinear forms and Good–Thomas tensorization are
classical. The contribution is the complete common-permutation criterion at
this interface, including nonlinear permutations, its constructor and exact
corroboration. No broad literature-priority claim is made. Predecessor files
and credit lines are unchanged.

The physical permutation, local roots, numerical resampling, coefficient
preparation, restoration, precision/tape, stock and complete caller costs
remain open. No native instruction trace, new supplier, full multiplication
theorem, selected cold replay, Lean or Docker is supplied. Independent human
and formal proof-kernel review are unclaimed.

## Open next questions

1. Can one actual caller exploit a successful common-permutation grid after
   its standard local roots and full movement costs are fixed? Begin with
   one complete transform and its input/output ABI. A grid alone supplies
   no physical saving.
2. When a grid fails the criterion, can an explicitly priced local root
   change make a common permutation cheaper than retaining the two maps?
   Begin with `(3,5)` and charge phase generation and the complete transform.
   Neither route is excluded by this theorem.

Structured questions and blockers are in [TASK.json](TASK.json).

## Verifier constraints

Power-of-ten inspection covers the new verifier. It has no recursion,
subprocesses, imports of predecessor engines, network operations or file
writes. Functions are below 60 lines. Input reads are capped at one MiB,
source rows at sixteen, axis count at four, each axis at 257 and total size
at 65,536. The actual exhaustive shapes have N at most 255; arbitrary
permutations have N at most six. All checks use explicit exceptions that
remain active under optimization. The normal and optimized warning-strict
replays are the available diagnostics. Rule 3 has a managed-runtime deviation:
CPython allocates integers and containers. These fixed finite bounds constrain
live collections; no fixed-allocation native implementation is claimed.
