# A dyadic rank-seven P104 projector below the real quarter-error floor

**An exact Gaussian-dyadic Hermitian projector answers PR6211's first
open next question. No new κ.**

For the same fixed 104-root Gram matrix K=RR^T/2, construct
D=I-zz*/65536 with complex rank seven and coefficients in Z[i,1/2].
Its approximation C=RDR^T/2 has exact maximum complex entry error
**16193/65536**, below **1/4** by **191/65536**. Both C and K-C are
positive semidefinite. The complete witness is

```text
z = (73-53i, 31+118i, 73-51i, 88+16i,
     73-51i, -15-51i, -87-15i, -88-17i),   z* z = 2^16.
```

PR6211 already shows complex coefficients can beat the sharp real floor.
Its examples contain odd denominators; this result closes that specific
coefficient-ring gap. It does not improve on PR6211's stronger error
witness or claim optimal error/minimal denominator. Rounding the old
matrix is insufficient: the retained control has rank eight and fails
exact projector idempotence.

## Reproduce

From the repository root, with CPython 3.12 and the standard library:

```sh
python3 -B scripts/research_package.py --package research/p104-dyadic-rank-seven
```

Expected: `PASS_REGISTERED_RESEARCH_PACKAGE`, with normal and optimized
copies of `PASS_P104_DYADIC_RANK_SEVEN`, `PASS_FRACTION_REALIFICATION`
and `PASS_BOUNDED_DYADIC_SEARCH`. Six bounded commands are registered.
All four external inputs are pinned in SOURCES.json. Frozen inputs,
shared code, selected records and upstream/ remain unchanged.

The principal check also runs directly and reads files only:

```sh
python3 -I -B -W error research/p104-dyadic-rank-seven/verify.py
```

[PROOF.md](PROOF.md) gives the exact argument and scope; WITNESS.json
records the vector, expected receipt and completed discovery coverage.
The same checks remain active under optimized Python (`-O`).

## Evidence

- All 10,816 entries of the literal Gram product are checked with exact
  integer Gaussian arithmetic. The largest squared root response is
  129544, uniquely at zero-based row 24. Gaussian-rational elimination
  checks the projector and an eight-root minor independently of the
  projection rank formula.
- A second same-author checker imports no primary or predecessor code.
  Fraction realification checks rank fourteen, real-part rank eight,
  and all 10,816 residual entries with a different root order.
- Nine semantic rejecting controls cover wrong normalization, missing
  conjugation, old odd denominators, a changed vector, false error,
  naive rounding and malformed root omissions. Four source-byte controls
  reject changed inputs. Sixteen real attaining projectors, global
  conjugation and sign changes of omitted representatives are positive
  scope controls.
- The bounded DP solves five closest-vector boxes on dyadic spheres,
  guided by PR6211's stronger witness, and stops at k=8. It does not
  minimize coefficient error. Failures at k=4..7 concern only the
  selected vectors, not all vectors or denominators. Domain, nonce,
  stopping rule and completed coverage are retained in PROOF/WITNESS.

Actual execution and the initial root-parser correction are recorded in
TASK.json and VALIDATION.json. This is exact finite arithmetic plus a
written proof, not independent human or formal-kernel review. No selected
scientific cold replay or physical supplier replay is claimed.

## Sources, overlap and scope

Base: `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
The selected record identifies PR6030, κ=781451/250000000. Its binding-only
orientation passed. The older number in the priority narrative was not
used as the frontier.

| Predecessor | Exact source head | Retained contribution |
| --- | --- | --- |
| [apoursh #6211](https://github.com/CrocSwap/integer-mult-bounds/pull/6211) | `369ad15647ad0df0b0ef6f4fcb060509b67f1823` | Complex witnesses, guide and explicit dyadic-projector handoff |
| [apoursh #6191](https://github.com/CrocSwap/integer-mult-bounds/pull/6191) | `be3fc854aa380b3d81e134ce9a4282468e4fa999` | Sharp real rank-seven comparison |
| [Nick Petalas #6183](https://github.com/CrocSwap/integer-mult-bounds/pull/6183) | `eaf77790466f34b86ce72080e3ec690e26dfacab` | Contractive problem, real projector and omission data |
| [Matarener #6166](https://github.com/CrocSwap/integer-mult-bounds/pull/6166) | `096938513138868f0ed27639061f1a5054900f96` | Cited P104-to-D8 physical identification |

All four are archived as partially reviewed in the base ledger; archival
inclusion is not scientific acceptance. Physical coordinate identification
remains a cited premise. Replay inputs are pinned to their exact copies at
the base commit; no pending branch or predecessor executable is required.

The repository handoff-first process led to an explicitly changed
coverage-law card for this local algebraic question. Bounded all-state
PR searches for 6191/6211, complex rank approximations and dyadic
projectors, the ledger and newest public handoffs found no competing
dyadic witness. Local overlap was sparse (79/8722 notes), and Discussion
coverage was incomplete. These checks do not certify novelty.
No pinned sprint issue was found, and connected tools cannot post to
Discussions; the advance claim and completion are recorded in TASK.json.

The real part of C has rank eight, and the residual has spectral norm 13.
Smaller individual coefficient error is not vanishing operator error.
An exact linear seven-channel reconstruction would lose one required
direction. Source access, native realization, correction, dirty
restoration, caller installation and the complete paid/target invoice
remain open. No completed supplier or paid-work saving is claimed.
All five framework assumptions and the selected κ are unchanged.

## Open next questions

Can an actual caller use this projection and handle its nonzero residual
at a favorable complete cost? Start with one source/consumer, trace the
exact rank-one residual through every required output, and charge
acquisition, delivery, native realization and restoration. The missing
caller and complete invoice are the blockers. Another approximation or
denominator search alone would not resolve them. TASK.json records this
question structurally; no broader search is reserved.

## Credit and license

New witness, bounded construction, proof and verification by **Jerry Chen
(@CubeJerry)** with substantial OpenAI Codex assistance. Armin Pourshafeie /
apoursh, Nick Petalas and Matarener retain the specific predecessor credit
above. Rohan Arun, Chafik Boukhalfa, Ali Romman, DreamingOfClouds, Cinna Davis,
Pierre-Loic Doulcet, icekylinx, zxv, Jacob Alan Sussman and the retained
P104/root/frame/native/helper/compiler/BIT lineage retain their source
contributions. Hermitian projection, Gram-rank and dynamic programming
are classical; no literature-priority claim. Apache-2.0.
