# Pending Windows adapter: enclosing process-limit audit

This package answers one explicit unrun handoff in [PR5721](https://github.com/CrocSwap/integer-mult-bounds/pull/5721), exact head `916cf98d5d8a448ec6515d211c6fe980a46a1694`. The adapter is **pending and absent from this main base**. This is a scoped lifecycle audit, not production adoption or a multiplication result.

## Contract and discriminator

An external controller creates a new Job Object with active-process and kill-on-close limits. It creates a probe suspended, assigns it before resuming, and never joins that new job itself. The frozen adapter starts a gate; that gate then attempts the same Python payload, which writes an exclusive sentinel and exits.

- On the measured host, limit2 permits the probe and gate Python processes but denies the payload. A separately identified System32/conhost.exe auxiliary is included in raw job accounting; the checked PID sets retain it explicitly. Require a payload-stage native error report, an exception preserving its native fields, exactly one gate launch, no sentinel, and a retained gate process handle already signaled before outer-job teardown.
- Limit3 permits the same probe, gate and payload Python processes; require successful launch, exit0 and the exact sentinel.
- Direct-Popen under limit2 permits probe+payload. This positive mutation distinguishes the adapter's extra gate from a payload/environment failure.

Assignment/setup rejection, timeout or rescue is not a passing denial. The observer forwards the frozen implementation, and a retained native handle avoids PID-reuse ambiguity. Checks occur before outer teardown, so kill-on-close cannot manufacture passing cleanup evidence. No breakaway flags or host-job policy changes are used.

The initial PATH launcher attempt failed before the payload and was rejected. A physical-interpreter attempt exposed the console-host auxiliary and correctly failed the original aggregate-count assertion. These attempts are retained; the final topology checks use the named outer job and exact PID/image sets. Limits and payload stay unchanged. No general console-host quota-exemption theorem is asserted. The final denial classification is the observed OSError errno12/winerror1816.

The Win64 structure sizes and offsets are checked before process creation. API rationale: Microsoft [nested jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs) and [basic job limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information).

## Evidence and reproduction

Native execution and receipt validation are recorded in VALIDATION.md. Python3.12, Windows64-bit and writable temporary storage are required for native evidence. A non-Windows receipt check must not be reported as a native rerun.

```sh
python3.12 scripts/research_package.py --package research/windows-job-policy-audit
# Native Windows rerun, separately from portable retained-receipt checks:
/path/to/physical/python.exe -B research/windows-job-policy-audit/verify.py
/path/to/physical/python.exe -B -O research/windows-job-policy-audit/verify.py
```

Use the actual CPython executable for native runs, not a PATH forwarding launcher. The saved receipt records the exact executable and images; the observed auxiliary topology is a host-specific acceptance premise.

The retained adapter is byte-identical to its origin. ORIGIN.json records the original path, head, Git blob and SHA256. The verifier authenticates the retained bytes before loading them. SOURCES.json separately pins the base catalogue and selected record. Pending source history is deliberately not merged into this contribution: integrating a descendant can otherwise change the source PR's GitHub state. This is a retained-source format, not a claim that the original head is ancestral to publication.

For independent origin comparison, fetch the original head explicitly, then compare the file bytes (optional for native replay of the already authenticated retained copy):

```sh
git fetch https://github.com/CrocSwap/integer-mult-bounds.git 916cf98d5d8a448ec6515d211c6fe980a46a1694
git rev-parse 916cf98d5d8a448ec6515d211c6fe980a46a1694:scripts/research_windows_git.py
```

Expected blob: `54e33b7556364fa531e49b2d33d4d10d6f38fa59`. Original-source history and external origin authenticity remain separately inspectable; replay uses no network.

## Scope, overlap and open next questions

Base a615e535914b130cdccf6b0eff3c3861d4a44f1c; priority revision8, selected6030 unchanged. The portable-replay card is changed from canonical payload comparison to the source's explicit restrictive-job handoff. Initial overlap covered309 open PRs,5978 Discussion records and all8720 HEAD notes at04:24–04:25UTC on2026-10-30, finding the predecessor and unrun obligation. This bounded search does not certify novelty. Canonical coordination: [claim/finding](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19285145).

## Open next questions

Shared-reader retry behavior, other policies/platforms, hard owner death during setup, abrupt parent termination, hostedCI and independent human review remain unclaimed. TASK.json gives the first steps and blockers. The status channel remains a trusted local channel, not a security boundary.

## Credit

AAAmirinu with substantial OpenAI Codex assistance, including separate AI source review. Credit josecarlosgonzalezroque-design for PR5721 integration; Mihir Srivastava for PR5463/5524; ywz65 for gated ownership and retained native-handle observations; Brian/JoyboyBrian, Nick Petalas, Arham Tahir, Woklerx, yssite, Paul Romeo, Tekalign, Douglas Colkitt and the retained source/fixture lineage. The retained source header is unchanged. Apache-2.0.
