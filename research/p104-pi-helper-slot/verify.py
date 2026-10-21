#!/usr/bin/env python3
"""Price Pi P_enc Pi on one helper and on the published N-port mask.

The argument is PROOF.md. These checks recompute the identity extension,
the scratch-free slot exchange, and the published scaffold arithmetic.
They do not import the predecessor packages.
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


def matvec(matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


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
                augmented[row][j] - factor * augmented[col][j]
                for j in range(2 * n)
            ]
    return [row[n:] for row in augmented]


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL_P104_PI_HELPER_SLOT " + message)


def published_mask():
    """Pinned H = diag(0_8, I_96) from the two-axis proof. Not a root census."""
    return [0] * 8 + [1] * 96


def scaffold_gate():
    """Recompute PROOF.md section 5 of the two-axis package from its parameters."""
    n = 104
    helpers = 72
    lines = n * n
    roles = 2 * lines + 2 * n * helpers
    width = 81
    calls = 2 * n
    local_mass = 2576
    local_progress = 2312
    progress = width * roles - lines
    remaining = progress - calls * local_progress
    lower = calls * local_mass + remaining
    capacity = width * roles
    return {
        "roles": roles,
        "progress": progress,
        "lower": lower,
        "capacity": capacity,
        "excess": lower - capacity,
    }


def apply_diagonal_pi(r, w, helper, diagonal):
    """Linear Pi for a diagonal H, including diagonals that are not projections."""
    out_r = []
    out_w = []
    for i, h_ii in enumerate(diagonal):
        j_ii = F(1) - h_ii
        out_r.append(j_ii * r[i] + h_ii * w[i])
        out_w.append(h_ii * r[i] + j_ii * w[i])
    return out_r, out_w, helper


def apply_pi(r, w, helper, mask):
    require(all(bit in (0, 1) for bit in mask), "slot swap requires a projection mask")
    return apply_diagonal_pi(r, w, helper, [F(bit) for bit in mask])


def apply_h(vector, mask):
    return [vector[i] if mask[i] else F(0) for i in range(len(mask))]


def apply_l(r, w, helper, data, t_matrix, mask):
    mixed = matvec(data, r)
    htw = apply_h(matvec(t_matrix, w), mask)
    return [mixed[i] + htw[i] for i in range(len(mask))], w[:], helper


def apply_l_inverse(r, w, helper, data_inverse, t_matrix, mask):
    htw = apply_h(matvec(t_matrix, w), mask)
    adjusted = [r[i] - htw[i] for i in range(len(mask))]
    return matvec(data_inverse, adjusted), w[:], helper


def apply_p(r, w, helper, k_matrix):
    return r[:], [w[i] + matvec(k_matrix, r)[i] for i in range(len(w))], helper


def apply_q(r, w, helper, data, data_inverse, t_matrix, k_matrix, mask):
    r, w, helper = apply_pi(r, w, helper, mask)
    r, w, helper = apply_l_inverse(r, w, helper, data_inverse, t_matrix, mask)
    r, w, helper = apply_p(r, w, helper, k_matrix)
    r, w, helper = apply_l(r, w, helper, data, t_matrix, mask)
    return apply_pi(r, w, helper, mask)


def apply_a(r, w, helper, data, t_matrix, mask):
    r, w, helper = apply_l(r, w, helper, data, t_matrix, mask)
    return apply_pi(r, w, helper, mask)


def apply_p_enc(r, w, helper, data, data_inverse, t_matrix, k_matrix, mask):
    r, w, helper = apply_l_inverse(r, w, helper, data_inverse, t_matrix, mask)
    r, w, helper = apply_p(r, w, helper, k_matrix)
    return apply_l(r, w, helper, data, t_matrix, mask)


def exchange_port(x, y):
    """Scratch-free swap by three additions. Returns steps, then the pair."""
    x = x + y
    first = (x, y)
    y = x - y
    x = x - y
    return first, (x, y)


def exchange_slots(r, w, helper, mask):
    additions = 0
    out_r = r[:]
    out_w = w[:]
    for i, bit in enumerate(mask):
        if not bit:
            continue
        _first, (out_r[i], out_w[i]) = exchange_port(out_r[i], out_w[i])
        additions += 3
    return out_r, out_w, helper, additions


def gaussian_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def gaussian_sub(left, right):
    return (left[0] - right[0], left[1] - right[1])


def gaussian_exchange(x, y):
    x = gaussian_add(x, y)
    y = gaussian_sub(x, y)
    x = gaussian_sub(x, y)
    return x, y


def check_exchange_program():
    first, swapped = exchange_port(F(4), F(9))
    require(first == (F(13), F(9)), "first addition is not yet the swap")
    require(swapped == (F(9), F(4)), "three additions swap the port")
    require(gaussian_exchange((1, 1), (2, -1)) == ((2, -1), (1, 1)), "Gaussian swap")
    broken_x, broken_y = F(4) + F(9), F(9)
    broken_y = broken_x - broken_y
    require((broken_x, broken_y) != (F(9), F(4)), "two additions do not swap")


def check_mask_and_gate():
    mask = published_mask()
    require(len(mask) == 104, "published mask length")
    require(mask[:8] == [0] * 8 and mask[8:] == [1] * 96, "published J/N split")
    swaps = sum(mask)
    require(swaps == 96, "swap count")
    r = [F(i + 1) for i in range(104)]
    w = [F(1000 + i) for i in range(104)]
    helper = F(-11)
    by_pi = apply_pi(r, w, helper, mask)
    by_exchange = exchange_slots(r, w, helper, mask)
    require(by_exchange[:3] == by_pi, "exchange realizes Pi")
    require(by_exchange[3] == 288, "288 additions")
    require(by_exchange[2] == helper and by_pi[2] == helper, "helper fixed by both")
    for i in range(8):
        require(by_pi[0][i] == r[i] and by_pi[1][i] == w[i], "J port fixed")
    for i in range(8, 104):
        require(by_pi[0][i] == w[i] and by_pi[1][i] == r[i], "N port swapped")
    # A helper-moving permutation is a different operator.
    moved = (by_pi[0], by_pi[1], helper + 1)
    require(moved != by_pi, "moving the helper leaves Pi")
    gate = scaffold_gate()
    require(gate["roles"] == 36608, "role count")
    require(gate["progress"] == 2954432, "persistent progress")
    require(gate["lower"] == 3009344, "lower mass")
    require(gate["capacity"] == 2965248, "capacity")
    require(gate["excess"] == 44096, "excess")
    require(gate["excess"] + 288 == 44384, "rank-1 reading of the exchange still fails")
    require(gate["excess"] > 81, "one helper chart gap does not clear the excess")
    return gate


def products_commute(left, right):
    n = len(left)
    left_right = zeros(n, n)
    right_left = zeros(n, n)
    for i in range(n):
        for k in range(n):
            for j in range(n):
                left_right[i][j] += left[i][k] * right[k][j]
                right_left[i][j] += right[i][k] * left[k][j]
    return left_right == right_left


def check_intertwiner(mask, data, t_matrix, k_matrix, samples):
    require(all(bit in (0, 1) for bit in mask), "H is a 0/1 projection")
    data_inverse = inverse(data)
    n = len(mask)
    separated = {"bare": False, "old": False}
    for r, w, helper in samples:
        require(len(r) == n and len(w) == n, "sample width")
        left = apply_q(
            *apply_a(r, w, helper, data, t_matrix, mask),
            data,
            data_inverse,
            t_matrix,
            k_matrix,
            mask,
        )
        right = apply_a(*apply_p(r, w, helper, k_matrix), data, t_matrix, mask)
        require(left == right, "Q A = A P")
        require(left[2] == helper and right[2] == helper, "dirty helper restored")
        bare = apply_p_enc(
            *apply_a(r, w, helper, data, t_matrix, mask),
            data,
            data_inverse,
            t_matrix,
            k_matrix,
            mask,
        )
        old = apply_p(*apply_a(r, w, helper, data, t_matrix, mask), k_matrix)
        if bare != right:
            separated["bare"] = True
        if old != right:
            separated["old"] = True
    require(separated["bare"], "P_enc alone misses the literal slots")
    require(separated["old"], "old P misses the literal slots")


def check_nonprojection():
    diagonal = [F(0), F(2)]
    r, w, helper = [F(1), F(2)], [F(3), F(4)], F(5)
    once = apply_diagonal_pi(r, w, helper, diagonal)
    twice = apply_diagonal_pi(*once, diagonal)
    require(twice[2] == helper, "even a bad diagonal fixes the helper coordinate")
    require(twice[:2] != (r, w), "a non-projection is not an involution")
    projection = apply_diagonal_pi(r, w, helper, [F(0), F(1)])
    require(projection == apply_pi(r, w, helper, [0, 1]), "projection formula is the slot swap")


def main():
    check_exchange_program()
    gate = check_mask_and_gate()
    # Small witness: D does not commute with T, and T does not commute with H.
    mask = [0, 0, 1, 1]
    data = [
        [F(1), F(1), F(0), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(0), F(0), F(1), F(1)],
        [F(0), F(0), F(0), F(1)],
    ]
    t_matrix = [
        [F(1), F(0), F(1), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(1), F(0), F(2), F(0)],
        [F(0), F(0), F(0), F(3)],
    ]
    require(not products_commute(data, t_matrix), "witness D and T do not commute")
    require(not products_commute(diag(mask), t_matrix), "witness H and T do not commute")
    k_matrix = inverse(t_matrix)
    samples = [
        ([F(1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], F(0)),
        ([F(2), F(-1), F(5), F(7)], [F(3), F(4), F(8), F(1)], F(-3)),
        ([F(0), F(0), F(1), F(1)], [F(9), F(0), F(0), F(2)], Fraction(1, 2)),
    ]
    check_intertwiner(mask, data, t_matrix, k_matrix, samples)
    # Published mask, with D = I and distinct positive scales. This checks the
    # extension at n = 104; it is not the physical pivot B0.
    wide = published_mask()
    wide_data = eye(104)
    wide_t = diag([F(i + 1) for i in range(104)])
    wide_k = inverse(wide_t)
    wide_samples = [
        (
            [F((i * 3) % 5) for i in range(104)],
            [F((i * 7) % 11) for i in range(104)],
            F(13),
        )
    ]
    check_intertwiner(wide, wide_data, wide_t, wide_k, wide_samples)
    check_nonprojection()
    print(
        "PASS_P104_PI_HELPER_SLOT "
        "swaps=96 additions=288 helper_fixed=1 chart_gap=81 "
        "excess=%s favorable=0 no_new_kappa" % gate["excess"]
    )


if __name__ == "__main__":
    main()
