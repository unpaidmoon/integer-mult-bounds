# Longer fixed-route G20 conjugations have no paid-moment gain

## Claim and boundary

Fix Ali Romman's final PR5708 `WORD.json.gz` and `PATHS.json`, pinned in
[SOURCES.json](SOURCES.json) at main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. Consider a single A2 conjugation
with at least four noncommuting contacts, with each correction kept at its
contact's original frame. Every such conjugation either encounters a missing
published route or has nonnegative paid-query moment change for every
`0 < t < 1`. The statement covers all contact lengths present on this word,
including its maximum of 33, rather than a chosen upper cutoff.
Among emitting candidates the minimum moment change is exactly zero for
every `0<t<1`. For example, zero-based scalar positions 9,399 and 10,815
bound a four-contact rewrite of `ADD(560,315)` with an unchanged histogram.

This is a finite certificate with a scoped algebraic sign proof. It extends
unpaidmoon's PR6290 question and fixed-contact-frame definition. PR6290's
one-to-three-contact result is cited, not re-established here. No assertion
about a changed route table, a sequence of rewrites or another word follows.

## Exact candidate class

Remove `Q` and `ZERO_Q` records from the pinned word to obtain 11,930 scalar
records on 685 roles. Write `G(a,b)` for `ADD(a,b)`, the characteristic-two
map `x_a <- x_a + x_b`. Choose any two occurrences of the same ordered
pair `(a,b)`, with positions `left < right`. Their frames may differ.

The open interval must contain no `INIT` or `ERASE` of `a` or `b`. A contact
is an ADD with destination `b` or source `a`. Every contact must have one
of the following forms, with the indicated correction:

| Contact | Constraint | Correction |
|---|---|---|
| `ADD(b,s)` | `s != a` | `ADD(a,s)` |
| `ADD(d,a)` | `d != b` | `ADD(d,b)` |

In particular, the reversed gate `ADD(b,a)` is outside this class. Require
at least four contacts. Delete the two outer gates and insert the correction
immediately after each contact, at that contact's original frame. All other
records retain their order and frame. These are the only changes allowed.

Completeness is finite and explicit. Group every ADD position by its ordered
operand pair, visit every ordered choice of two increasing positions in each
group, inspect every intervening record, and retain exactly the intervals
satisfying the conditions above. There is no contact cutoff or node budget.
The resulting domain has exactly 1,503 intervals. The certificate lists every
interval's endpoints, operands, contact count and outcome.

## Scalar endpoint

For each valid contact `C`, direct multiplication of elementary matrices gives
`G C G = C R`, where `R` is the indicated correction. The correction commutes
with its contact. Every noncontact commutes with `G`, including an erase or
initialization of a different role. Since `G^2 = I`, conjugation distributes
over the entire interval. Thus deleting the two outer gates and replacing
every contact by `C R` preserves the scalar map for any contact count.

The verifier also checks the complete endpoint separately for every one of
the 1,503 changed words, including those that later fail route emission.
Each row is a 685-bit coefficient mask, initially `e_i`. ADD is exact XOR;
only owned roles may be erased, and INIT requires their whole row to be zero.
The expected final row is zero on owned roles. On other roles it is `e_i`,
with the additional term `e_(i-111)` for `111 <= i < 222`.
This tests every independent scalar input column, not a sample of payloads.
The native address action remains a cited predecessor premise.

## Route contract and certificate

Use precisely the source emitter's rules. An ADD with zero source row is
omitted. Otherwise move its destination and source to its frame, in that
order. A published one-edge route incurs its rank once when the moved row
is nonzero, and zero when that row is zero. A missing edge rejects emission
even for a zero row. An uninitialized owned zero row may be initialized.
At the end return every public role to its final frame and require every
owned role to be zero. Owned cleanup has the source's zero-query convention.

The unchanged word provides the necessary reference histogram
`{1:1281, 2:1338, 3:58, 4:57, 5:102, 6:10}`. This reference is not a new
predecessor audit or a claim of full supplier admission. Every changed word
that emits receives a freshly reconstructed complete paid-query histogram.
The signed difference is new minus reference.

