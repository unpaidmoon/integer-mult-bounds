# Stop encoded Machin setup at its first zero floor term

**Scoped implementation/resource proof with finite physical corroboration.**
The actual PR3709 Machin setup can stop before the first denominator larger
than its fixed-point unit. At Q=16 this removes 39 of 48 quotient divisions,
including the new comparison and cleanup costs in its physical trace.
No new kappa, supplier admission or selected-frontier change is claimed.

[PROOF.md](PROOF.md) proves that the new interval encloses the real value,
lies inside the old interval, and saves divisions at every source precision
Q>=16. It preserves the source's sufficient twiddle error contract. Universal
bit equality, a whole-caller cost improvement and a wall-time gain are unclaimed.

```diff
 for each encoded arctangent term
   form its denominator
+  if denominator > unit, close the iterator and stop
   divide, update the signed interval, advance
 retain the original one-unit alternating-tail padding
```

## Evidence

The generated verifier receipt gives 512 exact rational interval cases,
72 strict/equality boundary cases, and 497 source precision counts. Four
physical pi fixtures at Q=16,21,32,64 use respectively 9,10,13,22 divisions
instead of 48,58,80,144. Every one reduces actual tape reads, writes and unit
head moves. Borrowed inputs are unchanged and all scratch leases return.
The Q=16 trace pays eleven new stopping comparisons, has 123233 reads,
20354 writes and 97974 moves, and uses peak sixteen leases.

Ten complete twiddle packets, in both directions at the five specified
precision/stage pairs, remain byte-identical to the original packets.
These are checks of the new adapter's finite compatibility, not a fresh
audit of the predecessor's mathematical result. Five controls expose loss
of stopping, stopping at equality, missing tail padding, invalid denominator
and an injected division failure. Every run authenticates live inputs and
prints a receipt bound to all package-file hashes; no receipt is handwritten.

The physical comparison covers pi_interval and consumption of its returned
endpoints. Fixture serialization, fixed-pool construction and final marker
erasure are outside both counters. Every new operation during the invocation
is counted. The comparisons field counts the new stopping site. The full
Taylor consumer runs in packet checks but is outside the Machin counters.
There is no timing percentage or global paid-invoice claim.

## Reproduce

From the worktree root, using CPython 3.12 and only its standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/encoded-machin-tail/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/encoded-machin-tail/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/encoded-machin-tail
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/encoded-machin-tail --check-source-history
```

Another CPython 3.12 path can replace the absolute interpreter path. The
expected scientific marker is `PASS_ENCODED_MACHIN_TAIL`; both registered
commands run all checks. The publication check requires a committed package
and full history. Set TMPDIR to an existing external scratch directory to
place the inherited temporary source cohorts there. Nothing is written into
the package. Hosted CI is recorded separately in the PR body.

## Scope and provenance

Canonical base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
[TASK.json](TASK.json) marks the card scope changed from wall-time replay
optimization to an originally posed precision/tape resource improvement.
The [advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19291975)
states that a wall-time gain is not predicted. [SOURCES.json](SOURCES.json)
pins the four live files and the historical catalogue/selected record.
No frozen file or shared production code changes; this is an opt-in adapter.

Whole product/convolution installation, production-sized GL64/O73 execution,
physical whole-caller timing, selected cold replay, Lean and all-size theorem
admission are unrun. The five selected framework assumptions remain. This
is neither a search-failure claim nor a complete multiplication theorem.
Independent human and formal proof-kernel review are unclaimed.

## Open next questions

Can the exact stopping adapter be installed in one complete physical caller
with a favorable whole-call cost? Preserve its precision, packets and
restoration boundary, and measure every preparation and execution stage.
The local operation reduction alone does not quantify that whole-call gain.
Production-scale execution and the full caller bill are the blockers.
[TASK.json](TASK.json) records the same bounded question. No follow-up is reserved.

## Credit

This contribution was produced by Nick Petalas. The signed summation and
physical tape consumer are Jose Manuel / jmbarrancoml's PR3709 work; the new
adapter retains their arithmetic and adds the stopping comparison and explicit
iterator closure. Credit Dugongue's PR4554 for the existing magnitude-based
Machin truncation precedent, Mason Hale's PR2313 interval reference, PR3640's
Fourier/tape lineage, Dugongue's PR2790 arithmetic/ABI precedent, and the
Nussbaumer/Quandalle and Harvey/van der Hoeven lineage retained by those sources.
The classical series, Machin identity and directed interval methods are not
claimed as new. Every predecessor file and notice is unchanged. New work
is Apache-2.0.
