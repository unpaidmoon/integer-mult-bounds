"""Exact cyclic invoices for two synchronized recursive modes. Apache-2.0."""

from fractions import Fraction

MAX_N = 64
MAX_H = 8
MAX_WORD = 4096
MAX_RESERVE = 128


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parameters(n: int, h: int) -> None:
    require(type(n) is int and 2 <= n <= MAX_N, "N must be an integer in 2..64")
    require(type(h) is int and 0 <= h <= MAX_H, "h must be an integer in 0..8")


def dyadic(exponent: int) -> Fraction:
    require(type(exponent) is int and abs(exponent) <= MAX_N + MAX_H,
            "dyadic exponent outside the supported stage range")
    if exponent >= 0:
        return Fraction(1 << exponent)
    return Fraction(1, 1 << -exponent)


def minimum_word(n: int, h: int) -> str:
    parameters(n, h)
    a = (2 * h + 1) * (2 * n - 1)
    b = 4 * h + 2
    word = "A" * a + "B" * b
    assert len(word) == (2 * h + 1) * (2 * n + 1)
    assert len(word) <= MAX_WORD
    return word


def stages(n: int, h: int, word: str) -> tuple[tuple[Fraction, Fraction], ...]:
    """Include the last-to-first adapter in the repeated cyclic contract."""
    parameters(n, h)
    require(isinstance(word, str) and 1 <= len(word) <= MAX_WORD,
            "word length must be in 1..4096")
    require(set(word) <= {"A", "B"}, "word alphabet must be A,B")
    a = (dyadic(1), dyadic(-1))
    b = (dyadic(-n), dyadic(n - 1))
    adapter = (dyadic(h), dyadic(h))
    result = []
    for index, letter in enumerate(word):
        result.append(a if letter == "A" else b)
        if letter != word[(index + 1) % len(word)]:
            result.append(adapter)
    assert len(word) <= len(result) <= 2 * len(word)
    return tuple(result)


def invoice(n: int, h: int, word: str) -> tuple[Fraction, Fraction]:
    product = (Fraction(1), Fraction(1))
    for stage in stages(n, h, word):
        product = (product[0] * stage[0], product[1] * stage[1])
    return product


def contractive(product: tuple[Fraction, Fraction]) -> bool:
    require(isinstance(product, tuple) and len(product) == 2
            and all(isinstance(x, Fraction) and x > 0 for x in product),
            "invoice must contain two positive rational coefficients")
    return max(product) < 1


def reserves(n: int, h: int, word: str) -> tuple[tuple[Fraction, Fraction], ...]:
    """Solve v_j = 1 + D_j v_(j+1) for the complete cyclic phase list."""
    factors = stages(n, h, word)
    require(len(factors) <= MAX_RESERVE, "reserve phase count exceeds 128")
    product = invoice(n, h, word)
    require(contractive(product), "reserve requires a strict cyclic contraction")
    result = []
    for start in range(len(factors)):
        prefix = (Fraction(1), Fraction(1))
        total = (Fraction(0), Fraction(0))
        for offset in range(len(factors)):
            total = (total[0] + prefix[0], total[1] + prefix[1])
            stage = factors[(start + offset) % len(factors)]
            prefix = (prefix[0] * stage[0], prefix[1] * stage[1])
        assert prefix == product
        result.append((total[0] / (1 - product[0]), total[1] / (1 - product[1])))
    return tuple(result)
