"""Deterministic reversible six-direction lattice gas with rotor memory.

This FHP-inspired model is distinct from the standard stochastic FHP collision
rule. A local rotor bit provides the memory required to make
the head-on collision rule exactly reversible.
"""

from __future__ import annotations

from random import Random
from typing import Tuple

State = Tuple[int, int, int, int, int, int, int]
PARTICLE_DIRECTIONS = 6





class Geometry:
    def __init__(self, size: int):
        self.size = size
        self.cells = size * size
        self.row_mask = (1 << size) - 1
        self.full_mask = (1 << self.cells) - 1
        self.last_row_shift = size * (size - 1)

        # 60-degree coordinate rotation:
        # (q, r) -> (q+r, -q), mapping direction d -> d+1.
        self.rotation_bit_map = []
        for r in range(size):
            for q in range(size):
                nq = (q + r) % size
                nr = (-q) % size
                self.rotation_bit_map.append(1 << (nr * size + nq))

        # Exact lookup tables make exhaustive short-lattice orbit audits fast
        # without changing the model or its integer state representation.
        self._east_table = self._west_table = None
        self._north_table = self._south_table = None
        if self.cells <= 16:
            state_count = 1 << self.cells
            self._east_table = tuple(self._east_direct(bits) for bits in range(state_count))
            self._west_table = tuple(self._west_direct(bits) for bits in range(state_count))
            self._north_table = tuple(self._north_direct(bits) for bits in range(state_count))
            self._south_table = tuple(self._south_direct(bits) for bits in range(state_count))

    def _east_direct(self, bits: int) -> int:
        result = 0
        for row_index in range(self.size):
            shift = row_index * self.size
            row = (bits >> shift) & self.row_mask
            rotated = (((row << 1) & self.row_mask) | (row >> (self.size - 1)))
            result |= rotated << shift
        return result

    def _west_direct(self, bits: int) -> int:
        result = 0
        for row_index in range(self.size):
            shift = row_index * self.size
            row = (bits >> shift) & self.row_mask
            rotated = (row >> 1) | ((row & 1) << (self.size - 1))
            result |= rotated << shift
        return result

    def _north_direct(self, bits: int) -> int:
        top_row = bits & self.row_mask
        return (bits >> self.size) | (top_row << self.last_row_shift)

    def _south_direct(self, bits: int) -> int:
        bottom_row = bits >> self.last_row_shift
        return ((bits << self.size) & self.full_mask) | bottom_row

    def east(self, bits: int) -> int:
        if self._east_table is not None:
            return self._east_table[bits]
        return self._east_direct(bits)

    def west(self, bits: int) -> int:
        if self._west_table is not None:
            return self._west_table[bits]
        return self._west_direct(bits)

    def north(self, bits: int) -> int:
        if self._north_table is not None:
            return self._north_table[bits]
        return self._north_direct(bits)

    def south(self, bits: int) -> int:
        if self._south_table is not None:
            return self._south_table[bits]
        return self._south_direct(bits)

    def rotate_board(self, bits: int) -> int:
        result = 0
        remaining = bits
        while remaining:
            low_bit = remaining & -remaining
            cell = low_bit.bit_length() - 1
            result |= self.rotation_bit_map[cell]
            remaining ^= low_bit
        return result


def validate_state(state: State, geometry: Geometry) -> None:
    assert isinstance(state, tuple) and len(state) == 7
    assert all(isinstance(board, int) for board in state)
    assert all(0 <= board <= geometry.full_mask for board in state)


def local_collision(mask: int, rotor: int) -> Tuple[int, int]:
    """
    Reference local collision on one cell.

    Opposite-pair masks:
      P0 = directions 0 and 3
      P1 = directions 1 and 4
      P2 = directions 2 and 5

    rotor=0: Pk -> P(k+1)
    rotor=1: Pk -> P(k-1)
    rotor toggles on such a collision.

    Alternating triplets 0,2,4 and 1,3,5 are swapped.
    """
    pairs = (
        (1 << 0) | (1 << 3),
        (1 << 1) | (1 << 4),
        (1 << 2) | (1 << 5),
    )
    triplet_a = (1 << 0) | (1 << 2) | (1 << 4)
    triplet_b = (1 << 1) | (1 << 3) | (1 << 5)

    if mask in pairs:
        index = pairs.index(mask)
        target = (index + 1) % 3 if rotor == 0 else (index - 1) % 3
        return pairs[target], rotor ^ 1

    if mask == triplet_a:
        return triplet_b, rotor
    if mask == triplet_b:
        return triplet_a, rotor

    return mask, rotor


