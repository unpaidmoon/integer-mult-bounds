"""Constructive support-stability certificate; no predecessor implementation.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance. Apache-2.0.
"""

from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalized(matrix, prime=None):
    require(prime in (None, 2, 3, 5, 7), "unsupported field")
    require(isinstance(matrix, list) and 1 <= len(matrix) <= 104, "matrix size")
    n = len(matrix)
    require(all(isinstance(row, list) and len(row) == n for row in matrix), "square matrix")
    require(all(type(x) in (int, Fraction) for row in matrix for x in row), "exact entries")
    rows = []
    for row in matrix:
        values = []
        for x in row:
            x = Fraction(x)
            if prime is None:
                values.append(x)
            else:
                require(x.denominator % prime != 0, "field denominator")
                values.append(x.numerator * pow(x.denominator, -1, prime) % prime)
        rows.append(values)
    require(all(rows[i][i] == 1 for i in range(n)), "unit diagonal")
    return rows


def rank(matrix, prime=None):
    rows = [row[:] for row in matrix]
    n, out = len(rows), 0
    for col in range(n):
        pivot = next((i for i in range(out, n) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[out], rows[pivot] = rows[pivot], rows[out]
        inverse = 1 / rows[out][col] if prime is None else pow(rows[out][col], -1, prime)
        for i in range(out + 1, n):
            coefficient = rows[i][col] * inverse
            if not coefficient:
                continue
            for j in range(col, n):
                rows[i][j] -= coefficient * rows[out][j]
                if prime is not None:
                    rows[i][j] %= prime
        out += 1
    return out


def strongly_connected(adjacency, active):
    """Tarjan decomposition; the certificate consumer uses reachability instead."""
    counter, stack, on_stack, low, ids, groups = 0, [], set(), {}, {}, []

    def visit(v):
        nonlocal counter
        ids[v] = low[v] = counter
        counter += 1
        stack.append(v)
        on_stack.add(v)
        for w in sorted(adjacency[v] & active):
            if w not in ids:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], ids[w])
        if low[v] == ids[v]:
            group = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                group.append(w)
                if w == v:
                    break
            groups.append(sorted(group))

    for v in sorted(active):
        if v not in ids:
            visit(v)
    return sorted(groups)


def cycle_singular(matrix, cycle, prime):
    product = Fraction(1) if prime is None else 1
    for i, j in zip(cycle, cycle[1:] + cycle[:1]):
        product *= matrix[i][j]
        if prime is not None:
            product %= prime
    determinant = 1 + (-1) ** (len(cycle) - 1) * product
    return determinant == 0 if prime is None else determinant % prime == 0


def block_form(matrix, keep, prime=None):
    """Return a visible reciprocal-pair/singleton partition, or reject."""
    keep = set(keep)
    pairs, singletons, seen = [], [], set()
    for i in sorted(keep):
        if i in seen:
            continue
        outgoing = [j for j in sorted(keep) if i != j and matrix[i][j]]
        incoming = [j for j in sorted(keep) if i != j and matrix[j][i]]
        if not outgoing and not incoming:
            singletons.append(i)
            seen.add(i)
            continue
        require(len(outgoing) == len(incoming) == 1 and outgoing == incoming,
                "residual is not a reciprocal block sum")
        j = outgoing[0]
        require(j not in seen and all(not matrix[j][k] and not matrix[k][j]
                for k in keep - {i, j}), "residual cross-block edge")
        value = matrix[i][j] * matrix[j][i]
        require((value if prime is None else value % prime) == 1,
                "residual pair is not rank one")
        pairs.append([i, j])
        seen.update((i, j))
    return pairs, singletons


def construct(matrix, prime=None):
    matrix = normalized(matrix, prime)
    n = len(matrix)
    adjacency = [{j for j in range(n) if j != i and matrix[i][j]} for i in range(n)]
    active, peeled = set(range(n)), []
    while True:
        components = strongly_connected(adjacency, active)
        cyclic = {v for group in components if len(group) > 1 for v in group}
        degree = {v: len(adjacency[v] & active) + sum(v in adjacency[w] for w in active)
                  for v in cyclic}
        candidate = next((v for v in sorted(cyclic) if degree[v] >= 3), None)
        if candidate is None:
            break
        peeled.append([candidate, degree[candidate]])
        active.remove(candidate)
    cycles = []
    for group in components:
        if len(group) == 1:
            continue
        cycle, start = [], min(group)
        v = start
        while not cycle or v != start:
            cycle.append(v)
            choices = adjacency[v] & active
            require(len(choices) == 1, "non-cycle residual component")
            v = next(iter(choices))
        require(set(cycle) == set(group), "cycle partition")
        cycles.append(cycle)
    cycle_vertices = {v for cycle in cycles for v in cycle}
    dag = active - cycle_vertices
    dag_order, unplaced = [], set(dag)
    while unplaced:
        v = next((v for v in sorted(unplaced)
                  if not any(v in adjacency[w] for w in unplaced)), None)
        require(v is not None, "residual DAG")
        dag_order.append(v)
        unplaced.remove(v)
    deleted = {v for v, _ in peeled}
    for cycle in cycles:
        if len(cycle) > 2:
            deleted.update(cycle[1:])
        elif not cycle_singular(matrix, cycle, prime):
            deleted.add(cycle[0])
    deleted.update(v for v in dag if adjacency[v] & dag)
    pairs, singletons = block_form(matrix, set(range(n)) - deleted, prime)
    r = rank(matrix, prime)
    m = sum(map(len, adjacency))
    d_value = sum(degree - 2 for _, degree in peeled)
    l_value = sum(len(cycle) - 2 for cycle in cycles)
    e_value = sum(len(adjacency[v] & dag) for v in dag)
    delta = r - (n - len(peeled) - len(cycles))
    return {
        "schema": "support-stability/1", "field": "Q" if prime is None else f"F{prime}",
        "n": n, "rank": r, "support": m, "excess": m - 2 * (n - r),
        "peeled": peeled, "cycles": cycles, "dag_order": dag_order,
        "D": d_value, "L": l_value, "E": e_value, "delta": delta,
        "deleted": sorted(deleted), "pairs": pairs, "singletons": singletons,
    }


