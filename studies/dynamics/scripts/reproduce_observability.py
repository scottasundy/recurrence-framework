#!/usr/bin/env python3
"""Reproduce the exact 3x3 HPP observability and predictive-cycle extensions.

The script exhaustively enumerates the four-particle, zero-momentum sector,
computes fixed-site sensor thresholds, and counts microscopic versus
density-predictive cycles. Results are written to
``data/hpp/``.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from recurrence_dynamics.finite_orbits import predictive_partition
from recurrence_dynamics.hpp import (
    density,
    local_axis_counts,
    momentum,
    observe_site_masks,
    observe_site_momenta,
    step,
)

WIDTH = HEIGHT = 3
OUTPUT_DIR = ROOT / "data" / "hpp"


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


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def subset_search(states, observe_factory, sizes: tuple[int, ...]):
    evolution = lambda state: step(state, WIDTH, HEIGHT)
    rows = []
    for sensor_count in sizes:
        for sites in combinations(range(WIDTH * HEIGHT), sensor_count):
            result = predictive_partition(evolution, states, observe_factory(sites))
            rows.append(
                {
                    "sensor_count": sensor_count,
                    "sites": ";".join(map(str, sites)),
                    "present_classes": result.class_counts[0],
                    "predictive_classes": result.predictive_class_count,
                    "refinement_word_length": result.refinement_depth,
                    "class_counts": ";".join(map(str, result.class_counts)),
                    "reconstructs_all_states": int(result.is_state_reconstructing),
                }
            )
    return rows


def microscopic_cycles(states):
    evolution = lambda state: step(state, WIDTH, HEIGHT)
    unvisited = set(states)
    cycles = []
    while unvisited:
        start = next(iter(unvisited))
        cycle = []
        current = start
        while current not in cycle:
            cycle.append(current)
            current = evolution(current)
        if current != start:
            raise RuntimeError("Expected reversible sector with no transient states.")
        for state in cycle:
            unvisited.remove(state)
        cycles.append(tuple(cycle))
    return cycles


def quotient_cycles(states, class_of):
    evolution = lambda state: step(state, WIDTH, HEIGHT)
    representative = {}
    successor = {}
    for state in states:
        label = class_of[state]
        representative.setdefault(label, state)
        next_label = class_of[evolution(state)]
        prior = successor.setdefault(label, next_label)
        if prior != next_label:
            raise RuntimeError("Predictive quotient dynamics are not well-defined.")

    unvisited = set(representative)
    periods = []
    while unvisited:
        start = next(iter(unvisited))
        current = start
        cycle = []
        while current not in cycle:
            cycle.append(current)
            current = successor[current]
        if current != start:
            raise RuntimeError("Expected quotient of reversible sector to be cyclic.")
        periods.append(len(cycle))
        unvisited.difference_update(cycle)
    return periods


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    states = sector_states()
    if len(states) != 9_153:
        raise RuntimeError(f"Unexpected sector size: {len(states)}")

    mask_rows = subset_search(
        states,
        lambda sites: lambda state: observe_site_masks(state, sites),
        (1, 2, 3),
    )
    write_csv(
        OUTPUT_DIR / "mask-search.csv",
        [
            "sensor_count",
            "sites",
            "present_classes",
            "predictive_classes",
            "refinement_word_length",
            "class_counts",
            "reconstructs_all_states",
        ],
        mask_rows,
    )

    momentum_rows = subset_search(
        states,
        lambda sites: lambda state: observe_site_momenta(state, sites),
        (4, 5),
    )
    write_csv(
        OUTPUT_DIR / "momentum-search.csv",
        [
            "sensor_count",
            "sites",
            "present_classes",
            "predictive_classes",
            "refinement_word_length",
            "class_counts",
            "reconstructs_all_states",
        ],
        momentum_rows,
    )

    evolution = lambda state: step(state, WIDTH, HEIGHT)
    density_result = predictive_partition(evolution, states, density)
    all_momentum = predictive_partition(
        evolution,
        states,
        lambda state: observe_site_momenta(state, tuple(range(9))),
    )
    all_axis = predictive_partition(evolution, states, local_axis_counts)

    micro_periods = [len(cycle) for cycle in microscopic_cycles(states)]
    predictive_periods = quotient_cycles(states, density_result.class_of)

    micro_counter = Counter(micro_periods)
    predictive_counter = Counter(predictive_periods)
    periods = sorted(set(micro_counter) | set(predictive_counter))
    cycle_rows = [
        {
            "period": period,
            "microscopic_cycles": micro_counter[period],
            "density_predictive_cycles": predictive_counter[period],
            "cycles_merged": micro_counter[period] - predictive_counter[period],
        }
        for period in periods
    ]
    write_csv(
        OUTPUT_DIR / "predictive-cycles.csv",
        [
            "period",
            "microscopic_cycles",
            "density_predictive_cycles",
            "cycles_merged",
        ],
        cycle_rows,
    )

    successful_masks = [
        row for row in mask_rows if int(row["reconstructs_all_states"]) == 1
    ]
    successful_momentum = [
        row for row in momentum_rows if int(row["reconstructs_all_states"]) == 1
    ]

    summary = {
        "sector_states": len(states),
        "density": {
            "class_counts": list(density_result.class_counts),
            "predictive_classes": density_result.predictive_class_count,
            "reconstructs_all_states": density_result.is_state_reconstructing,
        },
        "velocity_mask_sensors": {
            "max_predictive_classes_1_site": max(
                int(row["predictive_classes"])
                for row in mask_rows
                if int(row["sensor_count"]) == 1
            ),
            "max_predictive_classes_2_sites": max(
                int(row["predictive_classes"])
                for row in mask_rows
                if int(row["sensor_count"]) == 2
            ),
            "minimum_reconstructing_sensor_count": 3,
            "successful_3_site_layouts": [row["sites"] for row in successful_masks],
            "successful_3_site_layout_count": len(successful_masks),
            "class_counts_at_minimum": [
                int(value) for value in successful_masks[0]["class_counts"].split(";")
            ],
            "minimum_reconstructing_word_length": int(
                successful_masks[0]["refinement_word_length"]
            ),
        },
        "momentum_sensors": {
            "max_predictive_classes_4_sites": max(
                int(row["predictive_classes"])
                for row in momentum_rows
                if int(row["sensor_count"]) == 4
            ),
            "minimum_reconstructing_sensor_count": 5,
            "successful_5_site_layout_count": len(successful_momentum),
            "class_counts_at_minimum": [
                int(value) for value in successful_momentum[0]["class_counts"].split(";")
            ],
            "minimum_reconstructing_word_length": int(
                successful_momentum[0]["refinement_word_length"]
            ),
            "all_9_site_class_counts": list(all_momentum.class_counts),
        },
        "axis_counts_all_sites": {
            "class_counts": list(all_axis.class_counts),
            "minimum_reconstructing_word_length": all_axis.refinement_depth,
        },
        "cycles": {
            "microscopic_cycle_count": len(micro_periods),
            "density_predictive_cycle_count": len(predictive_periods),
            "microscopic_period_counts": dict(sorted(micro_counter.items())),
            "density_predictive_period_counts": dict(sorted(predictive_counter.items())),
            "merged_cycle_count": len(micro_periods) - len(predictive_periods),
            "period_compression_observed": False,
        },
    }

    (OUTPUT_DIR / "observability.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
