# DESI DR2 posterior provenance

the Cosmological Recurrence Study uses the official DESI DR2 Results II flat-LambdaCDM posterior for the combination of all DESI DR2 BAO measurements and the default CMB likelihood set. The bundled file `desi-projection.csv.gz` is a lossless column projection of the four public Cobaya chains to the fields needed by this study: `weight`, `H0`, `omega_m`, and `source_chain`.

The source directory is documented by DESI at:

`https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html`

The exact dataset directory is:

`cobaya/base/desi-bao-all_planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_planck-NPIPE-highl-CamSpec-TTTEEE_planck-act-dr6-lensing/`

The four source files were verified against the DESI-published checksum catalog before projection:

| File | SHA-256 |
|---|---|
| `chain.1.txt` | `00f3766f7a7b6370d21323886cd72869087b2b1346a04d729c8f3bc9e65ef698` |
| `chain.2.txt` | `33b154eebdf4e9dca3b8f02ed2680120879d35c10b32fef42261a490104e1dc1` |
| `chain.3.txt` | `d4717e7e5a13de851c86f24c87213faccef2b5f8747900274ab509d9dfa40aa2` |
| `chain.4.txt` | `c827cd767a4864ca28aa15c902bda32004e803050d4be330e25aefddd78b5c36` |

Projection summary: 59,891 rows; summed Cobaya weight 169,444.

`python scripts/fetch_desi.py` re-downloads the four files, verifies these hashes, and rebuilds the bundled projection.

DESI data are distributed under CC BY 4.0. This package changes the original chain files only by selecting the columns required by CRPS and renaming `omegam` to `omega_m`. Users should cite DESI DR2 Results II and follow the current DESI data-license and acknowledgment requirements at `https://data.desi.lbl.gov/doc/acknowledgments/`.
