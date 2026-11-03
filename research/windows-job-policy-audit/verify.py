#!/usr/bin/env python3
"""Bounded native audit of the unchanged, pending PR5721 checked_pipe adapter.

The controller never joins the new test job. A suspended probe joins first,
then launches the gate and payload. This is not a shared-reader integration
test. Prepared with substantial OpenAI Codex assistance; Apache-2.0.
"""
import argparse
import copy
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import types
import uuid

HERE = Path(__file__).resolve().parent
MODES = {"denied2": 2, "allowed3": 3, "direct2": 2}
SOURCE_COMMIT = "916cf98d5d8a448ec6515d211c6fe980a46a1694"
CONHOST_IMAGE = r"C:\Windows\System32\conhost.exe"
SENTINEL = b"requested payload ran\n"
PAYLOAD = ("import sys; from pathlib import Path; "
           "p=Path(sys.argv[1]); "
           "f=p.open('xb'); f.write(b'requested payload ran\\n'); f.close()")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate():
    origin = json.loads((HERE / "ORIGIN.json").read_text(encoding="utf-8"))
    require(origin["commit"] == SOURCE_COMMIT, "unexpected source commit")
    require(origin["path"] == "scripts/research_windows_git.py", "unexpected source path")
    require(origin["retained_path"] == "vendor/research_windows_git.py", "unexpected retained path")
    source = (HERE / origin["retained_path"]).read_bytes()
    require(hashlib.sha256(source).hexdigest() == origin["sha256"], "source SHA256 mismatch")
    blob = b"blob " + str(len(source)).encode("ascii") + b"\0" + source
    require(hashlib.sha1(blob).hexdigest() == origin["git_blob"], "source Git blob mismatch")
    return origin, source


def load_source():
    origin, source = authenticate()
    module = types.ModuleType("retained_windows_git")
    module.__file__ = str(HERE / origin["retained_path"])
    exec(compile(source, module.__file__, "exec", optimize=0), module.__dict__)
    return module


class BasicLimits(ctypes.Structure):
    _fields_ = [("ProcessTime", ctypes.c_int64), ("JobTime", ctypes.c_int64),
                ("Flags", wintypes.DWORD), ("MinWorkingSet", ctypes.c_size_t),
                ("MaxWorkingSet", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t), ("Priority", wintypes.DWORD),
                ("Scheduling", wintypes.DWORD)]


class IOCounts(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint64) for name in
                ("ReadOps", "WriteOps", "OtherOps", "ReadBytes", "WriteBytes", "OtherBytes")]


class ExtendedLimits(ctypes.Structure):
    _fields_ = [("Basic", BasicLimits), ("IO", IOCounts),
                ("ProcessMemory", ctypes.c_size_t), ("JobMemory", ctypes.c_size_t),
                ("PeakProcessMemory", ctypes.c_size_t), ("PeakJobMemory", ctypes.c_size_t)]


class Accounting(ctypes.Structure):
    _fields_ = [(name, ctypes.c_int64) for name in
                ("UserTime", "KernelTime", "PeriodUserTime", "PeriodKernelTime")] + [
                (name, wintypes.DWORD) for name in
                ("PageFaults", "TotalProcesses", "ActiveProcesses", "TerminatedProcesses")]


class StartupInfo(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("lpReserved", wintypes.LPWSTR),
                ("lpDesktop", wintypes.LPWSTR), ("lpTitle", wintypes.LPWSTR)] + [
                (name, wintypes.DWORD) for name in
                ("dwX", "dwY", "dwXSize", "dwYSize", "dwXCountChars", "dwYCountChars",
                 "dwFillAttribute", "dwFlags")] + [
                ("wShowWindow", wintypes.WORD), ("cbReserved2", wintypes.WORD),
                ("lpReserved2", ctypes.c_void_p), ("hStdInput", wintypes.HANDLE),
                ("hStdOutput", wintypes.HANDLE), ("hStdError", wintypes.HANDLE)]


class ProcessInformation(ctypes.Structure):
    _fields_ = [("hProcess", wintypes.HANDLE), ("hThread", wintypes.HANDLE),
                ("process_id", wintypes.DWORD), ("thread_id", wintypes.DWORD)]


class ProcessIds(ctypes.Structure):
    _fields_ = [("assigned", wintypes.DWORD), ("listed", wintypes.DWORD),
                ("ids", ctypes.c_size_t * 16)]


