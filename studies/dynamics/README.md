# Recurrence Dynamics Framework

This repository develops a reproducible framework for recurrence, predictive observability, hidden-state ambiguity, and predictive equivalence in deterministic dynamical systems. Its main question is:

> When does an observation contain enough information to determine the complete future of a system?

A repeated complete state fixes the subsequent future. A repeated density field, image, conserved quantity, or position snapshot may not. The framework separates complete-state recurrence, observational recurrence, finite-horizon agreement, predictive equivalence, permanent ambiguity, and near recurrence under explicitly declared observation maps.

The exact benchmark is an exhaustive analysis of the four-particle, zero-momentum sector of a reversible `3x3` HPP lattice gas under site-density observation. The repository also contains analytical results and reproducible examples for reversible cellular automata, lattice gases, exact hard-particle dynamics, irrational torus flow, Poincare recurrence, and quantum recurrence.

## Framework

The reusable protocol is documented in [`docs/framework.md`](docs/framework.md). It defines:

- the complete state, update map, analyzed sector, observation map, and diagnostic horizon;
- exact and finite-horizon equivalence relations;
- a recurrence and ambiguity classification system;
- finite-state partition refinement and stabilization;
- symmetry and time-reversal diagnostics;
- required reporting outputs and evidence levels;
- scoped extension procedures for AI systems, robotics, sensors, coarse-grained physics, model discrimination, and quantum diagnostics.

The finite HPP classification is the exact worked benchmark for the broader framework. Extensions to continuous, stochastic, sampled, or quantum systems require their own assumptions and do not automatically inherit the finite exhaustive guarantees.

## Principal HPP result

The full four-particle, zero-momentum sector of the `3x3` reversible HPP lattice gas contains 9,153 microscopic states. Exact partition refinement under site-density observation gives:

```text
Present-density classes:       495
Predictive classes:          9,126
Predictive singletons:       9,099
Predictive doubletons:          27
Ambiguous microscopic states:   54
```

The exceptional set has the exact structure

```math
54=18\times3=9\times2\times3.
```

- 18 distinct microscopic cycles have least period 3.
- The cycles form 9 time-reversal pairs.
- Each pair contains 2 different microscopic time orientations.
- Each cycle has 3 aligned phases.
- The 9 pairs therefore produce 27 predictive doubletons containing 54 states.

Density sees where particles are but not which way they are moving. For these special period-three trajectories, the forward and velocity-reversed microscopic movies cast the same density shadow forever.

The analytical theorem explains the mechanism. The exhaustive computation discovers and certifies that these 54 states are the complete exceptional set in the stated sector.

## Exact observability extension

The same exhaustive sector now includes fixed-site sensor searches and predictive-cycle certificates.

- **Velocity masks:** three fixed sites are necessary and sufficient among all fixed-site subsets; exactly six three-site layouts reconstruct all 9,153 states, and four snapshots suffice at the minimum.
- **Local momentum:** five fixed sites are necessary and sufficient; exactly 36 five-site layouts succeed, and seven snapshots suffice at the minimum.
- **All-site momentum:** two snapshots reconstruct all states.
- **Axis counts:** one present field plus one future field reconstructs all states.
- **Density:** complete future density still leaves 27 doubletons.
- **Predictive cycles:** 2,061 microscopic cycles become 2,052 density-predictive cycles through nine period-three orbit-pair mergers, with no period compression in this sector.

This establishes an exact space-time observability tradeoff while also proving that some coarse observations remain non-reconstructing even with unlimited future history. The generalized mathematics is in [`docs/predictive-quotient.md`](docs/predictive-quotient.md), and the machine-readable certificates are in [`data/hpp/`](data/hpp/).

## Period constraints and phase navigation

The framework includes exact recurrence-period constraints and phase navigation for
the reversible HPP model. The central decomposition is:

```text
complete state -> periodic/conserved invariants -> interaction fiber -> cycle -> phase
```

The framework includes analytic transport and diagonal-histogram clocks, exact
row/column line momenta, checkerboard sign modes, constant-memory period
finding, and atlas-free reversible phase localization once a period is known.

New exact benchmarks include:

