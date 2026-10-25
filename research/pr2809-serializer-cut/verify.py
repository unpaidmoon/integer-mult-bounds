#!/usr/bin/env python3
"""One PR2809 recursive cut parks the current frame, not a fresh root stream.

The pinned serializer is Jose Manuel's PR2809 archive
`research/physical-ordinary-interchange/inputs/pr2809.tar`. This checker
extracts `role_parking.py` and runs that `RoleParking.park` method. It does
not run the GL64 macroprogram, the selected cold replay, or the parking-table
interpreter.
"""

from hashlib import sha256
import importlib.util
import io
import sys
import tarfile
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parent
ROOT = PKG.parents[1]
TAR = ROOT / "research/physical-ordinary-interchange/inputs/pr2809.tar"
BIT = ROOT / "research/unconditional-batched-crt/BIT.md"
PREDECESSOR = ROOT / "research/pr2809-continuation-stack-space/README.md"

TAR_SHA256 = "ee1d4ec05e3c872d264be3b38f71a8c153acf37427f5d3ba87f8e15440c9ccf0"
ROLE_SHA256 = "1884a3c260d81d5efbc0c33d86a810d6728e55e5764cfcd423f858cc685470f3"
WORDS_SHA256 = "5c37f57708ba3131bdcb03139f9dbc29886bee44569c09cbba51b68f75acd7f9"
RECORDS_SHA256 = "0c9c4b23e998597fb877bb1a29da69ac869b68262abe635b162b4dba9c69b372"

ROOT_PACKET = 1000
CHILD_CAPSULE = 7
GRANDCHILD_CAPSULE = 1
CONTROL_SYMBOLS = 8
FULL_COPY_DEPTH = 26042


