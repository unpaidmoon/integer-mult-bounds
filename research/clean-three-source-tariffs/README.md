# Exact heterogeneous three-source clean-row tariffs

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped proof with finite corroboration. There are exactly **15
componentwise-minimal call profiles** in PR5372's three-source paid clean-row
contract. For arbitrary positive source prices b_0,b_1,b_2 and output prices
a_1,...,a_7, the exact optimum over every finite legal word is

```
2 sum b + sum a + min(2 min b, min(a_3,a_5,a_6) + min(a_1,a_2,a_4,a_7)).
```

The twelve six-source-call profiles double one even and one odd output's
readout; the three eight-source-call profiles read each output once. Every
legal call vector dominates one of these profiles. All fifteen are attained
and individually exposed by strictly positive prices. At uniform prices this
is `min(6b+9a,8b+7a)`, making PR5372's cheap-readout example optimal. The
[proof](PROOF.md) handles unbounded word lengths and arbitrary compatible
linear maps, including singular maps and unequal row dimensions.

This answers the heterogeneous-price/full-profile gap explicitly left in
[Ali Romman's PR5372 proof](../clean-connector-gray-optimum/PROOF.md). It is a
local tariff result, with no new kappa, physical supplier, complete multiplier
or selected-frontier change. The same paid extra row must be allocated,
zeroed and restored. Add its fixed admission/lifetime bill to the formula;
word-dependent physical costs require a separate comparison.

## Reproduction and evidence

From the repository root, with standard-library CPython 3.12. The exact local
interpreter is `/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12`,
version 3.12.15 on macOS arm64.

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/clean-three-source-tariffs/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -O -B research/clean-three-source-tariffs/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/clean-three-source-tariffs
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/clean-three-source-tariffs --check-source-history
```

The verifier prints a generated JSON receipt with status
`PASS_CLEAN_THREE_SOURCE_ALL_TARIFFS`, enumerated coverage counts and SHA256
bindings for package files and the two predecessor contract inputs. It writes
no artifacts. The registered runner executes warning-strict normal and
optimized commands separately. Each is bounded to 120 seconds.

The finite coverage is 9841 source words through length eight, 1350 restored
spanning words, 220 distinct minimum-readout vectors, all fifteen minimal
profiles, 128 visited sets, 3480 exact heterogeneous-price comparisons,
10320 rectangular-map dirty-input executions and 112 rejecting controls.
A visited-set shortest-path oracle prices arbitrary-length source walks
independently of the six/eight-call theorem. The proof explains its 1024-state
bound and the separate scope of the length-eight enumeration. These counts
are executions/configurations, not claims of distinct map assignments or
exhaustive real-price enumeration. The written proof supplies the universal
quantifiers. Independent human and formal proof-kernel review are unclaimed.

## Scope and sources

Base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8. The
selected record is conditional kappa .003125804; the current priority prose
still names an older selection. [TASK.json](TASK.json) declares the changed
card scope and [SOURCES.json](SOURCES.json) pins the exact contract inputs.
The card's required 945-pairing orientation control was run once; it is not
the new result or a new audit. No predecessor theorem or scientific suite was
rechecked as the deliverable.

Credit Ali Romman for PR5372's generic paid-clean contract analysis, uniform
price theorem and six-call example; Cinna Davis for PR1954's paid extra-row
extension and PR2271's related borrowed-source Gray tour; Ross Richardson for
PR943's original connector; Adam Gall for PR2063's dirty-alphabet tariff
comparison. The binary cube, parity argument, reflected Gray cycle and
shortest-path methods are classical. This contribution supplies the exact
three-source heterogeneous frontier, its lower bound and rerunnable checker.
All predecessor files and credit lines are unchanged.

The original dirty connector and target/source boundaries are preserved.
The theorem assumes complete map calls already have their declared contracts.
Recursive hosting, native/map lowering, physical descriptors, precision/tape,
stock, ownership admission and the selected compiler remain open. The five
selected framework assumptions are unchanged. No selected cold replay, Lean,
Docker, human review or proof-kernel verification is claimed. Finite CI replay
certifies the registered checks, not the universal theorem's independent review.

## Open next questions

1. Can one concrete recursive caller host the fifteen schedules with actual
   complete prices and a favorable fully charged invoice? First specify its
   row layout, allocation, map lowering, descriptor and restoration costs.
   These physical/caller contracts are not supplied here.
2. What is the heterogeneous frontier with four paid-clean source rows? First
   use the finite visited-set reduction to form candidate profiles, then
   prove a source-length reduction. The present parity argument gives only
   the three-source theorem. No larger search is reserved or run here.