- the full 3x3 four-particle zero-momentum sector: 9,153 states, 2,061 cycles,
  periods 3, 6, 9, and 12; six collision counts determine the period class;
- the full 4x4 four-particle zero-momentum sector: 94,336 states, 19,448 cycles,
  periods 2, 4, 6, 8, 12, 20, and 28; four density frames determine period
  class for every state;
- the existing 5x5 seed-B orbit (`seed=75202`): period 9,705, geometric factor
  5, and a 2,209-state invariant interaction fiber whose `F^5` cycle lengths
  are `1941, 46, 45, 44, 28, 18, 14, 14, 10, 9, 8, 8, 7, 5, 5, 4, 3`.

For the 5x5 reference state, exact invariants reduce the complete
14-particle zero-momentum sector from 2,240,809,149,480,000 states to 2,209
compatible interaction states.

See [`docs/periods.md`](docs/periods.md)
for proofs, evidence levels, empirical results, and nonclaims.

## Repository contents

- [`src/recurrence_dynamics/`](src/recurrence_dynamics/) - exact model implementations and finite-state orbit utilities.
- [`tests/`](tests/) - unit, reversibility, exhaustive HPP, catalog, and integrity tests.
- [`scripts/validate.py`](scripts/validate.py) - deterministic generation and repository validation entry point.
- [`scripts/verify_ambiguity.py`](scripts/verify_ambiguity.py) - independent self-contained HPP ambiguity verifier.
- [`scripts/reproduce_observability.py`](scripts/reproduce_observability.py) - exhaustive fixed-site sensor and predictive-cycle reproduction.
- [`data/hpp/ambiguity.csv`](data/hpp/ambiguity.csv) - machine-checkable 54-state certificate.
- [`data/hpp/ambiguity.png`](data/hpp/ambiguity.png) - aligned paired-cycle figure.
- [`paper/paper.tex`](paper/paper.tex) - manuscript source.
- [`paper/paper.pdf`](paper/paper.pdf) - compiled manuscript.
- [`docs/math.md`](docs/math.md) - definitions and theorem summary.
- [`docs/predictive-quotient.md`](docs/predictive-quotient.md) - general protocol-family predictive quotient and operational distinguishability.
- [`docs/framework.md`](docs/framework.md) - reusable diagnostic protocol, classifications, outputs, and extension rules.
- [`docs/reproduce.md`](docs/reproduce.md) - detailed reproducibility procedure.
- [`docs/periods.md`](docs/periods.md) - period constraints, interaction fibers, and phase navigation.
- [`data/periods/`](data/periods/) - exact certificates, exhaustive summaries, and the fixed 500-state empirical period sample.
- [`scripts/verify_periods.py`](scripts/verify_periods.py) - verifier for the principal exact results.
- [`manifest.sha256`](manifest.sha256) - integrity manifest for committed files.
- [`LICENSE.md`](LICENSE.md) - split-license scope and attribution terms.
- [`LICENSES/`](LICENSES/) - complete Apache-2.0 and CC-BY-4.0 license texts.

## Supported environment

The repository is tested with CPython 3.13. The package metadata requires `>=3.13,<3.14`.

Validated Python dependencies:

- matplotlib 3.10.8
- Pillow 12.2.0
- pytest 9.0.2 for testing
- setuptools 80.9.0 for the editable build

The paper build was tested with pdfTeX 1.40.26 from TeX Live 2025.

## Installation

