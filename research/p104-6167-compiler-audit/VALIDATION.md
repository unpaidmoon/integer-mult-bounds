# Validation record

Environment: Linux, CPython 3.12.14, standard library only. Exact base:
`2485805a6d47f36ea83ddde6327d453ac82d44dc`.

Completed during development:

- Selected metadata orientation: `python3 -B scripts/research_selected_baseline.py`
  passed `PASS_RESEARCH_BASELINE_BINDINGS_ONLY`. This was not a selected cold replay.
- Direct normal scientific replay passed: 4,100 arithmetic cases, 18 semantic
  controls, four parser/arithmetic rejections, power boundary 1013, j=47005.
- Registered normal and optimized scientific commands passed with the same
  complete recomputed receipt, before adding the file-boundary commands.
- Direct file-boundary test passed: one Git-free positive, seven actual
  source-byte corruptions and one output-receipt corruption.
- The five consumed files attributed to PR6167/PR6214/PR6109 matched their
  original Git-head blobs byte for byte; all three heads are ancestors of base.
- Metadata and source-pin check passed.

One initial control expected the equal-mass paid mutation to reach the printed
interval comparison. It correctly failed earlier at the actual moment-reserve
condition. The test was corrected to require that precise reason and an exact
lower bound proving the exhausted reserve. No scientific condition was weakened.

Publication-stage registered replay, committed-byte/ancestry check, official
export and remote tree confirmation are recorded below when executed. No
selected cold replay, full native/caller rerun, hosted CI, human review or
proof-kernel acceptance is claimed.

The complete four-command registered replay subsequently passed in normal and
optimized modes: two scientific replays and two file-boundary replays. Each
scientific run verified the same exact receipt; each boundary run passed one
Git-free positive and rejected seven corrupted source files plus one corrupted
receipt. AST inspection found only standard-library imports, no float literals
and no assertion statements in the scientific verifier.

Publication verification:

- `python3 -B scripts/check_research_commit.py --package research/p104-6167-compiler-audit --check-source-history`
  passed for all 15 package/input files and the base-history pin.
- Official export and integrity check passed for those 15 files. A separate
  export (16 files including its manifest), marked read-only, passed scientific
  and boundary commands in both normal and optimized modes with empty PATH and
  no Git repository. Every exported byte was unchanged after execution.
- The final code edit makes all text I/O explicitly UTF-8; the full registered
  replay passed again with the same mathematical receipt. No platform other
  than Linux/CPython 3.12.14 was tested.
- Canonical main was fetched again and remained
  `2485805a6d47f36ea83ddde6327d453ac82d44dc`; all eight checked guidance/selected
  paths were unchanged. Refreshed live overlap retained the same scoped handoff.

The public commit and complete root-tree equality are confirmed separately in
its PR handoff, after publication; this file does not predict a remote commit
hash. Hosted CI was not launched or claimed. The scientific source pins and
selected record remain unchanged.
