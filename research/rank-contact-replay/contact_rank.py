"""Exact bounded binary-subspace intersection engine. Apache-2.0.

The implementation was produced by Nick Petalas. Rank-nullity and binary
Gaussian elimination are classical; this module changes no contact formula.
"""

from collections.abc import Iterable


def binary_basis(rows: Iterable[int], width: int) -> tuple[int, ...]:
    """Internal elimination: callers bound row counts and coordinate widths."""
    pivots = [0] * width
    for row in rows:
        value = row
        for bit in range(width - 1, -1, -1):
            if not value & (1 << bit):
                continue
            if pivots[bit]:
                value ^= pivots[bit]
            else:
                pivots[bit] = value
                break
    return tuple(value for value in pivots if value)


def checked_basis(space: frozenset[int], n: int) -> tuple[int, ...]:
    """Validate the complete subspace, including its promised dimension."""
    if not isinstance(space, frozenset) or len(space) != 1 << n:
        raise ValueError("Expected a complete n-dimensional frozen subspace")
    if any(type(x) is not int or not 0 <= x < 1 << (2 * n) for x in space):
        raise ValueError("Subspace coordinate outside the binary ambient space")
    result = binary_basis(space, 2 * n)
    if len(result) != n:
        raise ValueError("Subspace cardinality and span dimension disagree")
    # Every input lies in this span. Equal cardinalities therefore imply equality.
    assert len(space) == 1 << len(result)
    return result


class ContactRank:
    """One-contact cache, owned by one replay; no global retained subspaces."""

    def __init__(self) -> None:
        self.u: frozenset[int] | None = None
        self.v: frozenset[int] | None = None
        self.n = 0
        self.ub: tuple[int, ...] = ()
        self.vb: tuple[int, ...] = ()
        self.old_rank = 0
        self.calls = 0
        self.preparations = 0

    def __call__(self, u: frozenset[int], v: frozenset[int], axis: int,
                 n: int) -> int:
        if type(n) is not int or not 1 <= n <= 9:
            raise ValueError("Supported contact widths are integers 1 through 9")
        if type(axis) is not int or not 0 <= axis < 1 << (2 * n):
            raise ValueError("Axis outside the binary ambient space")
        if u is not self.u or v is not self.v or n != self.n:
            # Prepare completely before publishing a new cache entry.
            ub, vb = checked_basis(u, n), checked_basis(v, n)
            old_rank = len(binary_basis(ub + vb, 2 * n))
            self.u, self.v, self.n = u, v, n
            self.ub, self.vb, self.old_rank = ub, vb, old_rank
            self.preparations += 1
        mask = (1 << n) - 1
        low, high = axis & mask, axis >> n
        moved = tuple(x ^ (axis if (((x & mask) & high).bit_count()
                                  + ((x >> n) & low).bit_count()) & 1 else 0)
                      for x in self.ub)
        new_rank = len(binary_basis(self.vb + moved, 2 * n))
        self.calls += 1
        result = new_rank - self.old_rank
        assert -1 <= result <= 1
        return result
