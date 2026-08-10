#!/usr/bin/env python3
"""Independent certificate verifier for the exhaustive 3x3 HPP result.

This script deliberately does not import the project package or the high-level
classification/generation code. It reconstructs the constrained state sector,
the HPP update, the stable future-density partition, and the exceptional orbit
structure from local definitions, then checks the committed CSV certificate.
"""

from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path
import sys
from typing import Hashable, Iterable

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "hpp" / "ambiguity.csv"

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
State = tuple[int, ...]
Density = tuple[int, ...]


def collide_cell(mask: int) -> int:
    if mask == EAST | WEST:
        return NORTH | SOUTH
    if mask == NORTH | SOUTH:
        return EAST | WEST
    return mask


def collide(state: State) -> State:
    return tuple(collide_cell(mask) for mask in state)


def stream(state: State) -> State:
    output = [0] * 9
    for cell, mask in enumerate(state):
        x = cell % 3
        y = cell // 3
        for direction in DIRECTIONS:
            if mask & direction:
                dx, dy = VECTOR[direction]
                destination = 3 * ((y + dy) % 3) + ((x + dx) % 3)
                output[destination] |= direction
    return tuple(output)


def unstream(state: State) -> State:
    output = [0] * 9
    for cell, mask in enumerate(state):
        x = cell % 3
        y = cell // 3
        for direction in DIRECTIONS:
            if mask & direction:
                dx, dy = VECTOR[direction]
                source = 3 * ((y - dy) % 3) + ((x - dx) % 3)
                output[source] |= direction
    return tuple(output)


def step(state: State) -> State:
    return stream(collide(state))


def inverse_step(state: State) -> State:
    return collide(unstream(state))


def reverse_velocities(state: State) -> State:
    output = []
    for mask in state:
        reversed_mask = 0
        for direction in DIRECTIONS:
            if mask & direction:
                reversed_mask |= OPPOSITE[direction]
        output.append(reversed_mask)
    return tuple(output)


def time_reverse(state: State) -> State:
    # Correct involution for the collide-then-stream update convention.
    return collide(reverse_velocities(state))


def particle_number(state: State) -> int:
    return sum(mask.bit_count() for mask in state)


def momentum(state: State) -> tuple[int, int]:
    px = py = 0
    for mask in state:
        for direction in DIRECTIONS:
            if mask & direction:
                dx, dy = VECTOR[direction]
                px += dx
                py += dy
    return px, py


def density(state: State) -> Density:
    return tuple(mask.bit_count() for mask in state)


def collision_count(state: State) -> int:
    return sum(mask in (EAST | WEST, NORTH | SOUTH) for mask in state)


def encode_state(state: State) -> str:
    code = sum(mask << (4 * index) for index, mask in enumerate(state))
    return f"{code:09x}"


def decode_state(text: str) -> State:
    assert len(text) == 9, f"invalid state encoding width: {text!r}"
    code = int(text, 16)
    assert code < (1 << 36), f"state encoding out of range: {text!r}"
    return tuple((code >> (4 * index)) & 0xF for index in range(9))


def parse_masks(text: str) -> State:
    values = tuple(int(value) for value in text.split())
    assert len(values) == 9, f"expected nine masks, got {text!r}"
    assert all(0 <= value <= 15 for value in values), f"invalid mask in {text!r}"
    return values


def density_encoding(state: State) -> str:
    values = density(state)
    return "/".join(
        "".join(str(value) for value in values[row * 3 : (row + 1) * 3])
        for row in range(3)
    )


