# K = 4, s = 4 misses the Theorem S bound over F2

**Negative result in the F2 multi-pair model. No new κ. The selected record stays κ = 781451/250000000.**

Theorem S, proved in [research/multipair-schedule-bound](../multipair-schedule-bound/README.md),
says that s stages on K bank pairs cost at least

    N ≥ 2K + ceil(2K / (s − 1))

pair-calls. Odd stage counts attain the bound by parallel borrowing chains.
The predecessor left even stage counts open. Its first open instance is
K = 4, s = 4: the bound is N = 11, while four parallel B1 chains at s = 3
cost N = 12.

## Result

Over F2, in that package's stage model (bridges quotiented out, a stage
[[I, H], [E, I]] with HE = EH = 0), no 4-stage schedule has N = 11.
Every 4-stage schedule therefore has N ≥ 12. Four stages do not beat three
stages at K = 4, and the minimum over schedules with at most four stages is
12, attained by the odd-stage chains.

The argument is the equality-signature skeleton of Theorem S plus an
exhaustive orbit search under GL(X) × GL(Y). One orbit of each reachable
stage-2 signature has no legal continuation, so the goal is unreachable.
[PROOF.md](PROOF.md) records the 18 edges, the orbit counts, and the
controls. [verify.py](verify.py) recomputes them.

## Scope

Original card: `coverage-law-change`. Scope status: **changed**.

The card asks whether a completed call can earn more independent productive
target credit. The predecessor already moved this card onto non-B_K schedules
and showed that, at a fixed stage count, no schedule beats the B-template's
pair-call density. This package decides the instance that predecessor left
open. It does not price the selected #6030 supplier, and the historical T74
percentages in the predecessor are not a limit on the current frontier.

The added value relative to merged PR #2052 is the K = 4, s = 4 decision.
PR #4164 is the other open question in that package (a third bank class) and
is untouched here.

## Reproduce

From the repository root, CPython 3.12, standard library only:

```sh
python3 scripts/research_package.py --package research/theorem-s-k4-s4 --check-only
python3.12 scripts/research_package.py --package research/theorem-s-k4-s4
```

The hook reruns `verify.py`. On the machine used for this package that run
took about 40 seconds. It checks the K = 2 frontier, finds a K = 2 equality
witness and rejects a one-bit corruption of it, agrees with a direct search
that K = 3 has no N = 8 schedule, and checks the K = 4 orbit counts above.

Source commits and hashes are in [SOURCES.json](SOURCES.json). The catalogue
and selected record are provenance. The verifier does not read their bytes
and does not rerun the selected supplier.

## Open next questions

- **Another field.** The integer skeleton still reaches waste 3, so the
  F2 obstruction is not a dimension obstruction. Deciding K = 4, s = 4 over
  Q, or showing the same signature block for every field, would say whether
  even s = 4 can beat s = 3 somewhere. A first step is the stage-2 orbits
  over F3, where the same rank list is small enough to represent by matrices
  once a constructive normal form replaces the F2 bit model.
- **The priced even case s = 8.** The predecessor's historical T74 arithmetic
  left s = 8 as the only even stage count that could move that old exponent,
  and only if the bound is attained exactly. K = 4 does not decide s = 8.
  The blocker is the same orbit growth at larger K, not a missing lemma at
  K = 4.

## Credit

Theorem S, the stage model, the K = 2 frontier, the K = 3 negative search,
and the odd-stage chain attainment are from themilkman216, with substantial
Claude assistance, in `research/multipair-schedule-bound` (merged PR #2052),
generalising `research/cross-shear-stage-bound` and citing
`research/format-limits-corrected`. The T74 words priced there come from
PR #1800 and its lineage.

Prepared by unpaidmoon with substantial Cursor Grok assistance.
Apache-2.0.
