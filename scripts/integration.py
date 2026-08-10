#!/usr/bin/env python3
"""Cross-module consistency checks for the combined recurrence framework."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPS_DIR = ROOT / "studies" / "coordinate"
CRPS_DIR = ROOT / "studies" / "cosmology"


def load_cps():
    path = CPS_DIR / "clock.py"
    spec = importlib.util.spec_from_file_location("cps_coordinate_clock", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load CPS coordinate module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    cps = load_cps()
    cfg = json.loads((CRPS_DIR / "config.json").read_text(encoding="utf-8"))
    ref = cfg["cps_reference"]

    check(math.isclose(ref["H0"], cps.H0, rel_tol=0, abs_tol=1e-12), "H0 mismatch")
    check(math.isclose(ref["Omega_m"], cps.OMEGA_M, rel_tol=0, abs_tol=1e-12), "Omega_m mismatch")
    check(math.isclose(ref["Omega_Lambda"], cps.OMEGA_L, rel_tol=0, abs_tol=1e-12), "Omega_Lambda mismatch")

    macrostate, phi, age = cps.coordinate_from_redshift(0.0)
    check(macrostate == "M3", "z=0 must be M3 under Cosmic Coordinate")
    check(math.isclose(phi, ref["Phi_C_now"], rel_tol=0, abs_tol=5e-11), "Phi_C_now mismatch")
    check(13.7 < age < 13.9, "reference age outside expected CPS range")

    canonical_spec = (CPS_DIR / "spec.md").read_bytes()
    frozen_spec = (CRPS_DIR / "data" / "coordinate.md").read_bytes()
    check(canonical_spec == frozen_spec, "CRPS frozen CPS spec differs from canonical Cosmic Coordinate")

    canonical_timeline = (CPS_DIR / "timeline.csv").read_bytes()
    frozen_timeline = (CRPS_DIR / "data" / "timeline.csv").read_bytes()
    check(canonical_timeline == frozen_timeline, "CRPS frozen CPS timeline differs from canonical Cosmic Coordinate")

    bound_path = CRPS_DIR / "outputs" / "probability-bound.csv"
    text = bound_path.read_text(encoding="utf-8")
    check("0.0,1.0" in text or "0,1" in text, "CRPS theory-agnostic bound is not [0,1]")

    print("Integration consistency: PASS")
    print(f"CPS reference: {macrostate} / Phi_C={phi:.10f} / age={age:.6f} Gyr")
    print("CRPS CPS snapshot: exact match")
    print("Model-agnostic recurrence bound: [0,1]")


if __name__ == "__main__":
    main()
