# Symmetric associators in the complete Frobenius recognizer caller

This contribution was produced by Nick Petalas. Independent human and formal
proof-kernel review are unclaimed. Apache-2.0.

## Result and scope

Claim type: scoped implementation-equivalence proof and local performance result.
An opt-in adapter reduces the complete primary PR5502 recognition caller's median
wall time from **1.415539 s to 0.489242 s**, a **65.44% reduction**. Five alternating
fresh-process pairs return byte-identical complete reports, with zero errors.
Baseline range is 1.369582 to 1.432597 s; adapted range is 0.477110 to 0.504267 s.
These measurements cover source authentication, interpreter startup, the entire
primary caller and JSON output. The companion exhaustive caller is compared
separately and is not part of this timing claim.

The change checks associativity once per unordered multiset of basis indices,
after the original commutativity check. No source file is changed. The original
recognition algorithm, unit recovery, Frobenius kernels, transporters, witness
checks, independent product equations and rejection fixtures remain in use.
No new algebra classification, supplier, kappa or selected-frontier change is
claimed. This is original implementation work on an existing verifier, not a
scientific audit of its algebra theorem.

## Equivalence proof

The source normalizes structure constants and validates their shape and prime
before calling its internal algebra-law kernel. On that same internal domain,
check commutativity in the same order and return the same error if it fails.
For a commutative bilinear multiplication, a basis triple i,j,k has at most
three possible bracketings:

```text
A = (e_i e_j) e_k
B = (e_i e_k) e_j
C = (e_j e_k) e_i
```

Commutativity identifies every left and right side in all six permutations
with one of A,B,C. For i<j<k, checking A=C and A=B is therefore necessary and
sufficient. If i=j<k, A may differ from B=C, so check A=C. If i<j=k, A=B may
differ from C, so again check A=C. If i=j=k the associativity equation follows
from commutativity alone. Enumerating i<=j<=k exhausts these cases. Bilinearity
makes basis-triple associativity equivalent to associativity on every vector.

Both kernels return exactly one of the same three values: no error, the
commutativity error, or the associativity error. The changed order cannot alter
which generic diagnostic is returned. Every subsequent deterministic source
operation consequently receives the same input and produces the same complete
recognition result and witness. This proof does not rely on recognizing a table
as a member of the target algebra family.

For passing n-dimensional commutative tables, the original kernel computes
2n^3 vector contractions. The adapter computes

```text
3 binom(n,3) + 2 n(n-1) = n(n-1)(n+2)/2.
```

It makes 2 binom(n,3)+n(n-1) = (n^3-n)/3 vector comparisons, versus n^3.
At n=16, actual instrumentation checks 2,160 contractions versus 8,192.
Both algorithms retain O(n^5) arithmetic complexity with dense structure
constants. This is a constant-factor reduction, not a new asymptotic bound.
The symmetry argument is classical; its application, adapter and measured
complete-caller gain are the contribution here.

## Evidence and reproduction