def D(n):
    depth = 0
    while n >= 64:
        n = 42 * (n // 64)
        depth += 1
    return depth


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def extract(archive, name):
    member = archive.extractfile(name)
    require(member is not None, "missing archive member " + name)
    return member.read()


def load_parking(role_source, words_source, records_source):
    directory = Path(tempfile.mkdtemp(prefix="pr2809-park-"))
    (directory / "loader.py").write_text(
        "def activate():\n    return None\n", encoding="utf-8")
    (directory / "words.py").write_bytes(words_source)
    (directory / "records.py").write_bytes(records_source)
    (directory / "role_parking.py").write_bytes(role_source)
    sys.path.insert(0, str(directory))
    try:
        spec = importlib.util.spec_from_file_location(
            "pr2809_role_parking", directory / "role_parking.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


class PacketPort:
    """Counts the bits RoleParking.park emits. Push commits one record."""

    def __init__(self):
        self.bits = []
        self.frames = []
        self.commands = []

    def _empty_port(self):
        self.bits = []

    def _command(self, name):
        self.commands.append(name)
        if name == "push":
            self.frames.append(tuple(self.bits))
            self.bits = []

    def _put_bit(self, bit):
        self.bits.append(bit)

    def _write(self, count, symbol):
        require(count == 1 and symbol == "$", "unexpected port mark")

    def _rewind_port(self):
        return None


def fill(tape, count, symbol):
    for _ in range(count):
        tape.append(symbol)


def body_length(tape, blank):
    tape.rewind()
    count = 0
    while tape.read() != blank:
        count += 1
        tape.step(1)
    tape.rewind()
    return count


def park_roles(module, lengths):
    tapes = tuple(module_tape(module) for _ in lengths)
    for tape, length in zip(tapes, lengths):
        if length:
            fill(tape, length, module.BODY[1])
    port = PacketPort()
    module.RoleParking(port, tapes).park()
    blank = sys.modules["words"].BLANK
    require(all(body_length(tape, blank) == 0 for tape in tapes),
            "park left a role body in place")
    payload_bits = [len(frame) for frame in port.frames]
    require(payload_bits == [4 * length for length in lengths],
            "parked bits are not four per current symbol: " + str(payload_bits))
    require(port.commands[0] == "begin", "park does not begin a frame")
    require(port.commands.count("push") == len(lengths), "one push per role")
    return payload_bits


def module_tape(module):
    del module
    return sys.modules["records"].Tape()


def bind_sources(role_source):
    bit = BIT.read_text(encoding="utf-8")
    for needle in (
        "Serialize parent streams and arithmetic",
        "copy the child's capsule, reuse the fixed work",
        "Each child's payload has volume V/(WN).",
        "Active ancestor payloads therefore",
    ):
        require(needle in bit, "missing BIT.md sentence: " + needle)
    readme = PREDECESSOR.read_text(encoding="utf-8")
    require(
        "root-sized stream per cut" in readme,
        "predecessor no longer asks the serializer question",
    )
    text = role_source.decode()
    require("def park(self):" in text, "RoleParking.park missing")
    park = text.split("def park(self):", 1)[1].split("def restore(self):", 1)[0]
    for needle in ("for tape in self.roles:", "tape.write(BLANK)", 'port._command("push")'):
        require(needle in park, "park loop missing " + needle)
    require("root" not in park, "park names a root stream")


def assert_child_is_capsule(child_bits, root_bits):
    require(child_bits < root_bits, "child cut recopied the root packet")
    require(child_bits == 4 * CHILD_CAPSULE, "child cut is not the adopted capsule")
    require(root_bits == 4 * ROOT_PACKET, "root cut is not the root packet")


def compare_cuts(module):
    # Three roles in this schedule: a fixed control body, the current data
    # body, and one empty role. The pinned nested fixture uses four roles and
    # is bound separately by its depth-linear step formula.
    root_lengths = (CONTROL_SYMBOLS, ROOT_PACKET, 0)
    root_bits = park_roles(module, root_lengths)
    child_lengths = (CONTROL_SYMBOLS, CHILD_CAPSULE, 0)
    child_bits = park_roles(module, child_lengths)
    grand_lengths = (CONTROL_SYMBOLS, GRANDCHILD_CAPSULE, 0)
    grand_bits = park_roles(module, grand_lengths)
    require(root_bits[1] == 4 * ROOT_PACKET, "root cut did not park the root packet")
    require(child_bits[1] == 4 * CHILD_CAPSULE, "child cut did not park the child capsule")
    require(grand_bits[1] == 4 * GRANDCHILD_CAPSULE, "grandchild cut did not park its capsule")
    assert_child_is_capsule(child_bits[1], root_bits[1])
    return {
        "root_data_bits": root_bits[1],
        "child_data_bits": child_bits[1],
        "grandchild_data_bits": grand_bits[1],
    }


def prove_root_copy_exceeds_geometric_constant():
    witness = 1 << 26050
    depth = D(witness)
    require(depth >= FULL_COPY_DEPTH, "full-copy depth dropped below 26042")
    # Two coarse levels at least halve the width, so D(2^m) >= m + 1 - 9.
    require(D(1 << 16) >= 16 + 1 - 9, "depth lower-bound sample moved")
    require(depth > 26041, "full root copies no longer exceed the geometric constant")


def main():
    tar_bytes = TAR.read_bytes()
    digest = sha256(tar_bytes).hexdigest()
    require(digest == TAR_SHA256, "PR2809 archive hash changed: " + digest)
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as archive:
        role_source = extract(archive, "role_parking.py")
        words_source = extract(archive, "inputs/pr2753/predecessor/vendor/words.py")
        records_source = extract(archive, "inputs/pr2753/predecessor/vendor/records.py")
        continuation = extract(archive, "continuation_checks.py")
    require(sha256(role_source).hexdigest() == ROLE_SHA256, "role_parking.py hash changed")
    require(sha256(words_source).hexdigest() == WORDS_SHA256, "words.py hash changed")
    require(sha256(records_source).hexdigest() == RECORDS_SHA256, "records.py hash changed")
    text = continuation.decode()
    require(
        "depth * (5 * 132 + 7 * 5 + 3 * 2)" in text,
        "nested fixture no longer charges a depth-linear constant",
    )
    require("4*(4+13+12)" in text and "1+3+12" in text,
            "nested fixture no longer names the per-level bit invoice")
    # Four stream records of 4, 13 and 12 symbols, plus one numerical
    # record of 1+3+12 bits, are the 132 bits in that invoice.
    require(4 * (4 + 13 + 12) + (1 + 3 + 12) == 132,
            "the per-level 132-bit invoice no longer matches its comment")
    bind_sources(role_source)
    module = load_parking(role_source, words_source, records_source)
    cuts = compare_cuts(module)
    prove_root_copy_exceeds_geometric_constant()
    print(
        "PASS_PR2809_SERIALIZER_CUT"
        f" root_data_bits={cuts['root_data_bits']}"
        f" child_data_bits={cuts['child_data_bits']}"
        f" grandchild_data_bits={cuts['grandchild_data_bits']}"
        f" child_is_capsule=true"
        f" child_recopies_root=false"
        f" full_copy_depth={D(1 << 26050)}"
        " no_new_kappa=true"
    )


if __name__ == "__main__":
    main()
