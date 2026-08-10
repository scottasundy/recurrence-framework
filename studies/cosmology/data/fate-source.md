# Fate-weight probability layer provenance

the Cosmological Recurrence Study uses the current cited DES-Dovekie comparison input, and leaves the fully theory-agnostic recurrence bound unchanged.

## Baseline Bayesian model comparison

Source: D. D. Y. Ong, D. Yallup, and W. Handley (2026), *The Bayesian view of DESI DR2 with unimpeded: Evidence and tension in a combined analysis with CMB and supernovae across cosmological models*, arXiv:2603.05472.

For DESI DR2 BAO + Planck CMB, the paper reports `ln B = -0.57 +/- 0.26` for `w0waCDM` relative to `LambdaCDM`. CRPS defines `B = Z_dynamic / Z_LambdaCDM`. With equal prior odds,

`P(dynamic | D, two-model set) = exp(ln B) / [1 + exp(ln B)]`.

This gives approximately 0.3612 dynamical-dark-energy weight and 0.6388 LambdaCDM weight. The +/- values in the output propagate only the reported numerical evidence uncertainty; they are not a complete systematic uncertainty.

## Comparison combinations

The current arXiv version reports `ln B = -0.01 +/- 0.27` after the corrected DES-Dovekie recalibration and `ln B = +3.32 +/- 0.27` for the original DES-SN5YR calibration. CRPS includes both only to demonstrate data/calibration sensitivity. The original DES-SN5YR combination is not used as the baseline.

These Bayes factors come from the Ong, Yallup & Handley Bayesian reanalysis and are conditional on its declared likelihoods, priors, and model set. DESI DR2 Results IV adds Lyman-alpha Alcock-Paczynski/full-shape information and reports frequentist significances; those values answer a different statistical question and are not substituted into this table.

## Ultimate-fate decomposition

The Bayesian evidence distinguishes only the selected cosmological model families. It does not determine whether a Lambda-like future is vacuum-stable or metastable, nor does a `w0-wa` phenomenological fit determine the remote future. CRPS therefore applies three explicit within-family sensitivity maps. These splits are assumptions recorded in `config.json`; they are not inferred from DESI.

The neutral `maximum_entropy_split` assigns equal weight to unresolved sub-branches within each top-level family. Its resulting six fate weights are useful for visualization but have no claim to being objective cosmological probabilities.

## Current DESI context

DESI DR2 Results IV (arXiv:2607.27410v3) reports a 2.7-sigma frequentist preference for time-evolving `w0-wa` dark energy over LambdaCDM for DESI+CMB. CRPS records this as context only. A frequentist significance is not converted into a model probability.
