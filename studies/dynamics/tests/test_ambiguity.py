from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path

from recurrence_dynamics.finite_orbits import predictive_partition
from recurrence_dynamics.hpp import (
    EAST,
    NORTH,
    SOUTH,
    WEST,
    collision_site_count,
    density,
    momentum,
    particle_number,
    reverse_velocities,
    state_from_hex,
    step,
    time_reverse_state,
)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "hpp" / "ambiguity.csv"
FIGURE = ROOT / "data" / "hpp" / "ambiguity.png"
PAPER_FIGURE = ROOT / "paper" / "figures" / "hpp-ambiguity.png"


def sector_states() -> tuple[tuple[int, ...], ...]:
    output = []
    for occupied_channels in combinations(range(36), 4):
        cells = [0] * 9
        for channel in occupied_channels:
            cells[channel // 4] |= 1 << (channel % 4)
        state = tuple(cells)
        if momentum(state) == (0, 0):
            output.append(state)
    return tuple(output)


def canonical_cycle(state):
    orbit = [state]
    following = step(state, 3, 3)
    while following != state:
        assert following not in orbit
        orbit.append(following)
        following = step(following, 3, 3)
    rotations = [tuple(orbit[offset:] + orbit[:offset]) for offset in range(len(orbit))]
    return min(rotations)


def test_exhaustive_hpp_partition_and_exceptional_structure():
    states = sector_states()
    assert len(states) == 9_153
    assert all(particle_number(state) == 4 for state in states)
    assert all(momentum(state) == (0, 0) for state in states)

    result = predictive_partition(lambda state: step(state, 3, 3), states, density)
    assert result.class_counts == (495, 6_948, 9_090, 9_126, 9_126)
    groups = tuple(result.classes().values())
    assert sum(len(group) == 1 for group in groups) == 9_099
    assert sum(len(group) == 2 for group in groups) == 27
    assert max(map(len, groups)) == 2

    ambiguous = {state for group in groups if len(group) == 2 for state in group}
    assert len(ambiguous) == 54
    cycles = {canonical_cycle(state) for state in ambiguous}
    assert len(cycles) == 18
    assert {len(cycle) for cycle in cycles} == {3}
    assert len({state for cycle in cycles for state in cycle}) == 54
    assert all(collision_site_count(state) == 0 for state in ambiguous)
    assert all(
        all(mask in {0, NORTH, EAST, SOUTH, WEST} for mask in state)
        for state in ambiguous
    )


def test_ambiguity_catalog_is_complete_unique_and_phase_aligned():
    with CATALOG.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 54
    assert len({row["state_encoding"] for row in rows}) == 54
    assert len({(row["cycle_id"], row["phase"]) for row in rows}) == 54
    assert {int(row["pair_id"]) for row in rows} == set(range(1, 10))
    assert len({row["cycle_id"] for row in rows}) == 18
    assert all(int(row["least_period"]) == 3 for row in rows)
    assert all(int(row["collision_sites"]) == 0 for row in rows)

    by_key = {
        (int(row["pair_id"]), row["cycle"], int(row["phase"])): row
        for row in rows
    }
    for pair_id in range(1, 10):
        for phase in range(3):
            left = state_from_hex(by_key[(pair_id, "A", phase)]["state_encoding"], 3, 3)
            right = state_from_hex(by_key[(pair_id, "B", phase)]["state_encoding"], 3, 3)
            assert density(left) == density(right)
        cycle_a = {
            state_from_hex(by_key[(pair_id, "A", phase)]["state_encoding"], 3, 3)
            for phase in range(3)
        }
        cycle_b = {
            state_from_hex(by_key[(pair_id, "B", phase)]["state_encoding"], 3, 3)
            for phase in range(3)
        }
        assert {reverse_velocities(state) for state in cycle_a} == cycle_b
        assert {time_reverse_state(state) for state in cycle_a} == cycle_b

        for cycle_name in ("A", "B"):
            for phase in range(3):
                row = by_key[(pair_id, cycle_name, phase)]
                state = state_from_hex(row["state_encoding"], 3, 3)
                successor = state_from_hex(row["successor_encoding"], 3, 3)
                predecessor = state_from_hex(row["predecessor_encoding"], 3, 3)
                reversed_state = state_from_hex(row["reversed_state_encoding"], 3, 3)
                partner_phase = int(row["velocity_reversal_partner_phase"])
                partner_cycle = row["velocity_reversal_partner_cycle"]
                shift = int(row["observation_reversal_shift"])
                assert successor == step(state, 3, 3)
                assert step(predecessor, 3, 3) == state
                assert reversed_state == reverse_velocities(state) == time_reverse_state(state)
                assert reversed_state == state_from_hex(
                    by_key[(pair_id, partner_cycle, partner_phase)]["state_encoding"], 3, 3
                )
                assert partner_phase == (shift - phase) % 3


def test_paired_cycle_figure_exists_and_has_no_text_metadata():
    from PIL import Image

    assert FIGURE.is_file()
    assert PAPER_FIGURE.is_file()
    assert FIGURE.read_bytes() == PAPER_FIGURE.read_bytes()
    with Image.open(FIGURE) as image:
        assert image.width >= 1200
        assert image.height >= 800
        assert not image.info
