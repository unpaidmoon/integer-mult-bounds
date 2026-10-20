"""Minimal X-character monomial multiplication for the cut58 floor.

The composition and polar-rank rules are the ones in Ross Richardson's
quadratic-chart code (PR #4082 source `root-chronology/quadratic_charts.py`),
trimmed to the operations this package uses. Apache-2.0.
"""
from dataclasses import dataclass
from functools import lru_cache

def need(cond, message):
    if not cond:
        raise ValueError(message)

def parity(x):
    return x.bit_count() & 1

def linear(rows, x):
    return sum(parity(r & x) << i for i, r in enumerate(rows))

def inverse(rows):
    n = len(rows)
    aug = [r | (1 << (n + i)) for i, r in enumerate(rows)]
    for i in range(n):
        pivot = next((j for j in range(i, n) if aug[j] >> i & 1), None)
        need(pivot is not None, "address rows must be invertible")
        aug[i], aug[pivot] = aug[pivot], aug[i]
        for j in range(n):
            if j != i and aug[j] >> i & 1:
                aug[j] ^= aug[i]
    return tuple(r >> n for r in aug)

@lru_cache(None)
def rank(rows):
    basis = {}
    for r in rows:
        while r:
            bit = r.bit_length() - 1
            if bit in basis:
                r ^= basis[bit]
            else:
                basis[bit] = r
                break
    return len(basis)

@dataclass(frozen=True)
class Mono:
    rows: tuple
    offset: int
    alpha: tuple
    quad: tuple
    constant: int = 0
    global_phase: int = 0

    def q(self, x):
        return (self.constant + sum(a for i, a in enumerate(self.alpha) if x >> i & 1)
                + 2 * sum(parity(r & x) for i, r in enumerate(self.quad) if x >> i & 1)) % 4

    def act(self, x):
        return linear(self.rows, x) ^ self.offset

    def __matmul__(self, other):
        return compose(self, other)

    def inv(self):
        return adjoint(self)

    def polar(self):
        form = [(self.alpha[i] & 1) << i for i in range(len(self.rows))]
        for i, row in enumerate(self.quad):
            for j in range(i + 1, len(form)):
                if row >> j & 1:
                    form[i] ^= 1 << j
                    form[j] ^= 1 << i
        return tuple(form)

def from_function(rows, offset, fn, global_phase=0):
    n = len(rows)
    c = fn(0) % 4
    alpha = tuple((fn(1 << i) - c) % 4 for i in range(n))
    quad = []
    for i in range(n):
        row = 0
        for j in range(i + 1, n):
            z = (fn((1 << i) | (1 << j)) - c - alpha[i] - alpha[j]) % 4
            need(z % 2 == 0, "phase must be quadratic")
            row |= (z // 2) << j
        quad.append(row)
    return Mono(tuple(rows), offset, alpha, tuple(quad), c, global_phase % 4)

@lru_cache(None)
def compose(a, b):
    n = len(a.rows)
    rows = tuple(
        sum(parity(a.rows[i] & sum(((b.rows[k] >> j) & 1) << k for k in range(n))) << j
            for j in range(n))
        for i in range(n))
    return from_function(
        rows, linear(a.rows, b.offset) ^ a.offset,
        lambda x: b.q(x) + a.q(b.act(x)), a.global_phase + b.global_phase)

@lru_cache(None)
def adjoint(a):
    rows = inverse(a.rows)
    off = linear(rows, a.offset)
    return from_function(rows, off, lambda x: -a.q(linear(rows, x) ^ off), -a.global_phase)

def identity(n):
    return Mono(tuple(1 << i for i in range(n)), 0, (0,) * n, (0,) * n)

def decode(data):
    return Mono(tuple(data["rows"]), data["offset"], tuple(data["alpha"]), tuple(data["quad"]),
                data.get("constant", 0), data.get("global_phase", 0))

def signature(g):
    return (g.rows, g.offset, g.alpha, g.quad, g.constant, g.global_phase)
