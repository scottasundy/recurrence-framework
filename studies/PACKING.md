# Packed studies layout

This package preserves the study source, scripts, tests, documentation, and configuration as normal files while bundling bulky generated/research assets to keep the package below 100 files.

Bundles:
- `cosmology/assets.zip` restores `data/`, `outputs/`, and `figures/`.
- `dynamics/assets.zip` restores `data/`, `supplemental/`, and `paper/figures/`.
- `observer/outputs.zip` restores `outputs/`.

Run `python unpack_assets.py` from this directory to restore the original asset paths before reproduction or validation workflows that expect those files directly.
