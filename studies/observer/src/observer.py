"""Operational observer-distance utilities for recurrence studies."""

from __future__ import annotations

from math import isclose
from typing import Iterable, Sequence


def total_variation(p: Sequence[float], q: Sequence[float]) -> float:
    """Total-variation distance between two finite probability distributions."""
    if len(p) != len(q):
        raise ValueError("distributions must have the same length")
    if any(x < 0 for x in p) or any(x < 0 for x in q):
        raise ValueError("probabilities must be nonnegative")
    if not isclose(sum(p), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("p must sum to one")
    if not isclose(sum(q), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("q must sum to one")
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def helstrom_success_probability(trace_distance: float) -> float:
    """Optimal one-shot binary discrimination success for equal priors.

    For quantum states rho and sigma with trace distance D,
    P_correct = (1 + D) / 2.
    """
    if not 0.0 <= trace_distance <= 1.0:
        raise ValueError("trace distance must lie in [0,1]")
    return 0.5 * (1.0 + trace_distance)


def finite_horizon_max_distance(
    history_a: Iterable,
    history_b: Iterable,
    metric,
) -> float:
    """Maximum observer distance across aligned finite histories."""
    a = list(history_a)
    b = list(history_b)
    if len(a) != len(b):
        raise ValueError("histories must have the same length")
    if not a:
        return 0.0
    return max(float(metric(x, y)) for x, y in zip(a, b))


def mask_hamming(mask_text_a: str, mask_text_b: str) -> int:
    """Velocity-bit Hamming distance for space-separated HPP cell masks."""
    a = [int(x) for x in mask_text_a.split()]
    b = [int(x) for x in mask_text_b.split()]
    if len(a) != len(b):
        raise ValueError("mask strings must describe equal-sized states")
    return sum((x ^ y).bit_count() for x, y in zip(a, b))


def first_below(rows: Sequence[dict], key: str, epsilon: float) -> dict:
    """Return first row in order whose numeric key lies below epsilon."""
    for row in rows:
        if float(row[key]) < epsilon:
            return row
    raise LookupError(f"no row below epsilon={epsilon}")
