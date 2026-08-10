from __future__ import annotations

import csv
import json
from itertools import combinations
from pathlib import Path

from recurrence_dynamics.finite_orbits import predictive_partition
from recurrence_dynamics.hpp import (
    local_axis_counts,
    momentum,
    observe_site_masks,
    observe_site_momenta,
    step,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hpp"


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


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_velocity_mask_search_certificate_is_complete_and_exact():
    rows = read_csv("mask-search.csv")
    assert len(rows) == 9 + 36 + 84

    by_count = {
        count: [row for row in rows if int(row["sensor_count"]) == count]
        for count in (1, 2, 3)
    }
    assert {row["sites"] for row in by_count[1]} == {
        str(i) for i in range(9)
    }
    assert len({row["sites"] for row in by_count[2]}) == 36
    assert len({row["sites"] for row in by_count[3]}) == 84

    assert max(int(row["predictive_classes"]) for row in by_count[1]) == 1_156
    assert max(int(row["predictive_classes"]) for row in by_count[2]) == 4_945

    successful = [
        row for row in by_count[3] if int(row["reconstructs_all_states"]) == 1
    ]
    assert {row["sites"] for row in successful} == {
        "0;4;8",
        "0;5;7",
        "1;3;8",
        "1;5;6",
        "2;3;7",
        "2;4;6",
    }
    assert {
        row["class_counts"] for row in successful
    } == {"322;3271;9123;9153;9153"}
    assert {
        int(row["refinement_word_length"]) for row in successful
    } == {4}


def test_momentum_search_certificate_is_complete_and_exact():
    rows = read_csv("momentum-search.csv")
    assert len(rows) == 126 + 126

    four = [row for row in rows if int(row["sensor_count"]) == 4]
    five = [row for row in rows if int(row["sensor_count"]) == 5]
    assert len({row["sites"] for row in four}) == 126
    assert len({row["sites"] for row in five}) == 126

    assert max(int(row["predictive_classes"]) for row in four) == 9_081
    assert not any(int(row["reconstructs_all_states"]) for row in four)

    successful = [
        row for row in five if int(row["reconstructs_all_states"]) == 1
    ]
    assert len(successful) == 36
    assert {
        row["class_counts"] for row in successful
    } == {"1181;8391;8766;9021;9143;9149;9153;9153"}
    assert {
        int(row["refinement_word_length"]) for row in successful
    } == {7}


def test_representative_sensor_partitions_reproduce_committed_results():
    states = sector_states()
    evolution = lambda state: step(state, 3, 3)

    mask_result = predictive_partition(
        evolution,
        states,
        lambda state: observe_site_masks(state, (0, 4, 8)),
    )
    assert mask_result.class_counts == (322, 3_271, 9_123, 9_153, 9_153)
    assert mask_result.is_state_reconstructing

    momentum_result = predictive_partition(
        evolution,
        states,
        lambda state: observe_site_momenta(state, (0, 1, 3, 5, 7)),
    )
    assert momentum_result.class_counts == (
        1_181,
        8_391,
        8_766,
        9_021,
        9_143,
        9_149,
        9_153,
        9_153,
    )
    assert momentum_result.is_state_reconstructing

    all_momentum = predictive_partition(
        evolution,
        states,
        lambda state: observe_site_momenta(state, tuple(range(9))),
    )
    assert all_momentum.class_counts == (6_841, 9_153, 9_153)

    axis_result = predictive_partition(evolution, states, local_axis_counts)
    assert axis_result.class_counts == (2_853, 9_153, 9_153)


def test_predictive_cycle_summary_and_extension_summary():
    cycle_rows = read_csv("predictive-cycles.csv")
    assert cycle_rows == [
        {
            "period": "3",
            "microscopic_cycles": "1341",
            "density_predictive_cycles": "1332",
            "cycles_merged": "9",
        },
        {
            "period": "6",
            "microscopic_cycles": "459",
            "density_predictive_cycles": "459",
            "cycles_merged": "0",
        },
        {
            "period": "9",
            "microscopic_cycles": "252",
            "density_predictive_cycles": "252",
            "cycles_merged": "0",
        },
        {
            "period": "12",
            "microscopic_cycles": "9",
            "density_predictive_cycles": "9",
            "cycles_merged": "0",
        },
    ]

    summary = json.loads(
        (DATA / "observability.json").read_text(encoding="utf-8")
    )
    assert summary["sector_states"] == 9_153
    assert summary["density"]["class_counts"] == [495, 6_948, 9_090, 9_126, 9_126]
    assert summary["velocity_mask_sensors"]["minimum_reconstructing_sensor_count"] == 3
    assert summary["momentum_sensors"]["minimum_reconstructing_sensor_count"] == 5
    assert summary["cycles"]["microscopic_cycle_count"] == 2_061
    assert summary["cycles"]["density_predictive_cycle_count"] == 2_052
    assert summary["cycles"]["merged_cycle_count"] == 9
    assert summary["cycles"]["period_compression_observed"] is False
