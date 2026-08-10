#!/usr/bin/env python3
"""Run all bundled scientific unit tests and umbrella integration checks."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, args: list[str], cwd: Path) -> None:
    print(f"\n=== {label} ===", flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def main() -> None:
    py = sys.executable
    run("Umbrella integration tests", [py, "-m", "pytest", "-q"], ROOT)
    run(
        "Recurrence Dynamics tests",
        [py, "-m", "pytest", "-q"],
        ROOT / "studies" / "dynamics",
    )
    run(
        "Cosmological Recurrence Study tests",
        [py, "-m", "pytest", "-q"],
        ROOT / "studies" / "cosmology",
    )
    run(
        "Observer indistinguishability tests",
        [py, "-m", "pytest", "-q"],
        ROOT / "studies" / "observer",
    )
    run("Cross-module consistency", [py, "scripts/integration.py"], ROOT)
    print("\nALL VERIFICATION CHECKS PASSED")


if __name__ == "__main__":
    main()