class Native:
    def __init__(self):
        require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8,
                "native audit requires 64-bit Windows")
        require((ctypes.sizeof(BasicLimits), BasicLimits.Flags.offset,
                 BasicLimits.ActiveProcessLimit.offset, ctypes.sizeof(ExtendedLimits),
                 ctypes.sizeof(Accounting), ctypes.sizeof(StartupInfo)) ==
                (64, 16, 40, 144, 48, 104), "unexpected native structure layout")
        api = ctypes.WinDLL("kernel32", use_last_error=True)
        h, d, b, p = wintypes.HANDLE, wintypes.DWORD, wintypes.BOOL, ctypes.c_void_p
        signatures = {
            "CreateJobObjectW": (h, p, wintypes.LPCWSTR),
            "OpenJobObjectW": (h, d, b, wintypes.LPCWSTR),
            "SetInformationJobObject": (b, h, ctypes.c_int, p, d),
            "AssignProcessToJobObject": (b, h, h),
            "TerminateJobObject": (b, h, wintypes.UINT),
            "TerminateProcess": (b, h, wintypes.UINT),
            "QueryInformationJobObject": (b, h, ctypes.c_int, p, d, p),
            "CreateProcessW": (b, wintypes.LPCWSTR, wintypes.LPWSTR, p, p, b,
                               d, p, wintypes.LPCWSTR, p, p),
            "ResumeThread": (d, h), "WaitForSingleObject": (d, h, d),
            "GetExitCodeProcess": (b, h, p), "CloseHandle": (b, h),
            "GetCurrentProcess": (h,),
            "OpenProcess": (h, d, b, d),
            "QueryFullProcessImageNameW": (b, h, d, wintypes.LPWSTR, p),
            "DuplicateHandle": (b, h, h, h, p, d, b, d),
        }
        for name, signature in signatures.items():
            function = getattr(api, name)
            function.restype, function.argtypes = signature[0], signature[1:]
            setattr(self, name, function)

    @staticmethod
    def checked(result):
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
        return result

    def duplicate(self, handle):
        duplicate = wintypes.HANDLE()
        owner = self.GetCurrentProcess()
        self.checked(self.DuplicateHandle(owner, handle, owner, ctypes.byref(duplicate),
                                          0, False, 2))
        return duplicate.value

    def process_identity(self, pid):
        handle = self.checked(self.OpenProcess(0x1000, False, pid))
        try:
            capacity = wintypes.DWORD(32768)
            buffer = ctypes.create_unicode_buffer(capacity.value)
            self.checked(self.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(capacity)))
            return {"pid": pid, "image": buffer.value}
        finally:
            self.checked(self.CloseHandle(handle))

    def job_pids(self, job):
        state = ProcessIds()
        self.checked(self.QueryInformationJobObject(job, 3, ctypes.byref(state), ctypes.sizeof(state), None))
        require(state.listed <= 16 and state.assigned == state.listed, "job PID list exceeded bounded buffer")
        return sorted(state.ids[:state.listed])


def exception_record(error):
    return {"type": type(error).__name__, **{name: getattr(error, name) for name in
            ("errno", "winerror", "strerror", "filename", "filename2")}}


