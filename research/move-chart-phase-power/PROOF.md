# MOVE absolute phase on the selected word is i^{p f}

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No new κ. Assumption ID: `native_all_columns`. This is one implication, not that assumption and not the other four.

## 1. Proposition

Let the selected word be `research/p104-helper470-twin-rung-removal/WORD.json.gz` on canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc` (PR #6030, κ = 781451/250000000). Its schema is `p104-accumulated-block-composition/2`. Each register carries a chart index. At column multiplicity `f ≥ 1` the physical operator of a width-1 Clifford `U` on `(C^2)^{⊗9}` is the tensor power `U^{(⊗)f}` on `f` consecutive 9-qubit blocks.

A `MOVE` from frame `a` to frame `b` denotes

```text
U = chart(a)^† chart(b),
```

where `chart(i)` is `canonical_frame(9, frames[i])` from `research/p104-native-channel/vendor/clifford_exact.py`. `lower_child(U)` splits `U` into monomial factors. `native_verify.recipe` turns those factors into a circuit. On this word every such circuit has left monomial phase `0`, and the right monomial contributes a single nontrivial residue `p ∈ {0,1,2,3}` together with a harmless `('phase', 0)` gate from the left factor. The global phase of `U` is `i^p`.

**Proposition.** For every integer `f ≥ 1`,

```text
U^{(⊗)f} = i^{p f} U_0^{(⊗)f},
```

where `U_0` is `U` with its global phase gates removed. The equality `i^{p f} = i^p` holds for every `f ≥ 1` if and only if `p = 0`. The selected word has 1,809 distinct MOVE operators, and 2,117 MOVE events, with `p ≠ 0`.

The identity `i^{p f}` is the global-phase case of the monomial lift already written for the older #5599 word in `research/p104-allwidth-native-certificate/PROOF.md` (`i^{p f + Σ_j q(x_j)}`). That certificate's pair set is not this word's pair set. The census below is the binding for the selected caller.

## 2. Lemmas

**Lemma A (global phase).** A gate `('phase', p)` multiplies every amplitude by `i^p` and commutes with every gate in the circuit. Therefore `U = i^p U_0`.

*Proof.* `clifford_exact.Op.zero_state` and `native_verify.state` both apply that gate by `mul_i` / `rotate` on every stored amplitude, with no address change. A scalar multiple of the identity commutes with every linear map, so the gates may be collected at the front. `monomial` appends the phase only after a phase-free tableau representative, and `lower_child` preserves the operator, including `zero_state`. ∎

**Lemma B (tensor power).** For every integer `f ≥ 1`, `U^{(⊗)f} = i^{p f} U_0^{(⊗)f}`.

*Proof.* For a scalar `c` and a linear map `A`, `(c A)^{(⊗)f} = c^f A^{(⊗)f}`. Take `c = i^p` and `A = U_0`. ∎

**Lemma C (the width-1 integer is not invariant).** `i^{p f} = i^p` for every integer `f ≥ 1` if and only if `p ≡ 0 (mod 4)`.

*Proof.* The case `f = 2` says `2p ≡ p (mod 4)`, hence `p ≡ 0 (mod 4)`. If `p ≡ 0 (mod 4)`, then `i^{p f} = 1 = i^p` for every `f`. The residues recorded by this compiler lie in `{0,1,2,3}`, so the condition is `p = 0`. ∎

The three nontrivial residues already fail at width 2:

| `p` | width-1 factor | width-2 factor |
|---:|---|---|
| 1 | `i` | `i^2 = -1` |
| 2 | `-1` | `i^4 = 1` |
| 3 | `-i` | `i^6 = -1` |

## 3. Binding to the selected caller

`verify.py` walks every event. A `MOVE` is accepted only when its source frame is the role's current chart, its private flag matches owned-slot membership, and the frame span strictly shrinks (private) or grows (public). The walk ends on the declared public exit charts. It counts 3,453 `MOVE`s and 18,404 `ADD`s. A source-frame edit and a reversed public nesting are rejected.

`lower_child` on the 2,886 distinct endpoint pairs, cached per chart, gives:

| `p` | distinct pairs | events |
|---:|---:|---:|
| 0 | 1077 | 1336 |
| 1 | 994 | 1255 |
| 2 | 239 | 246 |
| 3 | 576 | 616 |
| total | 2886 | 3453 |

For every pair the left phase is 0, the child rank equals the absolute frame-length gap, and the sum of the recipe's phase gates equals `p`. One operator of each residue is compared in `native_verify.state`: deleting the phase gates and rotating the phase-free image by `p` reproduces the original state, and rotating by `p+1` does not. Those four states are controls for Lemma A. Lemmas B and C are the identities above; they do not depend on a finite width sample.

The #5599 word at `research/p104-helper-subspace-splits/WORD.json.gz` has 3,447 `MOVE`s and 2,887 endpoint pairs. It shares 2,808 pairs with the selected word, leaves 79 pairs behind, and misses 78 pairs that the selected word uses. Those 78 pairs have phase counts 23, 17, 20, 18 and occur as 103 events (42, 18, 24, 19). #5974's dense certificate names the #5599 pairs, including the payload hash of that word's recipes. It does not name these 78 operators.

## 4. What remains

Per-column execution of the width-1 circuit, phase gate included on each column, is exactly `U^{(⊗)f}`. Lemma B says that implementation is consistent. The false reading is that the integer `p` stored for width 1 is itself the joint phase at every multiplicity.

This does not re-prove the width-1 identity between `U` and the frame formula `adjoint(frame(a)) + frame(b)`. The selected review already records that the primary checked signed native maps and absolute phases at width 1. That check is not an all-width theorem. Spectators, whole-job adapters and fixed-tape tariffs stay open.

`owned_erasure`, `compiler`, `precision_tape` and `analytic_recovery` are untouched. #5625 (CRT row reentry) and #5707 (root-prefix lowering) are partial interfaces of other callers. #5837 lifts `SCALE` / `ADD` / `COPY` on the #5599 word. #5974 (`research/p104-allwidth-native-certificate`) certifies factorwise tensor lift, including absolute phase, for that same #5599 word and shows one termwise closed form that does not lift. #5442 is the group-algebra lift for the older #5413 caller. None of those three is a census of this #6030 word. No outer row, admitted BIT budget or selected κ changes.

## 5. Downstream effect

An all-width certificate that copies the width-1 phase integer into one joint recipe, without replacing `p` by `p f (mod 4)`, mis-signs every nontrivial `MOVE` at width 2. A correct certificate tensors the width-1 operator, or raises each global phase in that way. The 1,336 phase-zero events are the only `MOVE`s on this word for which the two readings agree at every positive multiplicity.
