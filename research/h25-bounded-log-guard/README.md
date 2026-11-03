# Bounded retained-log guard

This package exports the exact tested H25 retained-log runner and its original
finite controls, with a small standalone replay adapter. The contribution is
bounded-memory inspection of retained regular stdout/stderr files: SHA256 reads
use 64 KiB blocks, check sizes before hashing and again afterward, and preserve
a primary STOP reason. A log changed during hashing cannot support PASS.
Usage diagnostics have a separate 16 KiB limit. The runner and fixture code are
byte-for-byte copies, rather than a new guard implementation.

The historical executed review in `historical/REVIEW.json` records eight process
controls and eight real-file controls, with fixtures through 32 MiB. Its largest
tracemalloc peak was 134,752 bytes; its recorded lifetime RSS high-water increment
was zero. These are historical finite observations, not a benchmark, a speedup,
or a claim about an entire verifier. Five expected STOP process attempts remain
part of that evidence. `historical/PROPOSAL.json`, `INTERFACE.txt` and
`SOURCE-MANIFEST.json` retain their earlier source-review-only labels verbatim;
the later executed review supplies the historical execution result.

Publication replay is recorded separately by the contributor after executing
this package. A future PASS is not supplied by this source export. There is no
numerical admission, native compilation, new κ, complete multiplication theorem,
or resumption of the paused broader six-area investigation.

## Reproduction

Use Linux with CPython 3.12, `/proc`, `flock`, GNU `/usr/bin/time`,
`/usr/bin/python3.12`, and `/usr/lib/python3.12/fractions.py`. The exact runner
retains those fixed system paths and its original `run_guarded.py STAGE JOB
LABEL` CLI. The adapter uses only the standard library and launches only the
unchanged finite fixture driver. No network or third-party installation is
needed.

From the repository root:

```sh
python3.12 -B research/h25-bounded-log-guard/verify.py
python3.12 -B -O research/h25-bounded-log-guard/verify.py
python3.12 -B scripts/research_package.py --package research/h25-bounded-log-guard --check-only
python3.12 -B scripts/research_package.py --package research/h25-bounded-log-guard
```

Every direct invocation creates a unique external `/tmp/h25-bounded-log-guard-*`
workspace and prints its path before executing controls. To choose a retained
location, use `--work-root /an/external/new-directory`. It must not exist and must
be outside the committed package. Committed package files can be read-only.
Neither the adapter nor the runner writes runtime files inside this package.
Success retains `RESULT.json`; failures retain `FAILURE.json` when execution has
entered the control loop, alongside all produced raw files and receipts. A
failure during setup can leave a partial external workspace. No automatic retry
or deletion occurs.

The adapter first authenticates `MANIFEST.json` and byte equality against
`PROVENANCE.json`, then copies the runner and frozen stage into that fresh
workspace. It regenerates only the runtime stage inventory and JOBS metadata;
source code remains exact. Normal and optimized invocations deliberately set
the finite child jobs' `optimized` flag to match the adapter. The original JOBS,
STAGE and CONTROL-BILL are retained untouched in `frozen-stage/`.

The eight original process cases are normal output, binary output, stderr,
nonzero exit, live oversized stdout, fast oversized stdout, fast oversized
stderr, and real-file finalization. The files case invokes the unchanged eight
real-file controls: empty, binary, exact 2 MiB boundary, 4 MiB and 32 MiB retained
files, deterministic final growth, deterministic post-hash cap growth, and STOP
precedence. The original file controls enforce traced hashing allocation at most
512 KiB and lifetime RSS increment at most 8 MiB. The adapter independently
checks raw hashes/counts, fixed fixture bytes, expected PASS/STOP classifications,
stage conservation and ledger continuity. Expected adverse STOP receipts must
pass those checks before the next job runs. A shell exit of 1 alone proves
nothing about a control.

