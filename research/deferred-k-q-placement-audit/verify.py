#!/usr/bin/env python3
"""Independent replay of the mode-0 K-conjugated Q counterexample.

The deferred-K checker records this witness as inherited and not recomputed.
This program reads the pinned literal word and evaluates the operators itself.
"""
from fractions import Fraction
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "research/deferred-k-query-sharing-component"
REPORT = PACKAGE / (
    "verification/inputs/outputs/kappa0033-race-20261024/plan/"
    "BALANCED-J-CURRENT-Q-FRAME-audit/REPORT-v1.md"
)
PROOF = PACKAGE / "PROOF.md"
N = 9
DIM = 1 << N
EMBED = (0, 9, 10, 11, 12, 13, 14, 15, 16)
WORD = (
    "D(quadratic=0, linear=[2,2,2,2,0,0,0,0,0])\n"
    "P(rows=[7,13,11,14,16,32,64,128,256])\n"
    "X(0)\n"
    "phase(0)."
)


def parity(value):
    return value.bit_count() & 1


def mv(rows, state):
    return sum(parity(row & state) << index for index, row in enumerate(rows))


def mul_i(real, imag, power):
    power %= 4
    if power == 0:
        return real, imag
    if power == 1:
        return -imag, real
    if power == 2:
        return -real, -imag
    return imag, -real


def zero():
    return [(Fraction(0), Fraction(0)) for _ in range(DIM)]


def basis(index):
    state = zero()
    state[index] = (Fraction(1), Fraction(0))
    return state


def apply_d(state, alpha):
    out = []
    for label, amplitude in enumerate(state):
        power = sum(alpha[bit] for bit in range(N) if label >> bit & 1) % 4
        out.append(mul_i(amplitude[0], amplitude[1], power))
    return out


def apply_p(state, rows):
    out = zero()
    for label, amplitude in enumerate(state):
        out[mv(rows, label)] = amplitude
    return out


def apply_p_inverse(state, rows):
    out = zero()
    for label, amplitude in enumerate(state):
        out[label] = state[mv(rows, label)]
    return out


def apply_x(state, shift):
    return [state[label ^ shift] for label in range(DIM)]


def apply_c(state, axis_mask, sign=1):
    out = [None] * DIM
    for label, (real, imag) in enumerate(state):
        other_real, other_imag = state[label ^ axis_mask]
        out[label] = (
            (real - sign * imag + other_real + sign * other_imag) / 2,
            (imag + sign * real + other_imag - sign * other_real) / 2,
        )
    return out


def apply_phase(state, power):
    return [mul_i(real, imag, power) for real, imag in state]


def fourier(axes, sign=1):
    def run(state):
        for axis in axes:
            state = apply_c(state, 1 << axis, sign)
        return state
    return run


def fourier_inverse(axes):
    # Adjoint reverses axis order and flips each C sign, matching clifford_exact.
    def run(state):
        for axis in reversed(axes):
            state = apply_c(state, 1 << axis, -1)
        return state
    return run


def parse_word(text):
    match = re.search(
        r"D\(quadratic=(\d+), linear=\[([0-9,\s]+)\]\)\s*"
        r"P\(rows=\[([0-9,\s]+)\]\)\s*"
        r"X\((\d+)\)\s*"
        r"phase\((\d+)\)\.",
        text,
    )
    if match is None:
        raise SystemExit("literal mode-0 K word not found in the pinned report")
    quadratic = int(match.group(1))
    linear = [int(item) for item in match.group(2).split(",")]
    rows = [int(item) for item in match.group(3).split(",")]
    shift = int(match.group(4))
    phase = int(match.group(5))
    if (quadratic, linear, rows, shift, phase) != (
        0, [2, 2, 2, 2, 0, 0, 0, 0, 0],
        [7, 13, 11, 14, 16, 32, 64, 128, 256], 0, 0,
    ):
        raise SystemExit("pinned report word differs from the stated mode-0 word")
    if match.group(0) != WORD:
        raise SystemExit("pinned report word text differs from the expected block")
    return linear, rows, shift, phase


def apply_k(state, linear, rows, shift, phase):
    state = apply_d(state, linear)
    state = apply_p(state, rows)
    state = apply_x(state, shift)
    return apply_phase(state, phase)


def apply_k_inverse(state, linear, rows, shift, phase):
    state = apply_phase(state, (-phase) % 4)
    state = apply_x(state, shift)
    state = apply_p_inverse(state, rows)
    adjoint_linear = [(-entry) % 4 for entry in linear]
    return apply_d(state, adjoint_linear)


def support(state):
    return [(index, real, imag) for index, (real, imag) in enumerate(state)
            if real != 0 or imag != 0]


