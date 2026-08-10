"""
Orbit-specific HPP interaction clock for the 5x5 seed-B recurrence orbit.

Calibrated facts:
- Full F-period: 9705 updates.
- Transport clock recovers t mod 5 analytically.
- After alignment, G = F^5 has period 1941.
- A degree-4 square-free occupancy kernel spans the full 1941-state macro-orbit.
- The calibrated Koopman eigenfunction recovers macro-phase s mod 1941.

Important:
This is an orbit-specific calibrated decoder, not a universal HPP law.
A universal +1 clock modulo 3 or 647 cannot exist over the whole 5x5,
14-particle sector because other cycles have macro-periods not divisible
by those moduli.
"""

from __future__ import annotations

import math
from pathlib import Path
import numpy as np

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
VECTOR = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}

FULL_PERIOD = 9705
LATTICE_SIZE = 5
PARTICLES = 14
TRANSPORT_MODULUS = 5
MACRO_PERIOD = 1941


def collide_cell(mask: int) -> int:
    if mask == (EAST | WEST):
        return NORTH | SOUTH
    if mask == (NORTH | SOUTH):
        return EAST | WEST
    return mask


def collide(state):
    return tuple(collide_cell(m) for m in state)


def stream(state, size=5):
    out = [0] * (size * size)
    for y in range(size):
        for x in range(size):
            m = state[y * size + x]
            for d in DIRECTIONS:
                if m & d:
                    dx, dy = VECTOR[d]
                    nx, ny = (x + dx) % size, (y + dy) % size
                    out[ny * size + nx] |= d
    return tuple(out)


def unstream(state, size=5):
    out = [0] * (size * size)
    for y in range(size):
        for x in range(size):
            m = state[y * size + x]
            for d in DIRECTIONS:
                if m & d:
                    dx, dy = VECTOR[d]
                    px, py = (x - dx) % size, (y - dy) % size
                    out[py * size + px] |= d
    return tuple(out)


def step(state, size=5):
    return stream(collide(state), size)


def inverse_step(state, size=5):
    return collide(unstream(state, size))


def transport_clock(state, size=5):
    total = 0
    for idx, m in enumerate(state):
        x, y = idx % size, idx // size
        if m & EAST:
            total += x
        if m & WEST:
            total -= x
        if m & NORTH:
            total -= y
        if m & SOUTH:
            total += y
    return total % size


def state_bits(state):
    bits = np.zeros(4 * len(state), dtype=np.uint8)
    for cell, m in enumerate(state):
        for b in range(4):
            bits[4 * cell + b] = (m >> b) & 1
    return bits


def degree4_kernel_from_overlap(c: int) -> float:
    return float(sum(math.comb(c, d) for d in range(5) if c >= d))


def load_model(path):
    z = np.load(path)
    return {
        "reference": tuple(int(v) for v in z["reference"]),
        "centers": z["centers"].astype(np.uint8),
        "alpha": z["alpha_real"] + 1j * z["alpha_imag"],
    }


def phase_mod_5(state, reference):
    delta = (transport_clock(state) - transport_clock(reference)) % 5
    # 14^{-1} mod 5 = 4
    return (delta * 4) % 5


def macro_phase(state, centers, alpha):
    b = state_bits(state).astype(np.int16)
    overlaps = centers.astype(np.int16) @ b
    k = np.array([degree4_kernel_from_overlap(int(c)) for c in overlaps])
    value = k @ alpha
    angle = np.angle(value) % (2 * np.pi)
    return int(np.rint(angle * MACRO_PERIOD / (2 * np.pi))) % MACRO_PERIOD


def decode_phase(state, model):
    """Return exact phase t mod 9705 for a state on the calibrated orbit."""
    reference = model["reference"]
    r = phase_mod_5(state, reference)

    aligned = tuple(state)
    for _ in range(r):
        aligned = inverse_step(aligned)

    s = macro_phase(aligned, model["centers"], model["alpha"])
    return (r + 5 * s) % FULL_PERIOD


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    model = load_model(here / "model.npz")
    print("Loaded calibrated 5x5 seed-B HPP interaction clock.")
    print("Full period:", FULL_PERIOD)
    print("Macro-period:", MACRO_PERIOD)