def validate_certificate(matrix, certificate, prime=None):
    """Check the emitted witness without Tarjan or the deletion constructor."""
    matrix = normalized(matrix, prime)
    n, cert = len(matrix), certificate
    require(isinstance(cert, dict) and cert.get("schema") == "support-stability/1", "schema")
    require(cert.get("field") == ("Q" if prime is None else f"F{prime}"), "field tag")
    require(type(cert.get("n")) is int and cert["n"] == n, "dimension tag")
    adjacency = [{j for j in range(n) if i != j and matrix[i][j]} for i in range(n)]
    active, d_value = set(range(n)), 0
    require(type(cert.get("peeled")) is list, "peel list")
    for step in cert["peeled"]:
        require(type(step) is list and len(step) == 2 and all(type(x) is int for x in step),
                "peel shape")
        v, degree = step
        require(v in active, "peel index")
        seen, queue = set(), list(adjacency[v] & active)
        while queue:
            w = queue.pop()
            if w not in seen:
                seen.add(w)
                queue.extend((adjacency[w] & active) - seen)
        require(v in seen, "peeled vertex is not cyclic")
        actual_degree = len(adjacency[v] & active) + sum(v in adjacency[w] for w in active)
        require(degree == actual_degree and degree >= 3, "peel degree")
        d_value += degree - 2
        active.remove(v)
    require(type(cert.get("cycles")) is list and type(cert.get("dag_order")) is list,
            "residual partition type")
    cycles, dag_order = cert["cycles"], cert["dag_order"]
    require(all(type(cycle) is list and len(cycle) >= 2 for cycle in cycles), "cycle shape")
    flat = [v for cycle in cycles for v in cycle] + dag_order
    require(all(type(v) is int for v in flat) and len(set(flat)) == len(flat)
            and set(flat) == active, "residual partition")
    u_value = 0
    for cycle in cycles:
        for i, j in zip(cycle, cycle[1:] + cycle[:1]):
            require(adjacency[i] & active == {j}, "cycle edge")
            require({w for w in active if i in adjacency[w]} == {cycle[cycle.index(i) - 1]},
                    "cycle incoming edge")
        u_value += not cycle_singular(matrix, cycle, prime)
    dag = set(dag_order)
    positions = {v: k for k, v in enumerate(dag_order)}
    require(all(positions[i] < positions[j] for i in dag for j in adjacency[i] & dag),
            "DAG order")
    r, m = rank(matrix, prime), sum(map(len, adjacency))
    h, c = len(cert["peeled"]), len(cycles)
    l_value = sum(len(cycle) - 2 for cycle in cycles)
    e_value = sum(len(adjacency[v] & dag) for v in dag)
    delta = r - (n - h - c)
    excess = m - 2 * (n - r)
    expected = {"rank": r, "support": m, "excess": excess, "D": d_value,
                "L": l_value, "E": e_value, "delta": delta}
    require(all(type(cert.get(k)) is int and cert[k] == v for k, v in expected.items()),
            "accounting fields")
    require(d_value >= h and delta >= u_value >= 0, "rank and peel lower bounds")
    require(m == 2 * h + d_value + 2 * c + l_value + e_value, "support accounting")
    require(excess == d_value + l_value + e_value + 2 * delta >= 0, "excess identity")
    deleted = cert.get("deleted")
    require(type(deleted) is list and all(type(v) is int and 0 <= v < n for v in deleted)
            and len(set(deleted)) == len(deleted), "deleted set")
    require(len(deleted) <= 2 * excess, "deletion budget")
    pairs, singletons = block_form(matrix, set(range(n)) - set(deleted), prime)
    require(cert.get("pairs") == pairs and cert.get("singletons") == singletons,
            "block certificate")
    return True
