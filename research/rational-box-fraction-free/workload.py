"""Declared complete CLI fixture, with a known exact optimum.

Produced by Nick Petalas. Apache-2.0.
"""


def problem():
    """Maximize alternating prices under a six-cycle's adjacent upper bounds."""
    return {
        "schema": "rational-box-lp/v1",
        "objective": [1, -2, 3, -4, 5, -6],
        "lower": [-1] * 6,
        "upper": [2] * 6,
        "feasible": [0] * 6,
        "constraints": [
            {"coefficients": [int(j in (i, (i + 1) % 6)) for j in range(6)],
             "bound": "1/3"}
            for i in range(6)
        ],
    }
