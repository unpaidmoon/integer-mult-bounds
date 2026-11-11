# Profile (2,1,1,0) fails support or a character

**Proof. No new κ and no word.**

In the PR2085/2112 model, every rational decomposition of the seven-call
profile `(2,1,1,0)/(1,1,1)` either misses a target as a subset sum or has an
additive character that detects two calls and four targets. Under the cited
determinant, character and support premises, the profile admits no word. The
argument is [PROOF.md](PROOF.md). The selected record stays
κ = `363005817/100000000000`.

Support holds exactly when one added frame is `Q` and the other two are a
nonzero rank-one pair summing to `A+2B`. Every such pair has odd reduced
denominator and even `c`-numerator, so the parity of that numerator detects
`P` and `Q` and misses both added frames. That character contributes two
calls and four targets.

## Scope and evidence

This is session r278, item 1 of the ordered eligible list read on
2026-11-11. Open handoffs whose later post completes them, whose canonical
artifact is an open pull request, or which say that no target was taken, are
dropped, as are the delivered 19 October index, the H25 chain, and the 2
November review artifacts. Updated notes are one request. Work already
delivered by this account is excluded, including #6942, #7013, #7035, #7051
and #7236. Three open handoffs remain, then the revision-8 next-decision
rows:

1. **This package.** Three signed added frames at seven calls (discussion
   comment 19377832, updating 19377345). #7128 leaves orbit O3 open and asks,
   first, whether `(2,1,1,0)/(1,1,1)` fails a character or target support.
   #7236 answers the previous first question, orbit O5, and leaves this one.
2. Eight-source singleton existence (comment 19537798). The 11 November
   search is still inconclusive, and `28 ≤ f(8) ≤ 32` is unchanged.
3. Six-source depth-two block at `c = 7` (comment 19537594). The 11 November
   search still leaves `c = 7` open.
4. Complex helpers (`p104-side-correction`): the proper-boundary rank bill
   left open by #7283.
5. BIT (`bit-helper-contract`).
6. New decoders and interfaces.
7. Supplier audit (`supplier-boundary-audit`).
8. All-size audit (`uniform-transfer-audit`).
9. Verification tooling (`replay-runtime`).
10. `bit-new-register-model`, beyond this changed scope.

Original card: `bit-new-register-model`, with `scope_status: changed`. The
card asks for a larger or nonabelian native alphabet. This package stays in
the abelian symmetric 2-by-2 model and answers one profile of the seven-call
handoff. The actual question, the reason for the scope change and the stop
rule are in [TASK.json](TASK.json). Pins are in [SOURCES.json](SOURCES.json).
Base commit `e54523517d0f03e58352e647c403a5af3e525a57`, priority revision 8.
The priority file on this main still quotes an older selected decimal; the
frontier value used here is the selected record.

Evidence classes:

1. **Proof.** Lemmas 1–4 and the theorem in [PROOF.md](PROOF.md), for every
   rational decomposition of this one profile. The twelve-offset support
   screen is exhaustive. The denominator parity is a 2-valuation argument.
2. **Finite corroboration, not the proof.** `verify.py` repeats the
   twelve-offset screen, expands the rank-one polynomial, and checks the
   character on the diagonal pair, the `(4/3)P` pair, and 323 parameter
   pairs with denominator at most 48. It also checks that the published
   character survivor of #7128 still misses support.

Premises (P1)–(P3) are not reproved. Predecessor replays, Lean, Docker and
`make frontier7000-verify` were not run. PR #7128's transport lemma is not
reproved, so the other seven profiles of orbit O3 stay conditional on that
lemma.

## Reproduce

Python 3.12 and the standard library, from the repository root:

```sh
python3 -B research/o3-profile-support-character/verify.py
python3 -I -W error -B research/o3-profile-support-character/verify.py
python3 -I -O -W error -B research/o3-profile-support-character/verify.py
python3 -B scripts/research_package.py --package research/o3-profile-support-character --check-only
python3 -B scripts/research_package.py --package research/o3-profile-support-character
```

Expected direct marker:

```text
PASS_O3_PROFILE_SUPPORT_CHARACTER sample=323 calls=2 targets=4 kappa=363005817/100000000000 no_new_kappa=true
```

The registered replay is the first command.

## Open next questions

1. Does every decomposition of `(0,1,1,1)/(1,1,2)` fail a character or fail
   target support? #7128 gives a decomposition that passes every character
   and fails support, and its box count finds no triple that passes both.
   The `Q`-frame argument here uses residual `(2,3,-1)` and does not apply
   to `diag(3,2)`. The first step is the same support classification for
   that residual. Nothing in this package blocks that classification.
2. If PR #7128's transport lemma is granted, the seven other profiles of
   orbit O3 are excluded with this one. A self-contained write-up would
   repeat the no-word statement after each of the eight label maps, without
   treating the finite profile list in `verify.py` as that proof.

## Credit

The register model is Cinna Davis's PR2085/2112 formal model. The
determinant, support and character premises are the PR2910 package as
recorded by apoursh in PR #6190 and
`research/bit-two-signed-frame-floor`. The census is discussion comment
19377345. The all-old-once exclusion is #6942. The O2 exclusions are #7013,
#7035 and #7051. Orbit O3, the character survivor
`-B + (5/2)Q + (1/4)(1,3)(1,3)^T`, and the question answered here are Nick
Petalas's PR #7128. #7236 records that the same question remains after the
O5 exclusion.

Prepared by unpaidmoon with substantial Cursor Grok assistance. No
independent human or formal-kernel review. New work is Apache-2.0.