def validate_case(record, mode):
    require(record["mode"] == mode and record["outer_limit"] == MODES[mode], "wrong case policy")
    require(record["observer_cleanup_used"] is False, "observer cleanup manufactured exit")
    gated = mode != "direct2"
    require(record["gate_count"] == int(gated), "wrong gate count")
    require(record["gate_wait_results"] == ([0] if gated else []), "gate was not already signaled")
    identities = record["outer_entry_identities"]
    probe_id = record["probe_identity"]["pid"]
    helpers = [item for item in identities if item["pid"] != probe_id]
    require(len(identities) == 2 and len(helpers) == 1
            and helpers[0]["image"] == CONHOST_IMAGE
            and record["probe_identity"] in identities
            and sorted(item["pid"] for item in identities) == record["probe_outer_pids_at_entry"],
            "outer job is not the probe plus observed System32 console host")
    require(record["gate_outer_pids_before_release"] ==
            ([sorted(record["probe_outer_pids_at_entry"] + [record["gate_pid"]])] if gated else []),
            "gate did not join the probe outer job")
    require(record["probe_entry_active_processes"] == 2
            and record["gate_outer_active_before_release"] == ([3] if gated else []),
            "unexpected aggregate process accounting")
    require(record["gate_argv_verified"] is gated, "wrong gate argv")
    if mode == "denied2":
        require(record["context_yielded"] is False, "denied launch yielded")
        require(record["sentinel_present"] is False and record["sentinel_matches"] is False,
                "denied payload ran")
        require(record["payload_returncode"] is None, "denied case returned a payload status")
        reports = record["launch_reports"]
        require(len(reports) == 1 and reports[0].get("status") == "oserror",
                "missing requested-executable denial report")
        report, error = reports[0], record["exception"]
        fields = {"errno", "winerror", "strerror", "filename", "filename2"}
        require(set(report) == fields | {"status"}, "wrong denial report fields")
        require(type(report["errno"]) is int and report["errno"] == 12
                and type(report["winerror"]) is int and report["winerror"] == 1816
                and isinstance(report["strerror"], str),
                "invalid native denial fields")
        require(all(report[k] is None or isinstance(report[k], str) for k in ("filename", "filename2")),
                "invalid native denial filenames")
        require(isinstance(error, dict) and set(error) == fields | {"type"}
                and error["type"] == "OSError" and all(error[k] == report[k] for k in fields),
                "native exception differs from launch report")
    else:
        require(record["exception"] is None and record["payload_returncode"] == 0,
                "positive payload did not exit successfully")
        require(record["sentinel_present"] is True and record["sentinel_matches"] is True,
                "positive sentinel missing or wrong")
        require(record["context_yielded"] is gated, "wrong context admission")
        require(record["launch_reports"] == ([{"status": "started"}] if gated else []),
                "wrong positive launch report")


def probe(mode, directory, job_name):
    native, source = Native(), load_source()
    outer_job = native.checked(native.OpenJobObjectW(4, False, job_name))  # QUERY only
    sentinel = directory / "payload-sentinel"
    require(not sentinel.exists(), "sentinel already exists")
    argv = [sys.executable, "-I", "-S", "-c", PAYLOAD, str(sentinel)]
    raw_reports, retained, outer_counts, outer_pids = [], [], [], []
    original_popen, original_interpret = source.REAL_POPEN, source.interpret_report
    record = {"mode": mode, "outer_limit": MODES[mode], "gate_count": 0,
              "gate_argv_verified": False, "context_yielded": False,
              "exception": None, "payload_returncode": None,
              "observer_cleanup_used": False}
    entry_state = Accounting()
    native.checked(native.QueryInformationJobObject(outer_job, 1, ctypes.byref(entry_state), ctypes.sizeof(entry_state), None))
    record["probe_entry_active_processes"] = entry_state.ActiveProcesses
    record["probe_identity"] = native.process_identity(os.getpid())
    record["probe_parent_identity"] = native.process_identity(os.getppid())
    record["probe_outer_pids_at_entry"] = native.job_pids(outer_job)
    record["outer_entry_identities"] = [native.process_identity(pid)
                                        for pid in record["probe_outer_pids_at_entry"]]

    def observed_popen(gate_argv, **kwargs):
        require(gate_argv[:4] == [sys.executable, "-I", "-S", "-c"]
                and json.loads(gate_argv[-1]) == argv, "gate target argv changed")
        record["gate_argv_verified"] = True
        before_state = Accounting()
        native.checked(native.QueryInformationJobObject(outer_job, 1, ctypes.byref(before_state), ctypes.sizeof(before_state), None))
        record["before_gate_active_processes"] = before_state.ActiveProcesses
        process = original_popen(gate_argv, **kwargs)
        retained.append(native.duplicate(int(process._handle)))
        record["gate_count"] += 1
        record["gate_pid"] = process.pid
        state = Accounting()
        native.checked(native.QueryInformationJobObject(outer_job, 1, ctypes.byref(state), ctypes.sizeof(state), None))
        outer_counts.append(state.ActiveProcesses)
        outer_pids.append(native.job_pids(outer_job))
        return process

    def observed_interpret(payload):
        raw_reports.append(payload)
        return original_interpret(payload)

    source.REAL_POPEN, source.interpret_report = observed_popen, observed_interpret
    options = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        try:
            if mode == "direct2":
                with subprocess.Popen(argv, **options) as process:
                    record["payload_returncode"] = process.wait(timeout=5)
            else:
                with source.checked_pipe(argv, **options) as process:
                    record["context_yielded"] = True
                    record["payload_returncode"] = process.wait(timeout=5)
        except OSError as error:
            record["exception"] = exception_record(error)
        record["launch_reports"] = [json.loads(payload) for payload in raw_reports]
        record["sentinel_present"] = sentinel.exists()
        record["sentinel_matches"] = sentinel.exists() and sentinel.read_bytes() == SENTINEL
        record["gate_wait_results"] = [native.WaitForSingleObject(handle, 0) for handle in retained]
        record["gate_outer_active_before_release"] = outer_counts
        record["gate_outer_pids_before_release"] = outer_pids
        (directory / "diagnostic.json").write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
        validate_case(record, mode)
        return record
    finally:
        for handle in retained:
            native.checked(native.CloseHandle(handle))
        native.checked(native.CloseHandle(outer_job))


