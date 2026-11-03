# Sharp support stability for the P104 rank relaxation

For a unit-diagonal matrix over **any field**, let `s = m - 2(n-r)`, where
`m` counts ordered off-diagonal nonzeros and `r` is the rank. A constructive
proof shows that deleting at most **2s matching row/column indices** leaves
only rank-one reciprocal pairs and singleton ones. The factor two is sharp.
The checker emits the exceptional indices, the retained blocks and an exact
cycle/rank accounting certificate.

For the P104 owned-delivery **matrix relaxation**, rank at most 56 and
`NEED = 96 + e` therefore imply at most `2e` exceptional indices. A new
mask-compatible rank-56 matrix with NEED 97 requires exactly two deletions.
This quantifies how constrained every near-minimizer is; it does not construct
an owned program. **No new kappa.**

The [proof](PROOF.md) independently corroborates Nick Petalas's PR6275
inequality/equality result by deterministic cycle deletion and principal minors,
then strengthens equality rigidity to a sharp stability bound. It does not use
the predecessor's random-order expectation, checker, rank code or witness.
The initial adversarial audit found no counterexample to the predecessor claim.
This is a scoped theorem with exact finite corroboration, not a failed search
presented as an impossibility theorem.

## Reproduce

From the repository root, CPython 3.12 and standard library only:

```sh
python3 -B scripts/research_package.py --package research/p104-support-independent-audit
```

Expected: two `PASS_P104_SUPPORT_STABILITY` markers,
two `PASS_INDEPENDENT_C_STABILITY_AUDIT` receipts, and
`PASS_REGISTERED_RESEARCH_PACKAGE`. Direct normal/optimized commands are
registered in `VERIFY.json`. The primary checker prints a generated JSON receipt
including the complete P104 witness, all field certificates, counts and
package/input hashes; the independent checker reports its separate census. No generated receipt is treated as an independent mathematical premise.

`stability.py` provides `construct(matrix, prime=None)` and
`validate_certificate(matrix, certificate, prime=None)`. `None` selects Q;
finite replay also supports F2, F3, F5 and F7. Rational input denominators
divisible by the chosen characteristic reject. The implementation is bounded
to 104 indices; the written theorem has no such bound. The validator checks
reachability, explicit partitions, ranks, complete support accounting, the
deletion budget and actual retained block coefficients. It never calls the
constructor or its Tarjan decomposition.

## Executed evidence

- Complete unit-diagonal domains: 4,165 binary matrices through dimension four
  and 739 ternary matrices through dimension three. Independent XOR-basis and
  determinant-minor rank oracles agree. Every small principal-subset deletion
  distance is checked; 18 positive-excess cases attain the factor two.
- All 21,700 dimension-five binary support matrices with at most five
  off-diagonal entries. The generated certificates are checked independently.
- 112 weighted rational/finite-field cycle and acyclic cases, lengths two
  through nine, including characteristic two and nonunit rational weights.
- The actual 104-port mask witness: rank 56, NEED 97 and excess one over
  Q/F2/F3/F5/F7; all 104 single-index deletions fail, while deleting `[1,2]`
  succeeds. Every mask entry is checked.
- Fourteen controls reject forged accounting, missing/reversed cycles, repeated
  or insufficient deletion, omitted blocks, a wrong field, a wrong peel degree,
  two changed source payloads and three invalid input types/field conditions.

An independent implementation by worker B additionally checks all 531,441
unit-diagonal 4×4 matrices over F3 by exact principal-subset deletion, with
32 sharp excess-one cases. Complete kernel enumeration independently checks
its rank routine on all 729 3×3 cases. Its P104 witness passes over
F2/F3/F5/F7/F11/F13. The script imports no primary package or predecessor code
and is included in the registered normal/optimized replay.

These are deterministic finite domains, not heuristic search. Stop rule:
finish the stated universal proof, a sharp P104-mask fixture and the complete
declared finite domains; do not expand into physical supplier admission.

## Sources, overlap and limits

Scientific base: `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision
8, selected PR6030 kappa `781451/250000000`. `SOURCES.json` binds the source
port payload, the P_M premise note and assignment provenance to this base.
Only the port field is read from the pinned PR5599 word; no predecessor
scientific executable runs.

The compared PR6275 proof is pinned to head
`681c547a36e742eceebbde04cb427bcd10cd3293`, path
`research/p104-rank-support-extremizers/PROOF.md`. Its prose is comparison
context, not an executable or logical dependency of this new proof. The
registered replay needs no pending-branch checkout or network access.
Main-tree README/PROOF searches found no support-stability predecessor;
the lead's all-state narrow PR search found PR6275 and contextual matches,
but no matching quantitative result. These bounded checks do not establish
literature priority or cover unpublished work. Coordination was local because
the available connected GitHub tools cannot post Discussions and `gh` was absent.

The P_M rank-to-paid and source/ownership premises remain cited, not audited
here. They do not transfer to P' accounting. A matrix certificate does not
prove legal gather/landing geometry, preservation of arbitrary inputs,
restoration, caller availability or a complete paid/productive invoice. The
physical NEED>=3597 objective remains open. All five selected assumptions
remain; no selected cold replay, native synthesis, compiler/tape/precision
proof, Lean verification or complete multiplier is supplied.

## Open next questions

Can the actual owned geometry exclude every reciprocal-pair block sum after
allowing a bounded exceptional set? Begin with an exact P_M source-content or
gather/landing constraint and test its behavior under principal deletion.
The blocker is preserving cancellations, branching, relays and all source/read
costs in that physical argument. No further search is justified by rank and
mask alone, because the sharp matrix witnesses already attain this relaxation.

## Attribution

By Jerry Chen, **@CubeJerry**, with substantial coordinated OpenAI Codex
assistance. Worker C supplied the proof and checker; a separate read-only AI
review checked the argument by induction, and the orchestrator inspected the
accounting proof. Worker B supplied an independent proof review and the
separate finite census. This is not independent human or proof-kernel acceptance.

Credit Nick Petalas/PR6275 for the prior support optimum and equality
classification; DreamingOfClouds/PR6170 for the P_M premises and physical gap;
Matarener/PR6267 for the owned-lineage/matrix distinction; Ali Romman/PR5599
and the retained P104/native/helper/controller/caller contributors for the
source ports. Classical graph, determinant and rank facts retain their
mathematical credit. Apache-2.0; predecessor sources and notices are unchanged.
