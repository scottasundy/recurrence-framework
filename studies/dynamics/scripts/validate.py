#!/usr/bin/env python3
"""Reproduction and validation entry point for the recurrence study."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, getcontext
from fractions import Fraction
import hashlib
from itertools import combinations
from math import lcm
import os
from pathlib import Path
from random import Random
import shutil
from statistics import mean, median
import subprocess
import sys
import tempfile
from typing import Callable, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from recurrence_dynamics.automaton import (  # noqa: E402
    all_states as ca_all_states,
    inverse_step as ca_inverse_step,
    step as ca_step,
)
from recurrence_dynamics.elastic_ring import (  # noqa: E402
    RingState,
    advance as ring_advance,
    first_sampled_repeat,
    fraction_text,
    kinetic_energy,
    momentum as ring_momentum,
    sample_orbit,
    time_reverse,
    torus_position_l1,
)
from recurrence_dynamics.finite_orbits import predictive_partition  # noqa: E402
from recurrence_dynamics.rotor import (  # noqa: E402
    Geometry as HexGeometry,
    balanced_random_state as hex_balanced_random_state,
    collision_count as hex_collision_count,
    density_preserving_velocity_swap as hex_density_preserving_velocity_swap,
    density_signature as hex_density_signature,
    direction_counts as hex_direction_counts,
    exact_cycle as hex_exact_cycle,
    inverse_step as hex_inverse_step,
    local_collision as hex_local_collision,
    macro_changed_cells as hex_macro_changed_cells,
    momentum as hex_momentum,
    particle_hamming as hex_particle_hamming,
    particle_number as hex_particle_number,
    rotate_state as hex_rotate_state,
    rotor_hamming as hex_rotor_hamming,
    step as hex_step,
)
from recurrence_dynamics.hpp import (  # noqa: E402
    DIRECTIONS,
    EAST,
    NORTH,
    SOUTH,
    WEST,
    balanced_random_state,
    collision_site_count,
    density,
    density_l1,
    find_cycle,
    find_density_counterexample,
    inverse_step as square_inverse_step,
    momentum,
    particle_number,
    reverse_velocities,
    state_from_hex,
    state_hex,
    time_reverse_state,
    step as square_step,
    velocity_bit_hamming,
    verify_complete_cycle,
)


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> None:
    print("+", " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=cwd, env=env)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows generated for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(relative_path: str, *, data_root: Path = DATA) -> list[dict[str, str]]:
    path = data_root / relative_path
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save_figure(path: Path) -> None:
    import matplotlib.pyplot as plt
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180, metadata={})
    plt.close()

    # Re-save the pixel data without textual PNG metadata.
    with Image.open(path) as image:
        clean = image.copy()
    clean.save(path, format="PNG")



def _align_cycle_to_density_word(
    cycle: tuple[tuple[int, ...], ...],
    word: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    for offset in range(len(cycle)):
        rotated = cycle[offset:] + cycle[:offset]
        if tuple(density(state) for state in rotated) == word:
            return rotated
    raise AssertionError("Cycle does not realize the requested density word.")


def _state_text(state: tuple[int, ...]) -> str:
    return " ".join(str(mask) for mask in state)


def _draw_hpp_state(axis, state: tuple[int, ...], title: str) -> None:
    import matplotlib.patches as patches

    direction_vectors = {
        NORTH: (0.0, -0.30),
        EAST: (0.30, 0.0),
        SOUTH: (0.0, 0.30),
        WEST: (-0.30, 0.0),
    }
    axis.set_xlim(0, 3)
    axis.set_ylim(3, 0)
    axis.set_aspect("equal")
    axis.set_xticks(range(4))
    axis.set_yticks(range(4))
    axis.grid(True, linewidth=0.9, color="0.25")
    axis.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    for spine in axis.spines.values():
        spine.set_linewidth(1.1)
        spine.set_color("black")
    for index, mask in enumerate(state):
        x = index % 3
        y = index // 3
        if mask:
            axis.add_patch(
                patches.Rectangle(
                    (x, y),
                    1,
                    1,
                    facecolor="0.82",
                    edgecolor="0.35",
                    hatch="///",
                    linewidth=0.5,
                    zorder=0,
                )
            )
        for direction, (dx, dy) in direction_vectors.items():
            if mask & direction:
                axis.arrow(
                    x + 0.5,
                    y + 0.5,
                    dx,
                    dy,
                    width=0.014,
                    head_width=0.14,
                    head_length=0.11,
                    length_includes_head=True,
                    color="black",
                    zorder=3,
                )
    axis.set_title(title, fontsize=10, pad=5)


def _density_code(state: tuple[int, ...]) -> str:
    return "/".join(
        "".join(str(value) for value in density(state)[row * 3 : (row + 1) * 3])
        for row in range(3)
    )


def generate_hpp_ambiguity_catalog(data_root: Path) -> None:
    """Write the complete 54-state certificate and a representative figure."""
    output = data_root / "hpp"
    output.mkdir(parents=True, exist_ok=True)

    states = _four_particle_zero_momentum_states()
    hpp_step = lambda state: square_step(state, 3, 3)
    result = predictive_partition(hpp_step, states, density)
    groups = tuple(result.classes().values())
    ambiguous_states = {
        state
        for group in groups
        if len(group) == 2
        for state in group
    }
    cycles = {_canonical_cycle(state, hpp_step) for state in ambiguous_states}
    cycles_by_word: dict[
        tuple[tuple[int, ...], ...],
        list[tuple[tuple[int, ...], ...]],
    ] = {}
    for cycle in cycles:
        word = _canonical_density_word(cycle)
        cycles_by_word.setdefault(word, []).append(cycle)

    rows: list[dict[str, object]] = []
    for pair_id, (word, paired_cycles) in enumerate(
        sorted(cycles_by_word.items()),
        start=1,
    ):
        assert len(paired_cycles) == 2
        aligned = sorted(
            _align_cycle_to_density_word(cycle, word)
            for cycle in paired_cycles
        )
        assert {
            frozenset(reverse_velocities(state) for state in cycle)
            for cycle in aligned
        } == {frozenset(aligned[0]), frozenset(aligned[1])}
        reversal_shifts = [
            shift
            for shift in range(3)
            if all(word[time] == word[(shift - time) % 3] for time in range(3))
        ]
        assert reversal_shifts
        reversal_shift = min(reversal_shifts)

        for cycle_index, cycle in enumerate(aligned):
            label = "A" if cycle_index == 0 else "B"
            partner_label = "B" if label == "A" else "A"
            cycle_id = f"P{pair_id:02d}-{label}"
            partner_cycle = aligned[1 - cycle_index]
            for phase, state in enumerate(cycle):
                reversed_state = reverse_velocities(state)
                partner_phase = partner_cycle.index(reversed_state)
                successor = cycle[(phase + 1) % 3]
                predecessor = cycle[(phase - 1) % 3]
                assert time_reverse_state(state) == reversed_state
                assert partner_phase == (reversal_shift - phase) % 3
                rows.append(
                    {
                        "pair_id": pair_id,
                        "cycle_id": cycle_id,
                        "cycle": label,
                        "phase": phase,
                        "state_encoding": state_hex(state, 3, 3),
                        "state_masks": _state_text(state),
                        "reversed_state_encoding": state_hex(reversed_state, 3, 3),
                        "reversed_state_masks": _state_text(reversed_state),
                        "density_encoding": _density_code(state),
                        "density": _state_text(density(state)),
                        "successor_encoding": state_hex(successor, 3, 3),
                        "next_state_masks": _state_text(successor),
                        "predecessor_encoding": state_hex(predecessor, 3, 3),
                        "previous_state_masks": _state_text(predecessor),
                        "velocity_reversal_partner_cycle": partner_label,
                        "velocity_reversal_partner_phase": partner_phase,
                        "observation_reversal_shift": reversal_shift,
                        "least_period": 3,
                        "collision_sites": collision_site_count(state),
                    }
                )

    assert len(rows) == 54
    write_csv(output / "ambiguity.csv", rows)

    representative_a = (1, 2, 0, 8, 4, 0, 0, 0, 0)
    representative_b = (8, 1, 0, 4, 2, 0, 0, 0, 0)
    orbit_a_list = [representative_a]
    orbit_b_list = [representative_b]
    for _ in range(2):
        orbit_a_list.append(square_step(orbit_a_list[-1], 3, 3))
        orbit_b_list.append(square_step(orbit_b_list[-1], 3, 3))
    orbit_a = tuple(orbit_a_list)
    orbit_b = tuple(orbit_b_list)

    assert all(density(left) == density(right) for left, right in zip(orbit_a, orbit_b))
    assert square_step(orbit_a[-1], 3, 3) == orbit_a[0]
    assert square_step(orbit_b[-1], 3, 3) == orbit_b[0]
    assert {reverse_velocities(state) for state in orbit_a} == set(orbit_b)

    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(2, 3, figsize=(9.4, 6.3))
    for phase in range(3):
        _draw_hpp_state(axes[0, phase], orbit_a[phase], f"Aligned phase {phase}")
        _draw_hpp_state(axes[1, phase], orbit_b[phase], f"Aligned phase {phase}")
    axes[0, 0].set_ylabel("Microscopic cycle A", fontsize=10, labelpad=12)
    axes[1, 0].set_ylabel("Microscopic cycle B", fontsize=10, labelpad=12)

    figure.suptitle(
        "Paired collision-free period-three HPP cycles with one shared density movie",
        fontsize=12,
        y=0.985,
    )
    figure.text(
        0.5,
        0.935,
        "Cycle B is the velocity-reversed partner of cycle A (with cyclic phase alignment).",
        ha="center",
        fontsize=9.5,
    )
    for y in (0.69, 0.305):
        figure.text(0.365, y, r"$\rightarrow$", ha="center", va="center", fontsize=16)
        figure.text(0.665, y, r"$\rightarrow$", ha="center", va="center", fontsize=16)
        figure.text(0.925, y, r"$\rightarrow$ phase 0", ha="center", va="center", fontsize=9)

    word = " -> ".join(_density_code(state) for state in orbit_a)
    figure.text(
        0.5,
        0.065,
        f"Shared density word (rows separated by /):  {word}  -> repeat",
        ha="center",
        fontsize=9.5,
    )
    figure.text(
        0.5,
        0.028,
        "Shading shows occupied cells; arrows show velocity channels. Opposite lattice edges are identified.",
        ha="center",
        fontsize=8.8,
    )
    figure.tight_layout(rect=(0.045, 0.11, 0.95, 0.91), h_pad=2.0, w_pad=2.6)
    save_figure(output / "ambiguity.png")


def _square_density_preserving_swap(
    state: tuple[int, ...],
    seed: int,
) -> tuple[tuple[int, ...], tuple[int, int, int, int]]:
    rng = Random(seed)
    particles = [
        (cell, direction)
        for cell, mask in enumerate(state)
        for direction in DIRECTIONS
        if mask & direction
    ]
    candidates: list[tuple[int, int, int, int]] = []
    for first_index, (cell_a, direction_a) in enumerate(particles):
        for cell_b, direction_b in particles[first_index + 1 :]:
            if cell_a == cell_b or direction_a == direction_b:
                continue
            if state[cell_a] & direction_b:
                continue
            if state[cell_b] & direction_a:
                continue
            candidates.append((cell_a, direction_a, cell_b, direction_b))
    if not candidates:
        raise RuntimeError("No density-preserving velocity swap exists.")
    cell_a, direction_a, cell_b, direction_b = rng.choice(candidates)
    changed = list(state)
    changed[cell_a] ^= direction_a
    changed[cell_b] ^= direction_b
    changed[cell_a] |= direction_b
    changed[cell_b] |= direction_a
    perturbed = tuple(changed)
    assert density(perturbed) == density(state)
    assert particle_number(perturbed) == particle_number(state)
    assert momentum(perturbed) == momentum(state)
    assert velocity_bit_hamming(perturbed, state) == 4
    return perturbed, (cell_a, direction_a, cell_b, direction_b)


def _cycle_or_none(
    initial: tuple[int, ...],
    width: int,
    height: int,
    cap: int,
):
    seen: dict[tuple[int, ...], int] = {}
    state = initial
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
        state = square_step(state, width, height)
    return None


def generate_square_reference(data_root: Path) -> None:
    output = data_root / "hpp"
    output.mkdir(parents=True, exist_ok=True)
    width = height = 5
    initial = (
        EAST, WEST, 0, WEST, SOUTH,
        0, NORTH, 0, 0, 0,
        0, 0, 0, 0, 0,
        EAST, 0, 0, WEST, 0,
        0, 0, 0, EAST, 0,
    )
    base = find_cycle(initial, width, height)
    verify_complete_cycle(initial, width, height, base)
    counterexample = find_density_counterexample(base.history, width, height)
    assert base.period == 175
    assert counterexample is not None
    assert (counterexample["t1"], counterexample["t2"]) == (13, 23)

    perturbed_values = list(initial)
    perturbed_values[0] ^= NORTH
    perturbed = tuple(perturbed_values)
    changed = find_cycle(perturbed, width, height)
    verify_complete_cycle(perturbed, width, height, changed)
    joint_period = lcm(base.period, changed.period)

    pair_rows = []
    state_a = initial
    state_b = perturbed
    for time in range(joint_period + 1):
        pair_rows.append(
            {
                "time": time,
                "velocity_bit_hamming": velocity_bit_hamming(state_a, state_b),
                "density_l1": density_l1(state_a, state_b),
            }
        )
        state_a = square_step(state_a, width, height)
        state_b = square_step(state_b, width, height)
    write_csv(output / "hamming.csv", pair_rows)

    sweep_rows = []
    for size in range(3, 8):
        for label, base_seed in zip(("A", "B", "C"), (101, 202, 303)):
            seed = base_seed + size * 1000 + 70_000
            state = balanced_random_state(size, seed, opposite_pairs=7)
            result = find_cycle(state, size, size)
            verify_complete_cycle(state, size, size, result)
            px, py = momentum(state)
            sweep_rows.append(
                {
                    "size": f"{size}x{size}",
                    "seed_label": label,
                    "rng_seed": seed,
                    "particles": particle_number(state),
                    "momentum_x": px,
                    "momentum_y": py,
                    "first_time": result.first_time,
                    "second_time": result.second_time,
                    "period": result.period,
                    "distinct_states": result.distinct_states,
                    "repeat_is_initial": result.begins_at_initial,
                }
            )
    write_csv(output / "size-sweep.csv", sweep_rows)


def generate_conserved_sector(data_root: Path) -> None:
    import matplotlib.pyplot as plt

    output = data_root / "perturbations"
    output.mkdir(parents=True, exist_ok=True)
    sizes = (5, 6, 7)
    trials_per_size = 50
    cycle_trials = 10
    steps = 2000
    particles = 14
    cycle_cap = 500_000
    direction_names = {NORTH: "N", EAST: "E", SOUTH: "S", WEST: "W"}

    trial_rows: list[dict] = []
    hamming_series: dict[int, list[list[int]]] = {size: [] for size in sizes}
    density_series: dict[int, list[list[int]]] = {size: [] for size in sizes}

    for size in sizes:
        for trial in range(trials_per_size):
            seed = 2_026_071_800 + size * 10_000 + trial
            initial = balanced_random_state(size, seed, opposite_pairs=7)
            perturbed, swap = _square_density_preserving_swap(
                initial, seed + 991_337
            )
            assert particle_number(initial) == particle_number(perturbed) == particles
            assert momentum(initial) == momentum(perturbed) == (0, 0)

            base_cycle = changed_cycle = None
            same_exact_cycle = pair_period = None
            if trial < cycle_trials:
                base_cycle = _cycle_or_none(initial, size, size, cycle_cap)
                changed_cycle = _cycle_or_none(perturbed, size, size, cycle_cap)
                assert base_cycle is not None and changed_cycle is not None
                assert base_cycle["first"] == changed_cycle["first"] == 0
                same_exact_cycle = perturbed in base_cycle["seen"]
                pair_period = lcm(base_cycle["period"], changed_cycle["period"])

            state_a = initial
            state_b = perturbed
            microscopic: list[int] = []
            macroscopic: list[int] = []
            first_micro_growth = None
            first_density_difference = None
            first_half_saturation = None
            for time in range(steps + 1):
                micro = velocity_bit_hamming(state_a, state_b)
                macro = density_l1(state_a, state_b)
                assert micro > 0
                microscopic.append(micro)
                macroscopic.append(macro)
                if first_micro_growth is None and micro > 4:
                    first_micro_growth = time
                if first_density_difference is None and macro > 0:
                    first_density_difference = time
                if first_half_saturation is None and micro >= particles:
                    first_half_saturation = time
                state_a = square_step(state_a, size, size)
                state_b = square_step(state_b, size, size)

            hamming_series[size].append(microscopic)
            density_series[size].append(macroscopic)
            cell_a, direction_a, cell_b, direction_b = swap
            trial_rows.append(
                {
                    "size": size,
                    "trial": trial,
                    "seed": seed,
                    "particles": particles,
                    "momentum_x": 0,
                    "momentum_y": 0,
                    "initial_density_equal": True,
                    "initial_hamming": 4,
                    "swap_cell_a": cell_a,
                    "swap_direction_a": direction_names[direction_a],
                    "swap_cell_b": cell_b,
                    "swap_direction_b": direction_names[direction_b],
                    "base_period": base_cycle["period"] if base_cycle else "",
                    "perturbed_period": changed_cycle["period"] if changed_cycle else "",
                    "pair_period_lcm": pair_period if pair_period is not None else "",
                    "same_exact_cycle": same_exact_cycle if same_exact_cycle is not None else "",
                    "first_micro_growth": first_micro_growth if first_micro_growth is not None else "",
                    "first_density_difference": first_density_difference if first_density_difference is not None else "",
                    "first_half_saturation": first_half_saturation if first_half_saturation is not None else "",
                    "max_hamming_2000": max(microscopic),
                    "mean_hamming_1001_2000": mean(microscopic[1001:]),
                    "mean_normalized_damage_1001_2000": mean(microscopic[1001:]) / (2 * particles),
                    "max_density_l1_2000": max(macroscopic),
                    "mean_density_l1_1001_2000": mean(macroscopic[1001:]),
                    "exact_reconvergence_observed": False,
                }
            )

    series_rows: list[dict] = []
    for size in sizes:
        for time in range(steps + 1):
            micro_values = [trajectory[time] for trajectory in hamming_series[size]]
            macro_values = [trajectory[time] for trajectory in density_series[size]]
            series_rows.append(
                {
                    "size": size,
                    "time": time,
                    "mean_hamming": mean(micro_values),
                    "median_hamming": median(micro_values),
                    "mean_normalized_damage": mean(micro_values) / (2 * particles),
                    "mean_density_l1": mean(macro_values),
                    "median_density_l1": median(macro_values),
                }
            )

    write_csv(output / "trials.csv", trial_rows)
    write_csv(output / "damage.csv", series_rows)

    plt.figure(figsize=(9, 5.5))
    for size in sizes:
        times = list(range(201))
        values = [
            mean(trajectory[time] for trajectory in hamming_series[size])
            / (2 * particles)
            for time in times
        ]
        plt.plot(times, values, label=f"{size}×{size}")
    plt.xlabel("Time step")
    plt.ylabel("Mean normalized microscopic Hamming distance")
    plt.title(
        "Same-sector damage spreading\n"
        "Initial density, particle number, energy, and momentum are identical"
    )
    plt.legend()
    plt.tight_layout()
    save_figure(output / "damage.png")

class ScalingGeometry:
    def __init__(self, size: int):
        self.size = size
        self.cells = size * size
        self.row_mask = (1 << size) - 1
        self.full_mask = (1 << self.cells) - 1
        self.last_row_shift = size * (size - 1)

    def east(self, bits: int) -> int:
        output = 0
        for y in range(self.size):
            shift = y * self.size
            row = (bits >> shift) & self.row_mask
            rotated = ((row << 1) & self.row_mask) | (row >> (self.size - 1))
            output |= rotated << shift
        return output

    def west(self, bits: int) -> int:
        output = 0
        for y in range(self.size):
            shift = y * self.size
            row = (bits >> shift) & self.row_mask
            rotated = (row >> 1) | ((row & 1) << (self.size - 1))
            output |= rotated << shift
        return output

    def north(self, bits: int) -> int:
        top = bits & self.row_mask
        return (bits >> self.size) | (top << self.last_row_shift)

    def south(self, bits: int) -> int:
        bottom = bits >> self.last_row_shift
        return ((bits << self.size) & self.full_mask) | bottom


ScalingState = tuple[int, int, int, int]


def scaling_collide(state: ScalingState) -> ScalingState:
    n, e, s, w = state
    sites = (e & w & ~(n | s)) | (n & s & ~(e | w))
    return n ^ sites, e ^ sites, s ^ sites, w ^ sites


def scaling_step(state: ScalingState, geometry: ScalingGeometry) -> ScalingState:
    n, e, s, w = scaling_collide(state)
    return geometry.north(n), geometry.east(e), geometry.south(s), geometry.west(w)


def scaling_inverse(state: ScalingState, geometry: ScalingGeometry) -> ScalingState:
    n, e, s, w = state
    return scaling_collide(
        (geometry.south(n), geometry.west(e), geometry.north(s), geometry.east(w))
    )


def scaling_particle_number(state: ScalingState) -> int:
    return sum(board.bit_count() for board in state)


def scaling_momentum(state: ScalingState) -> tuple[int, int]:
    n, e, s, w = state
    return e.bit_count() - w.bit_count(), s.bit_count() - n.bit_count()


def scaling_direction_counts(state: ScalingState) -> tuple[int, int, int, int]:
    return tuple(board.bit_count() for board in state)


def scaling_hamming(first: ScalingState, second: ScalingState) -> int:
    return sum((a ^ b).bit_count() for a, b in zip(first, second))


def scaling_density_signature(state: ScalingState) -> tuple[int, int, int]:
    n, e, s, w = state
    low_1 = n ^ e
    carry_1 = n & e
    low_2 = s ^ w
    carry_2 = s & w
    low = low_1 ^ low_2
    carry_low = low_1 & low_2
    middle = carry_1 ^ carry_2 ^ carry_low
    high = (carry_1 & carry_2) | (carry_1 & carry_low) | (carry_2 & carry_low)
    return low, middle, high


def scaling_macro_difference(first: ScalingState, second: ScalingState) -> int:
    left = scaling_density_signature(first)
    right = scaling_density_signature(second)
    return ((left[0] ^ right[0]) | (left[1] ^ right[1]) | (left[2] ^ right[2])).bit_count()


def scaling_collision_count(state: ScalingState) -> int:
    n, e, s, w = state
    return ((e & w & ~(n | s)) | (n & s & ~(e | w))).bit_count()


def _bits_from_cells(cells: list[int]) -> int:
    board = 0
    for cell in cells:
        board |= 1 << cell
    return board


def scaling_balanced_state(
    geometry: ScalingGeometry,
    channel_filling: float,
    seed: int,
) -> ScalingState:
    rng = Random(seed)
    particles = int(round(channel_filling * 4 * geometry.cells))
    assert particles % 2 == 0
    pair_count = particles // 2
    horizontal_pairs = pair_count // 2
    vertical_pairs = pair_count - horizontal_pairs
    counts = (vertical_pairs, horizontal_pairs, vertical_pairs, horizontal_pairs)
    state = tuple(
        _bits_from_cells(rng.sample(range(geometry.cells), count))
        for count in counts
    )
    assert scaling_particle_number(state) == particles
    assert scaling_momentum(state) == (0, 0)
    return state


def scaling_velocity_swap(
    state: ScalingState,
    geometry: ScalingGeometry,
    seed: int,
) -> ScalingState:
    rng = Random(seed)
    particles: list[tuple[int, int]] = []
    for direction, board in enumerate(state):
        remaining = board
        while remaining:
            bit = remaining & -remaining
            particles.append((bit.bit_length() - 1, direction))
            remaining ^= bit
    for _ in range(10_000):
        cell_a, direction_a = rng.choice(particles)
        cell_b, direction_b = rng.choice(particles)
        if cell_a == cell_b or direction_a == direction_b:
            continue
        if state[direction_b] & (1 << cell_a):
            continue
        if state[direction_a] & (1 << cell_b):
            continue
        changed = list(state)
        bit_a = 1 << cell_a
        bit_b = 1 << cell_b
        changed[direction_a] ^= bit_a
        changed[direction_b] ^= bit_b
        changed[direction_b] |= bit_a
        changed[direction_a] |= bit_b
        perturbed = tuple(changed)
        assert scaling_particle_number(perturbed) == scaling_particle_number(state)
        assert scaling_direction_counts(perturbed) == scaling_direction_counts(state)
        assert scaling_momentum(perturbed) == scaling_momentum(state)
        assert scaling_density_signature(perturbed) == scaling_density_signature(state)
        assert scaling_hamming(perturbed, state) == 4
        return perturbed
    raise RuntimeError("Could not find a valid velocity swap.")


def scaling_exact_cycle(
    initial: ScalingState,
    geometry: ScalingGeometry,
    cap: int,
):
    seen: dict[ScalingState, int] = {}
    state = initial
    initial_particles = scaling_particle_number(initial)
    initial_momentum = scaling_momentum(initial)
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
            assert scaling_particle_number(state) == initial_particles
            assert scaling_momentum(state) == initial_momentum
            assert scaling_inverse(scaling_step(state, geometry), geometry) == state
        state = scaling_step(state, geometry)
    return None


def generate_fixed_density(data_root: Path) -> None:
    import matplotlib.pyplot as plt

    output = data_root / "density-scaling"
    output.mkdir(parents=True, exist_ok=True)
    sizes = (4, 6, 8, 10)
    fillings = (0.125, 0.25, 0.375)
    trials_per_condition = 100
    steps = 1000
    cycle_sizes = (4, 6)
    cycle_trials = 5
    cycle_cap = 100_000

    trial_rows: list[dict] = []
    accumulator: dict[tuple[int, float], dict[str, list[float]]] = {}

    for size in sizes:
        geometry = ScalingGeometry(size)
        for filling in fillings:
            key = (size, filling)
            accumulator[key] = {
                "micro_sum": [0.0] * (steps + 1),
                "macro_sum": [0.0] * (steps + 1),
            }
            for trial in range(trials_per_condition):
                seed = (
                    2_026_071_800
                    + size * 1_000_000
                    + int(filling * 1000) * 1000
                    + trial
                )
                initial = scaling_balanced_state(geometry, filling, seed)
                perturbed = scaling_velocity_swap(initial, geometry, seed + 43_219)
                particles = scaling_particle_number(initial)
                maximum_micro = 2 * particles

                base_cycle = changed_cycle = None
                same_exact_orbit = pair_period = None
                if size in cycle_sizes and trial < cycle_trials:
                    base_cycle = scaling_exact_cycle(initial, geometry, cycle_cap)
                    changed_cycle = scaling_exact_cycle(perturbed, geometry, cycle_cap)
                    if base_cycle is not None:
                        assert base_cycle["first"] == 0
                    if changed_cycle is not None:
                        assert changed_cycle["first"] == 0
                    if base_cycle is not None and changed_cycle is not None:
                        same_exact_orbit = perturbed in base_cycle["seen"]
                        pair_period = lcm(base_cycle["period"], changed_cycle["period"])

                state_a = initial
                state_b = perturbed
                first_macro_split = None
                first_micro_growth = None
                first_half = None
                first_three_quarter = None
                max_micro = 0
                max_macro = 0
                tail_micro: list[float] = []
                tail_macro: list[float] = []
                collision_rates: list[float] = []

                for time in range(steps + 1):
                    micro = scaling_hamming(state_a, state_b)
                    macro = scaling_macro_difference(state_a, state_b)
                    assert micro > 0
                    normalized_micro = micro / maximum_micro
                    normalized_macro = macro / geometry.cells
                    accumulator[key]["micro_sum"][time] += normalized_micro
                    accumulator[key]["macro_sum"][time] += normalized_macro
                    max_micro = max(max_micro, micro)
                    max_macro = max(max_macro, macro)
                    if first_macro_split is None and macro > 0:
                        first_macro_split = time
                    if first_micro_growth is None and micro > 4:
                        first_micro_growth = time
                    if first_half is None and normalized_micro >= 0.5:
                        first_half = time
                    if first_three_quarter is None and normalized_micro >= 0.75:
                        first_three_quarter = time
                    if time >= 501:
                        tail_micro.append(normalized_micro)
                        tail_macro.append(normalized_macro)
                    if time < steps:
                        collision_rates.append(scaling_collision_count(state_a) / geometry.cells)
                        state_a = scaling_step(state_a, geometry)
                        state_b = scaling_step(state_b, geometry)

                searched = size in cycle_sizes and trial < cycle_trials
                trial_rows.append(
                    {
                        "size": size,
                        "channel_filling": filling,
                        "particles": particles,
                        "particles_per_cell": particles / geometry.cells,
                        "trial": trial,
                        "seed": seed,
                        "initial_density_equal": True,
                        "initial_direction_counts_equal": True,
                        "initial_momentum_equal": True,
                        "initial_hamming": 4,
                        "first_macro_split": first_macro_split if first_macro_split is not None else "",
                        "first_micro_growth": first_micro_growth if first_micro_growth is not None else "",
                        "first_half_saturation": first_half if first_half is not None else "",
                        "first_three_quarter_saturation": first_three_quarter if first_three_quarter is not None else "",
                        "max_micro_hamming": max_micro,
                        "max_normalized_micro_damage": max_micro / maximum_micro,
                        "max_macro_changed_cells": max_macro,
                        "max_normalized_macro_damage": max_macro / geometry.cells,
                        "tail_mean_normalized_micro_damage": mean(tail_micro),
                        "tail_mean_normalized_macro_damage": mean(tail_macro),
                        "mean_collision_sites_per_cell": mean(collision_rates),
                        "base_cycle_status": "closed" if base_cycle is not None else ("censored" if searched else "not_searched"),
                        "base_period": base_cycle["period"] if base_cycle is not None else "",
                        "perturbed_cycle_status": "closed" if changed_cycle is not None else ("censored" if searched else "not_searched"),
                        "perturbed_period": changed_cycle["period"] if changed_cycle is not None else "",
                        "same_exact_orbit": same_exact_orbit if same_exact_orbit is not None else "",
                        "pair_period_lcm": pair_period if pair_period is not None else "",
                        "exact_same_time_reconvergence": False,
                    }
                )

    series_rows: list[dict] = []
    for (size, filling), values in accumulator.items():
        for time in range(steps + 1):
            series_rows.append(
                {
                    "size": size,
                    "channel_filling": filling,
                    "time": time,
                    "mean_normalized_micro_damage": values["micro_sum"][time] / trials_per_condition,
                    "mean_normalized_macro_damage": values["macro_sum"][time] / trials_per_condition,
                }
            )

    summary_rows: list[dict] = []
    for filling in fillings:
        for size in sizes:
            rows = [row for row in trial_rows if row["size"] == size and row["channel_filling"] == filling]
            growth = [int(row["first_micro_growth"]) for row in rows if row["first_micro_growth"] != ""]
            half = [int(row["first_half_saturation"]) for row in rows if row["first_half_saturation"] != ""]
            three_quarter = [int(row["first_three_quarter_saturation"]) for row in rows if row["first_three_quarter_saturation"] != ""]
            closed = [row for row in rows if row["base_cycle_status"] == "closed" and row["perturbed_cycle_status"] == "closed"]
            summary_rows.append(
                {
                    "size": size,
                    "channel_filling": filling,
                    "particles": rows[0]["particles"],
                    "particles_per_cell": rows[0]["particles_per_cell"],
                    "trials": len(rows),
                    "macro_split_count": sum(row["first_macro_split"] != "" for row in rows),
                    "median_first_macro_split": median(int(row["first_macro_split"]) for row in rows if row["first_macro_split"] != ""),
                    "micro_growth_count": len(growth),
                    "median_first_micro_growth": median(growth) if growth else "",
                    "half_saturation_count": len(half),
                    "median_first_half_saturation": median(half) if half else "",
                    "three_quarter_saturation_count": len(three_quarter),
                    "tail_mean_normalized_micro_damage": mean(row["tail_mean_normalized_micro_damage"] for row in rows),
                    "tail_mean_normalized_macro_damage": mean(row["tail_mean_normalized_macro_damage"] for row in rows),
                    "mean_collision_sites_per_cell": mean(row["mean_collision_sites_per_cell"] for row in rows),
                    "cycle_searches": sum(row["base_cycle_status"] != "not_searched" for row in rows),
                    "closed_cycle_pairs": len(closed),
                    "changed_period_count": sum(row["base_period"] != row["perturbed_period"] for row in closed),
                    "same_orbit_count": sum(row["same_exact_orbit"] is True for row in closed),
                    "largest_closed_period": max(max(int(row["base_period"]), int(row["perturbed_period"])) for row in closed) if closed else "",
                }
            )

    write_csv(output / "trials.csv", trial_rows)
    write_csv(output / "summary.csv", summary_rows)
    write_csv(output / "damage.csv", series_rows)

    plt.figure(figsize=(9.5, 5.8))
    for filling in fillings:
        selected = [next(row for row in summary_rows if row["size"] == size and row["channel_filling"] == filling) for size in sizes]
        plt.plot(sizes, [row["tail_mean_normalized_micro_damage"] for row in selected], marker="o", label=f"channel filling {filling:.3f}")
    plt.xlabel("Lattice side length")
    plt.ylabel("Tail mean normalized microscopic damage")
    plt.title("Same-sector damage at fixed velocity-channel filling\nAverages over steps 501–1000 and 100 pairs per condition")
    plt.legend()
    plt.tight_layout()
    save_figure(output / "micro-damage.png")

    plt.figure(figsize=(9.5, 5.8))
    for filling in fillings:
        selected = [next(row for row in summary_rows if row["size"] == size and row["channel_filling"] == filling) for size in sizes]
        plt.plot(sizes, [row["tail_mean_normalized_macro_damage"] for row in selected], marker="o", label=f"channel filling {filling:.3f}")
    plt.xlabel("Lattice side length")
    plt.ylabel("Tail mean fraction of density-different cells")
    plt.title("Macroscopic divergence at fixed velocity-channel filling\nAverages over steps 501–1000 and 100 pairs per condition")
    plt.legend()
    plt.tight_layout()
    save_figure(output / "macro-damage.png")

def generate_hexagonal_rotor(data_root: Path) -> None:
    import matplotlib.pyplot as plt

    output = data_root / "rotor"
    output.mkdir(parents=True, exist_ok=True)
    sizes = (4, 6, 8, 10)
    densities = (0.5, 1.0, 1.5)
    trials_per_condition = 75
    steps = 1000
    cycle_trials = 5
    cycle_cap = 150_000

    for local_mask in range(64):
        for rotor in (0, 1):
            after = hex_local_collision(local_mask, rotor)
            assert hex_local_collision(*after) == (local_mask, rotor)

    trial_rows: list[dict] = []
    accumulator: dict[tuple[int, float], dict[str, list[float]]] = {}

    for size in sizes:
        geometry = HexGeometry(size)
        for particles_per_cell in densities:
            key = (size, particles_per_cell)
            accumulator[key] = {
                "particle_sum": [0.0] * (steps + 1),
                "rotor_sum": [0.0] * (steps + 1),
                "macro_sum": [0.0] * (steps + 1),
            }
            for trial in range(trials_per_condition):
                seed = (
                    2_026_071_800
                    + size * 1_000_000
                    + int(particles_per_cell * 1000) * 1000
                    + trial
                )
                initial = hex_balanced_random_state(geometry, particles_per_cell, seed)
                perturbed = hex_density_preserving_velocity_swap(initial, geometry, seed + 708_311)
                particles = hex_particle_number(initial)
                max_particle_distance = 2 * particles
                assert hex_particle_number(perturbed) == particles
                assert hex_direction_counts(initial) == hex_direction_counts(perturbed)
                assert hex_momentum(initial) == hex_momentum(perturbed) == (0, 0)
                assert hex_density_signature(initial) == hex_density_signature(perturbed)
                assert initial[6] == perturbed[6]
                assert hex_particle_hamming(initial, perturbed) == 4

                base_cycle = changed_cycle = None
                same_exact_orbit = pair_period = None
                searched = size == 4 and trial < cycle_trials
                if searched:
                    base_cycle = hex_exact_cycle(initial, geometry, cycle_cap)
                    changed_cycle = hex_exact_cycle(perturbed, geometry, cycle_cap)
                    if base_cycle is not None:
                        assert base_cycle["first"] == 0
                    if changed_cycle is not None:
                        assert changed_cycle["first"] == 0
                    if base_cycle is not None and changed_cycle is not None:
                        same_exact_orbit = perturbed in base_cycle["seen"]
                        pair_period = lcm(base_cycle["period"], changed_cycle["period"])

                state_a = initial
                state_b = perturbed
                first_macro = None
                first_particle_growth = None
                first_rotor = None
                first_half = None
                particle_reconvergence = None
                max_particle = 0
                max_rotor = 0
                max_macro = 0
                tail_particle: list[float] = []
                tail_rotor: list[float] = []
                tail_macro: list[float] = []
                collision_rates: list[float] = []

                for time in range(steps + 1):
                    particle_damage = hex_particle_hamming(state_a, state_b)
                    rotor_damage = hex_rotor_hamming(state_a, state_b)
                    macro_damage = hex_macro_changed_cells(state_a, state_b)
                    assert particle_damage + rotor_damage > 0
                    normalized_particle = particle_damage / max_particle_distance
                    normalized_rotor = rotor_damage / geometry.cells
                    normalized_macro = macro_damage / geometry.cells
                    accumulator[key]["particle_sum"][time] += normalized_particle
                    accumulator[key]["rotor_sum"][time] += normalized_rotor
                    accumulator[key]["macro_sum"][time] += normalized_macro
                    max_particle = max(max_particle, particle_damage)
                    max_rotor = max(max_rotor, rotor_damage)
                    max_macro = max(max_macro, macro_damage)
                    if first_macro is None and macro_damage > 0:
                        first_macro = time
                    if first_particle_growth is None and particle_damage > 4:
                        first_particle_growth = time
                    if first_rotor is None and rotor_damage > 0:
                        first_rotor = time
                    if first_half is None and normalized_particle >= 0.5:
                        first_half = time
                    if particle_reconvergence is None and time > 0 and particle_damage == 0 and rotor_damage > 0:
                        particle_reconvergence = time
                    if time >= 501:
                        tail_particle.append(normalized_particle)
                        tail_rotor.append(normalized_rotor)
                        tail_macro.append(normalized_macro)
                    if time < steps:
                        collision_rates.append(hex_collision_count(state_a, geometry) / geometry.cells)
                        state_a = hex_step(state_a, geometry)
                        state_b = hex_step(state_b, geometry)

                trial_rows.append(
                    {
                        "size": size,
                        "particles_per_cell": particles_per_cell,
                        "particles": particles,
                        "trial": trial,
                        "seed": seed,
                        "initial_density_equal": True,
                        "initial_direction_counts_equal": True,
                        "initial_momentum_equal": True,
                        "initial_rotor_field_equal": True,
                        "initial_particle_hamming": 4,
                        "first_macro_split": first_macro if first_macro is not None else "",
                        "first_particle_growth": first_particle_growth if first_particle_growth is not None else "",
                        "first_rotor_split": first_rotor if first_rotor is not None else "",
                        "first_half_particle_damage": first_half if first_half is not None else "",
                        "particle_micro_reconvergence_with_rotor_difference": particle_reconvergence if particle_reconvergence is not None else "",
                        "max_particle_hamming": max_particle,
                        "max_normalized_particle_damage": max_particle / max_particle_distance,
                        "max_rotor_hamming": max_rotor,
                        "max_normalized_rotor_damage": max_rotor / geometry.cells,
                        "max_macro_changed_cells": max_macro,
                        "max_normalized_macro_damage": max_macro / geometry.cells,
                        "tail_mean_normalized_particle_damage": mean(tail_particle),
                        "tail_mean_normalized_rotor_damage": mean(tail_rotor),
                        "tail_mean_normalized_macro_damage": mean(tail_macro),
                        "mean_collision_sites_per_cell": mean(collision_rates),
                        "base_cycle_status": "closed" if base_cycle is not None else ("censored" if searched else "not_searched"),
                        "base_period": base_cycle["period"] if base_cycle is not None else "",
                        "perturbed_cycle_status": "closed" if changed_cycle is not None else ("censored" if searched else "not_searched"),
                        "perturbed_period": changed_cycle["period"] if changed_cycle is not None else "",
                        "same_exact_orbit": same_exact_orbit if same_exact_orbit is not None else "",
                        "pair_period_lcm": pair_period if pair_period is not None else "",
                        "exact_complete_reconvergence": False,
                    }
                )

    rotation_cases = 300
    for case in range(rotation_cases):
        size = sizes[case % len(sizes)]
        geometry = HexGeometry(size)
        particles_per_cell = densities[case % len(densities)]
        state = hex_balanced_random_state(geometry, particles_per_cell, 9_000_000 + case)
        rotated = hex_rotate_state(state, geometry)
        for _ in range(100):
            assert rotated == hex_rotate_state(state, geometry)
            state = hex_step(state, geometry)
            rotated = hex_step(rotated, geometry)

    series_rows: list[dict] = []
    for (size, particles_per_cell), values in accumulator.items():
        for time in range(steps + 1):
            series_rows.append(
                {
                    "size": size,
                    "particles_per_cell": particles_per_cell,
                    "time": time,
                    "mean_normalized_particle_damage": values["particle_sum"][time] / trials_per_condition,
                    "mean_normalized_rotor_damage": values["rotor_sum"][time] / trials_per_condition,
                    "mean_normalized_macro_damage": values["macro_sum"][time] / trials_per_condition,
                }
            )

    summary_rows: list[dict] = []
    for particles_per_cell in densities:
        for size in sizes:
            rows = [row for row in trial_rows if row["size"] == size and row["particles_per_cell"] == particles_per_cell]
            growth = [int(row["first_particle_growth"]) for row in rows if row["first_particle_growth"] != ""]
            rotor_splits = [int(row["first_rotor_split"]) for row in rows if row["first_rotor_split"] != ""]
            closed = [row for row in rows if row["base_cycle_status"] == "closed" and row["perturbed_cycle_status"] == "closed"]
            summary_rows.append(
                {
                    "size": size,
                    "particles_per_cell": particles_per_cell,
                    "particles": rows[0]["particles"],
                    "trials": len(rows),
                    "macro_split_count": sum(row["first_macro_split"] != "" for row in rows),
                    "particle_growth_count": len(growth),
                    "median_first_particle_growth": median(growth) if growth else "",
                    "rotor_split_count": len(rotor_splits),
                    "median_first_rotor_split": median(rotor_splits) if rotor_splits else "",
                    "half_particle_damage_count": sum(row["first_half_particle_damage"] != "" for row in rows),
                    "particle_micro_reconvergence_count": sum(row["particle_micro_reconvergence_with_rotor_difference"] != "" for row in rows),
                    "tail_particle_damage": mean(row["tail_mean_normalized_particle_damage"] for row in rows),
                    "tail_rotor_damage": mean(row["tail_mean_normalized_rotor_damage"] for row in rows),
                    "tail_macro_damage": mean(row["tail_mean_normalized_macro_damage"] for row in rows),
                    "collision_sites_per_cell": mean(row["mean_collision_sites_per_cell"] for row in rows),
                    "cycle_audits": sum(row["base_cycle_status"] != "not_searched" for row in rows),
                    "closed_cycle_pairs": len(closed),
                    "changed_period_count": sum(row["base_period"] != row["perturbed_period"] for row in closed),
                    "same_orbit_count": sum(row["same_exact_orbit"] is True for row in closed),
                    "largest_closed_period": max(max(int(row["base_period"]), int(row["perturbed_period"])) for row in closed) if closed else "",
                }
            )

    write_csv(output / "trials.csv", trial_rows)
    write_csv(output / "summary.csv", summary_rows)
    write_csv(output / "damage.csv", series_rows)

    def make_chart(filename: str, key: str, ylabel: str, title: str) -> None:
        plt.figure(figsize=(9.5, 5.8))
        for particles_per_cell in densities:
            selected = [next(row for row in summary_rows if row["size"] == size and row["particles_per_cell"] == particles_per_cell) for size in sizes]
            plt.plot(sizes, [row[key] for row in selected], marker="o", label=f"{particles_per_cell:.1f} particles/cell")
        plt.xlabel("Hexagonal torus side length")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        save_figure(output / filename)

    make_chart(
        "particle-damage.png",
        "tail_particle_damage",
        "Tail mean normalized particle Hamming damage",
        "Hexagonal reversible lattice-gas particle damage\nSteps 501–1000; 75 paired trials per condition",
    )
    make_chart(
        "rotor-damage.png",
        "tail_rotor_damage",
        "Tail mean fraction of differing rotor bits",
        "Propagation into hidden collision-memory variables\nSteps 501–1000; 75 paired trials per condition",
    )
    make_chart(
        "macro-damage.png",
        "tail_macro_damage",
        "Tail mean fraction of density-different cells",
        "Hexagonal reversible lattice-gas density divergence\nSteps 501–1000; 75 paired trials per condition",
    )

def generate_continuous(data_root: Path) -> None:
    import matplotlib.pyplot as plt

    output = data_root / "continuous"
    output.mkdir(parents=True, exist_ok=True)
    initial = RingState(
        positions=(Fraction(1, 20), Fraction(7, 20), Fraction(13, 20), Fraction(17, 20)),
        velocities=(Fraction(3, 5), Fraction(-1, 5), Fraction(2, 5), Fraction(-2, 5)),
    )
    time_step = Fraction(1, 20)
    steps_per_period = 200
    base_orbit, _ = sample_orbit(initial, time_step, 2 * steps_per_period)
    repeat = first_sampled_repeat(base_orbit)
    assert repeat == (0, 200, 200)
    period = time_step * repeat[2]
    returned, collisions = ring_advance(initial, period)
    assert returned == initial and collisions == 36

    reversed_start, forward_collisions = ring_advance(initial, Fraction(37, 20))
    reversed_evolved, reverse_collisions = ring_advance(time_reverse(reversed_start), Fraction(37, 20))
    assert time_reverse(reversed_evolved) == initial
    assert forward_collisions == reverse_collisions == 7

    changed_velocities = list(initial.velocities)
    changed_velocities[0], changed_velocities[2] = changed_velocities[2], changed_velocities[0]
    perturbed = RingState(initial.positions, tuple(changed_velocities))
    assert ring_momentum(perturbed) == ring_momentum(initial)
    assert kinetic_energy(perturbed) == kinetic_energy(initial)
    changed_orbit, _ = sample_orbit(perturbed, time_step, 2 * steps_per_period)
    assert first_sampled_repeat(changed_orbit) == (0, 200, 200)

    distances = [
        torus_position_l1(first, second)
        for first, second in zip(base_orbit[: steps_per_period + 1], changed_orbit[: steps_per_period + 1])
    ]
    assert [
        i for i, (first, second) in enumerate(zip(base_orbit[:201], changed_orbit[:201]))
        if first.positions == second.positions
    ] == [0, 100, 200]

    orbit_rows = []
    for index in range(steps_per_period + 1):
        first = base_orbit[index]
        second = changed_orbit[index]
        orbit_rows.append(
            {
                "step": index,
                "time": fraction_text(index * time_step),
                "base_positions": "|".join(fraction_text(value) for value in first.positions),
                "base_velocities": "|".join(fraction_text(value) for value in first.velocities),
                "perturbed_positions": "|".join(fraction_text(value) for value in second.positions),
                "perturbed_velocities": "|".join(fraction_text(value) for value in second.velocities),
                "position_torus_l1": fraction_text(distances[index]),
                "positions_exactly_equal": first.positions == second.positions,
                "complete_states_equal": first == second,
            }
        )
    write_csv(output / "elastic-orbit.csv", orbit_rows)

    getcontext().prec = 80
    sqrt_two = Decimal(2).sqrt()
    convergent_rows = []
    p_previous, p_current = 1, 3
    q_previous, q_current = 1, 2
    while True:
        error = abs(Decimal(q_previous) * sqrt_two - Decimal(p_previous))
        velocity_error = abs(sqrt_two - Decimal(p_previous) / Decimal(q_previous))
        convergent_rows.append(
            {
                "p": p_previous,
                "q": q_previous,
                "torus_return_error": str(error),
                "rational_velocity_error": str(velocity_error),
            }
        )
        p_next = 2 * p_current + p_previous
        q_next = 2 * q_current + q_previous
        p_previous, p_current = p_current, p_next
        q_previous, q_current = q_current, q_next
        if q_previous > 1_000_000:
            break
    assert (convergent_rows[-1]["p"], convergent_rows[-1]["q"]) == (665857, 470832)
    write_csv(output / "torus-returns.csv", convergent_rows)

    plt.figure(figsize=(9.2, 5.5))
    plt.plot([float(index * time_step) for index in range(201)], [float(value) for value in distances])
    plt.xlabel("Time")
    plt.ylabel("Labeled-particle torus L1 position distance")
    plt.title("Same energy and momentum, different velocity assignment")
    plt.tight_layout()
    save_figure(output / "elastic-distance.png")

    plt.figure(figsize=(9.2, 5.5))
    plt.loglog(
        [int(row["q"]) for row in convergent_rows],
        [float(Decimal(row["torus_return_error"])) for row in convergent_rows],
        marker="o",
    )
    plt.xlabel("Integer candidate return time q")
    plt.ylabel("|q√2 − nearest integer|")
    plt.title("Arbitrarily close but never exact returns on a continuous torus")
    plt.tight_layout()
    save_figure(output / "torus-error.png")


def generate_all_data(data_root: Path) -> None:
    generate_square_reference(data_root)
    generate_hpp_ambiguity_catalog(data_root)
    generate_conserved_sector(data_root)
    generate_fixed_density(data_root)
    generate_hexagonal_rotor(data_root)
    generate_continuous(data_root)
    run([
        sys.executable,
        str(ROOT / "scripts" / "generate_periods.py"),
        "--output-root",
        str(data_root),
    ])


def copy_paper_figures(data_root: Path, paper_root: Path) -> None:
    paper_root.mkdir(parents=True, exist_ok=True)
    mapping = {
        data_root / "continuous" / "elastic-distance.png": paper_root / "elastic-distance.png",
        data_root / "continuous" / "torus-error.png": paper_root / "torus-error.png",
        data_root / "density-scaling" / "micro-damage.png": paper_root / "hpp-damage.png",
        data_root / "rotor" / "rotor-damage.png": paper_root / "rotor-damage.png",
        data_root / "hpp" / "ambiguity.png": paper_root / "hpp-ambiguity.png",
    }
    for source, destination in mapping.items():
        shutil.copyfile(source, destination)


def reproduce_data() -> None:
    generate_all_data(DATA)
    copy_paper_figures(DATA, ROOT / "paper" / "figures")
    print("Data and figures regenerated from source code.")


def verify_reproduction() -> None:
    with tempfile.TemporaryDirectory(prefix="recurrence-reproduction-") as temporary:
        generated = Path(temporary) / "data"
        generate_all_data(generated)
        failures: list[str] = []
        for committed in sorted(DATA.rglob("*")):
            if not committed.is_file() or committed.suffix.lower() not in {".csv", ".png"}:
                continue
            relative = committed.relative_to(DATA)
            candidate = generated / relative
            if not candidate.is_file():
                failures.append(f"missing generated file: {relative}")
                continue
            if committed.suffix.lower() == ".csv":
                if committed.read_bytes() != candidate.read_bytes():
                    failures.append(f"CSV mismatch: {relative}")
            else:
                try:
                    from PIL import Image, ImageChops, ImageStat

                    with Image.open(committed).convert("RGB") as left, Image.open(candidate).convert("RGB") as right:
                        if left.size != right.size:
                            failures.append(f"image-size mismatch: {relative}")
                            continue
                        difference = ImageChops.difference(left, right)
                        rms = sum(value * value for value in ImageStat.Stat(difference).rms) ** 0.5
                        if rms > 3.0:
                            failures.append(f"image mismatch: {relative} (RMS {rms:.3f})")
                except ImportError:
                    if committed.read_bytes() != candidate.read_bytes():
                        failures.append(f"PNG mismatch: {relative}")
        if failures:
            raise RuntimeError("\n".join(failures))
    print("Independent reproduction matched all committed tables and figures.")


def _four_particle_zero_momentum_states() -> tuple[tuple[int, ...], ...]:
    states = []
    for occupied_channels in combinations(range(36), 4):
        cells = [0] * 9
        for channel in occupied_channels:
            cells[channel // 4] |= 1 << (channel % 4)
        state = tuple(cells)
        if momentum(state) == (0, 0):
            states.append(state)
    return tuple(states)


def _canonical_cycle(
    initial: tuple[int, ...],
    step: Callable[[tuple[int, ...]], tuple[int, ...]],
) -> tuple[tuple[int, ...], ...]:
    orbit: list[tuple[int, ...]] = []
    state = initial
    while state not in orbit:
        orbit.append(state)
        state = step(state)
    if state != initial:
        raise AssertionError("Expected a reversible orbit to return to its initial state.")
    rotations = [tuple(orbit[offset:] + orbit[:offset]) for offset in range(len(orbit))]
    return min(rotations)


def _canonical_density_word(
    cycle: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    word = [density(state) for state in cycle]
    rotations = [tuple(word[offset:] + word[:offset]) for offset in range(len(word))]
    return min(rotations)



_SQUARE_SYMMETRIES = (
    ((1, 0), (0, 1)),
    ((0, -1), (1, 0)),
    ((-1, 0), (0, -1)),
    ((0, 1), (-1, 0)),
    ((-1, 0), (0, 1)),
    ((1, 0), (0, -1)),
    ((0, 1), (1, 0)),
    ((0, -1), (-1, 0)),
)


def _matrix_determinant(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )


def _transform_hpp_state(
    state: tuple[int, ...],
    matrix: tuple[tuple[int, int], tuple[int, int]],
    translate_x: int,
    translate_y: int,
) -> tuple[int, ...]:
    vector_by_direction = {
        NORTH: (0, -1),
        EAST: (1, 0),
        SOUTH: (0, 1),
        WEST: (-1, 0),
    }
    direction_by_vector = {
        vector: direction
        for direction, vector in vector_by_direction.items()
    }
    transformed = [0] * 9
    for y in range(3):
        for x in range(3):
            mask = state[3 * y + x]
            new_x = (
                matrix[0][0] * x
                + matrix[0][1] * y
                + translate_x
            ) % 3
            new_y = (
                matrix[1][0] * x
                + matrix[1][1] * y
                + translate_y
            ) % 3
            new_mask = 0
            for direction, (dx, dy) in vector_by_direction.items():
                if not mask & direction:
                    continue
                new_vector = (
                    matrix[0][0] * dx + matrix[0][1] * dy,
                    matrix[1][0] * dx + matrix[1][1] * dy,
                )
                new_mask |= direction_by_vector[new_vector]
            transformed[3 * new_y + new_x] = new_mask
    return tuple(transformed)


def validate_observability_result() -> None:
    checked_ca_states = 0
    for size in range(2, 9):
        states = tuple(ca_all_states(size))
        checked_ca_states += len(states)
        result = predictive_partition(ca_step, states, lambda state: state[1])
        expected = 2 ** (2 * size)
        assert result.class_counts == (2**size, expected, expected)
        assert result.is_state_reconstructing
    assert checked_ca_states == 87_376

    states = _four_particle_zero_momentum_states()
    hpp_step = lambda state: square_step(state, 3, 3)
    result = predictive_partition(hpp_step, states, density)
    assert len(states) == 9_153
    assert all(particle_number(state) == 4 for state in states)
    assert all(momentum(state) == (0, 0) for state in states)
    assert all(time_reverse_state(time_reverse_state(state)) == state for state in states)
    assert all(density(time_reverse_state(state)) == density(state) for state in states)
    assert all(
        time_reverse_state(square_step(time_reverse_state(state), 3, 3))
        == square_inverse_step(state, 3, 3)
        for state in states
    )
    assert result.class_counts == (495, 6_948, 9_090, 9_126, 9_126)

    groups = tuple(result.classes().values())
    class_sizes = [len(group) for group in groups]
    assert class_sizes.count(1) == 9_099
    assert class_sizes.count(2) == 27
    assert max(class_sizes) == 2

    ambiguous_states = {
        state
        for group in groups
        if len(group) == 2
        for state in group
    }
    assert len(ambiguous_states) == 54

    microscopic_cycles = {
        _canonical_cycle(state, hpp_step)
        for state in ambiguous_states
    }
    assert len(microscopic_cycles) == 18
    assert {len(cycle) for cycle in microscopic_cycles} == {3}
    assert all(
        collision_site_count(state) == 0
        for cycle in microscopic_cycles
        for state in cycle
    )
    assert all(
        sum(mask != 0 for mask in state) == 4
        and all(mask in {0, NORTH, EAST, SOUTH, WEST} for mask in state)
        for cycle in microscopic_cycles
        for state in cycle
    )

    cycles_by_density_word: dict[
        tuple[tuple[int, ...], ...],
        set[tuple[tuple[int, ...], ...]],
    ] = {}
    for cycle in microscopic_cycles:
        word = _canonical_density_word(cycle)
        cycles_by_density_word.setdefault(word, set()).add(cycle)
    assert len(cycles_by_density_word) == 9
    assert {len(cycles) for cycles in cycles_by_density_word.values()} == {2}
    for paired_cycles in cycles_by_density_word.values():
        first, second = tuple(paired_cycles)
        assert {
            reverse_velocities(state)
            for state in first
        } == set(second)
        assert {
            reverse_velocities(state)
            for state in second
        } == set(first)

    prototype = min(microscopic_cycles)
    all_symmetry_images = {
        _canonical_cycle(
            _transform_hpp_state(prototype[0], matrix, tx, ty),
            hpp_step,
        )
        for matrix in _SQUARE_SYMMETRIES
        for tx in range(3)
        for ty in range(3)
    }
    proper_images = {
        _canonical_cycle(
            _transform_hpp_state(prototype[0], matrix, tx, ty),
            hpp_step,
        )
        for matrix in _SQUARE_SYMMETRIES
        if _matrix_determinant(matrix) == 1
        for tx in range(3)
        for ty in range(3)
    }
    improper_images = {
        _canonical_cycle(
            _transform_hpp_state(prototype[0], matrix, tx, ty),
            hpp_step,
        )
        for matrix in _SQUARE_SYMMETRIES
        if _matrix_determinant(matrix) == -1
        for tx in range(3)
        for ty in range(3)
    }
    assert all_symmetry_images == microscopic_cycles
    assert len(proper_images) == len(improper_images) == 9
    assert proper_images.isdisjoint(improper_images)

    representative_a = (1, 2, 0, 8, 4, 0, 0, 0, 0)
    representative_b = (8, 1, 0, 4, 2, 0, 0, 0, 0)
    assert result.class_of[representative_a] == result.class_of[representative_b]
    assert _canonical_cycle(representative_a, hpp_step) != _canonical_cycle(
        representative_b, hpp_step
    )
    assert momentum(representative_a) == momentum(representative_b) == (0, 0)
    print("Exact predictive-state results validated.")


def has_value(row: dict[str, str], key: str) -> bool:
    return row[key].strip() != ""


def is_false(row: dict[str, str], key: str) -> bool:
    return row[key].strip().lower() in {"false", "0", "no"}


def validate_data() -> None:
    ambiguity = read_rows("hpp/ambiguity.csv")
    assert len(ambiguity) == 54
    assert {int(row["pair_id"]) for row in ambiguity} == set(range(1, 10))
    assert {row["cycle"] for row in ambiguity} == {"A", "B"}
    assert {int(row["phase"]) for row in ambiguity} == {0, 1, 2}
    assert len({row["cycle_id"] for row in ambiguity}) == 18
    assert len({row["state_encoding"] for row in ambiguity}) == 54
    assert len({(row["cycle_id"], row["phase"]) for row in ambiguity}) == 54
    assert all(int(row["least_period"]) == 3 for row in ambiguity)
    assert all(int(row["collision_sites"]) == 0 for row in ambiguity)
    assert all(
        sum(int(value) != 0 for value in row["state_masks"].split()) == 4
        for row in ambiguity
    )
    for pair_id in range(1, 10):
        pair_rows = [
            row for row in ambiguity
            if int(row["pair_id"]) == pair_id
        ]
        for phase in range(3):
            phase_rows = [
                row for row in pair_rows
                if int(row["phase"]) == phase
            ]
            assert len(phase_rows) == 2
            assert phase_rows[0]["density"] == phase_rows[1]["density"]

        keyed = {(row["cycle"], int(row["phase"])): row for row in pair_rows}
        for cycle_name in ("A", "B"):
            for phase in range(3):
                row = keyed[(cycle_name, phase)]
                state = state_from_hex(row["state_encoding"], 3, 3)
                successor = state_from_hex(row["successor_encoding"], 3, 3)
                predecessor = state_from_hex(row["predecessor_encoding"], 3, 3)
                reversed_state = state_from_hex(row["reversed_state_encoding"], 3, 3)
                partner_cycle = row["velocity_reversal_partner_cycle"]
                partner_phase = int(row["velocity_reversal_partner_phase"])
                shift = int(row["observation_reversal_shift"])
                assert successor == square_step(state, 3, 3)
                assert square_step(predecessor, 3, 3) == state
                assert reversed_state == reverse_velocities(state)
                assert reversed_state == time_reverse_state(state)
                assert reversed_state == state_from_hex(
                    keyed[(partner_cycle, partner_phase)]["state_encoding"], 3, 3
                )
                assert partner_phase == (shift - phase) % 3

    conserved = read_rows("perturbations/trials.csv")
    assert len(conserved) == 150
    assert sum(has_value(row, "first_density_difference") for row in conserved) == 150
    assert sum(has_value(row, "first_micro_growth") for row in conserved) == 139
    assert sum(is_false(row, "exact_reconvergence_observed") for row in conserved) == 150
    closed_conserved = [row for row in conserved if has_value(row, "base_period")]
    assert len(closed_conserved) == 30
    assert sum(row["base_period"] != row["perturbed_period"] for row in closed_conserved) == 26
    assert sum(row["same_exact_cycle"] == "False" for row in closed_conserved) == 30

    scaling = read_rows("density-scaling/trials.csv")
    assert len(scaling) == 1200
    assert sum(has_value(row, "first_macro_split") for row in scaling) == 1200
    assert sum(has_value(row, "first_micro_growth") for row in scaling) == 1158
    assert sum(has_value(row, "first_half_saturation") for row in scaling) == 669
    assert sum(is_false(row, "exact_same_time_reconvergence") for row in scaling) == 1200
    closed_scaling = [row for row in scaling if row["base_cycle_status"] == "closed" and row["perturbed_cycle_status"] == "closed"]
    assert len(closed_scaling) == 20
    assert sum(row["base_period"] != row["perturbed_period"] for row in closed_scaling) == 19
    assert sum(row["same_exact_orbit"] == "False" for row in closed_scaling) == 20

    rotor = read_rows("rotor/trials.csv")
    assert len(rotor) == 900
    assert sum(has_value(row, "first_macro_split") for row in rotor) == 900
    assert sum(has_value(row, "first_particle_growth") for row in rotor) == 852
    assert sum(has_value(row, "first_rotor_split") for row in rotor) == 849
    assert sum(is_false(row, "exact_complete_reconvergence") for row in rotor) == 900
    closed_rotor = [row for row in rotor if row["base_cycle_status"] == "closed" and row["perturbed_cycle_status"] == "closed"]
    assert len(closed_rotor) == 7
    assert sum(row["base_period"] != row["perturbed_period"] for row in closed_rotor) == 4
    assert sum(row["same_exact_orbit"] == "False" for row in closed_rotor) == 7

    torus = read_rows("continuous/torus-returns.csv")
    assert len(torus) == 16
    denominators = [int(row["q"]) for row in torus]
    errors = [Decimal(row["torus_return_error"]) for row in torus]
    assert denominators[-1] == 470832
    assert all(right < left for left, right in zip(errors, errors[1:]))

    orbit = read_rows("continuous/elastic-orbit.csv")
    assert orbit[0]["time"] == "0"
    assert any(row["time"] == "10" and row["complete_states_equal"] == "False" for row in orbit)

    square = read_rows("hpp/size-sweep.csv")
    assert len(square) == 15
    pair = read_rows("hpp/hamming.csv")
    assert len(pair) == 4726

    period4 = read_rows("periods/4x4-periods.csv")
    assert sum(int(row["state_count"]) for row in period4) == 94336
    assert sum(int(row["cycle_count"]) for row in period4) == 19448

    target5 = read_rows("periods/5x5-summary.csv")
    assert len(target5) == 1
    assert int(target5[0]["microscopic_period_T"]) == 9705
    assert int(target5[0]["fixed_histogram_line_momentum_fiber_states"]) == 2209
    assert int(target5[0]["interaction_macroperiod_T_over_g"]) == 1941

    empirical = read_rows("periods/5x5-sample.csv")
    assert len(empirical) == 500
    assert len({int(row["period"]) for row in empirical}) == 344
    assert min(int(row["period"]) for row in empirical) == 5
    assert max(int(row["period"]) for row in empirical) == 201810

    validate_observability_result()
    print("Data validation passed.")


def run_tests() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    run([sys.executable, "-m", "pytest", "-q"], env=env)



def run_certificate_verifier() -> None:
    run([sys.executable, str(ROOT / "scripts" / "verify_ambiguity.py")])


def run_period_navigation_verifier() -> None:
    run([sys.executable, str(ROOT / "scripts" / "verify_periods.py")])


def run_repository_validation() -> None:
    run([sys.executable, str(ROOT / "scripts" / "validate_repo.py")])

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_files() -> list[Path]:
    excluded_suffixes = {".aux", ".log", ".out", ".toc"}
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == "manifest.sha256":
            continue
        if any(part in {".git", ".pytest_cache", "__pycache__", ".venv", "venv", ".mypy_cache", ".ruff_cache", "build", "dist", ".validation_tmp"} for part in path.parts):
            continue
        if path.suffix in excluded_suffixes:
            continue
        if any(part.endswith(".egg-info") for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def write_manifest() -> None:
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in repository_files()]
    (ROOT / "manifest.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Manifest written for {len(lines)} files.")


def validate_integrity() -> None:
    manifest = ROOT / "manifest.sha256"
    failures: list[str] = []
    listed: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        listed.add(relative)
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing: {relative}")
        elif sha256(path) != expected:
            failures.append(f"hash mismatch: {relative}")
    actual = {path.relative_to(ROOT).as_posix() for path in repository_files()}
    for relative in sorted(actual - listed):
        failures.append(f"unlisted: {relative}")
    for relative in sorted(listed - actual):
        failures.append(f"manifest-only: {relative}")
    if failures:
        raise RuntimeError("\n".join(failures))
    print(f"Integrity validation passed for {len(listed)} files.")


def build_paper() -> None:
    if shutil.which("pdflatex") is None:
        print("Paper build skipped: pdflatex is not installed.")
        return
    paper_dir = ROOT / "paper"
    source = paper_dir / "paper.tex"
    env = os.environ.copy()
    env.update({"SOURCE_DATE_EPOCH": "0", "FORCE_SOURCE_DATE": "1", "TZ": "UTC"})
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", source.name]
    run(latex, cwd=paper_dir, env=env)
    run(latex, cwd=paper_dir, env=env)
    for suffix in (".aux", ".log", ".out", ".toc"):
        artifact = paper_dir / f"{source.stem}{suffix}"
        if artifact.exists():
            artifact.unlink()
    print(f"Paper built: {paper_dir / (source.stem + '.pdf')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "profile",
        choices=("test", "certificate", "period", "reproduce", "reproduction", "data", "repository", "integrity", "manifest", "paper", "all"),
        help="validation profile",
    )
    args = parser.parse_args()

    if args.profile == "test":
        run_tests()
    elif args.profile == "certificate":
        run_certificate_verifier()
    elif args.profile == "period":
        run_period_navigation_verifier()
    elif args.profile == "reproduce":
        reproduce_data()
    elif args.profile == "reproduction":
        verify_reproduction()
    elif args.profile == "data":
        validate_data()
    elif args.profile == "repository":
        run_repository_validation()
    elif args.profile == "integrity":
        validate_integrity()
    elif args.profile == "manifest":
        write_manifest()
    elif args.profile == "paper":
        build_paper()
    else:
        run_tests()
        run_certificate_verifier()
        run_period_navigation_verifier()
        verify_reproduction()
        validate_data()
        build_paper()
        run_repository_validation()
        validate_integrity()


if __name__ == "__main__":
    main()