def run_case(mode, directory):
    native = Native()
    job_name = "Local\\integer-mult-policy-" + uuid.uuid4().hex
    job = native.checked(native.CreateJobObjectW(None, job_name))
    collision = ctypes.get_last_error() == 183
    if collision:
        native.checked(native.CloseHandle(job))
        raise ValueError("test job name already exists")
    process = ProcessInformation()
    completed, assigned = False, False
    try:
        limits = ExtendedLimits()
        limits.Basic.Flags, limits.Basic.ActiveProcessLimit = 0x2008, MODES[mode]
        native.checked(native.SetInformationJobObject(job, 9, ctypes.byref(limits), ctypes.sizeof(limits)))
        startup = StartupInfo()
        startup.cb = ctypes.sizeof(startup)
        argv = [sys.executable, "-I", "-S"]
        if sys.flags.optimize:
            argv.append("-O")
        argv += [str(Path(__file__).resolve()), "--probe", mode, "--case-dir", str(directory),
                 "--job-name", job_name]
        command = ctypes.create_unicode_buffer(subprocess.list2cmdline(argv))
        native.checked(native.CreateProcessW(sys.executable, command, None, None, False,
                                             0x08000004, None, str(HERE), ctypes.byref(startup),
                                             ctypes.byref(process)))
        native.checked(native.AssignProcessToJobObject(job, process.hProcess))
        assigned = True
        state = Accounting()
        native.checked(native.QueryInformationJobObject(job, 1, ctypes.byref(state), ctypes.sizeof(state), None))
        require(state.ActiveProcesses == 1, "outer job did not contain exactly the suspended probe")
        require(native.ResumeThread(process.hThread) != 0xFFFFFFFF, "could not resume probe")
        native.checked(native.CloseHandle(process.hThread))
        process.hThread = None
        require(native.WaitForSingleObject(process.hProcess, 30000) == 0, "probe exceeded 30 seconds")
        exit_code = wintypes.DWORD()
        native.checked(native.GetExitCodeProcess(process.hProcess, ctypes.byref(exit_code)))
        result_path = directory / "probe.json"
        require(result_path.exists(), "probe exited without a result")
        envelope = json.loads(result_path.read_text(encoding="utf-8"))
        require(exit_code.value == 0 and envelope.get("ok") is True,
                "native probe failed: " + json.dumps(envelope, ensure_ascii=True))
        record = envelope["case"]
        validate_case(record, mode)
        state = Accounting()
        native.checked(native.QueryInformationJobObject(job, 1, ctypes.byref(state), ctypes.sizeof(state), None))
        require(state.ActiveProcesses == 0, "outer job still has an active process")
        record.update(probe_exit_code=0, outer_active_after_probe=0,
                      outer_active_before_resume=1,
                      controller_created_probe_pid=process.process_id,
                      controller_rescue_used=False, checked_before_outer_job_teardown=True)
        completed = True
        return record
    finally:
        if not completed:
            native.checked(native.TerminateJobObject(job, 1))
            if process.hProcess:
                if not assigned:
                    native.checked(native.TerminateProcess(process.hProcess, 1))
                require(native.WaitForSingleObject(process.hProcess, 5000) == 0,
                        "failed probe did not stop after controller rescue")
        if process.hThread:
            native.checked(native.CloseHandle(process.hThread))
        if process.hProcess:
            native.checked(native.CloseHandle(process.hProcess))
        native.checked(native.CloseHandle(job))


