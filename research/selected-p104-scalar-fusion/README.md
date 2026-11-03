# One fewer scalar ADD in the selected P104 word

The selected PR6030 word admits an exact one-ADD reduction, from 22,803 to
22,802 events. Replace its zero-based event 231 by
`["ADD",210,403,"1/2",3]` and omit event 392. Both original events are
`["ADD",210,403,"1/4",3]`. Every other event and every non-program field
is retained literally.

Claim type: finite exact certificate with a scoped rewrite proof. This is
a logical scalar-event improvement. The complete recursive paid and productive
profiles are unchanged, so no new kappa is claimed. This contribution was
produced by Nick Petalas. Independent human and formal proof-kernel review
are unclaimed. Apache-2.0.

## Proof

Write A(c) for the update `x_210 += c*x_403`. For an intervening ADD
`x_u += d*x_v`, the sufficient commutation conditions are `u != 403` and
`v != 210`. They follow either by expanding both compositions on arbitrary
inputs, or by multiplying their elementary matrices. A SCALE commutes with
A(c) when its role is neither 210 nor 403.

The 160 intervening events at indices 232 through 391 consist of 158 ADDs
and two SCALEs. Every one is at frame 3. Every ADD satisfies the displayed
conditions. The SCALEs act on roles 204 and 193, with coefficients 1/2
and -1. Thus every intervening event commutes with A(1/4). Move the later
A(1/4) left through this region and use
`A(1/4) A(1/4) = A(1/2)`. This proves equality on arbitrary inputs at the
end of the region, including all dirty roles. There are no intervening
MOVE, INIT, COPY or CLEAR events and no intermediate external boundary.

The region uses 133 roles. The verifier also constructs both complete
133 by 133 rational operators and checks every entry. A separate scalar
execution checks all 133 basis columns and eight dirty vectors. These are
finite corroboration of the displayed identity; the proof is not an
extrapolation from sample inputs. Tensoring the scalar identity with any
column space gives the same local rewrite at every column multiplicity.

The prefix, suffix, initial and final frames, live and owned sets, native
events, lifetimes and productive targets are identical. All later states
therefore agree exactly whenever the original program is defined. Each
native transition is applied to the same state. The original native and
caller results remain cited premises rather than new audit deliverables.
All 3,453 MOVE, 861 SCALE, 31 INIT, 31 CLEAR and 23 COPY events are retained;
the ADD count changes from 18,404 to 18,403. No intermediate rounded-error
bound or physical runtime comparison follows from exact endpoint equality.

## Reproduction

From the repository root, with CPython 3.12 and its standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/selected-p104-scalar-fusion/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -O -B research/selected-p104-scalar-fusion/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/selected-p104-scalar-fusion
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/selected-p104-scalar-fusion --check-source-history
```

Any CPython 3.12 installation can replace this local interpreter path.
Expected marker: `PASS_SELECTED_P104_SCALAR_FUSION`, with 17,689 exact
operator entries, 133 basis columns, eight dirty vectors and eleven
rejecting controls. Checks remain active under optimized Python.
The receipt is generated on stdout and binds all five package files,
the source word and the complete transformed word by SHA256. No receipt
is hand-written. The checker writes no files.

To materialize the full verified word, add `--emit-word` and redirect stdout
to a scratch location outside the checkout. This runs the same full checks
before emitting JSON. The package stores the two-event edit as code, avoiding
a second committed copy of the predecessor word.

## Scope and predecessor credit

The scientific base is canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. The current
source-binding orientation passes. It is metadata orientation, not a
scientific replay. The original `p104-side-correction` card is explicitly
changed to this scalar side result. Its full invoice improvement gate is
unmet. The first reduction ended the search; no maximality is claimed.
The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19291931)
records the question before the experiment.

Credit DreamingOfClouds for PR6030's full word and its PR5907 predecessor;
Ali Romman for PR5827's retained supplier chain and PR6169's distinct
common-response resynthesis on PR6144; and the P104/native/helper/controller/
caller/compiler/BIT lineage retained by those packages. PR5828 and the older
commuting-cancellation work are methodological predecessors. Elementary-matrix
commutation and addition of transvection coefficients are classical. The new
contribution is this literal selected-source reduction and its certificate.
No predecessor file or credit line is edited.

Before publication, live handoffs, active Discussions, open PRs, merged PR
queries and main README terms were searched. PR6169's certificate contains
no change to the two `210 <- 403` events, which its PR6144 input also retains.
That is an overlap check, not a replay of its mathematical result. Sparse
local overlap coverage is incomplete. Unpublished work and arbitrary nested
code are outside the search, so no global novelty guarantee is asserted.

The selected frontier is unchanged. Native all-column implementation, owned
erasure, compiler closure, precision/tape and analytic recovery remain the
five inherited framework assumptions. Native/caller/BIT/outer suites, rounded
execution, Lean and Docker are outside this contribution and were not run.
The exact proof does not establish a complete multiplication theorem,
supplier admission, a wall-time improvement or a better recursive invoice.

## Engineering bounds

There is no recursion, subprocess, network call or write path. The fixed
source has 22,803 events; both operators have 133 rows and columns and at
most 162 gates. Every function has fewer than 60 lines. Source reads are
capped at 256 KiB compressed and 4 MiB decompressed, package reads at 1 MiB
each. The word copy and exact rational matrices are bounded by this fixed
authenticated input. Python's dynamic allocation is a managed-runtime
deviation from Power of Ten rule 3; no allocation-free claim is made.
The compensating control is the fixed source hash and bounded finite
domains. Larger domains require revisiting the bounds. Warning-strict normal
and optimized execution provide the available diagnostics; no separate
static analyzer is configured. All semantic checks use explicit exceptions.

## Open next questions

Can a scalar rewrite also remove a native transition or change a legal
productive target? Start with one explicit paid-path topology and its full
signed invoice. The unchanged invoice here gives no kappa headroom, and the
family expansion gate must be met before another construction round.

Does this exact reduction admit a favorable rounded implementation? Compare
the complete intermediate error and precision cost of the two region
programs under one actual caller. Exact endpoint equality alone does not
settle that question. Neither follow-on is reserved by this contribution.
