# Exact row-output preservation

This scoped implementation proof was produced by Nick Petalas. Apache-2.0.
It treats Ali Romman's PR5637 recognizer and complete caller as credited
inputs. It does not reprove the tensor classification.

## Contract

Let `f` be an unmodified field constructed by the pinned `Field` class,
with order at most 25. Let `a` be a rectangular matrix of canonical field
elements, with at most 729 rows and at most 162 columns. The pivot width
is between zero and its row length. Empty matrices are allowed. The new
public `RowKernel.rref` validates this contract and returns exactly the
same full rows and ordered pivot columns as the pinned `rref`, including
every augmented column. It does not mutate or alias an input row.

These capacities contain the complete caller. Its seven fields have
orders 2, 3, 4, 8, 9, 16 and 25. Its positive fixtures have dimension at
most nine. The largest nucleus system therefore has at most `9^3 = 729`
rows and `2*9^2 = 162` columns. Its inverse and coordinate systems fit
these capacities. The complete F2/F4 domain has dimension two. The source
validation rejects malformed tensors before elimination, and its internal
field operations preserve canonical coefficients and rectangular shapes.
The private adapter calls `reduce` on these trusted internal matrices,
retaining explicit row/column capacity checks rather than repeating their
coefficient validation on every internal call.

## Stepwise identity

Preparation constructs the immutable table

```
updates[c][x][y] = f.add[x][f.mul[c][y]].
```

This is the original elimination expression for `x + c*y`. The table is
computed separately for each new field object. It is never keyed only by
field order, so different irreducible-polynomial presentations cannot share
an arithmetic cache accidentally. The copied multiplication, inverse and
negation tables likewise belong to that object.

Induct on the pivot-column loop. Initially both algorithms copy every
input row and have the same pivot list and next pivot-row index. If the
current rows agree, scanning from the same index chooses the same first
nonzero pivot or skips the same column. Both swap the same rows. The new
normalization binds `mul[inv[pivot]]` once and indexes it for each entry;
the source indexes that same row repeatedly. Thus their normalized full
rows agree, including columns outside the pivot width.

For each other nonzero row, both choose `c = -row[j]`. The new full-row
comprehension looks up `updates[c][x][y]`; the source evaluates its defining
expression. Hence every resulting entry agrees. The pivot list, next-row
index and termination condition agree. This proves exact returned rows
and pivot order, not only equality of row spaces. The copied rows also
prove input preservation and absence of input/output row aliases.

All other recognizer functions are unchanged. They resolve `rref` in their
own private loaded module. The adapter changes only that binding and the
field constructor that prepares its arithmetic. Consequently every later
branch, certificate, rejection reason and independent checker expression
has the same value on the declared domain. The unchanged verifier itself
still constructs and visits every tensor and orbit element.

## Costs and limits

The table holds `q^3 <= 15625` field-element references. Preparation costs
O(q^3) lookups, paid inside each complete timed process. The row algorithm
keeps the source's O(rows*columns*min(rows,width)) field-update bound.
The improvement is a constant-factor Python implementation change, with
no asymptotic improvement claimed. Replacing repeated attribute accesses
and nested arithmetic lookups by prepared table accesses is classical.

The adapter is scoped to this bounded caller. It is not a replacement for
the source API at arbitrary field order or dimension. Mutating a field's
arithmetic tables after preparation is outside the contract. There is no
new field-recognition theorem, supplier, kappa or selected-frontier change.

## Code constraints

The new functions are shorter than 60 lines. There is no recursion. All
kernel loops have capacities derived above. The benchmark has five to ten
pairs and a 150-second timeout per child, checks every child status and
stderr, and consumes its complete report before accepting a timing.

Rule 3, managed allocation. Python requires object and list allocation
during each elimination and process run. This deviation is confined to
the new bounded engine and replay harness. The engine permits at most
729 by 162 coefficients per matrix and 25 cubed fused entries per field.
It holds copied input/output rows and no history of previous matrices.
The source caller constructs a fixed finite field/fixture set. The
benchmark retains at most twenty small result reports and at most one
child process at a time. Capacity, invalid-input and complete-caller
checks exercise these bounds. A fixed-storage native implementation
would be a separate follow-up, not an asserted Python guarantee.

Rule 9, runtime dispatch. The private module adapter selects between the
pinned and prepared elimination implementations. Both targets are explicit
and have a fresh-process lifetime. Source authentication precedes import;
no global installed module or predecessor file is changed. Both complete
paths and the arithmetic-mutation rejection are exercised.

Rule 10, interpreted diagnostics. Registered checks use isolated,
warning-strict development mode with normal and optimized Python. Every
verification condition uses an explicit exception. No additional static
analyzer was found on PATH in the supplied environment. Syntax compilation and
AST inspection cover every new Python file; no assertion is needed for
the contracts to remain active under `-O`.