def validate_receipt(receipt, origin):
    require(receipt["schema_version"] == 1 and receipt["source"] == origin, "wrong receipt source")
    require(receipt["scope"] == "pending PR5721 checked_pipe; three isolated Windows job cases",
            "wrong receipt scope")
    require(len(receipt["cases"]) == 3, "wrong number of cases")
    for record, mode in zip(receipt["cases"], MODES):
        validate_case(record, mode)
        require(record["probe_exit_code"] == 0 and record["outer_active_after_probe"] == 0,
                "probe or outer job not finished")
        require(record["outer_active_before_resume"] == 1, "wrong suspended probe membership")
        require(record["controller_created_probe_pid"] == record["probe_identity"]["pid"],
                "observed probe differs from suspended assigned process")
        require(record["controller_rescue_used"] is False
                and record["checked_before_outer_job_teardown"] is True,
                "controller teardown manufactured exit")


def negative_controls(receipt, origin):
    mutations = [
        (0, "launch_reports", [], "missing requested-executable denial report"),
        (0, "sentinel_present", True, "denied payload ran"),
        (0, "gate_wait_results", [258], "gate was not already signaled"),
        (0, "gate_count", 0, "wrong gate count"),
        (0, "controller_rescue_used", True, "controller teardown manufactured exit"),
        (1, "sentinel_matches", False, "positive sentinel missing or wrong"),
        (2, "payload_returncode", 1, "positive payload did not exit successfully"),
    ]
    for index, field, value, message in mutations:
        bad = copy.deepcopy(receipt)
        bad["cases"][index][field] = value
        try:
            validate_receipt(bad, origin)
        except ValueError as error:
            require(str(error) == message, "negative control failed for the wrong reason")
        else:
            raise ValueError("receipt mutation was accepted: " + field)
    bad = copy.deepcopy(receipt)
    bad["cases"][0]["launch_reports"][0]["winerror"] = 2
    bad["cases"][0]["exception"]["winerror"] = 2
    try:
        validate_receipt(bad, origin)
    except ValueError as error:
        require(str(error) == "invalid native denial fields", "denial-class control failed for wrong reason")
    else:
        raise ValueError("unrelated native error accepted as quota denial")
    return len(mutations) + 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="save a fresh native CERTIFICATE.json")
    parser.add_argument("--check-receipt", action="store_true", help="validate archived evidence; no native execution")
    parser.add_argument("--probe", choices=MODES, help=argparse.SUPPRESS)
    parser.add_argument("--case-dir", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--job-name", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    origin, _ = authenticate()
    if args.probe:
        require(args.case_dir is not None and args.job_name is not None, "missing probe directory or job")
        try:
            envelope = {"ok": True, "case": probe(args.probe, args.case_dir, args.job_name)}
        except Exception as error:
            envelope = {"ok": False, "error_type": type(error).__name__, "error": str(error)}
            diagnostic = args.case_dir / "diagnostic.json"
            if diagnostic.exists():
                envelope["diagnostic"] = json.loads(diagnostic.read_text(encoding="utf-8"))
        (args.case_dir / "probe.json").write_text(json.dumps(envelope, sort_keys=True), encoding="utf-8")
        return 0 if envelope["ok"] else 1
    require(not (args.write and args.check_receipt), "cannot write during archived receipt validation")
    if args.check_receipt:
        receipt = json.loads((HERE / "CERTIFICATE.json").read_text(encoding="utf-8"))
        evidence = "archived receipt validation; no native processes launched"
    else:
        Native()
        with tempfile.TemporaryDirectory(prefix="job-policy-audit-") as temporary:
            cases = []
            for mode in MODES:
                directory = Path(temporary) / mode
                directory.mkdir()
                cases.append(run_case(mode, directory))
        receipt = {"schema_version": 1, "source": origin,
                   "scope": "pending PR5721 checked_pipe; three isolated Windows job cases",
                   "environment": {"platform": platform.platform(), "python": platform.python_version(),
                                   "executable": sys.executable, "optimized": bool(sys.flags.optimize)},
                   "cases": cases}
        evidence = "fresh native execution"
    validate_receipt(receipt, origin)
    controls = negative_controls(receipt, origin)
    if args.write:
        (HERE / "CERTIFICATE.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"evidence": evidence, "negative_controls": controls, "receipt": receipt}, sort_keys=True))
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