Exactly 1,450 intervals encounter a missing route. For each, the certificate
records the first required ordered frame pair absent from the table. These
are rejection witnesses relative to this table, not proofs that the native
geometry could never supply another route. The other 53 intervals emit.
Their entire signed histogram classification is:

| New minus reference | Count | Sign for `0 < t < 1` |
|---|---:|---|
| `2H1 - H2` | 15 | Strict loss |
| `3H1 + 2H2` | 10 | Strict loss |
| `2H2 - H4` | 5 | Strict loss |
| `2H1 + H2 + H3` | 4 | Strict loss |
| `H1 + 3H2` | 2 | Strict loss |
| `H1 + 2H2 - H5` | 2 | Strict loss |
| `H1 + H3 - H4` | 1 | Strict loss |
| Zero | 14 | Neutral |

Here `Hr` contributes `r^t`. All coefficients in three of the nonzero
shapes are positive, so their moment changes are positive. In each of the
other four shapes, one negative job of rank `R` is replaced by at least
two positive jobs whose ranks sum to `R`. For positive `a,b` and `0<t<1`,
`(a+b)^t < a^t+b^t`. For example, divide by `(a+b)^t` and use
`u^t > u` for `0<u<1` on `u=a/(a+b)` and `1-u`.
Iteration proves strict positivity for any such split. This covers the
whole open exponent interval without floating-point sampling or root search.

The complete canonical candidate certificate has SHA256
`577323306b7b7f2547ca660e6bbef1badc953959e2f7cd20de9e1f002e254889`.
Canonical bytes are UTF-8 from `json.dumps(result, sort_keys=True,
separators=(",", ":"))`. The optional generated receipt includes that whole
certificate and hashes of all package files and live inputs.

## Controls and limits

The verifier checks all 256 four-contact words over the two allowed contact
orientations on four roles. It checks their complete input-column endpoints
and rejects deletion of the first correction in each. Reversed contacts,
erased operands and short intervals are explicit exclusion controls.
The exact sign rule rejects the profitable shape `H1 - 2H2 + H3`, whose
negative sign follows from strict concavity. Routing controls distinguish
successful charging, a missing edge and a zero source.
The proof checks use explicit exceptions and remain active under `-O`.

This result concerns one rewrite of the final word and the paid-query part
of its bill. It provides no new productive target, ordinary BIT saving or
whole multiplication exponent. No global caller, adjoint/native address
replay, finite compiler, scalar allowance, physical storage, precision,
outer ledger, uniform program or rounded multiplier is certified here.
The five selected framework assumptions remain. Additional routes, correction
coframes and sequences through neutral words are not excluded.

## Implementation constraints

The verifier uses structured iteration without recursion. Its inputs are
hash-pinned before decompression and parsing. Each compressed input is below
two million bytes, the scalar dimensions are checked as 11,930 by 685, the
candidate list has a fail-closed capacity of 4,096, and XOR rows have at most
685 bits. Every pair search has the finite upper bound `C(11930,2)`; every
interval and replay has the corresponding fixed record bound. One changed
word is live at a time, with no more than `11930-2+33` records on this source.
No input limit truncates the claimed domain.

Power-of-ten rule 3 deviation: CPython and its standard JSON and gzip readers
allocate dynamically. This standalone finite checker cannot preallocate those
runtime internals. The exact authenticated inputs, checked dimensions and
candidate capacity bound its live data; the normal and optimized complete
checks exercise those bounds. A future unpinned input interface would require
bounded streaming parsers before relaxing this contract. All functions fit
within 60 physical lines. Warning-strict normal and optimized execution are
the available diagnostics; no static-analysis dependency is introduced.

## Credit

The new longer-contact result and standalone certificate were produced by
Nick Petalas. Unpaidmoon posed the four-or-more-contact question in PR6290.
Ali Romman supplied PR5708's word, emitter and scalar A2 construction, following
Dugongue, ai-nanachi and the native/controller/helper/ordinary/stock lineage
retained in that package. The A2 identities and strict subadditivity are
classical and are not claimed as new. No predecessor file or credit is changed.