def collide(state: State, geometry: Geometry) -> State:
    boards = list(state[:6])
    rotor = state[6]
    occupied_any = 0

    for board in boards:
        occupied_any |= board

    # Exact opposite-pair states.
    pair_sites = []
    for axis in range(3):
        first = axis
        opposite = axis + 3
        others = 0
        for direction in range(6):
            if direction not in (first, opposite):
                others |= boards[direction]

        sites = (
            boards[first]
            & boards[opposite]
            & ~others
            & geometry.full_mask
        )
        pair_sites.append(sites)

    all_pair_sites = pair_sites[0] | pair_sites[1] | pair_sites[2]
    rotor_zero = all_pair_sites & ~rotor & geometry.full_mask
    rotor_one = all_pair_sites & rotor

    # For rotor=0: pair axis k -> k+1.
    # For rotor=1: pair axis k -> k-1.
    pre_collision = tuple(boards)
    for axis, sites in enumerate(pair_sites):
        plus_sites = sites & rotor_zero
        minus_sites = sites & rotor_one

        if plus_sites:
            target = (axis + 1) % 3
            boards[axis] ^= plus_sites
            boards[axis + 3] ^= plus_sites
            boards[target] ^= plus_sites
            boards[target + 3] ^= plus_sites

        if minus_sites:
            target = (axis - 1) % 3
            boards[axis] ^= minus_sites
            boards[axis + 3] ^= minus_sites
            boards[target] ^= minus_sites
            boards[target + 3] ^= minus_sites

    rotor ^= all_pair_sites

    # Exact alternating triplets.
    triplet_a = (
        pre_collision[0]
        & pre_collision[2]
        & pre_collision[4]
        & ~(pre_collision[1] | pre_collision[3] | pre_collision[5])
        & geometry.full_mask
    )
    triplet_b = (
        pre_collision[1]
        & pre_collision[3]
        & pre_collision[5]
        & ~(pre_collision[0] | pre_collision[2] | pre_collision[4])
        & geometry.full_mask
    )
    triplet_sites = triplet_a | triplet_b

    for direction in range(6):
        boards[direction] ^= triplet_sites

    result = tuple(boards) + (rotor,)
    validate_state(result, geometry)
    return result


def step(state: State, geometry: Geometry) -> State:
    b0, b1, b2, b3, b4, b5, rotor = collide(state, geometry)

    east_0 = geometry.east(b0)
    east_1 = geometry.east(b1)
    west_3 = geometry.west(b3)
    west_4 = geometry.west(b4)

    return (
        east_0,
        geometry.north(east_1),
        geometry.north(b2),
        west_3,
        geometry.south(west_4),
        geometry.south(b5),
        rotor,
    )


def inverse_step(state: State, geometry: Geometry) -> State:
    b0, b1, b2, b3, b4, b5, rotor = state

    unstreamed = (
        geometry.west(b0),
        geometry.west(geometry.south(b1)),
        geometry.south(b2),
        geometry.east(b3),
        geometry.east(geometry.north(b4)),
        geometry.north(b5),
        rotor,
    )
    return collide(unstreamed, geometry)


def rotate_state(state: State, geometry: Geometry) -> State:
    particle_boards = [0] * 6

    # Direction d rotates to d+1.
    for direction in range(6):
        particle_boards[(direction + 1) % 6] = (
            geometry.rotate_board(state[direction])
        )

    rotor = geometry.rotate_board(state[6])
    return tuple(particle_boards) + (rotor,)


def particle_number(state: State) -> int:
    return sum(board.bit_count() for board in state[:6])


def direction_counts(state: State) -> Tuple[int, ...]:
    return tuple(board.bit_count() for board in state[:6])


def momentum(state: State) -> Tuple[int, int]:
    counts = direction_counts(state)
    q_component = counts[0] + counts[1] - counts[3] - counts[4]
    r_component = -counts[1] - counts[2] + counts[4] + counts[5]
    return q_component, r_component


def particle_hamming(first: State, second: State) -> int:
    return sum(
        (first[index] ^ second[index]).bit_count()
        for index in range(6)
    )


def rotor_hamming(first: State, second: State) -> int:
    return (first[6] ^ second[6]).bit_count()


def complete_hamming(first: State, second: State) -> int:
    return particle_hamming(first, second) + rotor_hamming(first, second)


def density_signature(state: State) -> Tuple[int, int, int]:
    """
    Exact bit-sliced sum of six one-bit occupancy channels.
    Encodes cell occupancy counts 0 through 6.
    """
    ones = 0
    twos = 0
    fours = 0

    for board in state[:6]:
        carry_to_twos = ones & board
        ones ^= board

        carry_to_fours = twos & carry_to_twos
        twos ^= carry_to_twos
        fours ^= carry_to_fours

    return ones, twos, fours


