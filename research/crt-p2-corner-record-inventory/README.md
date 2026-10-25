# Section-2 record inventory at the two p = 2 corners

**Finite certificate. No new κ.** The selected conditional value stays
`605457647/200000000000 = 0.003027288235`.

For the full shared-arena batch in `research/crt-arena-batch-threshold`,
replace one schoolbook product per tape action by the record comparisons in
PR #4192 section 2. Charge each of the `4 A J` key-field comparisons, and
each of the `V = N^2 - N - N h / 2` pairwise comparisons, at the same cap
`8 w^2`. Keep the inherited tape, rotation and CRT charges. [PROOF.md](PROOF.md)
shows that this batch is strictly below `E = 2^{4 ell} (p+2)^{16}` at both
excluded corners:

```text
(2, 1, 1):  B = 822078336      <  E = 68719476736
(2, 2, 2):  B = 12370604416    <  E = 1099511627776
```

The inherited majorant remains above `E` at those two triples
(`75548846976` and `1241895956864`). The same section-2 term is strictly
smaller than that majorant on the whole admissible domain, so the
predecessor's classification lifts the fit to every integer `p >= 2` and
`1 <= h <= ell <= p`. One schoolbook cap per arena cell per charged access
still fits the two corners as well. Neither statement is a machine lower
bound or a supplier admission.

## Selection

Session r41, item 9 of the ordered eligible list rebuilt from the r31 list
in `research/rank8-u2-entrance-obstruction` against canonical main
`32890bc5de034ab8fc93ac88ead7279a6a416d04`. Order: open handoffs from the
19 October index, then priority-table rows whose next decision is still
open, then catalogue cards not already in those rows. A closed smallest
task is removed and its first distinct open remainder stays in place.
Work this account already delivered, questions closed on current main,
questions covered by an open pull request, and topics on a fork `cursor/*`
branch are dropped.

1. Caller that accepts `(w, q, v_N)` without restoring the original source
   slots (comment 19030045).
2. Bind one complete-stream COPY child to its source-preserving caller
   (remainder of comment 19030047).
3. Cost to place `L561` onto the four scratch windows before `L546 -= L561`
   (remainder of comment 19030049).
4. Does the PR #2809 continuation serializer park the ancestor chain, or
   one root-sized stream per cut?
5. Four-provider ordinary/outer rebind.
6. Matched QQ16 park/restore bill against the external-call protocol.
7. Feasibility of the 1090-call idle `{3:22783, 5:1625, 48:138492}` inside
   the 841-pattern program.
8. Stored narrow band of at most `2p` off-diagonal entries per row, with
   rounding absolute error at most `2^{-5p}`.
9. This package.

The retiming handoff, the six-tape head-move bill, the `#4091` ceiling
itself, the monotone rank-8 producer, and the R437 fixed-tape parent bill
stay dropped: this account already delivered them or a refinement of them.
`p104-side-correction` is item 1, not a second row.

## Evidence and reproduction

The corner identities are exact integer arithmetic in [PROOF.md](PROOF.md).
[verify.py](verify.py) recomputes them, checks a second polynomial expansion,
checks the inherited majorant against the published exceptions, checks the
coefficient-one cell enlargement, and corroborates `T_record < T_scalar` on
all 45,759 triples with `2 <= p <= 64`. The proof of that comparison has no
`p <= 64` restriction. The all-domain fit cites the predecessor
classification and does not re-prove it. No predecessor executable is run.
The verifier authenticates its three live inputs by SHA256 and Git blob
identity. [SOURCES.json](SOURCES.json) also pins the selected record and the
originating catalogue.

From the repository root, using CPython 3.12 and its standard library:

```sh
python3 -I -W error -B research/crt-p2-corner-record-inventory/verify.py
python3 -I -O -W error -B research/crt-p2-corner-record-inventory/verify.py
python3 -B scripts/research_package.py --package research/crt-p2-corner-record-inventory
python3 -B scripts/check_research_commit.py --package research/crt-p2-corner-record-inventory --check-source-history
```

The direct verifier prints `PASS_CRT_P2_CORNER_RECORD_INVENTORY`. Normal and
optimized runs keep every check: the checker uses an explicit `require`, not
`assert`. Default replay does not rewrite [RESULT.json](RESULT.json);
`--write-result` regenerates that receipt on purpose. The last command is a
publication-byte preflight against the commit that contains this package.
Not run: Lean, Docker, the Beneš simulator, and native replay.

## Scope and credit

Base is canonical main `32890bc5de034ab8fc93ac88ead7279a6a416d04`, priority
revision 7. [TASK.json](TASK.json) refines `uniform-transfer-audit` to open
question 1 of the full-batch threshold. This is a tape-cost step of that
allowance, not a change of alphabet and not a kappa step.

An overlap search on 2026-10-25T07:21Z covered 398 open pull requests,
4819 discussion records and 7404 local notes. No open pull request or
discussion states this section-2 corner inventory. The nearest notes are
the open question in `research/crt-arena-batch-threshold` and the one-axis
bill in `research/crt-arena-root-axis`. Closed pull-request bodies were not
searched beyond those local notes. "No matches" is not a novelty proof.

Nick Petalas proved the inherited full-batch threshold and left these two
corners open. The one-axis bill and its schoolbook cap are unpaidmoon's
PR #4650. The CRT and rotation tariffs are unpaidmoon's PR #4377. ToikY's
PR #4192 supplies the arena census, the four-field scan and the pairwise
count; the vendored proof is unmodified. Cinna Davis supplies the shape of
`E` in PR #4100. Those claims are premises. Predecessor files are unchanged.
New work is Apache-2.0. Prepared by unpaidmoon with substantial Cursor Grok
assistance. Independent human and formal proof-kernel review are unclaimed.

## Open next questions

1. Can this full-batch allowance be composed with reservoir placement and the
   actual paid repair-key service of PR #4795? Begin with one complete entry,
   call and exit program, retaining all source-state queries and restoration
   charges. Physical movement and all-size caller premises remain external.
   The corner fit does not answer that composition.
2. Does a literal scalar transition table, rather than this comparison
   count, change either corner? The first step is to emit the fixed `w`-bit
   register steps for one four-field scan and price those steps at
   `(2, 2, 2)`. No such table is emitted here. The margin under the
   schoolbook cap does not substitute for that table.

The structured questions in [TASK.json](TASK.json) record relevance, first
steps and blockers.
