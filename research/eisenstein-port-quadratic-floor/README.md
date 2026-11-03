# A polar-rank obstruction for nonlinear Eisenstein messages

This contribution was produced by Nick Petalas. Apache-2.0.

For a fixed-support exact Eisenstein message code with one shared scalar
quadratic form q_t at each input port, let B_t be its binary polar form.
Every transmitted bit may combine these forms with arbitrary binary
coefficients and an arbitrary affine function. With N independent input
bits and the retained additive pairing price, the new obstruction is

    C >= N - sum_t rank(B_t)/2.

Only forms actually used by the encoder enter the sum. The proof also
shows that this is the strongest lower bound obtainable by restricting
each port to an affine subspace and applying the cited linear-copy floor.
The input restriction preserves independent demands at distinct ports.

This is a scoped written proof with finite exact corroboration. It builds
on Jose Manuel / jmbarrancoml's PR2017 linear theorem and responds to ywz65 /
PR2607's open genuinely nonlinear payload direction. Those results are
cited premises, not independently audited or replayed here. The alternating
form decomposition is classical; the contribution is its exact use in this
fixed-support restriction contract and its stricter nonlinear obstruction.

## First strict improvement

At one port put q=(u0+u1)(v0+v1), with an additional independent coordinate z.
Fixing individual coordinates requires two fixings to make q affine.
The single linear equation u0=u1 suffices, and its polar rank is two.
For forty five-bit ports, the new lower bound is **199**, compared with
**198** from the exact coordinate-face criterion of Nick Petalas / PR4895.
The demonstrated exact code costs **200**. No cheaper code is claimed.

More generally q=(sum u_i)(sum v_i), with s coordinates in each sum,
has exact coordinate restriction loss s and exact product-affine loss one.
The improvement in this restriction parameter is therefore unbounded.
The universal statement is the written argument in [PROOF.md](PROOF.md).
The first strict s=2 case is the literal finite decoder fixture.

## Reproduce

From the repository root, CPython 3.12 and the standard library suffice:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/eisenstein-port-quadratic-floor/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/eisenstein-port-quadratic-floor/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/eisenstein-port-quadratic-floor
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/eisenstein-port-quadratic-floor --check-source-history
```

Other hosts may substitute a CPython 3.12 executable. Each registered command
has a 120-second limit and generates its receipt on stdout. No generated
receipt or replay output is retained in the checkout. The marker is
`PASS_EISENSTEIN_PORT_QUADRATIC_FLOOR` followed by exact enumerated evidence
and SHA256 hashes of package files and all four live source inputs.

The verifier checks all **1,100** homogeneous quadratic forms through five
variables against an independent complete subspace/truth-table oracle.
It tests **387,405** subspace restrictions, including degenerate forms,
and **69,677** translated restrictions through four variables. Constructed
maximum isotropic spaces are checked directly. Another **64** three-bit
vector maps on two independent two-bit ports receive **1,600** complete
product-subspace checks, including equal nonzero quadratic coefficient
columns and inactive ports. The decoder fixture checks **1,280** local
input/receiver cases. Six malformed-form rejections and four mathematical
boundary controls delimit the implementation and model.

Local CPython 3.12.15 on macOS 27.0.1 arm64 passed both registered modes
and both direct commands. Direct normal/optimized elapsed times were
0.217/0.217 seconds, each below the 120-second registered limit. This is
a replay-budget observation, not a speedup claim. Warning-strict source
compilation and AST inspection pass; the longest function is 35 lines.
Ruff is unavailable in the local environment. Hosted CI is pending.

Finite checks corroborate the written theorem. They do not prove its
all-width quantifiers, re-establish the cited linear theorem, or constitute
independent human or formal proof-kernel review.

## Scope and provenance

[Task metadata](TASK.json) records the changed scope under
`complex-rank-shape-decoder`. This is a nonlinear decoder side result,
not a completed supplier or changed paid/productive histogram. The source
question is ywz65 / PR2607; the earlier coordinate-face result supplies a
comparison, not the assignment. The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19291977)
records the question, boundaries and overlap checks.

The package starts at canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. The selected
binding-only orientation passed and resolved selected PR6030. Historical
priority prose still mentions PR5599; the selected record governs. The
selected frontier is unchanged. [SOURCES.json](SOURCES.json) pins four
unchanged predecessor documents and historical catalogue/selected metadata.
No predecessor verifier is imported or executed.

The proof assumes fixed supports/widths, independent full binary demands,
zero-error decoding, orthogonal side information and additive pairing prices.
It permits one shared polar form per port. Cross-port quadratic products,
multiple independent polar forms at one port, adaptive queries, private
headers, errors and correlated inputs require a different argument.
The new bound need not be sharp for message cost. Native operations,
physical delivery/restoration, precision/tape, stock, compiler, analytic
recovery and a complete signed supplier invoice remain open. There is no
new kappa or complete multiplication theorem. Selected cold replay, Lean,
Docker, independent human review and formal-kernel review were not run.

Credit Michael Fischler / shiftybitshiftr / PR814 for the nonlinear model,
Jose Manuel / jmbarrancoml / PR2017 for the fixed-support block-linear floor,
Jonathan Lam / PR798 and Joel Pulikkan / GamingPuzzled for geometry and
pricing, ywz65 / PR2607 for the nonlinear payload question, Nick Petalas /
PR4895 for coordinate restrictions, and the retained Eisenstein, decoder
and construction lineage. Symplectic elimination, Boolean polarization,
and the isotropic dimension bound retain their classical status.

Power of Ten inspection is scoped to the new verifier. It has no recursion,
subprocesses, dynamic imports or writes. Its largest exhaustive dimension
is five and its subspace list has at most 374 entries. Functions remain
below sixty lines. Source inputs have explicit byte and inventory limits.
CPython integer/container allocation is a managed-runtime deviation from
static allocation; fixed mathematical domains bound live data. Warning-strict
normal and optimized replays provide the available runtime diagnostics.

## Open next questions

- Determine the exact product-affine restriction dimension for two independent
  quadratic forms at one port. Start with literal small alternating matrices
  and a complete common-isotropic-space oracle. The single-form rank formula
  does not determine their simultaneous restriction.
- Construct a genuinely nonlinear exact Eisenstein code with charge below
  total demand, if one exists. Specify source/reader sets and every additive
  charge, then calculate the restriction certificate. No lower-charge code
  or favorable complete physical invoice is supplied here.

Structured first steps and blockers are in TASK.json.
