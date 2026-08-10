#!/usr/bin/env python3
"""Print the integrated reference status without implying a physical recurrence phase."""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPS = ROOT / "studies" / "coordinate" / "clock.py"
CRPS = ROOT / "studies" / "cosmology"


def load_cps_module():
    spec = importlib.util.spec_from_file_location("cps_coordinate_clock", CPS)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load CPS coordinate module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_csv_row(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as f:
        return next(csv.DictReader(f))


def main() -> None:
    cps = load_cps_module()
    macrostate, phi, age = cps.coordinate_from_redshift(0.0)

    baseline = first_csv_row(CRPS / "outputs" / "de-sitter-baseline.csv")
    bound = first_csv_row(CRPS / "outputs" / "probability-bound.csv")
    config = json.loads((CRPS / "config.json").read_text(encoding="utf-8"))

    print("Cosmic Recurrence Framework")
    print(f"Reference cosmic coordinate: {macrostate} / Phi_C={phi:.4f}")
    print(f"Reference cosmic age: {age:.3f} Gyr")
    print("Physical recurrence-loop status: not established by current observations")
    print("Physical recurrence period/phase: not identified")
    print(
        "Conditional stable-de-Sitter thermodynamic exponent: "
        f"log10(t_thermo/yr)={float(baseline['log10_t_thermo_rec_years']):.5e}"
    )
    print(
        "Theory-agnostic marginalized recurrence probability: "
        f"[{bound['lower_bound']},{bound['upper_bound']}]"
    )
    print(
        "Reference status: " + config["cps_reference"]["status"]
    )


if __name__ == "__main__":
    main()
