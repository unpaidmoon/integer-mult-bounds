# Validation record

Executed on October 30, 2026 with CPython 3.12.11, standard library only,
on native Windows 11 build 26300. The checkout is based on canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. No predecessor executable is
imported or invoked by this package.

## Executed checks

```
python3.12 -B scripts/research_package.py --package research/cubic-pow2-repair --check-only
python3.12 -B scripts/research_package.py --package research/cubic-pow2-repair
```

Both passed. The latter runs the registered normal and optimized Python
commands, each bounded to 120 seconds, without rewriting the receipt.
Both recompute identical complete RESULT.json content and pass:

- Four cubic coefficient polynomial identities after clearing denominator
  `6r`, using exact Fraction coefficients in the symbolic arity r.
- Three finite-difference recurrences with zero base cases, establishing the
  first, second and third chronological power sums used in the defect.
- The two modulo-three residue transitions and numerator divisibilities that
  prove dyadic membership for powers of two.
- Ten coefficient fixtures at exponents 2,3,4,5,6,10,16,32,64,128. Only the
  first five materialize every original child; large cases are coefficient
  fixtures, not enormous execution claims.
- Five symbolic chronological arities r=4,8,16,32,64. Every original child,
  the repair, eager comparator, inverse repair and full inverse are retained.
- 375 dirty rational-input cases (75 per arity), executing 98,625 logical
  events in total. These are exact arithmetic events, not native transitions.
- Eight controls reject for pinned reasons: wrong universal weight, query
  sign, missing final shear, swapped query/shear order, source corruption
  despite a correct output, out-of-domain arity, non-dyadic weight and a
  falsely asserted pure-entry-B query premise.

The all-arity theorem is the written polynomial and divisibility proof;
finite samples alone do not prove it. The dyadic query lower bound is
credited to PR6212 and restated in PROOF.md. r4 exactly reproduces its known
identity; the r16 fixture tests the changed pure-entry-B hypothesis.

Root reviewed the checker and a separate AI reviewer derived the algebra,
read the proof and inspected code/control/count semantics without running a
second implementation. This is separate AI review, not independent human,
formal-kernel or hosted-CI acceptance. A final portability edit fixes LF
newlines for receipt regeneration; registered normal/-O replay passed after
that edit. Frozen source proofs remain byte-identical.

## Source and publication checks

The package metadata/pin check authenticates the two predecessor proof
inputs and base catalogue/selected provenance. Canonical main was fetched
before this round and again before publication; it remained the base above.
Live PR6212 and PR6215 heads remained respectively
`9c159482e0495b6a97e17e629debe66a0ceb9466` and
`0013c2b40c522ccd19670a8fbd4b1531f13fed2b`, both merged. Their archive status
is not treated as scientific validation. The inherited proof hashes are in
SOURCES.json; full declared history is reachable from this main base.

The final committed-byte/history command is:

```
python3.12 -B scripts/check_research_commit.py --package research/cubic-pow2-repair --check-source-history
```

The committed-byte/source-history check passed for all ten package and input
files, with declared history rooted at the base commit above. It is rerun
after this validation-record update to check the final publication bytes.
POSIX executable-mode checking is not claimed on this Windows host.

## Coordination and overlap

[Canonical claim/finding](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19285638)
was posted before implementation. The initial bounded search covered all
8,722 HEAD notes, 310 open PRs and 5,981 Discussion records. Before submission,
the refreshed snapshot covered 311 open PRs at 05:18 UTC, 5,982 Discussion
records at 05:20 UTC, and all 8,722/8,722 HEAD notes plus the two new package
notes. Pagination was complete with no warning. Body/README/TASK searches
are not code search or a global novelty certificate.

All-state targeted searches and the relevant handoffs identify PR6200's
rational predecessor and PR6212/6215's remaining dyadic question. The cubic
scalar-bank/coframe and norm-six feature matches have different interfaces.
No competing power-of-two cubic-reader family was identified. Prior known
r4, odd-exponent powers and exponents divisible by six remain credited;
no literature-priority claim follows from this coverage.

## Unrun or unclaimed

No whole selected-supplier replay, native or rounded cubic implementation,
Lean/Docker build, complete physical invoice, portable runtime measurement,
hosted-CI acceptance, independent human review or complete multiplication
theorem is supplied. Coefficient generation, controller preparation, routing,
precision and storage must be paid by an actual backend. Query count alone
is not a speedup. Selected PR6030, its budgets and the five framework
assumptions are unchanged.

Prepared by AAAmirinu with substantial OpenAI Codex assistance. Apache-2.0.