def macro_changed_cells(first: State, second: State) -> int:
    sig_a = density_signature(first)
    sig_b = density_signature(second)
    changed = (
        (sig_a[0] ^ sig_b[0])
        | (sig_a[1] ^ sig_b[1])
        | (sig_a[2] ^ sig_b[2])
    )
    return changed.bit_count()


def collision_count(state: State, geometry: Geometry) -> int:
    before = state
    after = collide(state, geometry)

    # Rotor toggles exactly at opposite-pair collision sites.
    pair_collisions = (before[6] ^ after[6]).bit_count()

    # Triplet collision sites toggle all six particle channels but no rotor.
    changed_particles = 0
    for direction in range(6):
        changed_particles |= before[direction] ^ after[direction]
    triplet_only = changed_particles & ~(before[6] ^ after[6])

    return pair_collisions + triplet_only.bit_count()


def boards_from_counts(
    geometry: Geometry,
    direction_counts_requested: Tuple[int, ...],
    rng: Random,
) -> Tuple[int, ...]:
    boards = []
    for count in direction_counts_requested:
        chosen = rng.sample(range(geometry.cells), count)
        board = 0
        for cell in chosen:
            board |= 1 << cell
        boards.append(board)
    return tuple(boards)


def balanced_random_state(
    geometry: Geometry,
    particles_per_cell: float,
    seed: int,
) -> State:
    """
    Generate zero-momentum states at a fixed particle density.

    Particle counts are allocated among the three opposite direction pairs.
    Opposite directions always have equal populations.
    """
    rng = Random(seed)
    particles = int(round(particles_per_cell * geometry.cells))
    assert particles % 2 == 0

    pair_total = particles // 2
    base = pair_total // 3
    remainder = pair_total % 3

    axis_counts = [base, base, base]
    axis_order = [0, 1, 2]
    rng.shuffle(axis_order)
    for index in range(remainder):
        axis_counts[axis_order[index]] += 1

    counts = (
        axis_counts[0],
        axis_counts[1],
        axis_counts[2],
        axis_counts[0],
        axis_counts[1],
        axis_counts[2],
    )
    assert all(count <= geometry.cells for count in counts)

    boards = boards_from_counts(geometry, counts, rng)
    rotor = rng.getrandbits(geometry.cells) & geometry.full_mask
    state = boards + (rotor,)

    validate_state(state, geometry)
    assert particle_number(state) == particles
    assert momentum(state) == (0, 0)
    return state


def density_preserving_velocity_swap(
    state: State,
    geometry: Geometry,
    seed: int,
) -> State:
    """
    Swap velocity labels of two particles in different cells.

    Preserves exact density, direction counts, particle number, momentum,
    energy, and the entire rotor field.
    """
    rng = Random(seed)
    particles: List[Tuple[int, int]] = []

    for direction, board in enumerate(state[:6]):
        remaining = board
        while remaining:
            low_bit = remaining & -remaining
            cell = low_bit.bit_length() - 1
            particles.append((cell, direction))
            remaining ^= low_bit

    for _ in range(20_000):
        cell_a, direction_a = rng.choice(particles)
        cell_b, direction_b = rng.choice(particles)

        if cell_a == cell_b or direction_a == direction_b:
            continue
        if state[direction_b] & (1 << cell_a):
            continue
        if state[direction_a] & (1 << cell_b):
            continue

        boards = list(state[:6])
        bit_a = 1 << cell_a
        bit_b = 1 << cell_b

        boards[direction_a] ^= bit_a
        boards[direction_b] ^= bit_b
        boards[direction_b] |= bit_a
        boards[direction_a] |= bit_b

        changed = tuple(boards) + (state[6],)

        assert density_signature(changed) == density_signature(state)
        assert direction_counts(changed) == direction_counts(state)
        assert particle_number(changed) == particle_number(state)
        assert momentum(changed) == momentum(state)
        assert changed[6] == state[6]
        assert particle_hamming(changed, state) == 4
        assert complete_hamming(changed, state) == 4
        return changed

    raise RuntimeError("No valid density-preserving velocity swap found.")


def exact_cycle(initial: State, geometry: Geometry, cap: int):
    seen: Dict[State, int] = {}
    state = initial
    initial_particles = particle_number(initial)
    initial_momentum = momentum(initial)

    for time in range(cap + 1):
        if state in seen:
            first = seen[state]
            return {
                "first": first,
                "second": time,
                "period": time - first,
                "distinct": len(seen),
                "seen": seen,
            }

        seen[state] = time

        if time % 257 == 0:
            assert particle_number(state) == initial_particles
            assert momentum(state) == initial_momentum
            assert inverse_step(step(state, geometry), geometry) == state
            assert step(inverse_step(state, geometry), geometry) == state

        state = step(state, geometry)

    return None
