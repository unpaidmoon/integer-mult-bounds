# Independent rational outer audit of PR6167

This answers the outer-arithmetic part of [PR6214's handoff](https://github.com/CrocSwap/integer-mult-bounds/pull/6214) for [PR6167](https://github.com/CrocSwap/integer-mult-bounds/pull/6167), head564a076b113621a93edc4e39968ee4e4a8c9caf0. The independent audit had rerun the authors' chain but explicitly left its54 strict and4 functional predicates unreconstructed. Here a separate evaluator uses reduced rational expressions and imports or calls no predecessor pricing/ledger code.

## Result and scope

At k=625729/200000000 and g=1/1400000000, the nine savings,54 distinct strict checks and4 functional checks match every pinned name and rational value. Full parameters are checked separately. The smallest strict slack is g/10=1/14000000000. The limiting saving is main_transform; its slack over k is2097809947/980000000000000000. PROOF.md derives these expressions and their positivity from the source definitions.

Three different BIT quantities must stay distinct: admitted saving17/5000; inherited stock atom3/1000; actual source atom1/250. The actual stock exponent beta*(249/250)=348599999253/350000000000 satisfies0<exponent<beta<1, with gap beta/250. Merely checking this exponent is positive would not establish its sublinear interpretation.

The source receipt's `margins` are savings, while named `<row>_above_kappa` values are slacks. Duplicate JSON names are rejected before a dictionary can erase them. The checker requires complete name sets, because many distinct obligations share the same numeric value.

## Verification and reproduction

```sh
python3.12 -B scripts/research_package.py --package research/p104-outer-rational-audit
```

SOURCES.json pins the candidate receipt/pricing, actual inherited definitions, earlier formula provenance, source BIT data and6214 handoff. The checker reads/authenticates those files but executes none of their Python. A deterministic exact result and semantic corruption controls are recorded in RESULT.json; VALIDATION.md records actual normal/-O runs and review. This is independent of the predecessor executable implementation, not independent of its mathematical definitions.

Base2485805a6d47f36ea83ddde6327d453ac82d44dc, priorityrevision8 and selected6030 unchanged. Both source heads were checked unchanged/merged; archival preservation is not scientific acceptance. Initial overlap covered309openPRs/5980Discussionrecords through04:59UTC and all8722HEADnotes, plus all-state6167 independent-outer search. Toolkit-v2's matching text concerns word-independent inventory and its real path retains author pricing; it does not supply this separate reconstruction. Bounded search is not novelty certification. [Canonical claim/finding](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19285465).

## Open next questions

PR6214's separate compiler-threshold handoff remains open. Choose the pinned integer inequality and compare boundary exponents independently before claiming that check. Native word/caller correctness, funding, all-size compiler, precision/tape and analytic hypotheses are inherited premises here. All five framework assumptions remain. A positive exact ledger does not supply an all-size multiplication theorem, admit a supplier, select a frontier or establish a new kappa.

TASK.json gives the next steps and blockers. No full mathematical replay, Lean, Docker, hostedCI or human/proof-kernel acceptance is claimed.

## Credit

AAAmirinu with substantial OpenAI Codex assistance, including separate proof work and AI review. Matarener/PR6214 posed the independent arithmetic gap. Ali Romman/PR6167/5827 supplies the candidate and pricing lineage; DreamingOfClouds the predecessor construction. The outer/controller/compiler and BIT formulas retain credit to zxv, Cao Yifan, Jacob Alan Sussman, Cinna Davis and the contributors named in the pinned sources. Classical rational simplification is background mathematics. Apache-2.0.
