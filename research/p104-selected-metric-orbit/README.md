# Sharp metric distortion for all three P104 frame-pair orbits

For the **actual 104 ports in selected PR6030**, the sharp common-real-metric
orthogonality-energy constant is **75/2=37.5**, with a six-dimensional
trace-free equality space. This strengthens PR6278's uniform coefficient 37
for this specific orbit. A complete classification further proves that **all**
disjoint E8 frame pairs form exactly three isometry classes, with sharp
constants 37, 37 and 75/2. They remain sharp for **complex Hermitian common
metrics**, with equality only in the real symmetric sector. This answers both
PR6278 orbit questions and broadens the metric domain. **No new κ.**

The complete exact spectrum is
`0^1, (75/2)^6, (151/4)^8, 38^7, (165/4)^4, (91/2)^6, (199/4)^4`.
Superscripts denote multiplicities. Six explicit rational symmetric involutions
attain the sharp constant; rational invertible common maps attain it arbitrarily
close to identity. [PROOF.md](PROOF.md) states the quantified result, all
normalizations and equality matrices. [ORBIT-PROOF.md](ORBIT-PROOF.md) gives
the complete three-class spectra, including a genuinely irrational block for
one class, and the exact finite coverage argument.
[HERMITIAN-PROOF.md](HERMITIAN-PROOF.md) proves the extension to complex common
maps by an exact skew-energy identity and checked root second moments.

This is a scoped proof with an exact finite coefficient certificate, not a
search over candidate deformations. All 36 dimensions of the symmetric-matrix
space are covered. It constrains a common real or complex ambient change of geometry;
it does not supply a decoder, native implementation or complete multiplier.
The extension exhaustively covers 2,025 orthogonal frames and all 1,260 frames
disjoint from a fixed one. Verified root reflections reduce every frame pair
to that domain, then checked signed coordinate symmetries give classes of
sizes 28, 336 and 896. A support-intersection invariant and the distinct energy
spectra each separate the classes.

## Reproduce

From the repository root, CPython 3.12 and the standard library:

```sh
python3 -B scripts/research_package.py --package research/p104-selected-metric-orbit
```

Expected: two `PASS_P104_SELECTED_METRIC_ORBIT` receipts, two
`PASS_P104_ALL_DISJOINT_FRAME_ORBITS` receipts, two independent spectrum and
Hermitian-extension receipts, two `PASS_INDEPENDENT_A8_ALL_SPECTRA` receipts, and
`PASS_REGISTERED_RESEARCH_PACKAGE`. The direct standalone command is
`python3 -W error -B research/p104-selected-metric-orbit/verify.py`;
adding `-O` must produce the same receipt. Normal replay is read-only.

The source is the selected compressed word's own `ports` field. No predecessor
program, the certificate generator or a numerical eigensolver is imported by
the direct checker. It reconstructs all 2,860 unordered orthogonal pairs,
checks 1,296 integer eigenvector equations, and proves all 36 certificate
columns independent modulo 1009. It also checks all 14,400 root Gram relations
and evaluates the six equality witnesses directly over every retained pair.

Twelve exact-reason rejection controls cover source bytes, ports/puncture,
missing/duplicate/corrupt eigenvectors, eigenvalues, matrix coefficients,
omitted edges, ordered-pair double counting, wrong Frobenius weights and
witness trace. One additional exact witness falsifies the larger coefficient
37.51. Normal and optimized commands execute all these checks.

The exact nullspace generator can independently regenerate the committed
certificate at a **new** output path:

```sh
python3 -B research/p104-selected-metric-orbit/generate.py --output /path/to/new-certificate.json
```

The generated JSON must equal `CERTIFICATE.json` byte for byte. The generator
refuses to overwrite an existing output. The verifier checks the generated
basis by a different algorithm: multiplication plus modular rank, rather
than repeating rational nullspace generation. The extension has a separate
`generate_orbits.py --output /path/to/new-orbits.json` command, whose result
must equal `ORBITS.json`; `verify_orbits.py` independently checks its exact
basis equations and exhaustive coverage, with eleven additional rejection
controls. Two more rejection controls protect the root second moments used by
the Hermitian extension. Its 336 class has a four-dimensional rational invariant block with
eigenvalues `(182±17√2)/4`, each twice; this is not rounded to a rational value.

