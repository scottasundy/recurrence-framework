"""Restore bundled study assets in-place.

Run from the studies directory:
    python unpack_assets.py
"""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
bundles = [
    ROOT / "cosmology" / "assets.zip",
    ROOT / "dynamics" / "assets.zip",
    ROOT / "observer" / "outputs.zip",
]
for bundle in bundles:
    if bundle.exists():
        with zipfile.ZipFile(bundle) as z:
            z.extractall(bundle.parent)
        print(f"restored {bundle.relative_to(ROOT)}")