Use CPython 3.12 and the standard library from the repository root:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/frobenius-symmetric-associator/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/frobenius-symmetric-associator
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/frobenius-symmetric-associator --check-source-history --check-modes
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/frobenius-symmetric-associator/benchmark.py
```

A different clean CPython 3.12 installation can replace the shown interpreter.
The direct verifier ends `PASS_FROBENIUS_SYMMETRIC_ASSOCIATOR`; registered replay
ends `PASS_REGISTERED_RESEARCH_PACKAGE`. Timing is opt-in and never a CI gate.
The benchmark prints a generated receipt with all ten samples, execution order,
interpreter/platform, load, exact output hash and code/source-manifest hashes.
Redirect it outside the checkout to retain it. No receipt is handwritten.

The registered normal and optimized commands retain both complete source callers.
New conformance checks cover every commutative two-dimensional table over F2,
F3 and F5, respectively 64, 729 and 15,625 tables; 64 complete API return-value
comparisons; 576 deterministic tables through dimension six; 480 noncommutative
precedence controls; both repeated-index cases and a distinct-middle-bracketing
trap; invalid selectors; and contraction instrumentation through dimension 16.
Input immutability is checked for all 16,418 exhaustive kernel comparisons.

The unchanged primary caller retains its 46 positive presentations, 3,217
independent basis-product equations, nine nonmembers, six malformed inputs,
two normalization controls and seven witness mutations. The unchanged companion
retains all 525 tiny fixed-unit tables and all 392 four-dimensional positive
target presentations. Comparing their complete reports tests the changed
implementation's behavior; their classification counts remain credited to PR5502.

The isolated profile of the original primary caller takes 3.452 s under
instrumentation, of which the algebra-law kernel takes 3.126 s cumulatively.
This identifies the limiter; profiling times are excluded from the benchmark.
The observed complete-command gain is smaller than the profile's removable
fraction. Both timed arms use the same fixture, source authentication, flags
and output checks. Neither arm has a tuning parameter or retained result cache.
The local host is macOS arm64, CPython 3.12.15, with 18 logical CPUs. Other work
was present, with load averages around 4.5 at measurement setup. Interleaving
shares that noise; the two measured ranges do not overlap. This is one host
and workload, not a universal runtime promise.

## Verification boundaries

SOURCES.json binds all four consumed source files by SHA256. Every execution
checks the live inputs before importing the recognizer and caller. VERIFY.json
also declares them for CI invalidation. There is no persistent cache to invalidate.
The metadata's historical catalogue and selected record are provenance only.
The adapter changes only its private loaded module and does not patch shared
modules or write source files. It exports no new public recognizer API.

All new functions are below 60 physical lines. Loops are bounded by explicit
finite input dimensions or checked sample counts; the scientific fixtures have
n<=16. The benchmark allows 5 to 15 pairs and gives each subprocess a 120-second
limit, checks its exit status and stderr, consumes its complete output and
requires the source success marker. Acceptance uses explicit exceptions under
normal and optimized Python. Syntax parsing and warning-strict development
mode accompany registered replay.

Python allocation is a managed-runtime deviation from fixed preallocation.
Within the registered finite domain, input storage is O(n^3), one contraction
uses O(n) live output, and the largest instrumentation list has 2,160 entries.
Imported source code retains its original resource behavior. Dynamic import and
the two explicit caller bindings are required adapter boundaries, with three
fixed source modules and two fixed caller choices. The temporary instrumentation
binding is restored in a finally block. A future public API must add its own
resource contract; this contribution changes no shared limits or validation policy.

The universal equivalence argument is written, not proof-kernel checked. Local
finite conformance is not independent mathematical acceptance of PR5502. Hosted
CI status belongs in the PR body. Native implementation, precision, physical
movement/restoration, complete paid invoices and all five selected framework
assumptions retain their previous status. No Lean, Docker or selected cold
supplier replay was run.

## Open next questions

- Should a public opt-in algebra-law backend use this implementation? First
  bind its internal normalized-table contract and run one actual external
  consumer. Adoption, caller resource limits and public diagnostics remain
  separate from this isolated result.
- Does algebra-law checking dominate a different actual tensor recognizer?
  Profile that complete caller before adapting it. Its possibly noncommutative
  input contract can prevent reuse of this reduction.

## Provenance and related work

Base: canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
The [advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19299804)
records the bounded question. Current selected bindings passed before work;
they are not a replay of the selected mathematics. Live open/account PRs,
recent handoffs, active Discussions, local reservations, targeted merged PR
searches and main-tree formula/object searches were checked before claiming.
The replay-runtime cache covered only 95 of 8,722 HEAD notes in this sparse
checkout; missing local matches do not establish novelty.

Credit apoursh / [PR5502](https://github.com/CrocSwap/integer-mult-bounds/pull/5502)
for the recognizer, complete callers, fixtures, witness API and independent
finite oracles. Credit Ali Romman / PR5459 and PR5316 for the Frobenius family
and recognition handoff, Nick Petalas / PR5252 for the separate etale comparison,
and David Ganz and the retained algebra/tensor lineage. Every predecessor file
and attribution remains unchanged. This result reserves no follow-on work.
