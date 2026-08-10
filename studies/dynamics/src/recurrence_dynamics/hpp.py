"""Reversible square-lattice HPP gas using exact immutable microstates.

Each cell is a four-bit velocity mask. The local head-on collision map is an
involution and streaming is a permutation on a periodic lattice.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from random import Random
from statistics import mean
from typing import Dict, List, Sequence, Tuple

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
VECTOR = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}
OPPOSITE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}
Microstate = Tuple[int, ...]
DensityState = Tuple[int, ...]


@dataclass(frozen=True)
class CycleResult:
    first_time: int
    second_time: int
    period: int
    distinct_states: int
    begins_at_initial: bool
    history: Tuple[Microstate, ...]


def validate_state(state: Microstate, width: int, height: int) -> None:
    assert width > 0 and height > 0
    assert isinstance(state, tuple)
    assert len(state) == width * height
    assert all(isinstance(mask, int) and 0 <= mask <= 15 for mask in state)


def collide_cell(mask: int) -> int:
    if mask == (EAST | WEST):
        return NORTH | SOUTH
    if mask == (NORTH | SOUTH):
        return EAST | WEST
    return mask


def collide(state: Microstate) -> Microstate:
    return tuple(collide_cell(mask) for mask in state)


def stream(state: Microstate, width: int, height: int) -> Microstate:
    validate_state(state, width, height)
    output = [0] * (width * height)
    for y in range(height):
        for x in range(width):
            mask = state[y * width + x]
            for direction in DIRECTIONS:
                if mask & direction:
                    dx, dy = VECTOR[direction]
                    nx = (x + dx) % width
                    ny = (y + dy) % height
                    output[ny * width + nx] |= direction
    result = tuple(output)
    validate_state(result, width, height)
    return result


def unstream(state: Microstate, width: int, height: int) -> Microstate:
    validate_state(state, width, height)
    output = [0] * (width * height)
    for y in range(height):
        for x in range(width):
            mask = state[y * width + x]
            for direction in DIRECTIONS:
                if not mask & direction:
                    continue
                dx, dy = VECTOR[direction]
                px = (x - dx) % width
                py = (y - dy) % height
                output[py * width + px] |= direction
    result = tuple(output)
    validate_state(result, width, height)
    return result


def step(state: Microstate, width: int, height: int) -> Microstate:
    return stream(collide(state), width, height)


def inverse_step(state: Microstate, width: int, height: int) -> Microstate:
    return collide(unstream(state, width, height))


def particle_number(state: Microstate) -> int:
    return sum(mask.bit_count() for mask in state)


def momentum(state: Microstate) -> Tuple[int, int]:
    px = py = 0
    for mask in state:
        for direction in DIRECTIONS:
            if mask & direction:
                dx, dy = VECTOR[direction]
                px += dx
                py += dy
    return px, py


def density(state: Microstate) -> DensityState:
    return tuple(mask.bit_count() for mask in state)


def local_momentum_field(state: Microstate) -> Tuple[Tuple[int, int], ...]:
    """Return the sitewise momentum vector ``(px, py)`` for every cell."""
    field = []
    for mask in state:
        px = int(bool(mask & EAST)) - int(bool(mask & WEST))
        py = int(bool(mask & SOUTH)) - int(bool(mask & NORTH))
        field.append((px, py))
    return tuple(field)


def local_axis_counts(state: Microstate) -> Tuple[Tuple[int, int], ...]:
    """Return sitewise ``(horizontal_count, vertical_count)`` occupancies."""
    return tuple(
        (
            int(bool(mask & EAST)) + int(bool(mask & WEST)),
            int(bool(mask & NORTH)) + int(bool(mask & SOUTH)),
        )
        for mask in state
    )


def observe_site_masks(state: Microstate, sites: Sequence[int]) -> Tuple[int, ...]:
    """Observe exact velocity masks at selected row-major site indices."""
    return tuple(state[index] for index in sites)


def observe_site_momenta(
    state: Microstate,
    sites: Sequence[int],
) -> Tuple[Tuple[int, int], ...]:
    """Observe sitewise momentum vectors at selected row-major indices."""
    field = local_momentum_field(state)
    return tuple(field[index] for index in sites)


def reverse_velocities(state: Microstate) -> Microstate:
    """Reverse every particle velocity without changing occupied sites."""
    reversed_cells = []
    for mask in state:
        reversed_mask = 0
        for direction in DIRECTIONS:
            if mask & direction:
                reversed_mask |= OPPOSITE[direction]
        reversed_cells.append(reversed_mask)
    return tuple(reversed_cells)


def time_reverse_state(state: Microstate) -> Microstate:
    """Return the time-reversed state for the collide-then-stream convention.

    If ``F = stream after collide`` and ``V`` reverses all velocities, then
    ``R = collide after V`` is an involution satisfying ``R F R = F^{-1}``.
    On collision-free states, ``R`` reduces to bare velocity reversal.
    """
    return collide(reverse_velocities(state))


def encode_state(state: Microstate, width: int, height: int) -> int:
    """Pack a row-major HPP state into four bits per lattice site."""
    validate_state(state, width, height)
    code = 0
    for index, mask in enumerate(state):
        code |= mask << (4 * index)
    return code


def decode_state(code: int, width: int, height: int) -> Microstate:
    """Decode the integer representation produced by :func:`encode_state`."""
    if not isinstance(code, int) or code < 0:
        raise ValueError("code must be a nonnegative integer")
    cell_count = width * height
    if code >= 1 << (4 * cell_count):
        raise ValueError("code contains bits outside the requested lattice")
    state = tuple((code >> (4 * index)) & 0xF for index in range(cell_count))
    validate_state(state, width, height)
    return state


def state_hex(state: Microstate, width: int, height: int) -> str:
    """Return a fixed-width hexadecimal encoding of a row-major state."""
    return f"{encode_state(state, width, height):0{width * height}x}"


def state_from_hex(text: str, width: int, height: int) -> Microstate:
    """Decode a fixed-width hexadecimal state encoding."""
    if len(text) != width * height:
        raise ValueError("hex state has the wrong number of lattice cells")
    try:
        code = int(text, 16)
    except ValueError as exc:
        raise ValueError("invalid hexadecimal state encoding") from exc
    return decode_state(code, width, height)


def velocity_bit_hamming(a: Microstate, b: Microstate) -> int:
    assert len(a) == len(b)
    return sum((left ^ right).bit_count() for left, right in zip(a, b))


def density_l1(a: Microstate, b: Microstate) -> int:
    assert len(a) == len(b)
    return sum(
        abs(left.bit_count() - right.bit_count())
        for left, right in zip(a, b)
    )


def collision_site_count(state: Microstate) -> int:
    return sum(
        mask in ((EAST | WEST), (NORTH | SOUTH))
        for mask in state
    )


def find_cycle(
    initial: Microstate,
    width: int,
    height: int,
    cap: int = 2_000_000,
) -> CycleResult:
    validate_state(initial, width, height)
    seen: Dict[Microstate, int] = {}
    history: List[Microstate] = []
    state = initial
    initial_particles = particle_number(initial)
    initial_momentum = momentum(initial)

    for time in range(cap + 1):
        if state in seen:
            first = seen[state]
            return CycleResult(
                first_time=first,
                second_time=time,
                period=time - first,
                distinct_states=len(seen),
                begins_at_initial=(first == 0),
                history=tuple(history),
            )

        seen[state] = time
        history.append(state)

        assert inverse_step(step(state, width, height), width, height) == state
        assert step(inverse_step(state, width, height), width, height) == state
        assert particle_number(state) == initial_particles
        assert momentum(state) == initial_momentum

        state = step(state, width, height)

    raise RuntimeError(
        f"No repeat found within cap={cap}; this is not evidence of no recurrence."
    )


def states_through(
    initial: Microstate,
    width: int,
    height: int,
    final_time: int,
) -> Tuple[Microstate, ...]:
    output: List[Microstate] = []
    state = initial
    for _ in range(final_time + 1):
        output.append(state)
        state = step(state, width, height)
    return tuple(output)


def verify_complete_cycle(
    initial: Microstate,
    width: int,
    height: int,
    result: CycleResult,
) -> None:
    start = result.first_time
    period = result.period
    orbit = states_through(initial, width, height, start + 2 * period)
    for time in range(start, start + period + 1):
        assert orbit[time + period] == orbit[time]


def find_density_counterexample(
    history: Sequence[Microstate],
    width: int,
    height: int,
):
    seen: Dict[DensityState, List[Tuple[int, Microstate]]] = {}
    for time, state in enumerate(history):
        image = density(state)
        for earlier_time, earlier_state in seen.get(image, []):
            if earlier_state == state:
                continue
            earlier_next = step(earlier_state, width, height)
            later_next = step(state, width, height)
            if density(earlier_next) != density(later_next):
                return {
                    "t1": earlier_time,
                    "t2": time,
                    "density": image,
                    "state1": earlier_state,
                    "state2": state,
                    "next_density1": density(earlier_next),
                    "next_density2": density(later_next),
                    "microstate_hamming": velocity_bit_hamming(
                        earlier_state, state
                    ),
                }
        seen.setdefault(image, []).append((time, state))
    return None


def balanced_random_state(
    size: int,
    seed: int,
    opposite_pairs: int = 7,
) -> Microstate:
    rng = Random(seed)
    cells = [0] * (size * size)
    occupied = set()
    for _ in range(opposite_pairs):
        pair = (EAST, WEST) if rng.randrange(2) == 0 else (NORTH, SOUTH)
        for direction in pair:
            while True:
                cell_index = rng.randrange(size * size)
                key = (cell_index, direction)
                if key not in occupied:
                    occupied.add(key)
                    cells[cell_index] |= direction
                    break
    result = tuple(cells)
    assert particle_number(result) == 2 * opposite_pairs
    assert momentum(result) == (0, 0)
    return result
