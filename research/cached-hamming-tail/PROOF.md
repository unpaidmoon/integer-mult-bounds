# Exact cached Hamming envelopes

This is an implementation-equivalence proof for the shared-tail predicate of
SHIN09-git's PR6046. The predecessor's completion theorem and canonical caller
remain cited premises. No predecessor mathematical claim is audited here.
The new contribution was produced by Nick Petalas. Apache-2.0.

Let P be the distinct visited vertices, with last vertex q in P. Let r be the
remaining edge budget. Write D(P) for the nonzero pair differences and define

```
H(q,r) = {x : weight(q XOR x) + weight(x) <= r}
U      = H(q,r) minus P.
```

The source's already simplified exact envelope is

```
E = D(P) union {p XOR x : p in P, x in U}.
```

The following identity removes the prefix-dependent exclusion from the support
calculation, while retaining it in the future-vertex count:

```
E = (D(P) union union_(p in P) (p XOR H(q,r))) minus {0}.
```

To prove inclusion from left to right, use U subset H. For the reverse inclusion,
consider an added x in H intersect P. For every p in P, p XOR x belongs to D(P)
unless p=x, in which case it is zero and is removed. Thus the larger cached set
adds no nonzero difference. This identity holds for arbitrary distinct vertices;
it does not require the path condition used by the source's completion theorem.

`tables` enumerates H for all 32 endpoints and all budgets 0 through 12. For each
distinct mask it computes all 32 XOR translations. A bitset stores membership
of vertex x at bit x. At coordinate i, XOR by 2^i exchanges the two halves of
each consecutive block of 2^(i+1) bit positions. `translate` performs that
exchange by two masks and shifts. The five coordinate exchanges commute, and
their product is exactly x maps to x XOR p. All masks have at most 32 bits.

For a validated source prefix, `envelope` forms U by `reach & (ALL XOR seen)`.
It ORs the precomputed translations for every old vertex into the literal
source pair support, then removes zero. Consequently both U and E equal the
source outputs exactly. The necessary conditions `|U| >= 12-|P|` and
`E = all nonzero masks` therefore return the same decision at every prefix.

The adapter retains the source's remaining-label and parity-union checks in
their original order. It changes only the subsequent shared-tail test in
`two_without_cap`. The source traversal, child order, simple-prefix gate,
closing-edge test and final word checks are unchanged. Induction along that
same traversal gives identical entered nodes, prunes, closed words and
universal words. The original predicate is restored on successful return and
on exceptions by a `finally` block. Each invocation has its own authenticated
source module; no shared file or maintained engine is mutated.

There are 416 reach entries and 13,312 logical translated entries. Identical
reach masks share translation tuples. Storage is bounded by those fixed counts;
it is not a prefix cache that grows with search history. Setup is paid once in
every candidate call and is included in both caller and full-process timing.
The remaining per-prefix support loop visits at most twelve old vertices.
The source's repeated scan over all 32 candidate vertices and nested old/new
pair loop disappear from this stage. The unchanged cheap checks and DFS still
cost time, so this is not a claim of the same speedup for a complete research
package, another census, another dimension or another Python implementation.

The verifier compares all 13,312 translations against literal set translation,
then all 21,640 canonical simple prefixes against the original kernel. It
compares the full returned word tuples from both complete callers. These finite
checks corroborate the identity and adapter proof; they do not establish new
word-census exclusions, a seven-label result, or the predecessor theorem.

## Implementation constraints

The new kernel has no recursion. Its fixed loops have bounds 5, 32, 13 and 12.
The finite verifier's iterative DFS has a 21,641-iteration guard and at most 56
pending entries. Benchmarking admits at most thirty pairs with thirty-second
child timeouts. The retained caller has unchanged recursive depth at most
eleven; that source-control deviation is bounded and not expanded here.

CPython allocates managed objects during execution. The live cache and prefix
state have the fixed bounds above; no allocation-free claim is made. The
source adapter compiles exactly one SHA-256-authenticated, declared Python file
to avoid stale bytecode. This bounded source loading and the private predicate
replacement are explicit metaprogramming and indirect-call deviations. No
untrusted code path or arbitrary callback is accepted. Warning-strict normal
and optimized verification exercise success, unsupported mode, adapter failure
and actual source-corruption paths. Runtime checks use exceptions so they
remain enabled under optimized Python.
