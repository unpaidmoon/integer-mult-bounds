# Validation and acceptance boundary

Windows11 build26300, physical CPython3.12.11 AMD64, standard library. Native source: PR5721 head916cf98d5d8a448ec6515d211c6fe980a46a1694; retained source SHA2569e3dfa9b8865d355c03529c2fe92d90e1c3b12a2adb8d505146d16757b2cba50. Byte comparison to the fetched original Git blob was performed when copying; frozen source was not edited.

## Native evidence

The first complete normal run and one optimized (-O) native repeat passed all three cases and eight exact-reason receipt mutations; the normal receipt is preserved. CERTIFICATE.json retains the environment, exact process/image sets, native fields, report status, sentinel outcomes, signaled gate handles, outer counts and pre-teardown observations.

- denied2: one gate, requested-payload OSError errno12/winerror1816; no sentinel; retained gate handle already signaled before probe exit/outer teardown.
- allowed3: same requested payload launched, exact sentinel, exit0, gate signaled.
- direct2: same payload launched without gate, exact sentinel, exit0.
- All three controller-created probe identities match the recorded runtime identity; the outer job is empty after probe exit, and no rescue was used.

The observed entry PID set contains the physical Python probe and one exact C:/Windows/System32/conhost.exe auxiliary. The gated snapshot adds exactly the retained gate PID. Raw accounting counts2/3 are kept rather than misreported as1/2. This is host-specific observation, not a general theorem about console-host quota accounting.

ATTEMPT.json preserves six failed or diagnostic attempts in order. The PATH launcher first caused denial before payload launch; that is rejected evidence. Subsequent diagnostics distinguished immediate from explicitly named outer-job accounting, selected the physical interpreter, and identified the console-host auxiliary. The original literal count/PID premise continued to fail until publicly refined. Process limits2/3 and payload were unchanged. No host policy was altered, and no failed attempt was relabeled as a passing payload audit.

## Portable and transport checks

The registered normal and optimized commands passed, validating the retained receipt, source hashes and eight mutations. The first metadata invocation rejected a missing exact Open next questions heading; the heading was corrected before the passing run. They launch no native processes. They establish internal evidence consistency, not a second native host or an independent reproduction of observations.

The package uses an explicit retained-source ORIGIN.json format. Standard SOURCES.json history covers only base provenance (catalogue/selected record); any standard source-history PASS is limited to those declared base rows. It does not authenticate pending5721 ancestry. That head is deliberately not merged here. Original origin comparison is documented separately in README.

Base a615e535914b130cdccf6b0eff3c3861d4a44f1c; submission refresh2485805a6d47f36ea83ddde6327d453ac82d44dc. Relevant guidance, selected6030 and priorityrevision8 are unchanged. Source5721 remains draft/open at the pinned head. Final remote overlap covered308 open PRs at04:36UTC and5979 Discussion records at04:38UTC, plus all base HEAD notes; no competing policy audit identified. Bounded coverage is not proof of novelty.

Source review by a separate Codex agent and root review are AI checks, not independent human or proof-kernel acceptance. Shared-reader retry, other policies/hosts, abrupt parent/owner death, POSIX/native CI, supplier admission and selected mathematical replay are outside scope.
