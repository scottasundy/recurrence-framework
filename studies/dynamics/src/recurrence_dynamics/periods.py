"""Exact period constraints and phase navigation for reversible HPP dynamics.

Finite-model results only. These utilities do not imply that physical reality
is finite, recurrent, or described by HPP dynamics.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm

from .hpp import (
    EAST, NORTH, SOUTH, WEST, Microstate,
    inverse_step, particle_number, step,
)


@dataclass(frozen=True)
class BrentResult:
    period: int
    evaluations: int


@dataclass(frozen=True)
class PhaseLocation:
    phase: int
    period: int
    residue: int
    residue_modulus: int
    direction: str
    updates_evaluated: int


def advance(state: Microstate, size: int, count: int, *, forward: bool = True) -> Microstate:
    if count < 0:
        raise ValueError("count must be nonnegative")
    update = step if forward else inverse_step
    for _ in range(count):
        state = update(state, size, size)
    return state


def brent_period(initial: Microstate, size: int, *, cap: int = 2_000_000) -> BrentResult:
    """Least first-return period using O(1) stored states."""
    if cap <= 0:
        raise ValueError("cap must be positive")
    power = lam = 1
    tortoise = initial
    hare = step(initial, size, size)
    evaluations = 1
    while tortoise != hare:
        if evaluations >= cap:
            raise RuntimeError(
                f"No recurrence detected within cap={cap}; this is not evidence of no recurrence."
            )
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = step(hare, size, size)
        evaluations += 1
        lam += 1
    if advance(initial, size, lam) != initial:
        raise AssertionError("exact-return check failed")
    return BrentResult(lam, evaluations)


def transport_clock(state: Microstate, size: int) -> int:
    """Phi = sum_E x - sum_W x - sum_N y + sum_S y (mod L)."""
    total = 0
    for i, mask in enumerate(state):
        x, y = i % size, i // size
        if mask & EAST: total += x
        if mask & WEST: total -= x
        if mask & NORTH: total -= y
        if mask & SOUTH: total += y
    return total % size


def transport_phase_residue(reference: Microstate, target: Microstate, size: int):
    n = particle_number(reference)
    if particle_number(target) != n:
        raise ValueError("particle-number mismatch")
    d = gcd(n, size)
    modulus = size // d
    if modulus == 1:
        return 0, 1
    delta = (transport_clock(target, size) - transport_clock(reference, size)) % size
    if delta % d:
        raise ValueError("target is outside the transport sector")
    residue = ((delta // d) * pow((n // d) % modulus, -1, modulus)) % modulus
    return residue, modulus


def _rotate_right(values, count):
    count %= len(values)
    return values if count == 0 else values[-count:] + values[:-count]


def diagonal_species_histograms(state: Microstate, size: int):
    """Histograms of E+N, E+S, W+N, W+S on matching diagonal coordinates."""
    hist = [[0] * size for _ in range(4)]
    for i, mask in enumerate(state):
        x, y = i % size, i // size
        e = int(bool(mask & EAST)); n = int(bool(mask & NORTH))
        s = int(bool(mask & SOUTH)); w = int(bool(mask & WEST))
        hist[0][(x - y) % size] += e + n
        hist[1][(x + y) % size] += e + s
        hist[2][(-x - y) % size] += w + n
        hist[3][(-x + y) % size] += w + s
    return tuple(tuple(v) for v in hist)


def rotated_histograms(histograms, count):
    return tuple(_rotate_right(values, count) for values in histograms)


def histogram_rotation_period(histograms) -> int:
    size = len(histograms[0])
    for p in range(1, size + 1):
        if rotated_histograms(histograms, p) == histograms:
            return p
    raise AssertionError("rotation by L must close")


def histogram_phase_residue(reference: Microstate, target: Microstate, size: int):
    h0 = diagonal_species_histograms(reference, size)
    ht = diagonal_species_histograms(target, size)
    modulus = histogram_rotation_period(h0)
    for residue in range(modulus):
        if rotated_histograms(h0, residue) == ht:
            return residue, modulus
    raise ValueError("target is outside the reference histogram class")


def line_momenta(state: Microstate, size: int):
    row_px = [0] * size
    col_py = [0] * size
    for i, mask in enumerate(state):
        x, y = i % size, i // size
        row_px[y] += int(bool(mask & EAST)) - int(bool(mask & WEST))
        col_py[x] += int(bool(mask & SOUTH)) - int(bool(mask & NORTH))
    return tuple(row_px), tuple(col_py)


def checkerboard_modes(state: Microstate, size: int):
    density_mode = px_mode = py_mode = 0
    for i, mask in enumerate(state):
        x, y = i % size, i // size
        sign = -1 if (x + y) % 2 else 1
        e = int(bool(mask & EAST)); n = int(bool(mask & NORTH))
        s = int(bool(mask & SOUTH)); w = int(bool(mask & WEST))
        density_mode += sign * (e + n + s + w)
        px_mode += sign * (e - w)
        py_mode += sign * (s - n)
    return density_mode, px_mode, py_mode


def analytic_period_divisor(state: Microstate, size: int) -> int:
    divisor = histogram_rotation_period(diagonal_species_histograms(state, size))
    if size % 2 == 0 and any(checkerboard_modes(state, size)):
        divisor = lcm(divisor, 2)
    return divisor


def interaction_fiber_signature(state: Microstate, size: int):
    return diagonal_species_histograms(state, size), line_momenta(state, size)


def collision_orientation_frame(state: Microstate):
    ew, ns = EAST | WEST, NORTH | SOUTH
    return tuple(1 if m == ew else 2 if m == ns else 0 for m in state)


def locate_phase(reference: Microstate, target: Microstate, size: int, period: int) -> PhaseLocation:
    """Exact constant-memory phase location on a known recurrent orbit."""
    if period <= 0:
        raise ValueError("period must be positive")
    residue, modulus = histogram_phase_residue(reference, target, size)
    if period % modulus:
        raise ValueError("period conflicts with histogram clock")
    if reference == target:
        return PhaseLocation(0, period, residue, modulus, "reference", 0)

    backward = advance(target, size, residue, forward=False)
    back_depth = residue
    forward_alignment = (-residue) % modulus
    forward = advance(target, size, forward_alignment, forward=True)
    forward_depth = forward_alignment
    evaluations = residue + forward_alignment

    if backward == reference:
        return PhaseLocation(back_depth % period, period, residue, modulus, "backward", evaluations)
    if forward == reference:
        return PhaseLocation((period - forward_depth) % period, period, residue, modulus, "forward", evaluations)

    for _ in range(period // modulus + 1):
        backward = advance(backward, size, modulus, forward=False)
        back_depth += modulus
        evaluations += modulus
        if backward == reference:
            return PhaseLocation(back_depth % period, period, residue, modulus, "backward", evaluations)

        forward = advance(forward, size, modulus, forward=True)
        forward_depth += modulus
        evaluations += modulus
        if forward == reference:
            return PhaseLocation((period - forward_depth) % period, period, residue, modulus, "forward", evaluations)

    raise RuntimeError("reference not reached within declared period")