From the repository root:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e . --no-deps
```

On Windows, activate with `.venv\Scripts\activate`.

## Run the tests

```bash
python -m pytest
```

Expected result: all tests pass with no failures or skipped scientific checks.

## Verify the ambiguity certificate independently

```bash
python scripts/verify_ambiguity.py
```

Expected successful output:

```text
Sector states: 9153
Predictive singletons: 9099
Predictive doubletons: 27
Ambiguous states: 54
Period-3 cycles: 18
Time-reversal pairs: 9
Validation: PASS
```

The verifier does not import the project package or the high-level classification code. It independently defines the local HPP collision, streaming, inverse, time reversal, sector enumeration, and predictive partition refinement, then checks the committed CSV certificate.

## Regenerate data and figures

Regenerate every deterministic CSV and PNG under `data/`, then refresh the manuscript figures:

```bash
python scripts/validate.py reproduce
```

Successful completion prints:

```text
Data and figures regenerated from source code.
```

This command regenerates the exact HPP ambiguity catalog and paired-cycle figure as well as the other numerical studies.

## Validate exact claims

```bash
python scripts/validate.py data
```

Expected final lines:

```text
Exact predictive-state results validated.
Data validation passed.
```

## Check clean regeneration

Regenerate deterministic outputs in a temporary directory and compare them with the committed files:

```bash
python scripts/validate.py reproduction
```

Expected output:

```text
Independent reproduction matched all committed tables and figures.
```

CSV files are compared byte-for-byte. PNG files are stripped of textual metadata and compared by pixel content with a strict tolerance.

## Rebuild the manuscript

With `pdflatex` available:

```bash
python scripts/validate.py paper
```

The command compiles [`paper/paper.tex`](paper/paper.tex) twice and writes [`paper/paper.pdf`](paper/paper.pdf). Build-time metadata is suppressed and temporary TeX files are removed.

## Validate repository hygiene

```bash
python scripts/validate.py repository
```

This checks relative links, figure paths, line endings, temporary files, nested archives, local paths, PNG text fields, and PDF metadata.

## Check file integrity

```bash
python scripts/validate.py integrity
```

To rewrite the manifest after an intentional, validated change:

```bash
python scripts/validate.py manifest
```

Do not update the manifest merely to conceal an unexplained difference.

## Complete local verification

```bash
python scripts/validate.py all
```

This runs the test suite, independent certificate verifier, clean regeneration comparison, exact-data checks, manuscript build, repository hygiene validation, and integrity validation.

## Continuous integration

Routine pushes and pull requests run the test suite, independent certificate verifier, exact-data validation, repository hygiene checks, and manifest verification through [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

The clean regeneration comparison is intentionally excluded from routine CI because it reruns every deterministic experiment and can be computationally expensive. [`.github/workflows/reproduce.yml`](.github/workflows/reproduce.yml) runs that check only when manually dispatched or when a GitHub release is published, with a 90-minute job timeout.

## Certificate format

[`ambiguity.csv`](data/hpp/ambiguity.csv) contains one row for each exceptional microscopic state. Each row records:

- pair, cycle, and aligned phase identifiers;
- fixed-width state and velocity-reversed encodings;
- site-density encoding;
- successor and predecessor encodings;
- velocity-reversal partner phase;
- observation-word reversal shift;
- least period;
- active collision count.

The verifier rejects missing rows, duplicate assignments, invalid successors or predecessors, wrong periods, collision sites, incomplete reversal pairs, and any mismatch between the catalog and the independently recomputed predictive doubletons.

## Reproducibility model

Authoritative source files are the Python model implementations, validation scripts, tests, LaTeX source, and fixed experiment parameters. Generated scientific data are committed under `data/`. Generated manuscript figures are copied into `paper/figures/`. The PDF is a compiled output.

The exhaustive HPP claim is computer-assisted but finite and exact: every state in the stated sector is enumerated, no sampling is used, and the independent verifier reconstructs the classification from lower-level definitions.

## Scope and limitations

- The exhaustive HPP classification applies only to the `3x3`, four-particle, zero-momentum sector and the site-density observation map.
- Observational indistinguishability under density is not physical identity and does not imply indistinguishability under richer measurements.
- The lattice models are mathematical test systems, not proposed microscopic laws of nature.
- Finite-time Hamming damage is not a Lyapunov exponent.
- A capped cycle search is censored, not evidence of nonrecurrence.
- Poincare neighborhood recurrence and quantum near recurrence are distinct from exact finite-state recurrence.

## Citation

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). No DOI is hard-coded in the repository.

## License

This repository uses a split license:

- software is licensed under the [Apache License 2.0](LICENSES/Apache-2.0.txt);
- the manuscript, documentation, figures, and generated data are licensed under [Creative Commons Attribution 4.0 International](LICENSES/CC-BY-4.0.txt).

See [`LICENSE.md`](LICENSE.md) for the exact scope, attribution requirements, and treatment of mixed files.
