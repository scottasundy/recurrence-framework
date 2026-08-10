#!/usr/bin/env python3
"""Reproduce and verify the master recurrence repository."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(label: str, args: list[str], cwd: Path) -> None:
    print(f"\n=== {label} ===", flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="also run deterministic data reproduction, certificates, and deep dynamics validation",
    )
    parser.add_argument(
        "--paper",
        action="store_true",
        help="also rebuild the dynamics PDF when pdflatex is available",
    )
    args = parser.parse_args()
    py = sys.executable

    run(
        "Observer indistinguishability outputs",
        [py, "run.py"],
        ROOT / "studies" / "observer",
    )
    run(
        "Cosmology outputs and figures",
        [py, "run.py"],
        ROOT / "studies" / "cosmology",
    )
    run(
        "Cosmic coordinate reference",
        [py, "clock.py"],
        ROOT / "studies" / "coordinate",
    )

    if args.full:
        dynamics = ROOT / "studies" / "dynamics"
        run(
            "Exact HPP sensor-observability and predictive-cycle reproduction",
            [py, "scripts/reproduce_observability.py"],
            dynamics,
        )
        for label, profile in [
            ("Independent HPP ambiguity certificate", "certificate"),
            ("Exact period-navigation verification", "period"),
            ("Deterministic dynamics reproduction", "reproduction"),
            ("Dynamics data validation", "data"),
            ("Dynamics repository validation", "repository"),
            ("Dynamics integrity validation", "integrity"),
        ]:
            run(label, [py, "scripts/validate.py", profile], dynamics)

    if args.paper:
        run(
            "Dynamics paper build",
            [py, "scripts/validate.py", "paper"],
            ROOT / "studies" / "dynamics",
        )

    run("All automated verification", [py, "scripts/verify.py"], ROOT)
    print("\nMASTER RECURRENCE REPRODUCTION COMPLETE")


if __name__ == "__main__":
    main()
