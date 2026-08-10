from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPS_DIR = ROOT / "studies" / "coordinate"
CRPS_DIR = ROOT / "studies" / "cosmology"


def load_cps():
    spec = importlib.util.spec_from_file_location("cps_coordinate_clock", CPS_DIR / "clock.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cps_reference_coordinate_matches_crps_config():
    cps = load_cps()
    cfg = json.loads((CRPS_DIR / "config.json").read_text(encoding="utf-8"))
    ref = cfg["cps_reference"]
    m, phi, age = cps.coordinate_from_redshift(0.0)
    assert m == "M3"
    assert math.isclose(phi, ref["Phi_C_now"], rel_tol=0, abs_tol=5e-11)
    assert math.isclose(cps.H0, ref["H0"], rel_tol=0, abs_tol=1e-12)
    assert math.isclose(cps.OMEGA_M, ref["Omega_m"], rel_tol=0, abs_tol=1e-12)
    assert math.isclose(cps.OMEGA_L, ref["Omega_Lambda"], rel_tol=0, abs_tol=1e-12)
    assert 13.7 < age < 13.9


def test_cosmology_contains_exact_cosmic_coordinate_snapshot():
    assert (CPS_DIR / "spec.md").read_bytes() == (
        CRPS_DIR / "data" / "coordinate.md"
    ).read_bytes()
    assert (CPS_DIR / "timeline.csv").read_bytes() == (
        CRPS_DIR / "data" / "timeline.csv"
    ).read_bytes()


def test_model_agnostic_recurrence_probability_is_unrestricted():
    with (CRPS_DIR / "outputs" / "probability-bound.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        row = next(csv.DictReader(f))
    assert float(row["lower_bound"]) == 0.0
    assert float(row["upper_bound"]) == 1.0


def test_readme_explicitly_separates_cosmic_coordinate_from_recurrence_phase():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "not a recurrence-cycle phase" in readme
    assert "cannot" in readme.lower()


def test_observer_summary_preserves_exact_distinctions():
    summary = json.loads((ROOT / "studies" / "observer" / "outputs" / "summary.json").read_text())
    assert summary["hpp"]["predictive_doubletons"] == 27
    assert summary["hpp"]["microscopic_states_in_permanent_ambiguity"] == 54
    assert summary["hpp"]["observer_density_distance_for_certified_pairs"] == 0
    assert summary["irrational_torus"]["exact_positive_recurrence"] is False
    assert summary["human_observer_threshold"]["status"] == "not numerically identified"
