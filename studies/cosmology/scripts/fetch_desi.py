#!/usr/bin/env python3
"""Fetch the official DESI DR2 flat-LambdaCDM DESI+CMB chains and rebuild the compact CRPS projection.

The script verifies the four source-chain SHA-256 hashes before producing
``data/desi-projection.csv.gz``.  The main study does not
require network access because that compact projection is bundled.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
from urllib.request import urlretrieve

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = (
    "https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/cobaya/base/"
    "desi-bao-all_planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_"
    "planck-NPIPE-highl-CamSpec-TTTEEE_planck-act-dr6-lensing"
)
EXPECTED = {
    1: "00f3766f7a7b6370d21323886cd72869087b2b1346a04d729c8f3bc9e65ef698",
    2: "33b154eebdf4e9dca3b8f02ed2680120879d35c10b32fef42261a490104e1dc1",
    3: "d4717e7e5a13de851c86f24c87213faccef2b5f8747900274ab509d9dfa40aa2",
    4: "c827cd767a4864ca28aa15c902bda32004e803050d4be330e25aefddd78b5c36",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def project(path: Path, source_chain: int) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as f:
        names = f.readline().strip().lstrip("#").split()
    df = pd.read_csv(
        path,
        sep=r"\s+",
        comment="#",
        header=None,
        names=names,
        usecols=["weight", "H0", "omegam"],
    ).rename(columns={"omegam": "omega_m"})
    df["source_chain"] = source_chain
    return df


def main() -> None:
    rows = []
    with tempfile.TemporaryDirectory(prefix="crps-desi-") as tmp:
        tmp = Path(tmp)
        for i in range(1, 5):
            p = tmp / f"chain.{i}.txt"
            urlretrieve(f"{BASE}/chain.{i}.txt", p)
            digest = sha256(p)
            if digest != EXPECTED[i]:
                raise RuntimeError(f"SHA-256 mismatch for chain.{i}.txt: {digest}")
            rows.append(project(p, i))
    out = pd.concat(rows, ignore_index=True)
    target = ROOT / "data/desi-projection.csv.gz"
    out.to_csv(target, index=False, compression="gzip")
    print(f"Wrote {len(out)} rows, total weight {int(out.weight.sum())}, to {target}")


if __name__ == "__main__":
    main()
