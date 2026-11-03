"""End-to-end evidence for the new emitter; produced by Nick Petalas."""

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path
import platform
from random import Random
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from compiler import Machine, compile_machine, require, width_bound  # noqa: E402
from ram import RAM  # noqa: E402


def input_words(scale, tapes, output_length):
    body = [scale, output_length]
    for tape in tapes:
        body.extend((len(tape), *tape))
    return [len(body), *body]


def reference_step(machine, state, heads, tapes):
    observed = tuple(tape.get(head, 0) for tape, head in zip(tapes, heads))
    transition = machine.delta.get((state, observed))
    if transition is None:
        return None
    state, writes, moves = transition
    for tape, head, symbol in zip(tapes, heads, writes):
        tape[head] = symbol
    return state, [head + direction for head, direction in zip(heads, moves)]


def address(metadata, block, tape, position):
    magnitude = position if position >= 0 else -position - 1
    tag = 2 * tape + int(position < 0)
    word = metadata["base"] + metadata["stride"] * (magnitude // block) + tag
    offset = metadata["field_bits"] * (magnitude % block)
    return word, offset


def compare_boundary(vm, metadata, state, heads, tapes, span):
    require(metadata["boundaries"][vm.pc] == state, "state mismatch")
    block = 1 << vm.get(4)
    mask = (1 << metadata["field_bits"]) - 1
    require(vm.get(5) == block - 1, "packing metadata mismatch")
    for tape, head in enumerate(heads):
        encoded = 2 * head if head >= 0 else -2 * head - 1
        require(vm.get(metadata["heads"][tape]) == encoded, "head mismatch")
        for position in range(-span, span + 1):
            word, offset = address(metadata, block, tape, position)
            actual = (vm.get(word) >> offset) & mask
            require(actual == tapes[tape].get(position, 0), "tape mismatch")


def initialize_case(machine, tapes, output_length, scale, limit, code, metadata):
    require(len(tapes) == machine.tapes and all(len(t) <= 1024 for t in tapes),
            "fixture tape shape")
    require(all(type(s) is int and 0 <= s < machine.alphabet
                for t in tapes for s in t), "fixture symbol")
    width = width_bound(machine, len(code), scale, tuple(map(len, tapes)),
                        limit, output_length)
    vm = RAM(width, code, input_words(scale, tapes, output_length))
    lam = (scale + 2).bit_length() - 1
    q = lam // (8 * metadata["field_bits"])
    block = 1 << max(0, q.bit_length() - 1)
    span = max((len(t) for t in tapes), default=0) + limit + output_length + 2
    high_mask = vm.mask ^ ((1 << (metadata["field_bits"] * block)) - 1)
    protected = {}
    for index in range((span + block - 1) // block + 1):
        for tag in range(2 * machine.tapes):
            word = metadata["base"] + metadata["stride"] * index + tag
            vm.put(word, high_mask)
            protected[word] = high_mask
    vm.put(vm.mask, 29)  # Exterior data word, never a tape/control address.
    return vm, span, block, high_mask, protected


def run_case(machine, tapes, output_length, scale=0, limit=40, mutation=None):
    code, metadata = compile_machine(machine)
    if mutation is not None:
        code = mutate(code, metadata, mutation)
    vm, span, block, high_mask, protected = initialize_case(
        machine, tapes, output_length, scale, limit, code, metadata)
    reference = [dict(enumerate(tape)) for tape in tapes]
    heads, state, transitions, entered, halted = [0] * machine.tapes, 0, 0, False, False
    lam = (scale + 2).bit_length() - 1
    k = machine.tapes
    per_transition = 45 * k + 3 * k * machine.alphabet ** k + 1
    bound = 19 + 4 * lam + 5 * (block.bit_length() - 1) + 4 * k
    bound += 26 * sum(map(len, tapes)) + per_transition * (limit + 1)
    bound += 22 * output_length
    require(bound <= 10000000, "fixture microinstruction cap")
    for _ in range(bound + 1):
        if vm.pc in metadata["boundaries"]:
            if entered:
                result = reference_step(machine, state, heads, reference)
                require(result is not None, "boundary after missing transition")
                state, heads = result
                transitions += 1
            entered = True
            compare_boundary(vm, metadata, state, heads, reference, span)
            observed = tuple(t.get(h, 0) for t, h in zip(reference, heads))
            if transitions == limit and (state, observed) in machine.delta:
                break
        if not vm.step():
            observed = tuple(t.get(h, 0) for t, h in zip(reference, heads))
            require(entered and (state, observed) not in machine.delta,
                    "premature halt")
            require(vm.pc == metadata["halt"] and vm.cursor == len(vm.inputs),
                    "genuine halt/input consumption")
            expected = [reference[machine.output].get(j, 0)
                        for j in range(output_length)]
            require(vm.output == expected, "output mismatch")
            compare_final(vm, metadata, reference, span)
            before = (vm.pc, vm.steps, dict(vm.memory), tuple(vm.output))
            require(not vm.step(), "nonterminal halt")
            require(before == (vm.pc, vm.steps, vm.memory, tuple(vm.output)),
                    "halt changed state")
            halted = True
            break
    else:
        raise ValueError("microinstruction bound")
    require(vm.steps <= bound and vm.get(vm.mask) == 29, "cost/exterior memory")
    require(all(vm.get(word) & high_mask == value
                for word, value in protected.items()), "high padding clobbered")
    require(all(word >= metadata["base"] for word in vm.data_writes),
            "tape/control alias")
    return {"halted": halted, "steps": vm.steps, "transitions": transitions,
            "block": block, "written_words": len(vm.data_writes),
            "program_sha256": hashlib.sha256(repr(code).encode()).hexdigest(),
            "output": vm.output}


def compare_final(vm, metadata, tapes, span):
    block = 1 << vm.get(4)
    mask = (1 << metadata["field_bits"]) - 1
    for tape in range(len(tapes)):
        for position in range(-span, span + 1):
            word, offset = address(metadata, block, tape, position)
            require((vm.get(word) >> offset) & mask == tapes[tape].get(position, 0),
                    "final tape mismatch")


def mutate(code, metadata, fault):
    changed = list(code)
    if fault == "halt":
        changed[metadata["halt"]] = ("jump", metadata["halt"])
    elif fault == "output":
        changed = [("write", 31) if i[0] == "write" else i for i in changed]
    elif fault == "head":
        changed[2] = ("set", 2, 1)
    elif fault == "bank":
        changed = [("set", 35, 0) if i[0] == "set" and i[1] == 35
                   and i[2] == 2 else i for i in changed]
    elif fault == "clear_word":
        changed = [("set", 26, 0) if i[0] == "and" and i[1] == 26
                   else i for i in changed]
    elif fault == "packing":
        changed = [("set", 16, 0) if i[0] == "set" and i[1] == 16
                   else i for i in changed]
    else:
        raise ValueError("unknown mutation")
    require(tuple(changed) != code, "mutation did not change code")
    return tuple(changed)


def one_transition_cases():
    results = []
    for k in (1, 2):
        for reads in product(range(2), repeat=k):
            for writes in product(range(2), repeat=k):
                for moves in product((-1, 0, 1), repeat=k):
                    machine = Machine(k, 2, 2, {(0, reads): (1, writes, moves)})
                    tapes = [[s, 1 - s, s] for s in reads]
                    results.append(run_case(machine, tapes, 4, 1 << 64))
    return results


def random_cases():
    rng, results = Random(20261030), []
    for k in (1, 2, 3):
        for case in range(24):
            alphabet, states, delta = 3, 3, {}
            for state in range(states):
                for reads in product(range(alphabet), repeat=k):
                    if rng.randrange(6) != 0:
                        writes = tuple(rng.randrange(alphabet) for _ in range(k))
                        moves = tuple(rng.randrange(-1, 2) for _ in range(k))
                        delta[state, reads] = (rng.randrange(states), writes, moves)
            tapes = [[rng.randrange(alphabet) for _ in range(rng.randrange(9))]
                     for _ in range(k)]
            machine = Machine(k, alphabet, states, delta, case % k)
            scale = (0, 1 << 32, 1 << 64, 1 << 128, 1 << 250)[case % 5]
            results.append(run_case(machine, tapes, case % 10, scale))
    return results


def directed_cases():
    results = []
    for k, alphabet, scale in product((1, 2, 4), (1, 2, 3, 4),
                                      (0, 1 << 32, 1 << 128, 1 << 250)):
        # Every tape makes a long excursion in both sign banks and returns.
        delta = {}
        moves = (-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1)
        for q, direction in enumerate(moves):
            for reads in product(range(alphabet), repeat=k):
                delta[q, reads] = (q + 1, tuple((s + 1) % alphabet for s in reads),
                                  (direction,) * k)
        machine = Machine(k, alphabet, 16, delta, k - 1)
        results.append(run_case(machine, [[alphabet - 1] * 5 for _ in range(k)],
                                7, scale, limit=16))
    for direction in (-1, 1):
        machine = Machine(1, 2, 1, {(0, (s,)): (0, (1 - s,), (direction,))
                                   for s in range(2)})
        results.append(run_case(machine, [[1, 0, 1]], 0, 1 << 128, limit=80))
    # Cross-copy depends on every observed symbol before the first write.
    swap = {(0, pair): (1, pair[::-1], (0, 0)) for pair in product(range(4), repeat=2)}
    for pair in product(range(4), repeat=2):
        results.append(run_case(Machine(2, 4, 2, swap), [[pair[0]], [pair[1]]],
                                3, 1 << 64))
    return results


def reject_controls():
    machine = Machine(2, 3, 2, {(0, (s, t)): (1, (t, s), (-1, 1))
                                for s, t in product(range(3), repeat=2)}, 1)
    faults = ("head", "bank", "clear_word", "packing", "output", "halt")
    rejected = []
    for fault in faults:
        try:
            run_case(machine, [[1, 2], [2, 1]], 4, 1 << 64, mutation=fault)
        except ValueError as error:
            rejected.append({"fault": fault, "reason": str(error)})
    require(len(rejected) == len(faults), "emitted mutation escaped")
    bad = (Machine(0, 2, 1, {}), Machine(5, 2, 1, {}), Machine(1, 5, 1, {}),
           Machine(1, 2, 17, {}), Machine(1, 2, 1, {}, 1),
           Machine(1, 2, 1, {(0, (0,)): (0, (2,), (0,))}),
           Machine(1, 2, 1, {(0, (0,)): (0, (0,), (2,))}),
           Machine(1, 2, 1, {(1, (0,)): (0, (0,), (0,))}))
    invalid = 0
    for item in bad:
        try:
            compile_machine(item)
        except ValueError:
            invalid += 1
    require(invalid == len(bad), "invalid machine accepted")
    return rejected, invalid


def predecessor_comparison():
    manifest = json.loads((ROOT / "SOURCES.json").read_text())
    sources = {}
    for pin in manifest["files"]:
        if pin["usage"] == "input":
            path = ROOT.parents[1] / pin["path"]
            raw = path.read_bytes()
            require(hashlib.sha256(raw).hexdigest() == pin["sha256"],
                    "predecessor source hash")
            sources[pin["path"]] = raw
    key = "research/word-ram-transfer/compiler/tm_to_ramstd.py"
    namespace = {"__name__": "pinned_unpacked_reference"}
    exec(compile(sources[key], key, "exec"), namespace)
    count = 0
    for k, direction, output_length in product((1, 2, 3), (-1, 1), (0, 5)):
        delta = {(0, reads): (1, tuple((s + 1) % 3 for s in reads),
                              (direction,) * k)
                 for reads in product(range(3), repeat=k)}
        machine, tapes = Machine(k, 3, 2, delta), [[1, 2, 0, 1] for _ in range(k)]
        result = run_case(machine, tapes, output_length, 1 << 64)
        code, _ = namespace["compile_tm"](k, 3, 2, delta)
        old_input = [output_length]
        for tape in tapes:
            old_input.extend((len(tape), *tape))
        vm = namespace["VM"](32, code, [len(old_input), *old_input])
        for _ in range(100000):
            if not vm.step():
                break
        else:
            raise ValueError("paired unpacked fixture limit")
        require(vm.out == result["output"], "paired unpacked output mismatch")
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    require(sys.version_info[:2] == (3, 12), "CPython 3.12 required")
    # Authenticate source bytes before any scientific execution.
    paired = predecessor_comparison()
    results = one_transition_cases() + random_cases() + directed_cases()
    rejected, invalid = reject_controls()
    dense = run_case(Machine(2, 4, 1, {}), [[1, 2, 3, 0] * 32] * 2,
                     128, 1 << 48, limit=0)
    require(dense["block"] == 2 and dense["written_words"] == 128,
            "dense storage refinement")
    receipt = {"status": "PASS_EMITTED_PACKED_TM", "claim_type": "scoped proof",
               "python": platform.python_version(), "cases": len(results),
               "halting_cases": sum(r["halted"] for r in results),
               "nonhalting_prefixes": sum(not r["halted"] for r in results),
               "tm_transitions": sum(r["transitions"] for r in results),
               "ram_instructions": sum(r["steps"] for r in results),
               "block_sizes": sorted({r["block"] for r in results}),
               "paired_unpacked_cases": paired, "rejected_mutations": rejected,
               "invalid_machine_rejections": invalid,
               "dense_storage": {"symbols": 256, "words": 128,
                                 "ram_instructions": dense["steps"],
                                 "program_sha256": dense["program_sha256"]},
               "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(ROOT.iterdir()) if p.is_file()}}
    output = json.dumps(receipt, sort_keys=True, indent=2) + "\n"
    if args.receipt is not None:
        require(args.receipt.is_absolute() and ROOT not in args.receipt.parents,
                "receipt must be an external absolute path")
        with args.receipt.open("x") as stream:
            require(stream.write(output) == len(output), "short receipt write")
    print(output, end="")


if __name__ == "__main__":
    main()