## Provenance and verification scope

Canonical base: `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
The selected conditional κ remains `781451/250000000=0.003125804`.
[SOURCES.json](SOURCES.json) pins the exact word, catalogue and selected record.
The full selected source-binding orientation passed at this base in the lead
workspace; it is metadata orientation, not a selected scientific replay.

Nick Petalas's PR6278 at `5badad3af2ff7f6c325f20813a6176cc7e3111c0` is the
uniform-energy predecessor. It is cited for motivation and the open question,
not used as an executable or theorem premise. The finite matrix calculations
here establish all three inequalities directly. The selected labels
are read from DreamingOfClouds's PR6030 word, with the retained Matarener/A8
root convention. Input signs and ordering do not change the energy.

A separate lead implementation reconstructed the spectrum using nonorthogonal
A8 coordinates and exact integer ranks, importing no worker or predecessor
code; it obtained all the same multiplicities. This is independent
implementation by an AI-assisted reviewer, not independent human or formal
proof-kernel acceptance. A separate worker independently checked all frame
coverage and symmetry classes with maximal-clique enumeration and union-find
in 9-dimensional roots, and supplied the support-intersection separator.
Local registered and committed-byte/export checks
are recorded with publication; hosted CI is a separate status.

Root-level live overlap checks inspected the new PR6278 handoff. A bounded
main-tree README/PROOF search for `75/2`, `37.5`, common-metric and
orthogonality-energy found no earlier same-object result. Sparse local-note,
Discussion pagination and unpublished coverage are incomplete. A lack of
matches does not certify novelty. Discussions posting was unavailable in this
session; a local allocation manifest retained the narrow claim.

## Limits

The energy uses absolute inner products of originally unit roots, before
separate normalization of the transformed vectors. Common real symmetric and
complex Hermitian metrics are included. Independent port motions, arbitrary
masked fitting matrices and normalized correlations are excluded. All disjoint deleted-frame orbits are covered;
overlapping frame pairs and other root systems are excluded. All five framework
assumptions remain: native_all_columns, owned_erasure, compiler,
precision_tape and analytic_recovery. No native synthesis, dirty restoration,
complete invoice, selected cold replay, Lean or Docker run is claimed.

## Open next questions

- Study a precisely stated separately normalized correlation defect. Its
  transformed root lengths introduce a different, nonlinear problem; the
  current absolute-energy theorem makes no claim for that contract.
- Test one explicitly different decoder contract, with independent motions or
  a changed physical consumer. Its complete preparation, restoration, routing and
  native costs remain the blocker; the present inequality is not a universal
  obstruction.

The structured questions and changed task scope are in [TASK.json](TASK.json).

By Jerry Chen, **@CubeJerry**, with substantial OpenAI Codex assistance
(research worker A, independent worker D frame verification and the separator,
and independent lead energy verification/Hermitian mechanism). Credit Nick Petalas
(PR6278), Matarener(PR6166), DreamingOfClouds(PR6030), Ali Romman, Brett
Halligan(PR1212), Aaron Wang(PR1292), Josie Elliston(PR1389/1399), and the
retained E8/native/helper/controller lineage. Classical root coordinates,
spectral theory and exact linear algebra retain their usual mathematical
credit. New material is Apache-2.0.

The registered `independent.py` uses nonorthogonal A8 coordinates and exact
generalized ranks. It also verifies the Hermitian mechanism through all 9D
root second moments and a separate 28-dimensional skew energy matrix identity
(784 entries). It imports none of the primary geometry or certificate code.

[INDEPENDENT-REVIEW.md](INDEPENDENT-REVIEW.md) reconstructs all three spectra
by rational elimination in a second nonorthogonal A8 operator chart, including
the irrational block and positive-definite sharp attainers. Its separate
`independent_orbits.py` implementation is registered in both Python modes.
