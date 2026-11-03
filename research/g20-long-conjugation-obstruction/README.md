# Longer fixed-route G20 conjugations attain a minimum paid-moment change of zero

Every single A2 conjugation with four or more contacts on the final
[PR5708 word](https://github.com/CrocSwap/integer-mult-bounds/pull/5708)
either encounters a missing published route or fails to improve the paid-query
moment for any exponent `0<t<1`. Corrections stay at their original contact
frames. Among the emitting candidates the minimum change is exactly zero,
attained by 14 words. No new kappa or supplier admission is claimed.

This answers the longer-contact, fixed-frame part of open question 2 in
[unpaidmoon's PR6290](https://github.com/CrocSwap/integer-mult-bounds/pull/6290),
head `9d2916b07402aca2133ab315230b9c761cc9eff7`. The one-to-three-contact
result remains that predecessor's contribution. This package enumerates only
the new four-or-more-contact domain. See the model and sign proof in
[PROOF.md](PROOF.md).

## Exact result and evidence

| Outcome | New candidates |
|---|---:|
| Missing published route | 1,450 |
| Emitted, strictly larger moment throughout `0<t<1` | 39 |
| Emitted, identical paid histogram | 14 |
| Total | 1,503 |

All 1,503 changed words retain the exact scalar endpoint on all 685 independent
input columns. Their contact counts range from 4 to 33. The enumeration has
no contact cutoff: it visits every equal-gate interval on the fixed 11,930-record
scalar word. Each missing-route record gives the first absent ordered frame
pair, and each emission gives its complete signed paid histogram.
Every strict-loss shape is positive by positivity or strict subadditivity;
no floating-point or exponent sampling is used.

The standalone checker tests 256 four-contact identities and 256 missing
correction mutants, plus seven boundary, sign and routing controls. It uses
explicit exceptions under both normal and optimized Python. A generated
receipt can contain the complete candidate certificate and SHA256 bindings
for all six package files and every live input. Its canonical certificate
digest is `577323306b7b7f2547ca660e6bbef1badc953959e2f7cd20de9e1f002e254889`.

## Reproduce

From the repository root, with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/g20-long-conjugation-obstruction/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/g20-long-conjugation-obstruction/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/g20-long-conjugation-obstruction
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/g20-long-conjugation-obstruction --check-source-history
```

Any CPython 3.12 interpreter can replace the local absolute path. Each direct
check prints `PASS_G20_LONG_CONJUGATION_OBSTRUCTION candidates=1503
missing_route=1450 emitted=53 neutral=14 strict_loss=39 min_contacts=4
max_contacts=33`. The registered runner prints `PASS_REGISTERED_RESEARCH_PACKAGE`.
The optional `--output /absolute/path/outside/checkout/receipt.json` writes a
generated, source-bound receipt. It never writes into the checkout.

Exact source commits, Git blobs and SHA256 pins are in
[SOURCES.json](SOURCES.json); the changed card scope and structured follow-ups
are in [TASK.json](TASK.json). The selected record and catalogue are historical
provenance. The three live inputs are authenticated before use. Neither the
predecessor verifier nor its larger caller is executed.

## Limitations

The result fixes the final PR5708 word, one conjugation, original correction
frames and the published routes. A missing route is not a geometric impossibility.
Further rewrites through neutral neighbors, added routes and different correction
frames remain open. The certificate concerns the finite scalar endpoint and
paid-query component, not a complete signed supplier invoice. Native/adjoint
address action, the global caller, scalar allowance, target admission, compiler,
precision, physical tape/storage and outer predicates were not replayed.
No uniform program, rounded multiplier or proof-kernel verification is supplied.
The five selected framework assumptions and selected kappa `781451/250000000`
remain unchanged. Independent human and formal proof-kernel review are unclaimed.

## Open next questions

1. Can one of the 14 new neutral rewrites expose a later paid saving? Generate
   one listed neutral word, enumerate its changed intervals and price the
   complete emitted bill. This matters because the theorem permits one rewrite
   only. No neutral-neighbor search or caller admission is supplied here.
2. Can a new native route or a moved correction frame rescue a rejected interval?
   Start with one recorded missing frame pair, construct its actual native
   action, and charge routes, targets, scalar fees and restoration. These costs
   and the complete physical caller remain unresolved.

## Credit

The new longer-contact result and certificate were produced by Nick Petalas.
Credit unpaidmoon for PR6290's question and fixed-frame definition, and
Ali Romman for PR5708's word, row-sensitive emitter and A2 construction,
following Dugongue, ai-nanachi and all retained native, controller, helper,
ordinary and stock sources. The standard A2 identity and subadditivity proof
are not claimed as new. No predecessor file or credit line is changed.
New work is Apache-2.0.
