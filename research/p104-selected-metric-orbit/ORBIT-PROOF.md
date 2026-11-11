# Complete disjoint-frame orbit and energy classification

This extends [PROOF.md](PROOF.md) from the source-bound selected puncture to
all punctures of the same 120 E8 root lines by two disjoint orthonormal
8-frames. The result is a finite exact classification, not a random search or
an extrapolation from the selected orbit. **No new κ.**

## Theorem and conventions

Use exactly the root lines, normalization, orthogonality energy and Frobenius
inner product defined in PROOF.md. Let `F,G` be two disjoint orthonormal frames
of these root lines, and let `Q` be their 104-line complement. Two pairs are
equivalent if an orthogonal map preserving the 120-line root set carries one
pair to the other. There are **exactly three equivalence classes**, for both
ordered and unordered frame pairs. Their complete energy spectra on the
36-dimensional real symmetric-matrix space are:

| Type: number of G for fixed F | Spectrum, with multiplicities as exponents | Sharp trace-free constant | Equality dimension |
| --- | --- | --- | --- |
| 28 | `0^1,37^6,38^16,(91/2)^12,54^1` | 37 | 6 |
| 336 | `0^1,37^1,(75/2)^8,38^12,((182−17√2)/4)^2,(91/2)^10,((182+17√2)/4)^2` | 37 | 1 |
| 896 | `0^1,(75/2)^6,(151/4)^8,38^7,(165/4)^4,(91/2)^6,(199/4)^4` | 75/2 | 6 |

Thus every real symmetric metric perturbation satisfies

\[
 E_Q(M)\ge c_Q\left\|M-\frac{\operatorname{tr}M}{8}I\right\|_F^2,
\]

where the exact sharp value is 37 or 75/2 as in the table. The selected PR6030
port set is in the 896 type. Equality holds precisely when the trace-free part
belongs to the lowest positive eigenspace certified for that type. For any
nonzero such symmetric matrix A, `I+tA` is positive definite for sufficiently
small real t; hence sharpness also holds among positive definite common real
metrics. The stronger rational-common-map attainers for the actual selected
orbit remain in PROOF.md. No rational square-root claim is made for the other
two types.

The theorem concerns a shared real metric and unnormalized absolute inner
products; it does not concern independently normalized correlations, unrelated
port motions, arbitrary masked fitting matrices, native decoder synthesis or
complete multiplication accounting. HERMITIAN-PROOF.md separately extends
the sharp constants and equality spaces to complex Hermitian common metrics;
the full 36-dimensional spectrum displayed here is the real-symmetric sector.

## Finite domain and constructive reduction

The exact source labels are all 9-bit masks of weight 3 or 7. Their signed
9-dimensional representatives and normalization are in PROOF.md. Write `c(q)`
for twice the unit root in the orthonormal coordinates of

```
F = (7,25,42,52,76,82,97,127).
```

All `c(q)` are integral and have squared norm 4. The checker derives them from
the 9-dimensional coordinates, checks all 14,400 Gram identities, and uses
source labels as permanent identifiers. A root line appears once, while its
negative represents the same line.

`enumerate_frames` performs an exhaustive increasing-prefix clique search in
the 120-vertex graph of exact orthogonality. At each prefix it tries every
remaining larger vertex adjacent to all previous choices. No valid completion
is pruned except when too few candidates remain to reach eight vertices.
Every eight-clique has one increasing ordering, so the search is both complete
and duplicate-free. There are exactly **2,025** frames. Their intersection
sizes with F have census `{0:1260,1:512,2:224,4:28,8:1}`.

For each of the 120 root lines a, apply the exact reflection

\[
 c\longmapsto c-\frac{c\cdot c(a)}2c(a).
\]

This is an orthogonal reflection because `||c(a)||²=4`. Each transformation
is checked to permute the 120 root lines. Closure traversal from F under all
120 reflections reaches exactly the independently enumerated 2,025 frames.
Consequently every first frame can be carried to F by a verified root-set
isometry; no external transitivity theorem or unverified group order is used.
It is enough to classify the **1,260** frames disjoint from F.

## Stabilizer coverage and separation

Use the eight individual coordinate sign flips and these six coordinate
permutations, with convention `c'_i=c[p_i]`:

```
(0,1,2,3,5,4,7,6)    (0,1,2,3,6,7,4,5)
(0,1,3,2,4,5,7,6)    (0,1,4,5,2,3,6,7)
(0,2,1,3,4,6,5,7)    (1,0,2,3,4,5,7,6)
```

Every generator is a literal orthogonal signed permutation. The checker
verifies that each permutes all 120 root lines and fixes F as a line set.
Their generated subgroup partitions the full disjoint-frame domain as follows:

| Size | Lexicographically first G | Intersection histogram of its column supports |
| --- | --- | --- |
| 28 | `(11,21,38,56,140,146,161,191)` | `{0:16,4:12}` |
| 336 | `(11,21,44,50,134,152,161,191)` | `{0:8,2:16,4:4}` |
| 896 | `(11,22,44,49,133,152,162,191)` | `{0:4,2:24}` |

