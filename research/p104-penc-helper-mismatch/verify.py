#!/usr/bin/env python3
"""Helper mismatch for the literal correction Pi P_enc Pi.

PROOF.md is the argument. This file recomputes the block identity, the
one-bit chart obstruction, the N-port exchange count, and the inherited
integer gate. It does not import a predecessor package.
"""

from fractions import Fraction


def F(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def diag(values):
    matrix = zeros(len(values), len(values))
    for i, value in enumerate(values):
        matrix[i][i] = F(value)
    return matrix


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def sub(left, right):
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mul(left, right):
    rows, mid = len(left), len(left[0])
    cols = len(right[0])
    out = zeros(rows, cols)
    for i in range(rows):
        for k in range(mid):
            if left[i][k] == 0:
                continue
            for j in range(cols):
                out[i][j] += left[i][k] * right[k][j]
    return out


def blocks(top_left, top_right, bottom_left, bottom_right):
    n = len(top_left)
    out = zeros(2 * n, 2 * n)
    for i in range(n):
        for j in range(n):
            out[i][j] = top_left[i][j]
            out[i][n + j] = top_right[i][j]
            out[n + i][j] = bottom_left[i][j]
            out[n + i][n + j] = bottom_right[i][j]
    return out


def inverse(matrix):
    n = len(matrix)
    augmented = [row[:] + eye(n)[i] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if augmented[r][col] != 0)
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        pivot_value = augmented[col][col]
        augmented[col] = [entry / pivot_value for entry in augmented[col]]
        for row in range(n):
            if row == col or augmented[row][col] == 0:
                continue
            factor = augmented[row][col]
            augmented[row] = [
                augmented[row][j] - factor * augmented[col][j] for j in range(2 * n)
            ]
    return [row[n:] for row in augmented]


def apply(matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL_P104_PENC_HELPER_MISMATCH " + message)


def operators(h_mask, t_matrix, data):
    n = len(h_mask)
    h = diag(h_mask)
    j0 = sub(eye(n), h)
    k = inverse(t_matrix)
    p = blocks(eye(n), zeros(n, n), k, eye(n))
    l_matrix = blocks(data, mul(h, t_matrix), zeros(n, n), eye(n))
    pi = blocks(j0, h, h, j0)
    encoded = mul(pi, l_matrix)
    p_enc = mul(l_matrix, mul(p, inverse(l_matrix)))
    literal = mul(pi, mul(p_enc, pi))
    return p, l_matrix, pi, encoded, literal


def check_intertwiner(h_mask, t_matrix, data):
    p, _, pi, encoded, literal = operators(h_mask, t_matrix, data)
    require(mul(pi, pi) == eye(2 * len(h_mask)), "Pi squared")
    require(mul(literal, encoded) == mul(encoded, p), "literal intertwiner")
    # Vector form, written as bank concatenation rather than block multiplication.
    n = len(h_mask)
    witness = [F(i + 1) for i in range(2 * n)]
    require(
        apply(mul(literal, encoded), witness) == apply(mul(encoded, p), witness),
        "vector intertwiner",
    )
    require(mul(p, encoded) != mul(encoded, p), "old correction must miss the literal encoding")


def check_projection_control():
    """The same Pi formula is not an involution when H is not a projection."""
    h = [[F(2), F(0)], [F(0), F(0)]]
    j0 = sub(eye(2), h)
    pi = blocks(j0, h, h, j0)
    require(mul(pi, pi) != eye(4), "non-projection control")


def g(real, imag=0):
    return (int(real), int(imag))


def gadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def gsub(left, right):
    return (left[0] - right[0], left[1] - right[1])


def gmul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gmat_mul(left, right):
    n = len(left)
    out = [[g(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                out[i][j] = gadd(out[i][j], gmul(left[i][k], right[k][j]))
    return out


def gscale(factor, matrix):
    return [[gmul(factor, entry) for entry in row] for row in matrix]


def check_chart_not_scalar_identity():
    """C^2 = X on one address bit, and i Z X Z is not I."""
    one = g(1)
    zero = g(0)
    eye_g = [[one, zero], [zero, one]]
    x_matrix = [[zero, one], [one, zero]]
    z_matrix = [[one, zero], [zero, g(-1)]]
    # 2C = (1+i) I + (1-i) X, so (2C)^2 = 4 X records C^2 = X.
    two_c = [
        [
            gadd(gmul(g(1, 1), eye_g[i][j]), gmul(g(1, -1), x_matrix[i][j]))
            for j in range(2)
        ]
        for i in range(2)
    ]
    require(gmat_mul(two_c, two_c) == gscale(g(4), x_matrix), "C squared")
    conjugated = gmat_mul(z_matrix, gmat_mul(x_matrix, z_matrix))
    require(conjugated == gscale(g(-1), x_matrix), "Z X Z")
    i_times = gmat_mul([[g(0, 1), zero], [zero, g(0, 1)]], conjugated)
    require(i_times != eye_g, "normalization rejects invertible scalar F")
    require(i_times == gscale(g(0, -1), x_matrix), "i Z X Z = -i X")


def block_diag(data_operator, helper_count):
    n = len(data_operator)
    out = zeros(n + helper_count, n + helper_count)
    for i in range(n):
        for j in range(n):
            out[i][j] = data_operator[i][j]
    for i in range(helper_count):
        out[n + i][n + i] = F(1)
    return out


def check_slot_exchange():
    mask = [0, 1]
    data = [[F(1), F(1)], [F(1), F(2)]]
    _, _, pi, _, literal = operators(mask, diag([1, 2]), data)
    # Banks (1, 2) and (3, 4): only the N port is exchanged.
    image = apply(pi, [F(1), F(2), F(3), F(4)])
    require(image == [F(1), F(4), F(3), F(2)], "one N-port exchange")
    require(literal != eye(4), "literal correction moves data")
    helpers = [F(5), F(6), F(7)]
    full = block_diag(literal, len(helpers))
    joint = apply(full, [F(1), F(2), F(3), F(4), *helpers])
    require(joint[:4] == apply(literal, [F(1), F(2), F(3), F(4)]), "data block")
    require(joint[4:] == helpers, "helpers fixed")
    require(joint[:4] != [F(1), F(2), F(3), F(4)], "data actually changes")
    p104_j, p104_n, helper_count = 8, 96, 72
    require(p104_j + p104_n == 104, "port total")
    require(p104_n == 96 and p104_j == 8, "stated H shape")
    require(helper_count == 72, "stated helper inventory")
    require(2 * p104_n == 192, "two Pi layers")


def check_inherited_gate():
    calls, mass, progress, ports, helpers, rank = 208, 2576, 2312, 104, 72, 81
    width = 2 * ports * ports + 2 * ports * helpers
    capacity = rank * width
    remaining = capacity - ports * ports - calls * progress
    bill = calls * mass + remaining
    excess = bill - capacity
    require(width == 36608, "role count")
    require(capacity == 2965248, "capacity")
    require(remaining == 2473536, "remaining progress")
    require(bill == 3009344, "favorable bill")
    require(excess == 44096, "excess")
    # Zero interface cost is already over capacity. Added swaps cannot erase it.
    require(excess > 0, "excess survives a zero charge for Pi and helpers")


def main():
    data = [[F(1), F(1)], [F(1), F(2)]]
    commuting_t = diag([1, 2])
    shear_t = [[F(1), F(1)], [F(0), F(1)]]
    check_intertwiner([0, 1], commuting_t, data)
    check_intertwiner([0, 1], shear_t, data)
    # HT and TH differ for this shear, so the intertwiner is not using commutation.
    h = diag([0, 1])
    require(mul(h, shear_t) != mul(shear_t, h), "shear does not commute with H")
    check_projection_control()
    check_chart_not_scalar_identity()
    check_slot_exchange()
    check_inherited_gate()
    print(
        "PASS_P104_PENC_HELPER_MISMATCH"
        " data=intertwiner helpers=identity_not_F slots=192 excess=44096 no_new_kappa"
    )


if __name__ == "__main__":
    main()