def enumerate_sector() -> tuple[State, ...]:
    states: list[State] = []
    for occupied_channels in combinations(range(36), 4):
        cells = [0] * 9
        for channel in occupied_channels:
            cells[channel // 4] |= 1 << (channel % 4)
        state = tuple(cells)
        if momentum(state) == (0, 0):
            states.append(state)
    return tuple(states)


def canonical_labels(keys: Iterable[Hashable]) -> list[int]:
    labels_by_key: dict[Hashable, int] = {}
    labels: list[int] = []
    for key in keys:
        if key not in labels_by_key:
            labels_by_key[key] = len(labels_by_key)
        labels.append(labels_by_key[key])
    return labels


def predictive_partition(states: tuple[State, ...]) -> tuple[tuple[int, ...], list[int], list[int]]:
    index = {state: position for position, state in enumerate(states)}
    assert len(index) == len(states), "sector enumeration contains duplicates"
    successors = []
    observations = []
    for state in states:
        following = step(state)
        assert following in index, "sector is not forward invariant"
        successors.append(index[following])
        observations.append(density(state))

    labels = canonical_labels(observations)
    counts = [len(set(labels))]
    while True:
        refined = canonical_labels(
            (observations[index_value], labels[successors[index_value]])
            for index_value in range(len(states))
        )
        counts.append(len(set(refined)))
        if refined == labels:
            break
        labels = refined
    return tuple(counts), labels, successors


def least_period(state: State) -> int:
    current = state
    for period in range(1, 10_000):
        current = step(current)
        if current == state:
            return period
    raise AssertionError("period search exceeded bound")


def canonical_cycle(state: State) -> tuple[State, ...]:
    orbit = [state]
    current = step(state)
    while current != state:
        assert current not in orbit, "bijective orbit failed to return to initial state"
        orbit.append(current)
        current = step(current)
    rotations = [tuple(orbit[offset:] + orbit[:offset]) for offset in range(len(orbit))]
    return min(rotations)


def read_catalog() -> list[dict[str, str]]:
    assert CATALOG.is_file(), f"missing certificate: {CATALOG}"
    with CATALOG.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "pair_id",
        "cycle_id",
        "cycle",
        "phase",
        "state_encoding",
        "state_masks",
        "reversed_state_encoding",
        "reversed_state_masks",
        "density_encoding",
        "density",
        "successor_encoding",
        "next_state_masks",
        "predecessor_encoding",
        "previous_state_masks",
        "velocity_reversal_partner_cycle",
        "velocity_reversal_partner_phase",
        "observation_reversal_shift",
        "least_period",
        "collision_sites",
    }
    assert rows, "certificate is empty"
    assert required.issubset(rows[0]), f"certificate columns missing: {sorted(required - set(rows[0]))}"
    return rows