Each registered command has a 180-second limit; the adapter allows 170 seconds
for the sequential subprocess loop. The original runner retains 180 seconds per
attempt, 1 GiB sampled process-group RSS, 2 MiB per ordinary output channel, and
its 600/2400-second aggregate phase choices. This replay initializes a fresh
600-second phase, with eight finite jobs and less than 44 MiB of real-file
fixtures. Mutable runtime results are external and excluded from the shipped
manifest. The manifest covers immutable shipped bytes except its own recursive
entry; it checks package consistency, not independent authenticity or arbitrary
transitive system dependencies.

## Limits

Linux `/proc` group RSS is sampled, and RSS controls use process lifetime
high-water changes, rather than continuous memory traces. Finite controls do
not establish behavior for arbitrary hostile filesystems, unlimited output,
or every race. Only retained regular stdout/stderr paths are admitted. Symlinks,
unlinks and open/read errors fail closed, preserving an unclosed attempt that
requires reconciliation before another attempt. This package preserves those
failure semantics and does not add recovery for them.

The source inventory still materializes source files and stage/receipt metadata.
The bounded-memory claim concerns stdout/stderr and usage diagnostics. It does
not cover arbitrary source, manifest, receipt or historical metadata sizes.
Small files read by the adapter are part of this fixed package's finite scope.
The adapter's SHA256 comparison does not independently prove correctness of the
runner it authenticates.

Process-group cleanup is the original contract. A descendant that creates a
new group/session can escape it. An external timeout that terminates the adapter
or runner is not proof of descendant cleanup or successful completion; inspect
the retained workspace before retrying. The adapter adds no general process-tree
containment. It never interprets cleanup as evidence that unfinished work passed.

`runner_wall_seconds` includes source/log postprocessing, but ends before its
receipt construction, writing and printing. Runner-ledger sums exclude this tail;
publication accounting must separately charge the complete outer invocation and
its own metering tail as available, without inventing unmeasured costs. Historical
review costs remain historical. Exact old absolute paths and hashes in the
retained review identify old local evidence; those raw runtime trees are not
shipped or required for a cold replay. Fresh outputs provide current evidence.

## Open next questions

Structured next questions are in `TASK.json`.

* Can retained-log path drift be given an explicit bounded failure receipt?
  This would make unclosed attempts easier to reconcile. First specify and
  source-review a separate unlink/symlink/open-error control set. It is blocked
  on an explicitly authorized follow-up; this package preserves the old runner.
* Can process lifetime containment cover descendants that detach from the group?
  This matters for hostile subprocesses. First compare an explicit Linux
  cgroup-based lifetime contract with the existing session cleanup boundary.
  It requires a separately authorized implementation and available cgroup
  permissions; the current finite controls do not answer it.

## Sources and credit

The exact external source export and copy-equality hashes are recorded in
`PROVENANCE.json`. `SOURCES.json` binds upstream task provenance at the declared
canonical base. Local predecessor bytes do not have fabricated upstream Git blob
IDs: their self-contained copies are checked directly against recorded SHA256
pins. Frozen upstream `research/h25-bookkeeping` is unchanged.

Predecessor: [H25 bookkeeping contribution, PR6029](https://github.com/CrocSwap/integer-mult-bounds/pull/6029).
Retain that contribution's attribution and the local H25 runner/control authors'
credit. This package is a focused portable export and replay adapter for the
later log-handling checkpoint; it does not claim new authorship of predecessor
runner structure, controls, resource/receipt semantics, or old review evidence.
Prepared for Chris R / Clear1nsight with substantial OpenAI Codex assistance.
New contribution and retained H25 material are offered under Apache-2.0, the
repository license. No third-party mathematical or native code is added.

## Recorded standalone release checks

The normal and deliberate optimized registered commands passed locally on Linux CPython 3.12.3. `VALIDATION.json` records their real finite results and source-conservation receipts. These are tool correctness checks, not a scientific runtime comparison. Parent staging failures and the repaired adapter read-only-copy failure remain retained externally. Final sealed-export and hosted checks have separate receipts; no future PASS is asserted here.
