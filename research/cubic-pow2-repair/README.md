# Three dyadic cubic repairs for power-of-two arities

For every `r=2^s>=4`, the fixed cubic-reader contract of [apoursh's PR6212](https://github.com/CrocSwap/integer-mult-bounds/pull/6212) admits an appended repair with **three nonzero weighted-cube queries and two integer source shears**. All original children remain in order, and arbitrary incoming source and target values are preserved as required. The inherited unrestricted dyadic lower bound makes three queries optimal in this contract; no runtime optimality is claimed.

Let `A,B` be the entry sources. The deferred children leave `a=A+rB` and create the excess

```
f_r = 3S1 A^2 B + 3S2 A B^2 + S1^2 B^3,
S1 = r(r-1)/2, S2 = r(r-1)(2r-1)/6.
```

The uniform identity is

```
f_r = c1 (A+rB)^3 + c2 (A+rB/2)^3 + c0 A^3,
c1 = (r-1)(r-2)/(6r),
c2 = 2(r^2-1)/(3r),
c0 = -(r-1)(5r+2)/(6r).
```

Each weight is dyadic: `r` is a power of two and a numerator factor cancels the remaining factor three. From the actual deferred source, execute

```
y -= c1*a^3
a -= (r/2)*b
y -= c2*a^3
a -= (r/2)*b
y -= c0*a^3
```

This ends at `(y0+r*A^3,A,B)`, exactly the eager comparator. [PROOF.md](PROOF.md) proves the identity, coefficient admissibility, chronological restoration and inherited query minimum for all powers of two, independently of finite examples.

## What this adds

PR6212 already gives the same `r=4` identity, as well as three-query repairs for `r=2 mod3`. These include odd-exponent powers of two and remain credited controls. PR6215 also gives three queries when `s` is divisible by six (`r=1 mod9`, for example `r=64`). The remaining power-of-two count cases relative to these two sources have `s=2 or4 mod6`, excluding the known `s=2` case. This package supplies one formula and chronological schedule for **every** power-of-two arity. The first new power-of-two case relative to those constructions is `r=16`:

```
f_16 = (35/16)(A+16B)^3 + (85/8)(A+8B)^3 - (205/16)A^3.
```

In [PR6215](https://github.com/CrocSwap/integer-mult-bounds/pull/6215), `r=16` needs four queries **when a nonzero pure original-entry-B cube is required**. None of our three forms is pure entry `B`, so this changes that hypothesis and does not contradict its restricted lower bound. Both predecessor proof files are live inputs pinned at base `2485805a6d47f36ea83ddde6327d453ac82d44dc` in [SOURCES.json](SOURCES.json). Their originating heads are `9c159482e0495b6a97e17e629debe66a0ceb9466` (6212) and `0013c2b40c522ccd19670a8fbd4b1531f13fed2b` (6215).

The canonical [claim and handoff](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19285638) records the bounded scope. The original `joint-query-controller` card is retained in [TASK.json](TASK.json), with its explicit narrowing to a coefficient-feasibility lemma. This does not reopen the unrelated fixed-channel helper-injection models or satisfy the full family expansion gate.

## Evidence and reproduction

[verify.py](verify.py) uses exact rational arithmetic and does not execute predecessor code. It checks a polynomial identity in the symbolic arity, literal retained-child/repair executions and reversals, source positive controls and failure modes. [RESULT.json](RESULT.json) is compared to recomputation, not trusted as the answer. [VALIDATION.md](VALIDATION.md) records the executed environment, counts and publication-byte checks.

From the repository root with Python 3.12 and no third-party dependencies:

```sh
python3.12 -B scripts/research_package.py --package research/cubic-pow2-repair --check-only
python3.12 -B scripts/research_package.py --package research/cubic-pow2-repair
python3.12 -B scripts/check_research_commit.py --package research/cubic-pow2-repair --check-source-history
```

The registered replay runs normal and optimized Python, each with a 120-second timeout. The final command needs committed publication bytes and full Git history. Only `verify.py --write` regenerates the receipt; ordinary replay compares it.

## Paid boundary and limitations

Use the predecessor's complete weighted-query prices `Q_c^a` and source-shear prices `L_c`. The eager bill is `r Q_1^a + r L_1 + r L_-1`. The deferred bill retains `r Q_1^a + r L_1` and adds

```
Q_-c1^a + L_-r/2 + Q_-c2^a + L_-r/2 + Q_-c0^a.
```

Every displayed event is paid, including its actual coefficient. Coefficient generation, routing, precision, storage, dispatch and controller preparation require their complete backend charges. Fewer repair queries or shears alone do not prove a cheaper execution. Exact arithmetic, no intermediate observation/output feedback, and the unchanged-child contract are essential. Rounded/native execution, an all-arity classification, a complete supplier bill and a new multiplication theorem are not supplied. The selected result and its five framework assumptions are unchanged. Archive intake, if any, is not independent scientific acceptance.

## Open next questions

1. For one arity and supplied backend, compare the complete repair invoice above with `r L_-1`. This is the first useful decision about runtime; missing coefficient or physical costs are blockers, not zeros. Stop if extra charges consume the gain.
2. For a still-unclassified non-power-of-two arity, check the live handoff before attempting a three-query construction. A single proof or scoped obstruction would extend the arithmetic classification; this package does not establish it.

## Credit

Prepared by AAAmirinu with substantial OpenAI Codex assistance, including separate AI algebra/code review. Apache-2.0. No independent human or formal-kernel acceptance is claimed.

apoursh's PR6212 supplies the dyadic two-query obstruction and the known `r=4` and `r=2 mod3` constructions; PR6215 supplies the required-pure-entry-B classification. Nick Petalas's PR6200 supplies the fixed cubic-reader defect, rational lower-bound argument and restoration interface. Sricharan Vagvala / theon199's PR1532, Adam Gall's PR1205 and Hanson Sun's PR1246 retain the quadratic and linear deferral lineage credited by those sources. Binary-form power decomposition and coefficient comparison are classical; no literature-priority claim is made.
