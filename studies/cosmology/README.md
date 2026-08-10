# Cosmological Recurrence Study

This study asks:

> Given the universe we observe today, which physically viable futures permit recurrence, what recurrence scale follows under each set of assumptions, and what probability can be assigned after separating observational uncertainty from unresolved future theory?

## Main result

Current cosmological observations do **not** identify a unique unconditional probability that our universe will recur. If far-future model probabilities and microscopic recurrence assumptions are left unrestricted, the data-only marginalized probability is only partially identified:

$$
P(\mathrm{recurrence}\mid D,\mathrm{unrestricted\ future\ theory})\in[0,1].
$$

Because this interval is the full logical probability range, it should be read as a **non-identifiability result**, not as an informative probability estimate, a uniform distribution, or a 50/50 statement. The substantive result is the explicit decomposition of the observational and theoretical assumptions that would have to be supplied to narrow it.

Inside an assumed eternal, stable, positive-$\Lambda$ future, the conventional finite-patch thermodynamic estimate is calculable. At the declared Cosmic Coordinate reference point, the study obtains approximately:

- asymptotic de Sitter horizon time: **17.2105 Gyr**;
- de Sitter entropy: **$3.18835\times10^{122}\,k_B$**;
- thermodynamic recurrence scale: **$\log_{10}(t_{\rm thermo}/{\rm yr})=1.38468\times10^{122}$**.

This is a conditional thermodynamic scale, **not** a computed quantum $\varepsilon$-recurrence time for the observed universe.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run.py
python -m pytest
```

The default run uses the bundled compact projection of the official DESI posterior and does not require network access.

## Principal outputs

- `paper/paper.md`
- `outputs/de-sitter-posterior.csv`
- `outputs/gaussian-check.csv`
- `outputs/probability-bound.csv`
- `outputs/model-weights.csv`
- `outputs/fate-sensitivity.csv`
- `outputs/prior-sensitivity.csv`
- `outputs/quantum-epsilon.csv`
- `outputs/finite-horizon.csv`
- `outputs/big-rip.csv`
- `outputs/entropy.csv`

## Interpretation rules

1. Never report a near recurrence as exact recurrence.
2. Never call the entropy-exponential de Sitter scale a quantum epsilon-recurrence time unless a metric, epsilon, and applicable microscopic model are supplied.
3. Never interpret a phenomenological dark-energy fit as a guaranteed far-future law without an explicit extrapolation model.
4. Never replace an unidentified theoretical probability with 0.5 merely because it is unknown.
5. Never present fate-decomposition sensitivity assumptions as measured ultimate-fate probabilities.
6. Never interpret restricted model-family Bayesian weights as probabilities over all possible cosmological theories. The published 63.9%/36.1% weights in this study are specifically the equal-prior `LambdaCDM` versus `w0waCDM` comparison for DESI DR2 BAO + Planck CMB from Ong, Yallup & Handley; they are not DESI collaboration fate probabilities.
7. Treat DESI DR2 Results IV's Lyman-alpha AP/full-shape frequentist significance as a distinct result, not as a replacement for the restricted Bayesian weights used here.
8. Always separate observational parameter uncertainty from future-model, vacuum-stability, and recurrence-theory uncertainty.