def equal(left, right):
    return all(a == b for a, b in zip(left, right))


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def main():
    text = REPORT.read_text(encoding="utf-8")
    proof = PROOF.read_text(encoding="utf-8")
    linear, rows, shift, phase = parse_word(text)
    require("K^-1 X1 K = -X7" in text, "report no longer states the conjugation identity")
    require("a|0> - b|7>" in text, "report no longer states the routed output")
    require("Km0 supplies a width-one counterexample" in proof,
            "PROOF.md no longer names the Km0 counterexample")
    require("bare positive C1" in proof, "PROOF.md no longer states bare positive C1")

    # G maps basis vector e_i to rows[i] when rows are the linear forms of output bits.
    # The stated action G(1)=7 is the image of mask 1.
    require(mv(rows, 1) == 7, "G(1) is not 7")
    require(mv(rows, 7) == 1, "G(7) is not 1")
    for mask in range(16):
        require(mv(rows, mv(rows, mask)) == mask, "G is not an involution on the low nibble")
    for bit in range(4, N):
        require(mv(rows, 1 << bit) == (1 << bit), "a high basis vector moved")

    k_zero = apply_k(basis(0), linear, rows, shift, phase)
    require(support(k_zero) == [(0, Fraction(1), Fraction(0))], "K|0> is not |0>")

    k_inv_one = apply_k_inverse(basis(1), linear, rows, shift, phase)
    require(support(k_inv_one) == [(7, Fraction(-1), Fraction(0))], "K^-1|1> is not -|7>")

    # K^-1 X_1 K = -X_7 on every computational basis vector.
    for label in range(DIM):
        routed = apply_k_inverse(
            apply_x(apply_k(basis(label), linear, rows, shift, phase), 1),
            linear, rows, shift, phase,
        )
        target = apply_phase(apply_x(basis(label), 7), 2)
        require(equal(routed, target), "conjugation failed at basis " + str(label))

    bare = apply_c(basis(0), 1, 1)
    require(support(bare) == [
        (0, Fraction(1, 2), Fraction(1, 2)),
        (1, Fraction(1, 2), Fraction(-1, 2)),
    ], "bare Q|0> is not a|0>+b|1>")
    wrapped = apply_k_inverse(
        apply_c(apply_k(basis(0), linear, rows, shift, phase), 1, 1),
        linear, rows, shift, phase,
    )
    require(support(wrapped) == [
        (0, Fraction(1, 2), Fraction(1, 2)),
        (7, Fraction(-1, 2), Fraction(1, 2)),
    ], "routed Q|0> is not a|0>-b|7>")
    require(not equal(bare, wrapped), "bare and routed outputs unexpectedly agree")

    # Source placement: R is C on axes 0..8, low axis first; D is axes 1..8.
    # Rightmost-first composition R = D Q means Q first, then D.
    for label in range(DIM):
        left = fourier(range(1, N))(apply_c(basis(label), 1, 1))
        right = fourier(range(N))(basis(label))
        require(equal(left, right), "R != D Q at basis " + str(label))
        kr = apply_k(right, linear, rows, shift, phase)
        rk = fourier(range(N))(apply_k(basis(label), linear, rows, shift, phase))
        require(equal(kr, rk), "K does not commute with R at basis " + str(label))
        kq = apply_k(apply_c(basis(label), 1, 1), linear, rows, shift, phase)
        qk = apply_c(apply_k(basis(label), linear, rows, shift, phase), 1, 1)
        require(not equal(kq, qk), "K unexpectedly commutes with Q at basis " + str(label))

    local7 = 7
    global7 = sum(1 << EMBED[bit] for bit in range(N) if local7 >> bit & 1)
    require(global7 == 1537, "local 7 does not lift to global mask 1537")
    require(sum(1 << EMBED[bit] for bit in range(N) if 1 >> bit & 1) == 1,
            "local 1 does not stay global mask 1")

    # Failure control: clearing one linear phase removes the minus on |7>.
    mutated = list(linear)
    mutated[0] = 0
    mutated_image = apply_k_inverse(basis(1), mutated, rows, shift, phase)
    require(support(mutated_image) != [(7, Fraction(-1), Fraction(0))],
            "phase mutation still produced -|7>")

    print("PASS_DEFERRED_K_Q_PLACEMENT")
    print("bare_Q_zero=a|0>+b|1>")
    print("routed_Q_zero=a|0>-b|7>")
    print("conjugation=K^-1 X1 K=-X7 on all 512 basis states")
    print("placement=R=D Q on all 512 basis states; K commutes with R and not with Q")
    print("lift_local7=1537")


if __name__ == "__main__":
    main()
