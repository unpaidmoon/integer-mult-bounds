# Sum-only consumer of the encoded P104 exit

**Negative budget result. No new kappa.** Discussion #1166 comment 19032700,
task 2, asks for one downstream consumer that keeps the PR #3943 encoded
endpoint and does not pay an unaffordable source return. This package prices
the consumer whose published outputs are the corrected sums `w_i` on `Y_i` at
`H_i`, with `q` and the 72 dirty helpers left in place and `x` not restored.

The native bill still fails. The protocol pays the same 192 rank-one
transports as PR #3943's source-preserving return. Its scalar arithmetic is
smaller, and that scalar gap is not a rank-profile gap. Selected kappa stays
`0.001672660197076918`.

## What is proved here

The producer placement is taken from PR #3943 at
`2cba526a4ebe0ef6c3c0143498adcf67dca97941`: `w_N` sits on `X_N` at `H_n`,
`w_J` sits on `Y_J` at `H_j`, `q` sits on `X_J` at FULL, and `v_N` sits on
`Y_N` at FULL. This package does not replay the 3,642-event prefix or the
1,664-event tail. The inherited encoded profile is
`(1282, 58, 86, 104, 48, 24, 8, 8)`, mass 2,576, and the published
optimistic progress credit is 2,312.

From that exit the sum-only continuation is:

1. Lift each of the 96 `X_n` banks from `H_n` to FULL.
2. Clear `Y_n` by the unit update `Y_n -= Y_n`, then add `Y_n += X_n`.
3. Descend `Y_n` from FULL to `H_n`.

On every checked integer pattern, including one-port separating inputs,
`Y_N` becomes `w_N`, `Y_J` stays `w_J`, `q` and all 72 helpers stay put, and
`X_N` still holds `w_N` at FULL. So `x` is not recovered. The schedule is
192 transports and 192 unit additions, with no half-coefficient pass and no
restoring doubles. PR #3943's source-preserving adapter uses the same 192
transports plus 960 unit additions, 104 halves and 104 doubles.

The occupancy floor is the same 192. The 96 target hyperplanes are pairwise
incomparable, so one nested transport has at most one of them as an endpoint.
Publishing `w_n` on the distinct bank `Y_n` at `H_n` needs one departure of
`X_n` and one arrival of `Y_n`. The copy schedule meets that count.

Native mass is therefore `2576 + 192 = 2768`, the same mass PR #3943 already
rejects for the legacy return. In that equal-profile screen, with
`s = 9`, `m = 73`, `W = 832` and progress `2312`, the paid-mass lower bound
is 64,008 against capacity 60,736, deficit **3,272**. Subtracting the 768
saved unit additions from the native mass is a different accounting and is
rejected here; those additions are not rank children. The untouched encoded
exit, deficit 1,544 in the same screen, is PR #3943's result and is not
re-proved from the word.

## What this does not establish

No literal 5,370-event producer was executed. No physical owner, phase,
signed-floor width, tape, or opposite orientation is supplied. Clearing by
`Y -= Y` is one unit addition in characteristic not 2; a model that forbids
a self-update can spend one CLEAR instead, and the transport floor does not
move. A consumer that reads `w_N` from `X_N` and never publishes it on `Y_N`
is outside the floor. The equal-profile screen is the published necessary
test, not an owner embedding and not a universal P104 obstruction.

This is not PR #4006. That fusion returns `X = x` on the source-preserving
variant and saves 768 cleanup additions inside the correction word. It does
not remove the 192-transport native increment charged when the corrected
sums have to occupy the `Y` hyperplanes.

## Reproduce

Python 3.12, standard library, from the repository root:

```sh
python3 scripts/research_package.py --package research/p104-encoded-sum-consumer
```

The direct check prints

```text
PASS_ENCODED_SUM_CONSUMER transports=192 unit_adds=192 halves=0 native_mass=2768 deficit_s9=3272 encoded_deficit_s9=1544 x_restored=0
```

## Open next questions

A useful successor has to publish a different interface or delete native
children. One candidate is a consumer that reads `w_N` on `X_N` at `H_n`
and does not move those 96 banks onto `Y`. That interface avoids this
192-transport floor, but the inherited encoded mass 2,576 still misses the
published nine-stage screen by 1,544 before any new charge. Price it only
with a changed coverage credit or a named deletion of rank children, and
stop when the favorable bill remains above capacity.

## Credit

The encoded exit, the profile, the progress credit and the source-preserving
adapter are Chris R / Clear1nsight, PR #3943, following PR #3882. The channel
lineage is Rohan Arun / PR #1972, Chafik Boukhalfa / PR #1991 and Adam Gall /
PR #1940. The occupancy method follows the terminal-floor argument recorded
in that package. New work is the sum-only schedule, its separating-input
floor and the observation that the scalar gap does not change the rejected
native mass. unpaidmoon, with substantial Cursor Grok assistance. Apache-2.0.
No independent human or formal-kernel review.
