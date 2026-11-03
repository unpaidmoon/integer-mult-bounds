# Exact signed packing and preserved replay coverage

This is a scoped implementation proof. Kronecker substitution and Gaussian
integer arithmetic are standard. The contribution is their bounded signed
implementation in the literal PR6208 primary checker, with the source-bound
runner and complete-path timing experiment. It proves no new Clifford result.

## A signed dot product

Let n be between 1 and 16. Let integer vectors a and b have component
magnitudes at most M and N. Let l and r be the maximum component bit lengths.
The implementation chooses

    d = l + r + bit_length(2n),  B = 2^d.

Since M < 2^l and N < 2^r, including the all-zero case with bit length zero,
the chosen B satisfies B > 2nMN + 1. Write C = nMN. Form

    A = sum a_i B^i,
    R = sum b_(n-1-i) B^i,
    A R = sum c_j B^j.

Every coefficient has magnitude at most C, and
c_(n-1) = sum a_i b_i. The lower coefficients contribute a quantity of
magnitude at most C/(B-1) < 1/2 after division by B^(n-1).
Therefore rounding that quotient to its nearest integer removes precisely the
lower coefficients. All higher coefficients are multiples of B. Taking the
rounded value modulo B gives c_(n-1) modulo B. The centered representative,
in [-B/2, B/2), is the actual c_(n-1), since its magnitude is less than B/2.
For n=1 there is no lower tail and the implementation omits rounding.

Rounding is necessary for negative digits. A packed polynomial equal to -1
has central coefficient zero at position one, yet floor division by B gives
-1. Merely centering the digit after floor division would give the wrong answer.
The checker retains this rejecting control.

## Gaussian matrix multiplication

For rows a = x + iy and columns b = u + iv, apply the signed dot identity to
the four real dot products. The result is

    real(a b) = dot(x,u) - dot(y,v),
    imag(a b) = dot(x,v) + dot(y,u).

The maximum bit lengths are taken across both components of each input
matrix, so the same B bounds all four products. Column reversal in pack is
exactly the reversal in R above. The raw numerator matrix therefore equals
the source numerator matrix in every entry. The denominator is the product
of the positive input denominators. Reducing all numerator components and
that denominator by their joint gcd gives the same canonical pair as the
unchanged source. This also handles a zero product.

The arithmetic accepts square dimensions 1 through 16 and input numerator
components and denominators of at most 4096 bits. The source uses dimension
16 in every one of its 85 products. All 170 literal operands have maximum
component magnitude one. The wider domain is an implementation contract,
not an additional native-operator claim.

## Bounded resources and implementation constraints

No new function is recursive. Arithmetic loops have at most 16 rows, 16
columns, two components and 512 input scalar components per matrix. The
packing width is at most 8198 bits. Each packed operand has fewer than
16 times 8198 bits; each packed product has fewer than 32 times 8198 bits.
There are 4n packed operands, and at most n squared output pairs. The
denominator product has at most 8192 bits. These are conservative live-data
bounds; they do not measure interpreter allocator overhead.

All new functions are below 60 lines. Input bounds are checked before packs
are allocated. Shape and denominator errors propagate before source output.
Non-integer numerator components are rejected by int.bit_length. Subprocesses
have 60-second timeouts, and return codes, stderr and completion outputs are
checked. Warning-as-error replay runs both normally and with optimization.
The registered commands also enable Python development mode. Ruff, mypy and
pyflakes were unavailable locally; AST compilation and the bounded-function
inspection supplement executable checks without claiming a separate lint pass.

Power of Ten deviations are confined to this package:

- Rule 3, managed allocation. Python integers, tuples and interpreter calls
  allocate dynamically. The enforced dimensions and bit lengths bound live
  arithmetic data as above. Temporary source-corruption copies contain exactly
  five pinned files and are removed on every normal or exceptional exit.
  A fixed-capacity implementation would be needed for a native port.
- Rule 8, dynamic module loading. The runner loads one fixed primary source
  module to retain its predicates unchanged. Five exact SHA256 input checks
  precede compilation of the authenticated primary bytes, bypassing .pyc files.
  Mutation tests reject a change to each input. Documents and the unchanged
  independent CLI still require a stable checkout between authentication and
  execution; no atomic snapshot claim is made. A standalone future source
  release could use a normal import.
- Rule 9, function substitution and test callbacks. The private loaded module's
  multiply slot is bound to the new kernel, or to one shadow comparator in
  the coverage check. All other call targets stay fixed. Eleven bounded input
  controls and five source controls use callbacks. No dispatch target comes
  from input data. A future shared arithmetic interface could remove this seam.

## Literal coverage and evidence boundary

The new verifier runs the complete primary once unchanged, then runs it again
with a shadow comparator at every multiply call. All 85 canonical products,
covering 21760 Gaussian output entries, must match exactly. Complete stdout
must also match, including all seven original hypothesis controls. It then
checks the actual new CLI output and executes the unchanged independent
checker. Normal and optimized registered commands repeat the entire procedure.
Separate arithmetic controls cover 16275 signed vector pairs, 71 matrix cases,
the negative lower-tail control, 11 invalid inputs and five corrupted sources.

The benchmark measures the complete four-command scientific suite: primary
normal, primary optimized, independent normal, independent optimized. On the
new side only the primary entry point changes. Process startup, imports,
source authentication and output capture are timed. All four stdout digests
must match on all ten bundles. The new equivalence and regression suite is
additional verification work and is outside this performance comparison.

The predecessor's matrix, Pauli, Bell and Clifford mathematics remains
apoursh / Armin Pourshafeie's work. Nick Petalas retains PR6192's cap and Bell
method; Ross Richardson retains the earlier cubic and Pauli-character lineage.
No supplier, new exponent, physical invoice, native all-column realization,
formal-kernel proof or complete multiplication theorem is established here.
