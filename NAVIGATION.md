# Repository Contents

`README.md` is the canonical master scientific document.

## Core studies

### `studies/dynamics/`

Exact and near recurrence, deterministic reversibility, predictive observability, hidden-state ambiguity, continuous near recurrence, Poincaré/quantum recurrence notes, perturbation studies, exact period constraints, invariant interaction fibers, phase navigation, sensor selection, source code, tests, data, figures, and the exact/near recurrence manuscript.

Principal bundled results include:

- exact 3×3 HPP sector: 9,153 states and 2,061 cycles;
- 27 predictive doubletons / 54 permanently density-ambiguous microscopic states;
- exact 4×4 sector: 94,336 states and 19,448 cycles;
- 5×5 reference period 9,705;
- 2,209-state invariant interaction fiber;
- interaction macroperiod 1,941;
- 500-state empirical period sample and predictor summary;
- exact periodic continuous benchmark and irrational-torus near-return benchmark;
- conserved-sector and fixed-density perturbation datasets;
- hexagonal rotor-gas perturbation datasets.

### `studies/observer/`

Operational observer-indistinguishability calculations built directly from the exact dynamics data.

Outputs include:

- `hpp.csv`
- `perturbations.csv`
- `torus.csv`
- `quantum.csv`
- `summary.json`

This layer explicitly separates complete-state mismatch from observer-accessible mismatch and leaves the human/cosmological observer threshold unidentified until a physical observer model is supplied.

### `studies/coordinate/`

The declared cosmological reference coordinate, timeline, specification, and runnable coordinate calculator.

Reference present:

`M3 / Phi_C=0.7376`

This is a composition coordinate, not a recurrence phase.

### `studies/cosmology/`

Fate-conditioned cosmological recurrence analysis, source code, tests, bundled DESI posterior projection, provenance, generated CSV outputs, figures, and canonical Markdown manuscript.

Principal outputs include:

- conditional de Sitter horizon/entropy calculations;
- DESI posterior propagation;
- restricted model-family Bayesian weights;
- fate-decomposition sensitivity tables;
- prior-conditioned recurrence sensitivity;
- constant-$w$ finite-end scenarios;
- finite-horizon thermodynamic recurrence calculations;
- quantum epsilon-recurrence input requirements;
- model-agnostic recurrence partial-identification bound `[0,1]` (a non-identifiability result, not an estimated probability distribution).

## Repository metadata

- `CITATION.cff` — citation metadata for the standalone master repository.
- `.zenodo.json` — Zenodo-ready deposition metadata.
- `LICENSE.md` and `LICENSES/` — umbrella and bundled licensing information.
- `manifest.sha256` — integrity manifest for the complete repository snapshot.

## Cross-study material

- `docs/findings.md` — evidence-qualified ledger of exact, theorem-level, derived, conditional, conceptual, metaphysical, audit, and auxiliary findings.
- `docs/implementation.md` — code architecture, algorithms, reproduction flow, outputs, and extension points.
- `docs/theory.md` — unified theoretical interpretation, observer consequences, physical-distinction problem, and metaphysical boundary.
- `docs/interpretation.md` — concrete recurrence scenarios translating the benchmark mathematics into physically meaningful distinctions, including detection time and biographical recurrence, with explicit cosmological nonclaims.
- `docs/framework.md` — how the layers connect without overclaiming.
- `docs/results.md` — compact result register.
- `docs/evidence.md` — evidence type and scope for each result.
- `docs/boundaries.md` — explicit nonclaims.
- `docs/reproduce.md` — commands and reproduction paths.
- `SOURCES.md` — source register and provenance.
- `validation.txt` — validation status.
- `manifest.sha256` — master integrity manifest.

## Run

Install:

```bash
python -m pip install -r requirements.txt
```

Verify:

```bash
python scripts/verify.py
```

Reproduce main outputs:

```bash
python run.py
```

Deep deterministic reproduction:

```bash
python run.py --full
```

Optional manuscript PDF rebuild when LaTeX is installed:

```bash
python run.py --paper
```

GitHub Actions workflows are included under `.github/workflows/`.
