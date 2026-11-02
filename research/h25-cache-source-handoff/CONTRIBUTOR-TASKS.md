# Contributor tasks: N22, P07 and P02

Please claim a task on this PR with the exact branch/head, intended files and a bounded work period. Link resulting fixes or reviews back to the same conversation. Local source work is paused and has released these tasks; this request does not reserve the work for Clear1nsight. Coordinate N22/P07 together and let P02 proceed independently. Preserve this frozen snapshot and publish corrections as new files/versions or a separate scoped package.

## A. Repair and review G12 for N22 and P07

**Why it matters.** N22 must reach the real capacity boundary through 85,196 genuine retained original entries and a pending next original store. P07 additionally checks that the original fallback completes every remaining case with the independent original count and outputs. Both depend on trustworthy reference production, transport and cleanup. The accepted local protocol is already supplied; reuse its exact accepted scope instead of starting over.

**First repair: identity representation.** In [parent source](snapshot/areas/cache-s0308-source-completion-v2/g12-custody-implementation/g12_reference_parent_v1.py.txt), lines 1645-1648, `candidate_pin` emits the manifest identity as a tuple. The [consumer](snapshot/areas/cache-s0308-source-completion-v2/g12-custody-implementation/g12_reference_cold_consumer_v1.py.txt) installs that value in a FileRecord whose validator requires an exact dictionary. Choose one handoff representation and an explicit checked conversion at the consumer boundary, preserving every identity/type/currentness check. The review identifies exact spans and the subsequent string-key accesses.

**Second repair: cleanup and first failure.** Bare `finally` close loops in the parent preflight paths can replace an earlier error with a later close error and stop before closing remaining descriptors. Reuse the existing first-primary/ordered-secondary handling. Every known descriptor close must be attempted independently, with the original primary preserved and unknown/failed cleanup still non-successful. Preserve both original rejected branches in the new evidence.

**Required independent review.** Inspect the exact changed pins, source maps and reversible changes to predecessors. Verify both known findings are resolved. Then finish the explicitly unreviewed remainder: all 18 negative branches, schema predicates, syscall races, allocation failures, ownership/currentness and aliases, and cleanup outcomes. Do not treat the author's static counts or an AST parse as independent correctness evidence. Review the actual parent-to-adapter-to-consumer-to-candidate path, not separate compatible-looking snippets.

**Acceptance for this task.** An independent source review must explicitly accept the corrected integrated scope and identify remaining external obligations. A repaired draft, accepted design or isolated local protocol does not by itself add N22/P07 body credit. Whole source adoption and runtime results remain separate.

**Avoid expanding scope.** The [scope clarification](snapshot/review/cache-s0308-source-completion-v2/g12-custody-independent/G12-CUSTODY-SOURCE-SCOPE-CLARIFICATION-v1.json) removes the added requirement to construct a new enclosing accounting API as an original source prerequisite. Preserve the full symbolic cost categories and unknown tails. Do not reopen a generic accounting-framework project to fix these two source defects.

## B. Implement and review P02's accepted reference bridge

**Why it matters.** P02 requires full typed/order equality for original roles, rank events, trace and outputs, plus original native-counter evidence. Authentic references come from the original baseline and candidate modes. Keep their producers and the optimized candidate's independent comparison boundary unchanged.

**First step.** Implement the exact [v4 design](snapshot/areas/cache-s0308-source-completion-v2/p02-reference-bridge/DESIGN-v4.json), using [source interfaces](snapshot/areas/cache-s0308-source-completion-v2/p02-reference-bridge/SOURCE-INTERFACES-v3.json) and [source pins](snapshot/areas/cache-s0308-source-completion-v2/p02-reference-bridge/SOURCE-PINS-v3.json). The local helper and two-suspension driver are already supplied. The missing bridge has four scoped pieces: reference parent, original-producer adapter, cold consumer and a minimally derived reference-bound driver. Do not imply these four pieces have already passed source review.

**Critical ordering.** Validate the original pure namespace, run and validate the native lane, and require both known writer chains and their streams/descriptors closed. Only then retain both outputs, compare all six raw outputs and full trace, jointly recheck identities and seal the pair. Earlier retention of only the pure side was rejected; preserve that failure history. Unknown writers, aliases, closure or source drift must reject.

**Acceptance for this task.** Supply exact source pins/maps, a complete inverse to the accepted local driver, unchanged original helper/producers, and independent review of the parent/adapter/consumer/driver graph, strict decoding, artifact custody, first-error preservation, cleanup and symbolic costs. The design review already accepted the corrected mechanism at its stated scope; implementation review remains required.

## C. Independent review and later qualification

Reviewers can separately assess A or B after freezing the author's exact files. Return accepted scope, concrete findings, checked evidence and unreviewed obligations. Do not count both a design and its implementation as separate original candidates. Preserve the fixed denominator of 52 and the distinction between bounded source acceptance, complete adoption, actual execution, full-caller validation and measured gain.

Before any future runtime work, establish a complete source closure and explicit owner, guards, resource limits and funding for that environment. Preserve original oracles, assertions, types/order, rejection controls, raw failures and full cost accounting. No scientific replay or target execution is requested as part of this archive's integrity check. A new contributor's runtime allowance must be declared independently; the historical local 2400-second allowance is not transferable.
