# Independent mode-0 check of deferred-K Q placement

**No new κ.** The selected conditional result stays the value pinned in
`certificates/selected-result.json` at base
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. This does not admit a global
caller and does not change the eight-H1 deferred-K invoice.

## Scope and evidence

The merged component in `research/deferred-k-query-sharing-component`
removes eight old-h queries and pays 120 bare current-source queries.
Its proof states that `q = R D^{-1}` is bare positive `C1` on physical
axis 0, and that mode-0 `Km0` is a width-one counterexample to wrapping
those queries by `K`. The component checker records that counterexample
as inherited from the frozen source audit and not recomputed by an engine.

This package recomputes it. The literal word, read from the pinned report
`REPORT-v1.md` (SHA256
`fb60187fea8346539abb61a08b1c525825cc84bd7c2847eb44a7c9590f3abee3`), is

```text
D(quadratic=0, linear=[2,2,2,2,0,0,0,0,0])
P(rows=[7,13,11,14,16,32,64,128,256])
X(0)
phase(0).
```

Apply `D`, then `P`, then `X`, then the phase. On nine bits:

- `K|0⟩ = |0⟩` and `K^{-1}|1⟩ = -|7⟩`.
- `K^{-1} X_1 K = -X_7` on every computational basis vector.
- Bare `Q = a I + b X_1`, with `a = (1+i)/2` and `b = (1-i)/2`, sends
  `|0⟩` to `a|0⟩ + b|1⟩`.
- The wrapped operator sends `|0⟩` to `a|0⟩ - b|7⟩`.
- Writing composition with the rightmost factor applied first,
  `R = D Q` on every basis vector: `Q` is one positive `C` on axis 0 and
  `D` is the positive `C` product on axes 1 through 8, low axis first.
  So bare `Q` is `D^{-1} R`, which is the report's `R D^{-1}` in that
  application order.
- The same `K` commutes with this `R` and fails to commute with bare `Q`,
  on every basis vector.
- Source axes `[0,9,10,11,12,13,14,15,16]` send local mask 7 to global
  mask `1537 = 2^0 + 2^9 + 2^10` and leave local mask 1 at global mask 1.

Clearing the first linear phase is a negative control: `K^{-1}|1⟩` is then
not `-|7⟩`.

The check is an operator identity for this word. It does not rerun the
native body, install Q120, or price a caller.

## Reproduce

From the repository root:

```sh
python3 scripts/research_package.py --package research/deferred-k-q-placement-audit --check-only
python3 -B scripts/research_package.py --package research/deferred-k-q-placement-audit
```

Direct command: `python3 -I -Werror -B research/deferred-k-q-placement-audit/verify.py`.
Expected token: `PASS_DEFERRED_K_Q_PLACEMENT`. One mode is about one minute
on CPython 3.12.

## Open next questions

Can a version-correct global occurrence ledger fund a gain from this
overlay? The component's own economics note still requires at least 28
further H1 deletions or genuine reuses at `C = .00330007` if only H1
counts change, and the standalone profile loses for every `0 < C < 1`.
The first step is to bind one real caller occurrence by input version,
owner, chart, phase, axes, and lifetime. No such caller is in this
package.

Can the helper and owned raw inverse-transpose be emitted? Start from the
ordered routes. The mode-0 calculation does not supply them.

## Credit

The deferred-K component, literal word, and inherited counterexample are
Chris R / Clear1nsight's PR #5423, with the peer fused-T placement,
Dillon Amburgey / dillona #5402, Ali Romman #5411, zxv #5419, and the
retained native, helper, and precision authors named in that package.
The source-frame audit that first read `Km0` is the pinned
`BALANCED-J-CURRENT-Q-FRAME-audit` report. This package only recomputes
that operator witness.

Prepared by unpaidmoon with substantial Cursor Grok assistance.
Apache-2.0. This is not a formal verification of the multiplication theorem.