For each pair of the eight roots in G, take the cardinality of the intersection
of their nonzero coordinate supports in the F basis; the histogram includes
all 28 unordered pairs. Every orthogonal isometry fixing the eight F lines
is a signed coordinate permutation, so this histogram is invariant under the
*entire* stabilizer, whether or not the displayed generators generate it.
The three different histograms therefore separate the three subgroup orbits
under the full stabilizer. All 1,260 frames are covered, so there can be no
additional classes. This combinatorial separator was independently supplied
and checked by research worker D using a different frame enumeration.

The source-selected deleted second frame
`(67,104,137,162,266,289,448,491)` occurs in the 896 class. Transitivity gives
2,551,500 ordered disjoint frame pairs overall, with respective type counts
56,700, 680,400 and 1,814,400. The three spectra below are different, so
swapping the two frames cannot merge distinct types. Therefore the unordered
pair counts are 28,350, 340,200 and 907,200, respectively.

## Exact spectra, including the irrational block

For each displayed representative, reconstruct its own 104 roots and all
2,860 unordered orthogonal pairs. Use the same 36 symmetric entries and
Frobenius weights `W=diag(1^8,2^28)` as PROOF.md. Summing the squared linear
forms gives the integral matrix H with `E(A)=aᵀHa/16`.

`ORBITS.json` contains 104 integer eigenvectors for the rational spectral
blocks of these three matrices. The checker verifies every exact equation
`Hv=μWv`, where `μ=16λ`, and verifies each nonzero block has trace zero. The
zero block is exactly the scalar identity. For the 28 and 896 types, 36
independent vectors cover each whole matrix space. For the 336 type, the
rational blocks supply 32 dimensions; the remaining four are represented by
the following symmetric matrices in the F basis. Let `Eij` denote the
symmetric matrix with ones in positions `(i,j)` and `(j,i)` when `i≠j`:

```
b1 = diag(1,1,0,0,-1,-1,0,0)
b2 = diag(0,0,1,1,0,0,-1,-1)
b3 = E01 - E45
b4 = E23 + E67.
```

In this ordered basis the exact action of `L=W⁻¹H` is

\[
 C=\begin{pmatrix}
 796&0&0&-68\\
 0&796&68&0\\
 0&68&660&0\\
 -68&0&0&660
 \end{pmatrix}.
\]

The checker verifies `HB=WBC` entry by entry. After regrouping `(b1,b4)` and
`(b2,b3)`, there are two 2×2 blocks with characteristic polynomial
`μ²−1456μ+520736`, hence eigenvalues `728±68√2`, each twice. Dividing by 16
gives the two irrational values in the theorem. Both exceed 75/2 since
`32²>2·17²`, so they do not affect the sharp constant 37 for this orbit.
The polynomial identity `C²−1456C+520736I=0` is checked exactly as well.

All 36 certificate columns for each type are independent modulo the prime
1009, which proves rational and real independence. Since H is symmetric and
W is positive definite, L is self-adjoint in the Frobenius inner product.
The complete bases and verified action establish all the eigenvalues,
multiplicities, equality dimensions and sharp constants, with no numerical
eigensolver in generation or replay. Distinct full spectra also independently
separate the three isometry classes.

## Reproduction, controls and limits

The registered package command runs both the selected and complete-orbit
checkers, each normally and with `-O`. `verify_orbits.py` expects receipt
`PASS_P104_ALL_DISJOINT_FRAME_ORBITS`, 2,025 frames, 1,260 disjoint frames,
orbit sizes `[28,336,896]`, and sharp constants `[37,37,75/2]`.

Its eleven rejection controls cover a missing frame, inadequate orbit
coverage, an invalid root-set symmetry, wrong orbit size/representative,
corrupt and duplicate eigenvectors, altered quadratic polynomial/action/basis
dimension, and ordered-pair double counting. Two further root-moment controls
protect the Hermitian extension. These supplement the selected checker's
thirteen controls. Exact rational generation is available as

```sh
python3 -B research/p104-selected-metric-orbit/generate_orbits.py --output /path/to/new-orbits.json
```

The output must equal ORBITS.json byte for byte. The generator refuses to
overwrite existing files. The fixed domain includes **all** disjoint frame
pairs of this root set, with no random seed or unsearched remainder; track
seed 31 selects the research task and is not a computational random seed.
The stopping rule is complete frame coverage, three exact spectra and equality
spaces, and one source-bound selected-orbit identification. Overlapping frame
pairs and other root systems are outside scope.

The finite checker is ordinary Python, not a proof-kernel formalization.
Its exhaustive combinatorial argument and complete exact spectral certificate
are reviewable without accepting a failed search as an impossibility theorem.
A separate reviewer uses maximal-clique enumeration and union-find in original
9-dimensional coordinates for coverage. The lead separately reconstructs the
selected spectrum in a nonorthogonal A8 chart. These are independent
AI-assisted implementations; independent human or hosted-CI acceptance is not
claimed. The selected multiplier, source pins and all five inherited framework
assumptions are unchanged.

Jerry Chen, @CubeJerry; substantial OpenAI Codex assistance from worker A,
worker D (independent frame coverage and separator), and the lead (independent
selected energy). Credit Nick Petalas's PR6278 for the uniform coefficient37
and the explicit orbit-classification question; the canonical P104/E8
construction and coordinate lineage remain as credited in README.md.
