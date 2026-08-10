"""Exact and near recurrence for linear flows on a two-torus."""

from __future__ import annotations

from fractions import Fraction
from math import sqrt
from typing import Iterator


def rational_torus_exact_period(vx: Fraction, vy: Fraction) -> int:
    """Return a positive integer period for a rational velocity vector.

    On q(t)=(vx*t, vy*t) mod 1, an integer period is the least common multiple
    of the two denominators after reduction.
    """
    from math import lcm

    if vx == 0 and vy == 0:
        return 1
    return lcm(vx.denominator, vy.denominator)


def irrational_torus_return_error(q: int) -> float:
    """Distance of (q, sqrt(2) q) mod 1 from the origin in the second coordinate.

    The first coordinate is exactly zero modulo one at integer time q.
    """
    if q <= 0:
        raise ValueError("q must be positive")
    value = sqrt(2.0) * q
    nearest = round(value)
    return abs(value - nearest)


def sqrt2_convergents(limit_denominator: int) -> Iterator[Fraction]:
    """Yield continued-fraction convergents p/q to sqrt(2)."""
    if limit_denominator < 1:
        return
    p_nm2, p_nm1 = 0, 1
    q_nm2, q_nm1 = 1, 0
    while True:
        a = 1 if q_nm1 == 0 else 2
        p = a * p_nm1 + p_nm2
        q = a * q_nm1 + q_nm2
        if q > limit_denominator:
            return
        yield Fraction(p, q)
        p_nm2, p_nm1 = p_nm1, p
        q_nm2, q_nm1 = q_nm1, q


def exact_positive_recurrence_for_sqrt2_flow() -> bool:
    """Return False for q(t)=(t,sqrt(2)t) mod 1.

    Exact recurrence at T>0 would require T integer and sqrt(2)T integer.
    Their ratio would make sqrt(2) rational, a contradiction.
    """
    return False
