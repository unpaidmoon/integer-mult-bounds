# Exact quarter turns preserve the complete replay

The contribution is a scoped implementation refinement and a local performance
measurement. It does not prove a new Fourier admission theorem.

## Kernel equality

The retained oracle represents an element of `Z[z]/Phi_m(z)` by its canonical
integer coefficient tuple of length `degree(Phi_m)`. Its `root_mul(a,e)` returns
`z^e a` after reduction. All caller values are immutable tuples.

For `m=4`, `Phi_4(z)=z^2+1`, so write `a=x+yz`. The four residues of `e` give

| `e mod 4` | Coefficient tuple of `z^e a` |
|---|---|
| 0 | `(x,y)` |
| 1 | `(-y,x)` |
| 2 | `(-x,-y)` |
| 3 | `(y,-x)` |

These identities hold for every pair of integers and every integer exponent,
including negative exponents. Python's remainder chooses the required residue
in `0..3`. This is exactly the four-branch implementation in `specialize`.
Returning the existing tuple in the first case is safe because tuples and their
integer entries are immutable and the caller has no object-identity contract.
For every other order, the wrapper calls the captured original function with
the original arguments. No table, cached result, admission formula or inferred
Fourier identity replaces an oracle calculation.

The precondition is a normally constructed retained `Ring` and a canonical
integer coefficient tuple. Malformed manually forged rings or tuples are not
new public inputs. The executable interface accepts no such user data.

## Caller preservation

The adapter changes only the `root_mul` method in a newly loaded private oracle
module. Every invocation is replaced by an equal tuple value. Induction over
the unchanged caller's evaluation order therefore preserves every transform,
pointwise product, direct convolution, classification comparison, witness,
digest update and canonical receipt. All other ring methods are unchanged.
The complete retained `main()` still compares the reconstructed receipt with
the retained `EXPECTED.json`, including all ordered digests and witness data.

The eleven retained tests are loaded separately and receive the same exact
replacement in their own private oracle module. Their predicates, fixtures and
control mutations are unchanged. Their existing overwrite-protection subprocess
still executes the retained original CLI, exactly as the original test does.
The temporary `sys.argv` replacement used by `main()` is restored in `finally`.
No predecessor file or shared import is edited.

Seven exact live-source hashes are checked before loading executable source.
The original upstream-binding check also runs inside the retained caller.
Registered replay supplies its private bytecode-cache namespace. Direct commands
assume a normal source checkout without hostile preexisting Python bytecode.
These are source and execution contracts, not adversarial sandbox guarantees.

## Finite evidence and rejection

The new check compares 7,225 Gaussian kernel cases against the retained generic
arithmetic: every integer pair in `[-8,8]^2` and exponent in `[-12,12]`.
It also compares 1,127 fallback cases across the other 23 orders in `1..24`.
These finite comparisons corroborate the all-integer identity above.

The complete optimized caller reconstructs the same 357,184 reduced decisions,
22,688 shared-routine decisions, 10,662 literal basis pairs, five dense pairs,
1,136 mismatched-address witnesses and nine semantic controls. The eleven tests
include the separate unreduced 32,768-case two-point domain. These counts are
the preserved workload, not new scientific coverage.

Actual replacement by the identity, exponent negation or exponent increment
must fail the retained literal calculations. Seven separately corrupted source
files must fail authentication, and an unknown source entry must be rejected.
All guards use explicit exceptions and remain active under `-O`.

## Performance scope

`benchmark.py` starts ten alternating fresh-process pairs. Both arms load the
same sources, authenticate the same inputs, run the same retained scientific
`main()` and compare the same full receipt inside the timed interval. Only the
kernel installation differs. Every return code and stdout hash is checked.
The eleven tests and the new conformance controls are checked separately and
are not included in the reported scientific-caller timing.

The untimed baseline profile observed 884,778 root multiplications and 0.204 s
of its 1.625 s in that function. Profile overhead changes the timing and those
figures are not benchmark samples. The remaining enumeration, tuple sums and
non-Gaussian arithmetic explain why this single specialization cannot double
the complete replay speed.

The published measurement is one host/workload, with concurrent unrelated
research processes. Alternation reduces drift bias; it does not establish a
universal speed guarantee. Timing is not a CI acceptance threshold.
