"""Independent free-block certificate for the PR6280 consumer.

Prepared for @CubeJerry with OpenAI Codex assistance. Apache-2.0.
Only AB=1 is reduced. In particular BA, GA and BG are not commuted.
"""
from fractions import Fraction


def require(ok, message):
    if not ok:
        raise ValueError(message)


def normal(word):
    """Unique normal form: the length-reducing rule AB -> empty has no overlaps."""
    stack = []
    for letter in word:
        if stack and stack[-1] == "A" and letter == "B":
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def atom(name):
    return {(name,): Fraction(1)}


ZERO = {}
ONE = {(): Fraction(1)}


def add(*terms):
    answer = {}
    for term in terms:
        for word, coefficient in term.items():
            answer[word] = answer.get(word, 0) + coefficient
    return {w: c for w, c in answer.items() if c}


def scale(term, coefficient):
    return {w: c * coefficient for w, c in term.items() if c * coefficient}


def mul(*terms):
    answer = ONE
    for term in terms:
        products = {}
        for left, lc in answer.items():
            for right, rc in term.items():
                key = normal(left + right)
                products[key] = products.get(key, 0) + lc * rc
        answer = {w: c for w, c in products.items() if c}
    return answer


def mm(left, right):
    return [[add(*(mul(left[i][k], right[k][j]) for k in range(2)))
             for j in range(2)] for i in range(2)]


def chain(*chronological):
    value = [[ONE, ZERO], [ZERO, ONE]]
    for step in chronological:
        value = mm(step, value)
    return value


def typed(matrix):
    """A:X->Z, B:Z->X, and G/H/J:Z->Z; each block has its actual type."""
    types = {"A": ("X", "Z"), "B": ("Z", "X"),
             "G": ("Z", "Z"), "H": ("Z", "Z"), "J": ("Z", "Z")}
    objects = ("X", "Z")
    for i in range(2):
        for j in range(2):
            for word in matrix[i][j]:
                current = objects[j]
                for letter in reversed(word):
                    domain, codomain = types[letter]
                    require(current == domain, "ILL_TYPED_WORD")
                    current = codomain
                require(current == objects[i], "ILL_TYPED_BLOCK")


def check():
    a, b, g, h, j = (atom(s) for s in "ABGHJ")
    q = add(ONE, scale(mul(b, a), -1))
    s = [[q, b], [a, ZERO]]
    upper = [[ONE, b], [ZERO, ONE]]
    lower = [[ONE, ZERO], [a, ONE]]
    upper_negative = [[ONE, scale(b, -1)], [ZERO, ONE]]
    lower_negative = [[ONE, ZERO], [scale(a, -1), ONE]]
    sign = [[ONE, ZERO], [ZERO, scale(ONE, -1)]]
    ident = [[ONE, ZERO], [ZERO, ONE]]

    def use(f):
        return [[ONE, ZERO], [ZERO, f]]

    def induced(f):
        return [[add(q, mul(b, f, a)), ZERO], [ZERO, ONE]]

    equations = {
        "repeat_b": (chain(upper, lower_negative, upper, sign), s),
        "repeat_a": (chain(sign, lower, upper_negative, lower), s),
        "involution": (chain(s, s), ident),
        "one_consumer": (chain(s, use(g), s), induced(g)),
        "ordered_composition": (chain(induced(g), induced(h)), induced(mul(h, g))),
        "three_consumer_fusion": (
            chain(s, use(g), s, s, use(h), s, s, use(j), s),
            chain(s, use(g), use(h), use(j), s)),
        "three_consumer_target": (
            chain(s, use(g), use(h), use(j), s), induced(mul(j, h, g))),
    }
    for name, (actual, expected) in equations.items():
        typed(actual)
        typed(expected)
        require(actual == expected, "NC_IDENTITY_" + name)
    # These are nonzero symbolic defects, not failures of a sampled matrix.
    defects = {
        "native_order": chain(s, use(h), use(g), s) != induced(mul(h, g)),
        "missing_final_exchange": chain(s, use(g)) != induced(g),
        "omitted_sign": chain(upper, lower_negative, upper) != s,
        "BA_not_identity": mul(b, a) != ONE,
    }
    require(all(defects.values()), "NC_CONTROL_DID_NOT_DISTINGUISH")
    return {"universal_block_identities": len(equations),
            "nonzero_free_defects": len(defects),
            "rewrite_relation": "AB=I_Z only; no commutations"}
