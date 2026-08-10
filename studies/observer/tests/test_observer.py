from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from observer import helstrom_success_probability, total_variation

spec = importlib.util.spec_from_file_location("observer_run", ROOT / "run.py")
assert spec is not None and spec.loader is not None
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)


def test_total_variation():
    assert total_variation([1, 0], [1, 0]) == 0
    assert total_variation([1, 0], [0, 1]) == 1


def test_quantum_helstrom_rule():
    assert helstrom_success_probability(0.0) == 0.5
    assert helstrom_success_probability(0.1) == 0.55
    assert helstrom_success_probability(1.0) == 1.0


def test_exact_hpp_predictive_doubletons():
    rows = run.build_hpp_ambiguity()
    assert len(rows) == 27
    assert all(r["observer_density_distance"] == 0 for r in rows)
    assert all(r["velocity_bit_hamming"] > 0 for r in rows)
    assert all(r["predictively_indistinguishable_forever"] for r in rows)


def test_irrational_torus_thresholds():
    rows = run.build_torus_thresholds()
    expected = {
        "1e-01": 5,
        "1e-02": 70,
        "1e-03": 408,
        "1e-04": 5741,
        "1e-05": 80782,
        "1e-06": 470832,
    }
    assert {r["observer_tolerance"]: r["first_listed_integer_return_time_q"] for r in rows} == expected
    assert all(r["exact_positive_recurrence"] is False for r in rows)


def test_initially_hidden_perturbations_become_visible():
    rows = run.build_perturbation_summary()
    assert sum(r["trials"] for r in rows) == 150
    assert all(r["all_initial_density_observations_equal"] for r in rows)
    assert all(r["all_became_density_distinguishable_at_step_1"] for r in rows)