def verify() -> None:
    states = enumerate_sector()
    assert len(states) == 9_153, f"sector count mismatch: {len(states)}"
    assert len(set(states)) == len(states), "duplicate sector states"
    assert all(particle_number(state) == 4 for state in states), "particle-number constraint failed"
    assert all(momentum(state) == (0, 0) for state in states), "momentum constraint failed"
    assert all(inverse_step(step(state)) == state for state in states), "inverse update failed"
    assert all(time_reverse(time_reverse(state)) == state for state in states), "time reversal is not involutive"
    assert all(time_reverse(step(time_reverse(state))) == inverse_step(state) for state in states), (
        "time-reversal conjugacy R F R = F^{-1} failed"
    )
    assert all(density(time_reverse(state)) == density(state) for state in states), (
        "density is not invariant under time reversal"
    )

    class_counts, labels, successors = predictive_partition(states)
    assert class_counts == (495, 6_948, 9_090, 9_126, 9_126), class_counts

    groups: dict[int, list[State]] = {}
    for state, label in zip(states, labels):
        groups.setdefault(label, []).append(state)
    class_sizes = [len(group) for group in groups.values()]
    assert class_sizes.count(1) == 9_099, "predictive singleton count mismatch"
    assert class_sizes.count(2) == 27, "predictive doubleton count mismatch"
    assert set(class_sizes) == {1, 2}, "unexpected predictive class size"

    doubletons = [tuple(group) for group in groups.values() if len(group) == 2]
    ambiguous = {state for group in doubletons for state in group}
    assert len(ambiguous) == 54, "ambiguous-state count mismatch"

    cycles = {canonical_cycle(state) for state in ambiguous}
    assert len(cycles) == 18, "period-three cycle count mismatch"
    assert all(len(cycle) == 3 for cycle in cycles), "exceptional cycle length mismatch"
    assert len({state for cycle in cycles for state in cycle}) == 54, "cycles are not disjoint"
    assert all(least_period(state) == 3 for state in ambiguous), "least period is not three"
    assert all(collision_count(state) == 0 for state in ambiguous), "exceptional collision found"
    assert all(time_reverse(state) == reverse_velocities(state) for state in ambiguous), (
        "collision-free reversal reduction failed"
    )

    rows = read_catalog()
    assert len(rows) == 54, f"certificate row count mismatch: {len(rows)}"
    assert len({row["state_encoding"] for row in rows}) == 54, "duplicate state assignment"
    assert len({(row["cycle_id"], row["phase"]) for row in rows}) == 54, (
        "duplicate cycle-phase assignment"
    )
    assert {int(row["pair_id"]) for row in rows} == set(range(1, 10)), "pair identifiers mismatch"
    assert {row["cycle"] for row in rows} == {"A", "B"}, "cycle labels mismatch"
    assert {int(row["phase"]) for row in rows} == {0, 1, 2}, "phase labels mismatch"
    assert len({row["cycle_id"] for row in rows}) == 18, "cycle identifier count mismatch"

    row_by_state: dict[State, dict[str, str]] = {}
    row_by_key: dict[tuple[int, str, int], dict[str, str]] = {}
    for row in rows:
        pair_id = int(row["pair_id"])
        cycle = row["cycle"]
        phase = int(row["phase"])
        state = decode_state(row["state_encoding"])
        row_by_state[state] = row
        row_by_key[(pair_id, cycle, phase)] = row

        assert row["cycle_id"] == f"P{pair_id:02d}-{cycle}", "cycle identifier mismatch"
        assert parse_masks(row["state_masks"]) == state, "state masks disagree with encoding"
        reversed_state = decode_state(row["reversed_state_encoding"])
        assert parse_masks(row["reversed_state_masks"]) == reversed_state, (
            "reversed masks disagree with encoding"
        )
        assert reversed_state == reverse_velocities(state), "velocity reversal mismatch"
        assert row["density_encoding"] == density_encoding(state), "density encoding mismatch"
        assert parse_masks(row["density"]) == density(state), "density tuple mismatch"

        successor = decode_state(row["successor_encoding"])
        predecessor = decode_state(row["predecessor_encoding"])
        assert parse_masks(row["next_state_masks"]) == successor, "successor masks mismatch"
        assert parse_masks(row["previous_state_masks"]) == predecessor, "predecessor masks mismatch"
        assert successor == step(state), "certificate successor mismatch"
        assert predecessor == inverse_step(state), "certificate predecessor mismatch"
        assert int(row["least_period"]) == least_period(state) == 3, "period certificate mismatch"
        assert int(row["collision_sites"]) == collision_count(state) == 0, (
            "collision certificate mismatch"
        )

    assert set(row_by_state) == ambiguous, "certificate has omissions or nonexceptional states"

    cycle_sets: dict[str, set[State]] = {}
    for state, row in row_by_state.items():
        cycle_sets.setdefault(row["cycle_id"], set()).add(state)
    assert all(len(cycle) == 3 for cycle in cycle_sets.values()), "certificate cycle size mismatch"
    assert len({frozenset(cycle) for cycle in cycle_sets.values()}) == 18, (
        "duplicate microscopic cycles in certificate"
    )

    pair_phase_classes: set[frozenset[State]] = set()
    for pair_id in range(1, 10):
        cycle_a = cycle_sets[f"P{pair_id:02d}-A"]
        cycle_b = cycle_sets[f"P{pair_id:02d}-B"]
        assert cycle_a.isdisjoint(cycle_b), "paired microscopic cycles overlap"
        assert {reverse_velocities(state) for state in cycle_a} == cycle_b, (
            "cycle pair is not related by velocity reversal"
        )
        assert {reverse_velocities(state) for state in cycle_b} == cycle_a, (
            "reverse cycle pairing is not involutive"
        )
        for phase in range(3):
            row_a = row_by_key[(pair_id, "A", phase)]
            row_b = row_by_key[(pair_id, "B", phase)]
            state_a = decode_state(row_a["state_encoding"])
            state_b = decode_state(row_b["state_encoding"])
            assert density(state_a) == density(state_b), "aligned phase densities differ"
            pair_phase_classes.add(frozenset((state_a, state_b)))

            reversal_shift = int(row_a["observation_reversal_shift"])
            assert int(row_b["observation_reversal_shift"]) == reversal_shift, (
                "pair reversal shifts disagree"
            )
            assert density(state_a) == density(
                decode_state(row_by_key[(pair_id, "A", (reversal_shift - phase) % 3)]["state_encoding"])
            ), "density word is not reversal invariant up to phase shift"
            partner_a = row_by_key[
                (
                    pair_id,
                    row_a["velocity_reversal_partner_cycle"],
                    int(row_a["velocity_reversal_partner_phase"]),
                )
            ]
            assert int(row_a["velocity_reversal_partner_phase"]) == (
                reversal_shift - phase
            ) % 3, "phase-alignment formula mismatch"
            assert decode_state(partner_a["state_encoding"]) == reverse_velocities(state_a), (
                "row-level reversal partner mismatch"
            )

    assert pair_phase_classes == {frozenset(group) for group in doubletons}, (
        "predictive doubletons are not exactly the nine paired three-phase movies"
    )

    # Stable classes are equality classes of the complete future-density process.
    # Since the certificate exhausts all 27 non-singleton classes and each is a
    # velocity-reversal pair, no additional ambiguity mechanism occurs here.
    assert sum(len(group) == 1 for group in groups.values()) == 9_099

    print("Sector states: 9153")
    print("Predictive singletons: 9099")
    print("Predictive doubletons: 27")
    print("Ambiguous states: 54")
    print("Period-3 cycles: 18")
    print("Time-reversal pairs: 9")
    print("Validation: PASS")


def main() -> int:
    try:
        verify()
    except (AssertionError, OSError, ValueError) as exc:
        print(f"Validation: FAIL - {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
