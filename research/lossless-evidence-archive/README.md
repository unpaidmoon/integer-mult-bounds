# Standalone lossless evidence archive

A bounded, standard-library tool for retaining complete run trees as a standalone
content-addressed archive and restoring their exact paths, regular-file bytes,
empty directories and ordinary permission modes. Repeated file payloads share
one raw SHA-256 blob **inside the derivative archive**. Original evidence is
retained. No automatic post-run integration or original-file deletion is supplied.

This contribution packages the stable local revision 5 implementation and its
original finite controls, without changing their bytes. It adds a small explicit
replay adapter and self-contained source pins. It preserves the independent
oracle instead of substituting the archiver's own checks for restoration evidence.
It complements the frozen [PR6029](https://github.com/CrocSwap/integer-mult-bounds/pull/6029)
resource-control contribution; that predecessor package is unchanged.

## Evidence and claim boundary

The three small JSON records in [`evidence/`](evidence/) are exact retained local
reviews, copied with their original SHA-256 hashes in
[`RETAINED-SOURCES.json`](RETAINED-SOURCES.json). Their absolute/local references
are historical provenance; the referenced large payloads and complete outcome
check files are not included in this contribution.

The historical real archive review records 27 closed runs containing 1,179
regular files, 312 directories and 743,333,823 logical bytes. Its archive contains
263 files and 63,103,336 logical bytes, including 229 unique blobs and 32 metadata
files. The archive representation is smaller by 680,230,487 bytes, or
**91.5107675653%**. Exact paths, bytes, directory structure and ordinary modes were
restored into independent file identities. All originals remained present:
**workspace reclaimed bytes were zero**. Keeping the originals, archive,
restoration and identified execution records produced a retained total of
1,551,106,286 logical bytes in that historical review's scope.

That prior guarded invocation used 67.91564102901611 seconds child wall time,
16.47 rounded child CPU seconds and 35,284 KiB peak RSS. Its encompassing charge
was 68.02 seconds. Recorded complete payload reads were 4,584,304,464 bytes and
payload writes were 805,484,586 bytes; metadata IO was additional. Operation,
child and queue timings are nested and must not be added. The final residual
accounting receipt's own write tail remained excluded. These figures describe
the historical local invocation, not a new contribution replay or a portable
performance prediction.

The finite historical review records normal and Python `-O` success, each with
98 cases: 5 positive rows and 93 expected STOP rows. The positive fixture's archive
is larger than its tiny source because metadata and tools have overhead.
Earlier v2/v3/v4 local attempts remain STOP outcomes; the successful v5 review
does not rewrite them. Current contribution replay results must be established
separately by executing the commands below; a retained historical review does
not establish a new PASS.

The full historical payload is not vendored or replayed by `verify.py`. Its prior
full inventory/archive/restore checks occurred inside the authenticated guarded
parent invocation. The historical outcome review authenticated retained evidence
and metadata, without a second full payload replay. This is a finite software
and evidence-retention contribution. It establishes no scientific speedup,
multiplication theorem, κ improvement, automatic retention admission or universal
filesystem correctness.

## Replay the finite controls

Linux with `renameat2(RENAME_NOREPLACE)`, ordinary filesystem permissions, user
xattr support and Python 3.12 is the intended environment. No dependencies,
network, Git history, original local workspace or writable package source are
needed for direct replay. The adapter reads authenticated `.py` source directly
and never loads implementation bytecode caches. It creates a fresh private
external `/tmp/lossless-evidence-archive-*/controls` directory and leaves **all**
fixtures, partial artifacts, per-operation START/RESULT records, STOP outcomes
and the ordered `CASE-PREFIX.jsonl` in place on success or failure.

From the repository root:

```sh
python3.12 -B research/lossless-evidence-archive/verify.py
python3.12 -B -O research/lossless-evidence-archive/verify.py
```

The same commands work on an exported directory by replacing the script path
with its absolute path. A direct invocation can instead specify `--output
/absolute/private-parent/fresh-controls`; the parent must already be owned by
the caller with mode 0700, and the output must be absent and outside the package.
Every invocation needs a fresh output. Do not rerun into a failed attempt or
erase its evidence. START prints the retained output path before execution.

The adapter authenticates `archive.py`, `oracle.py`, `controls.py`, `USAGE.md` and
`COVERAGE-v5.json`, invokes the original finite controls, rechecks source identity,
and checks the exact 98-case coverage, 5/93 outcomes, original custody and final
journal agreement. Explicit checks remain enabled with `-O`. A 175-second alarm
and at most 1 GiB address space bound the process; registered commands use a
180-second timeout. The original controls enforce their 48 MiB aggregate fixture
bill before final report writing, maximum 96 negative cases, 128 prefix rows,
4,096 bytes per journal row and 1 MiB total journal. Final report/setup metadata
are additional retained bytes; the inner fixture census is not a complete process
IO or footprint measurement. No scientific modules or subprocesses are used.
Run the two modes serially and retain failed output for explicit review.

Registered metadata and replay commands, when this package is committed in the
upstream repository, are:

```sh
python3.12 -B scripts/research_package.py --package research/lossless-evidence-archive --check-only
python3.12 -B scripts/research_package.py --package research/lossless-evidence-archive
```

The generic launcher needs the repository and provenance Git history. Direct
standalone replay retains its separate Git-free contract.

## Archive a completed run tree

[`USAGE.md`](USAGE.md) is the byte-exact operational guide copied into every
archive. Create the independent inventory only after the selected run tree has
finished writing and every run receipt is closed. Hold any required writer
exclusion in the caller; this standalone tool does not establish application
closure or process lifecycle by itself.

All paths must be absolute, with ordinary existing parents and fresh external
attempt/destination directories. Destination parents must be caller-owned, mode
0700 and free of xattrs/ACLs. First create an independent inventory with
`oracle.py`; retain its returned digest externally. Then use `archive.py create`
with that expected inventory digest. Preserve the returned ROOT digest outside
the package and use it with `verify` and `restore`. A package-local digest cannot
prove historical completeness against an externally shortened package.

Creation/restoration publish a fresh sibling stage through Linux no-replace
rename. There is no overwrite or fallback publication path. Full restored bytes
are independently checked before publication. Only RESULT.json PASS completes
an operation; a completion marker or published destination alone cannot turn a
post-rename failure into success. Every failed stage and raw receipt remains.
Restoration requires no access to the historical source path. Never hardlink an
archive copy or infer that a reused blob name authenticates its bytes.

Supported restoration covers ordinary modes with owner-read access for files
and owner-read/search access for directories. Ownership, timestamps and inode
identities are recorded provenance, not promised restoration fields. Symlinks
including ancestors, special file types, special permission bits, owner-
inaccessible objects, xattrs/ACLs, invalid names, aliases, overlaps and unsupported
publication fail closed. The same-tree custody comparator excludes exactly
`counts.allocated_bytes`; every other logical, identity and mode field remains
in deep equality. Both full inventories and allocation observations remain
retained. Diagnostic allocated-block sums do not identify shared physical extents.

See [`COVERAGE-v5.json`](COVERAGE-v5.json) for concrete controls and unexecuted
boundaries, including privileged ACL/device setup, bind mounts, physical
power-loss durability and exhaustive mode enumeration. Injected failures test
software handling, not every filesystem or hardware fault.

## Open next questions

- **Can another independent environment restore a complete real archive?**
  This tests portability of the documented contract. Start with a newly closed,
  caller-authorized run tree and separately retained inventory/ROOT digests;
  retain complete restore evidence and account for all costs. It is blocked by
  authorization, storage/resource budget and availability of the full payload;
  this contribution intentionally includes only finite fixtures and small reviews.
- **Which unsupported filesystem features merit a separate contract?**
  ACLs, links and special files require explicit semantics before expansion.
  Start by specifying one feature and a tiny adversarial fixture. Any expansion
  requires implementation changes, independent review and new finite gates;
  passing the current controls does not admit that expansion.
- **Can retention safely follow an application's closed run?**
  Writer closure, exact selection, caller ownership and receipt finalization
  determine whether a complete tree has been selected. Start with a separate
  reviewed lifecycle contract. Automatic hooking remains outside this package
  and outside the current publication authorization; broader work stays paused.

## Attribution and license

Prepared for Chris R / Clear1nsight with substantial OpenAI Codex assistance.
Chris R / Clear1nsight's original local archive/oracle/control work, its independent source
and outcome reviews, and the frozen PR6029 predecessor retain their provenance
and contributor credit; see `RETAINED-SOURCES.json` for exact local origins.
Original repository research and tooling retain Douglas Colkitt and the credited
upstream contributors' attribution; no authorship of predecessor work is claimed.
The package is contributed under the repository's Apache-2.0 license. It does
not vendor another scientific package or alter upstream frozen artifacts.

## Recorded standalone release checks

The normal and deliberate optimized registered commands passed locally on Linux CPython 3.12.3. `VALIDATION.json` records their real finite results and source-conservation receipts. These are tool correctness checks, not a scientific runtime comparison. Parent staging failures and the repaired adapter read-only-copy failure remain retained externally. Final sealed-export and hosted checks have separate receipts; no future PASS is asserted here.
