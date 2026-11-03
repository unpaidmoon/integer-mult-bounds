# H25 cache-source components and contribution handoff

This archive publishes reusable source work and the exact remaining blockers for **N22, P07 and P02**. It is a source-and-review handoff. The accepted local protocols, accepted P02 reference-bridge design and rejected G12 integration are separate components with different acceptance scopes.

The local checkpoint records **49 of 52 bounded source candidates accepted**. That count is historical source-review evidence. This export does not reproduce the complete evidence closure for all 49, qualify complete source adoption, run a candidate, validate the complete caller or measure a speedup. All three requested candidates remain open. The six-area source effort is paused; contributors are invited to take the explicit tasks below.

## Components and evidence

| Component | Status | Starting point |
|---|---|---|
| N22/P07 local candidate protocol | Independently accepted within its local source scope; external reference custody remains required | [protocol review](snapshot/review/cache-s0308-source-completion-v2/g12-protocol-independent/G12-CANDIDATE-PROTOCOL-REVIEW-v2.json), [frozen source list](snapshot/areas/cache-s0308-source-completion-v2/g12-protocol-repair/FREEZE-v2.json) |
| N22/P07 parent, adapter, consumer and candidate integration | Authored source rejected on two established defects; review incomplete | [rejection](snapshot/review/cache-s0308-source-completion-v2/g12-custody-source-independent/G12-CUSTODY-SOURCE-REVIEW-v1.json), [frozen source list](snapshot/areas/cache-s0308-source-completion-v2/g12-custody-implementation/FREEZE-v1.json) |
| P02 local two-suspension protocol | Independently accepted only at the local protocol boundary | [protocol review](snapshot/review/cache-s0308-source-completion-v2/p02-protocol-independent/P02-PROTOCOL-REVIEW-v1.json), [frozen source list](snapshot/areas/cache-s0308-source-completion-v2/p02-implementation/FREEZE-v1.json) |
| P02 dual-reference bridge | Corrected v4 design accepted; concrete bridge implementation and review outstanding | [accepted design](snapshot/areas/cache-s0308-source-completion-v2/p02-reference-bridge/DESIGN-v4.json), [review](snapshot/review/cache-s0308-source-completion-v2/p02-reference-independent/P02-REFERENCE-DESIGN-v4-DELTA-REVIEW-v1.json) |

See [CONTRIBUTOR-TASKS.md](CONTRIBUTOR-TASKS.md) for independently claimable work and acceptance tests. Use the new PR conversation as the canonical coordination thread. Claim a lane there before editing; N22 and P07 share G12 and should have one coordinated owner. P02 can proceed separately. A reviewer should be independent of the author whose change they assess.

## How to read the archive

Start with [the original coverage specification](snapshot/areas/cache-s0308-source-completion-v1/coverage/COVERAGE-SPEC-v1.json), then the task-specific review and source. [MANIFEST.json](MANIFEST.json) maps every preserved original path to its public relative path, size and SHA-256. Code snapshots have an additional `.txt` suffix so they are inert reading material; their content bytes and embedded predecessor credit are unchanged. Frozen JSON documents preserve their original paths and status at creation. A later review can reject a source file whose author freeze says ready: the decision table above and the latest cited reviews govern this handoff.

Every named source in the selected G12 implementation freeze and the P02 reference source-pin set is bundled. This is a curated source archive, not a portable runtime installation. The manifest's reference index explicitly shows other references that are outside this export. Reconstruct and independently review the relevant dependency closure before any future integration; do not replace missing references with dummy values, cached PASS results or caller-supplied success flags. Original local authorization records are historical evidence and do not grant a contributor access or authority.

## Reproduction and validation scope

From the repository root:

```sh
cd research/h25-cache-source-handoff
sha256sum -c CHECKSUMS.sha256
```

This checks archival bytes only and should be a short metadata operation; its duration is host dependent. No target imports, candidate/helper execution, compiler, native work, scientific run or decoder is performed by this command. There is no registered runtime replay in this package. The `.py.txt` files must not be run as validation of this handoff.

Publication checks compare every copied byte against its frozen source, verify selected review/source hashes, check the relative documentation links, and verify the committed file inventory. They do not re-award source acceptance. [VALIDATION.json](VALIDATION.json) records the exact metadata-only checks and unrun obligations. The original failed source and reviews remain retained.

## Existing independently usable packages

- [PR6316](https://github.com/CrocSwap/integer-mult-bounds/pull/6316), `f99829cfc669c0aa61d7d505b0a58f7e697c6582`: bounded retained-log handling and finite controls.
- [PR6317](https://github.com/CrocSwap/integer-mult-bounds/pull/6317), `336015471e4f1bb95998f293aa76823fe11e33d5`: lossless evidence archive and exact-restoration controls.

Both were freshly observed open and unmerged while preparing this handoff. Their validation and limitations remain in those PRs; they are not duplicated or dependencies of this archive. The common H25 predecessor is [PR6029](https://github.com/CrocSwap/integer-mult-bounds/pull/6029), `e05aad954689d0ee21baff19b4674f1fcb2e838f`. Its historical performance claims do not transfer to the new cache candidates.

## Cost and completion boundaries

The local checkpoint records 63.770533479 policy-charged seconds out of a 2400-second guarded allowance. That is not a complete physical-time total or a budget grant to external contributors. Historical timing gaps, current complete costs and the final metadata-publication timing tail remain unknown. This packaging operation does not resolve them. No minimum percentage improvement is imposed; any future gain must be measured with the preserved full checks and complete stated costs.

Complete source acceptance, adoption, actual execution, full-caller equality and measured gain are separate obligations. Reaching 52/52 source candidates would not complete the six-area goal. Mathematical work, the selected frontier and existing packages are unchanged.

## Open next questions

1. Can a narrowly corrected G12 handoff and cleanup implementation satisfy the remaining independent source checks for both N22 and P07?
2. Can a contributor implement the accepted P02 v4 bridge while preserving the original producers, ordering and independent reference evidence?
3. After source acceptance, can the complete caller and full cost gates be qualified in an explicitly budgeted environment?

The smallest useful first steps, blockers and success tests are in [CONTRIBUTOR-TASKS.md](CONTRIBUTOR-TASKS.md). A focused repair, independent rejection or clearly evidenced partial result is useful.

## Credit

Chris R / Clear1nsight; substantial OpenAI Codex assistance, including the separately attributed source authors and independent agent reviewers retained in the snapshot. Prior source and PR6029 contributor notices remain in their exact source bytes. The original Douglas R. Colkitt circuit/network lineage and all intermediate native and verification contributors retain their attribution. See the repository Apache-2.0 LICENSE and NOTICE. Local agent review is not independent human review or a formal proof-kernel result.
