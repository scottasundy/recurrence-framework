# External source verification

Verification date: **2026-08-09**.

The combined package preserves the source/provenance files inside each component study. In addition, the time-sensitive cosmology claims were checked against the following primary/public sources at integration time:

- DESI DR2 publications index: `https://data.desi.lbl.gov/doc/papers/dr2/`
- DESI DR2 BAO cosmology-chain documentation: `https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html`
- DESI DR2 Results II: `https://arxiv.org/abs/2503.14738`
- DESI DR2 Results IV: `https://arxiv.org/abs/2607.27410`
- Ong, Yallup & Handley Bayesian reanalysis, current v2: `https://arxiv.org/abs/2603.05472`

At verification time:

- the DESI data documentation confirmed the DR2 `cobaya` posterior-chain organization and default CMB likelihood combination used by CRPS;
- DESI DR2 Results IV v3 reported a `2.7 sigma` preference for `w0-wa` over LambdaCDM for DESI+CMB after inclusion of the Lyman-alpha AP measurement;
- Ong, Yallup & Handley reported `ln B = -0.57 +/- 0.26` for DESI DR2 BAO + Planck CMB and `ln B = -0.01 +/- 0.27` after the corrected DES-Dovekie calibration; these are the values used by the Cosmological Recurrence Study.

This file records source consistency; it does not convert those external results into probabilities for specific ultimate cosmic fates.
