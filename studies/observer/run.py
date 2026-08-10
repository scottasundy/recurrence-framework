#!/usr/bin/env python3
"""Reproduce observer-indistinguishability outputs from bundled recurrence data."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DYNAMICS = REPO / "studies" / "dynamics"
sys.path.insert(0, str(ROOT / "src"))

from observer import helstrom_success_probability, mask_hamming, first_below


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build_hpp_ambiguity() -> list[dict]:
    """Build 27 aligned predictive doubletons from the exact 54-state certificate."""
    rows = read_csv(DYNAMICS / "data" / "hpp" / "ambiguity.csv")
    index = {(r["cycle_id"], int(r["phase"])): r for r in rows}
    out = []

    for r in rows:
        if not r["cycle_id"].endswith("-A"):
            continue
        pair_id = int(r["pair_id"])
        partner_cycle = f"P{pair_id:02d}-{r['velocity_reversal_partner_cycle']}"
        partner_phase = int(r["velocity_reversal_partner_phase"])
        partner = index[(partner_cycle, partner_phase)]

        density_equal = r["density_encoding"] == partner["density_encoding"]
        hamming = mask_hamming(r["state_masks"], partner["state_masks"])

        # The certificate records both cycles as least-period-3 and collision free.
        # Equal aligned density words over their complete period imply equality forever.
        certified_forever = (
            density_equal
            and int(r["least_period"]) == 3
            and int(partner["least_period"]) == 3
            and int(r["collision_sites"]) == 0
            and int(partner["collision_sites"]) == 0
        )

        out.append({
            "pair_id": pair_id,
            "phase": int(r["phase"]),
            "state_a": r["state_encoding"],
            "state_b": partner["state_encoding"],
            "velocity_bit_hamming": hamming,
            "density_equal_at_aligned_phase": density_equal,
            "least_period": 3,
            "observer_density_distance": 0 if certified_forever else 1,
            "predictively_indistinguishable_forever": certified_forever,
            "hidden_information_equal_prior_bits": 1,
        })

    if len(out) != 27:
        raise RuntimeError(f"expected 27 predictive doubletons, found {len(out)}")
    if not all(r["predictively_indistinguishable_forever"] for r in out):
        raise RuntimeError("HPP ambiguity certificate failed observer check")
    if not all(r["velocity_bit_hamming"] > 0 for r in out):
        raise RuntimeError("paired HPP states must be microscopically distinct")
    return out


def build_torus_thresholds() -> list[dict]:
    rows = read_csv(DYNAMICS / "data" / "continuous" / "torus-returns.csv")
    epsilons = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    out = []
    for eps in epsilons:
        hit = first_below(rows, "torus_return_error", eps)
        out.append({
            "observer_tolerance": f"{eps:.0e}",
            "first_listed_integer_return_time_q": int(hit["q"]),
            "torus_return_error": float(hit["torus_return_error"]),
            "exact_positive_recurrence": False,
            "interpretation": "near return below declared finite resolution; not exact recurrence",
        })
    return out


def build_quantum_table() -> list[dict]:
    distances = [1.0, 0.1, 0.01, 0.001, 0.000001, 0.0]
    return [{
        "trace_distance": d,
        "optimal_one_shot_identification_probability": helstrom_success_probability(d),
        "excess_over_random_guess": helstrom_success_probability(d) - 0.5,
    } for d in distances]


def build_perturbation_summary() -> list[dict]:
    rows = read_csv(DYNAMICS / "data" / "perturbations" / "trials.csv")
    grouped: dict[int, list[dict]] = {}
    for r in rows:
        grouped.setdefault(int(r["size"]), []).append(r)

    out = []
    for size, group in sorted(grouped.items()):
        first = [int(float(r["first_density_difference"])) for r in group]
        initial_equal = all(r["initial_density_equal"].strip().lower() == "true" for r in group)
        hammings = sorted({int(r["initial_hamming"]) for r in group})
        out.append({
            "lattice_size": size,
            "trials": len(group),
            "all_initial_density_observations_equal": initial_equal,
            "initial_velocity_bit_hamming_values": ";".join(map(str, hammings)),
            "min_first_density_difference_step": min(first),
            "max_first_density_difference_step": max(first),
            "all_became_density_distinguishable_at_step_1": all(x == 1 for x in first),
        })
    return out


def build_outputs(output_dir: Path = ROOT / "outputs") -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    hpp = build_hpp_ambiguity()
    torus = build_torus_thresholds()
    quantum = build_quantum_table()
    perturb = build_perturbation_summary()

    write_csv(
        output_dir / "hpp.csv",
        hpp,
        [
            "pair_id","phase","state_a","state_b","velocity_bit_hamming",
            "density_equal_at_aligned_phase","least_period","observer_density_distance",
            "predictively_indistinguishable_forever","hidden_information_equal_prior_bits",
        ],
    )
    write_csv(
        output_dir / "torus.csv",
        torus,
        [
            "observer_tolerance","first_listed_integer_return_time_q","torus_return_error",
            "exact_positive_recurrence","interpretation",
        ],
    )
    write_csv(
        output_dir / "quantum.csv",
        quantum,
        [
            "trace_distance","optimal_one_shot_identification_probability",
            "excess_over_random_guess",
        ],
    )
    write_csv(
        output_dir / "perturbations.csv",
        perturb,
        [
            "lattice_size","trials","all_initial_density_observations_equal",
            "initial_velocity_bit_hamming_values","min_first_density_difference_step",
            "max_first_density_difference_step","all_became_density_distinguishable_at_step_1",
        ],
    )

    summary = {
        "hpp": {
            "microscopic_states_in_exact_sector": 9153,
            "present_density_classes": 495,
            "predictive_classes": 9126,
            "predictive_doubletons": 27,
            "microscopic_states_in_permanent_ambiguity": 54,
            "observer_density_distance_for_certified_pairs": 0,
            "hidden_information_per_equal_prior_doubleton_bits": 1,
            "meaning": "microscopically distinct states can be perfectly indistinguishable forever under the declared density observation",
        },
        "perturbations": {
            "trials": sum(int(r["trials"]) for r in perturb),
            "initial_density_equal": True,
            "all_density_separated_after_one_update": all(r["all_became_density_distinguishable_at_step_1"] for r in perturb),
            "meaning": "other initially hidden microscopic differences become observable almost immediately",
        },
        "irrational_torus": {
            "exact_positive_recurrence": False,
            "near_recurrence_at_every_listed_finite_tolerance": True,
            "meaning": "a system can be operationally recurrent at finite resolution while lacking an exact recurrence clock",
        },
        "quantum": {
            "metric": "trace distance",
            "equal_prior_optimal_success_rule": "P_correct=(1+D)/2",
            "cosmological_numeric_epsilon_recurrence_time": "not identified",
        },
        "human_observer_threshold": {
            "status": "not numerically identified",
            "reason": "requires a declared physical observer model, accessible measurements, noise, causal region, lifetime, and tolerance",
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    summary = build_outputs()
    print(json.dumps(summary, indent=2))
