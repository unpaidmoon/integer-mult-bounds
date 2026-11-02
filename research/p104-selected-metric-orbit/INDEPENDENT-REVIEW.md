# Independent exact review of all three energy spectra

Reviewed Worker A's `research/p104-selected-metric-orbit` at commit
`0fb40d096e78cb332c4de0dc9e6e35b6f5e640d3`, against canonical base
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. No blocker was found in the
normalization, rational multiplicities, four-dimensional quadratic block,
sharp constants, equality dimensions, or positive-definite sharpness.
**No new κ.**

## Separate mathematical construction

`independent_orbits.py` imports neither the author's implementation nor the author's
104 rational eigenvectors. It constructs the 120 root lines directly in the
nine-dimensional sum-zero hyperplane: integer vectors `3(e_i-e_j)` and vectors
with three coordinates 2 and six coordinates -1. These are `3r`, where each
root `r` has squared norm 2. The source WORD is authenticated by SHA256
`7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f`.
The frame classification and representative coverage were separately checked
by a separate maximal-clique/union-find implementation; this review addresses spectra of its three representatives.

Use the nonorthogonal A8 chart `B=[e_0-e_8,...,e_7-e_8]` and write every
physical symmetric operator as `A=B S B^t`. The 36 coordinates of `S` are its
8 diagonal and 28 upper off-diagonal entries. The Gram matrix `W` is computed
as the Frobenius Gram matrix of the 36 literal nine-dimensional operators
`B E_ij B^t`. Thirty-six positive exact rational LDL pivots certify `W>0`.

For each root let `w=B^t r`, which is integral. On unit roots `u=r/sqrt(2)`,
`u^t A v = w^t S w'/2`. Sum the outer products of the corresponding integer
linear forms over all unordered orthogonal pairs in the puncture. This gives
an independently assembled integer matrix `H` with

```
E(A) = s^t H s / 4;       ||A||_F^2 = s^t W s.
```

Each puncture has exactly 2,860 such pairs. This independent chart has energy
denominator 4, whereas the author's orthonormal F chart has denominator 16;
the conversion is explicitly accounted for rather than copying a normalization.
The identity on the hyperplane has `S=I-J/9`, lies in the kernel, and has
squared Frobenius norm 8. The trace linear form in this chart is twice the sum
of all 36 coordinates.

Exact rational Gaussian elimination and back substitution compute the
nullities of `H-4λW`. These yield all the stated rational multiplicities:

| Orbit size | Rational spectrum, with multiplicities |
|---|---|
|28|0:1, 37:6, 38:16, 91/2:12, 54:1|
|336|0:1, 37:1, 75/2:8, 38:12, 91/2:10|
|896|0:1, 75/2:6, 151/4:8, 38:7, 165/4:4, 91/2:6, 199/4:4|

The nonzero rational eigenspaces are checked to be trace-free. Their dimensions
sum to 36, 32 and 36. Distinct eigenspaces are independent, and `W>0` makes the
generalized operator self-adjoint, so these are full spectra for sizes 28 and
896 without relying on the author's eigenvectors or modular-rank certificate.

## The remaining four dimensions

The four matrices displayed in ORBIT-PROOF.md are treated as claimed data,
converted into physical nine-dimensional matrices using the fixed frame, then
into this separate A8 chart. Their coefficient columns `V` have exact rank 4.
The checker verifies, against its independently assembled size-336 energy,

```
4 H V = W V C,
C = [[796,0,0,-68],[0,796,68,0],[0,68,660,0],[-68,0,0,660]].
```

This factor 4 is required: the author's C represents `16λ`, while the new
pencil represents `4λ`. Two explicit 2-by-2 blocks have eigenvalues
`728 +/- 68 sqrt(2)`, each occurring once in each block. The exact polynomial
`C^2-1456 C+520736 I=0` and trace 2912 are independently checked. Its polynomial
is nonzero at each rational eigenvalue already accounted for, so these four
dimensions have zero intersection with the rational 32-dimensional sector.
Consequently the full reported size-336 spectrum is complete. Dividing by16
gives `(182 +/- 17 sqrt(2))/4`; both exceed `75/2`, certified by `32^2>2*17^2`.

It follows that the sharp trace-free constants are 37, 37 and 75/2, with
equality dimensions 6, 1 and 6. This conclusion uses exact algebra only.

## Positive-definite sharpness and controls

For each representative the independently computed minimal eigenspace supplies
a nonzero trace-free operator A. Set
`t=1/(2 max_i sum_j |A_ij|)` in the physical nine-dimensional chart. The
operator `I_V+tA` is positive definite since the absolute row-sum bound
controls the symmetric operator norm. Its A8-coordinate matrix also passes
exact rational LDL with eight positive pivots. The deterministic examples use
`t=1/4,1/16,1/24`, respectively, and attain the claimed energy-to-anisotropy
ratio exactly. This establishes sharpness within positive-definite metrics,
without claiming a rational square root for these metrics.

Three controls detect doubling the energy normalization, changing one sign in
the quadratic action, and dropping a quadratic basis column. Both normal and
`-O` runs with warnings as errors produce the identical receipt
`PASS_INDEPENDENT_A8_ALL_SPECTRA`.

Reproduction from this package directory (or use the registered runner):

```sh
python3 -B -W error independent_orbits.py --source /path/to/research/p104-helper470-twin-rung-removal/WORD.json.gz
python3 -O -B -W error independent_orbits.py --source /path/to/research/p104-helper470-twin-rung-removal/WORD.json.gz
```

This is an exact finite check and mathematical review, not a proof-kernel
formalization or independent human review. The accepted selected multiplier,
physical supplier accounting, and five inherited assumptions are unchanged.
The claimed geometry remains the canonical A8/E8 realization; this review
independently reconstitutes its energy rather than proving an unrelated
coordinate identification. Predecessor credit: the canonical P104/E8 source
lineage, Nick Petalas's PR6278 uniform bound and classification question, and
Worker A's new classification and certificates. Jerry Chen, @CubeJerry;
substantial OpenAI Codex assistance from research worker D (seed79).
