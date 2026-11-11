# Classify dyadic cubic repairs on directions 0,d,2d

For the fixed cubic reader of Nick Petalas's PR6200, a three-query dyadic
repair on entry-source directions `A, A+dB, A+2dB` exists **exactly when r
or r-1 is a power of two** (`r>=3`). The theorem allows arbitrary nonmonic
dyadic forms on these directions and general dyadic source frames. The
entry-A direction must be at an end of the progression.

The proof forces `d=r/2` or `d=(r-1)/2`; an odd prime dividing the relevant
denominator cannot cancel. The first branch is AAAmirinu's PR6246. The
additional branch `r=2^s+1` has three nonzero weighted-cube queries and
three integer source shears, retaining every original child and restoring
arbitrary incoming sources/output exactly. Apoursh's PR6212 already supplies
the unrestricted three-query lower bound for r>2, so this branch attains it.

At the first new count case r=33, subtract

```text
(187/32)(A+32B)^3 + (341/16)(A+16B)^3 - (869/32)A^3
```

using the actual six-event schedule in [PROOF.md](PROOF.md). The new cases
relative to PR6212/6215/6246 include r=33 and r=129 and their infinite
exponent classes. The r=3 identity and the earlier three-query residue
classes retain predecessor credit. Classical three-node quadrature explains
the construction; no historical-priority claim is made.

**No new κ.** This is a local coefficient/restoration result. Weighted queries
and source changes keep their individual prices in the complete symbolic
event bill. No physical backend, favorable complete cost recurrence, rounded
implementation or supplier admission is supplied. All five selected framework
assumptions remain; the selected result is unchanged.

## Why the restriction matters

- The r=14 unequal-direction integer repair from PR6212 succeeds outside
  this family. Equal-step exclusion is not a general four-query lower bound.
- At r=50, directions `-35,0,35` also give three integer queries. This is
  equally spaced with zero **in the middle**, and is an explicit positive
  scope control. The theorem requires directions `0,d,2d`.
- A formal coefficient identity alone is insufficient. Omitting the first
  r=33 source shift, or querying before it, fails the actual dirty-state
  execution. Both mutations are rejected.

## Reproduce

From the repository root, with CPython 3.12 and no third-party dependencies:

```sh
python3.12 -B scripts/research_package.py --package research/cubic-equal-step-classification
```

Expected: `PASS_REGISTERED_RESEARCH_PACKAGE`, after both scripts pass in
normal and optimized Python. Direct checks are `verify.py` and `crosscheck.py`
inside this directory. Neither imports predecessor executable code. Committed
receipts [RESULT.json](RESULT.json) and [CROSSCHECK.json](CROSSCHECK.json)
record the exact domains and results; [VALIDATION.md](VALIDATION.md) records
checks actually executed, environment, transport tests and limitations.

The written proof establishes the infinite-domain classification. Finite
evidence includes twelve polynomial identities; both rational branches for
r=3..1024; 10,944 spacing tests; fifteen literal symbolic child/repair programs;
189 dirty rational cases with 56,916 events including inverses; and fourteen
primary rejection controls. The separate implementation derives defects by
binary block concatenation and weights by rational Gaussian elimination,
checks 510 systems and 1,020 nonmonic rescalings, and has six controls.
Both paths check very large arities through `2^128+1` without claiming to
execute that many original children. The two scope-positive programs above
are separately checked. These are two implementations by the same
AI-assisted contributor, not independent human or formal-kernel acceptance.

## Sources, overlap and scope

Base: `2485805a6d47f36ea83ddde6327d453ac82d44dc`, canonical main, priority
revision 8. The selected certificate is PR6030, κ=0.003125804; historical
priority prose still naming PR5599 is not used as the frontier.

Exact predecessor heads:

| Source | Head | What is reused |
|---|---|---|
| PR6212, apoursh | `9c159482e0495b6a97e17e629debe66a0ceb9466` | Interface, dyadic lower bound, known r=3 and integer constructions |
| PR6215, apoursh | `0013c2b40c522ccd19670a8fbd4b1531f13fed2b` | Pure-original-B classification and covered residue classes |
| PR6246, AAAmirinu | `3d21b913efac1e3731bee7f0f4f4a8a84fecec37` | Entire power-of-two branch and its source chronology |

[SOURCES.json](SOURCES.json) pins source bytes and historical catalogue/selected
provenance. The first two proof inputs are unchanged main files. The pending
PR6246 proof is retained byte-for-byte with its Git blob and SHA256, without
requiring that pending commit as an ancestor. No predecessor code, frozen
archive, selected certificate, shared script or upstream file is modified.

The broader `joint-query-controller` card is explicitly changed to this local
side result. [TASK.json](TASK.json) records the initial local claim, three
candidates, seed, stop rule, bounded overlap and refresh checks. No sprint
issue was present; Discussion mutation is unavailable in the connected
GitHub tools and no gh CLI is installed, so coordination is recorded locally.
The overlap check covers all 8,722 main note records plus bounded live PR and
newest-handoff searches; it is not a global novelty certificate. Ledger entries
for PR6212/6215 remain partially reviewed: source retention is not theorem
acceptance. Final freshness and publication handoff are recorded in TASK.json.

## Open next questions

1. Which remaining arities admit three queries with other direction patterns?
   This restriction cannot settle them. Begin with one unclaimed arity and
   solve its four coefficient equations, then build the chronological repair.
   A finite failed search would not prove a four-query lower bound.
2. Does a real backend make the r=33 repair cheaper than eager restoration?
   Bind every query/shear tariff to a concrete caller and test the complete
   inequality in PROOF.md, including preparation, routing, precision, storage
   and all recursive children. Those missing prices block supplier expansion.

## Credit and license

Prepared for **@CubeJerry with substantial OpenAI Codex assistance** in algebra,
proof, both implementations, self-review, verification and packaging. Apache-2.0.
Nick Petalas (#6200), apoursh (#6212/#6215), and AAAmirinu (#6246) retain the
specific contributions above. Sricharan Vagvala/theon199 (#1532), Adam Gall
(#1205) and Hanson Sun (#1246) retain the quadratic/linear deferral lineage.
All predecessor source notices are preserved. No human review, Lean/kernel
proof, hosted scientific CI, full selected replay or complete multiplication
theorem is claimed.
