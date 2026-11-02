# Exact rank execution of mapped contacts

This scoped implementation proof and the accompanying code were produced by
Nick Petalas. David Ganz / Dugongue's PR4841 supplies the retained geometric
formula, caller, graph and expected receipt. Rank-nullity and binary Gaussian
elimination are classical. No new geometric lower bound is claimed.

## Equality of the two actual-change computations

Let U,V be n-dimensional subspaces of F2^(2n), with bases B_U,B_V. For any
axis a, define T_a(x)=x+omega(x,a)a, where omega is the standard alternating
binary symplectic form. Since omega(a,a)=0, T_a is linear and T_a^2=I.
Consequently T_a(B_U) is a basis of T_a(U).

The retained function computes

    dim(U intersect V) - dim(T_a(U) intersect V).

Rank-nullity gives dim(U intersect V)=2n-rank(B_U union B_V), and the
corresponding identity holds for T_a(U). Subtraction therefore yields

    rank(T_a(B_U) union B_V) - rank(B_U union B_V).

This is exactly `ContactRank.__call__`. Its elimination works over F2 by
XOR, so no floating-point or modular reconstruction premise enters. Isotropy
of U and V is unnecessary. The code accepts 1<=n<=9, matching and bounding
the source caller's domain. The same algebraic identity holds in every n.

The difference lies in {-1,0,1}. Indeed T_a(B_U)-B_U has row space inside
the line spanned by a, so the two concatenated matrices differ by a
rank-at-most-one matrix. The runtime assertion checks this consequence.

For an input set S of size 2^n, `checked_basis` validates ambient coordinates
and span dimension n. Every point of S belongs to its computed span; the
equal cardinalities imply that S is the entire subspace. This also rejects
incomplete or nonclosed sets. Booleans are rejected as coordinates and axes.

## One-contact cache and complete caller

The cache stores one pair of immutable frozensets, their bases, width and
original union rank. Object identity and width are tested on every call.
Repeated equal sets with different identities are recomputed. A new cache
entry is published only after both subspaces validate. Axis validation
precedes access. Failed preparation leaves the preceding cache usable.
The cache owns no state outside one replay and retains no historical contacts.

The retained `small` and `actual_graph` functions execute without edits.
Only the `actual_change` function reference in one freshly loaded module is
replaced. The distinct retained `change_formula`, chosen edges, fixed seed,
sampled axes, actual maps, rank checks and all receipt fields stay literal.
The replacement never calls `change_formula`. The candidate still performs
79,360 actual-change computations and 1,240 contact preparations. Complete
receipt equality is checked against the authenticated retained JSON.

For a contact queried q times, preparation uses at most 2^(n+1) input
vectors once. Each subsequent query moves n basis vectors and eliminates
2n rows, instead of moving and intersecting a set of 2^n vectors. Work is
O(2^n n^2 + q n^3) elementary binary steps per contact, compared with
O(q 2^n n) for a literal bit-cost implementation of the retained set route.
These are algorithmic envelopes, not measured machine costs or a new supplier
tariff. The physically relevant supplier program itself is unchanged.

## Checks and scope

`verify.py` compares the new engine directly with the retained literal
intersection on all Lagrangian pairs through n=3, all axes including zero,
and all 35 binary 2-planes, including nonisotropic ones. It adds 72 wider
pairs through n=9, invalid inputs, cache-failure and sign/constant mutants.
It then executes the complete retained caller with the replacement installed.
The benchmark runs that whole caller with each engine in fresh processes,
checks its receipt, and requires identical stdout hashes on every run.

The written proof establishes replacement equivalence. The finite checks
exercise its implementation; they are not a new proof of the predecessor's
geometric claims. The full PR4841 five-command package, graph regeneration,
native supplier, compiler, physical caller, precision and outer admission are
outside this contribution. No selected assumption or kappa changes.

## Code constraints

Every new loop has a finite bound. Subspaces contain at most 512 points;
ambient width is at most 18; basis unions contain at most 18 vectors. The
conformance domains are explicit finite sets and the benchmark accepts five
through nine pairs, with a 120-second subprocess limit. All functions are
under 60 physical lines. Rejection checks remain active with optimization.

Power of Ten rule 3 deviation: CPython allocates integer and collection
objects during elimination. The public n<=9 check bounds live data to one
contact's two at-most-512-point sets, two nine-vector bases and an 18-vector
elimination buffer, plus caller-owned source data. No growing contact cache
is used. A fixed-buffer implementation is a possible later port; it is not
required for this Python research replay. The tests exercise the n=9 bound
and invalid widths. Runtime/library allocator internals are not inspected.

Power of Ten rules 8 and 9 deviation: the unchanged caller is loaded through
one explicit authenticated file path, and one module function reference is
replaced by one explicit callable object. This is necessary to run the real
frozen caller without modifying its files. There is no input-selected module
or callback registry. Exact hash checks precede loading, and complete caller
and invalid-source controls cover the boundary. No source implementation is
generated or evaluated from a string. A future upstream adoption could use
an ordinary explicit engine parameter instead of this isolated adapter.

Warning-strict normal and optimized execution, source compilation and AST
function-length inspection pass locally. Ruff and mypy are not installed in
the available environment; no static-type-checker pass is claimed. Their
absence does not suppress a diagnostic or change shared repository checks.
