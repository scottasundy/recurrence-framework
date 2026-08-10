# Reproducibility

## Environment

Validated environment:

- CPython 3.13.5
- matplotlib 3.10.8
- Pillow 12.2.0
- pytest 9.0.2
- setuptools 80.9.0
- pdfTeX 1.40.26 / TeX Live 2025

The package metadata requires Python `>=3.13,<3.14`.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e . --no-deps
```

## Test suite

```bash
python -m pytest
```

The tests cover HPP state encoding and decoding, streaming, local collision, global inverse evolution, time-reversal conjugacy, conservation laws, sector enumeration, predictive partition counts, all 54 ambiguous states, the 18 least-period-three cycles, the nine time-reversal pairs, absence of active collisions, catalog uniqueness, figure metadata, and integrity consistency, together with the other models in the study.

## Independent HPP verifier

```bash
python scripts/verify_ambiguity.py
```

The verifier is self-contained and does not import `recurrence_dynamics` or `scripts/validate.py`. It independently implements:

- the local collision rule;
- streaming and inverse streaming;
- the collide-then-stream update and inverse;
- the correct time-reversal involution;
- exact state-sector enumeration;
- stable future-density partition refinement;
- microscopic orbit decomposition;
- CSV certificate validation.

Successful output is:

```text
Sector states: 9153
Predictive singletons: 9099
Predictive doubletons: 27
Ambiguous states: 54
Period-3 cycles: 18
Time-reversal pairs: 9
Validation: PASS
```


## Period-navigation extension

Verify the principal exact claims:

```bash
python scripts/verify_periods.py
```

Regenerate the new certificates and fixed empirical sample:

```bash
python scripts/generate_periods.py
```

The optional regression is supplemental:

```bash
python -m pip install -r requirements-analysis.txt
python scripts/analyze_periods.py
```

## Regenerate committed outputs

```bash
python scripts/validate.py reproduce
```

This reruns every deterministic experiment and rewrites generated CSV and PNG files under `data/`. It also refreshes figures under `paper/figures/`.

The HPP generator recomputes the predictive partition, rewrites the 54-state certificate, and reconstructs the paired-cycle figure from exact states.

## Clean regeneration comparison

```bash
python scripts/validate.py reproduction
```

The command creates a temporary data tree, reruns all generators, and compares the candidate outputs with the committed outputs. CSV comparison is byte-for-byte. PNG textual metadata is removed, and image comparison uses dimensions and pixel differences rather than relying only on binary hashes.

### CI execution policy

Routine pushes and pull requests do not run this profile because it reruns the full experiment suite and may require substantially more time than the fast verification checks. The `Full Reproduction` GitHub Actions workflow runs it on manual dispatch and on published releases, with a 90-minute timeout.

## Exact claim validation

```bash
python scripts/validate.py data
```

This profile rechecks all reported row counts and exact finite-state results. It includes the HPP class-count sequence, singleton and doubleton counts, cycle count, least period, collision-free property, symmetry organization, and reversal pairing.

## Manuscript build

```bash
python scripts/validate.py paper
```

The paper is compiled twice with `pdflatex`. Build timestamps are normalized with `SOURCE_DATE_EPOCH`, `FORCE_SOURCE_DATE`, and `TZ=UTC`. Temporary build files are deleted. PDF metadata fields are suppressed.

## Repository hygiene and metadata

```bash
python scripts/validate_repo.py
```

This checks internal Markdown links, LaTeX figure paths, line endings, prohibited local paths, nested archives, temporary files, PNG text metadata, and PDF authoring metadata.

## Integrity manifest

```bash
python scripts/validate.py manifest
python scripts/validate.py integrity
```

`manifest.sha256` records committed repository files except itself and excluded temporary build products. Integrity validation rejects missing, changed, unlisted, and manifest-only files.

## Complete verification

```bash
python scripts/validate.py all
```

The complete profile runs:

1. the test suite;
2. the independent HPP certificate verifier;
3. clean regeneration comparison;
4. exact-data validation;
5. manuscript build;
6. repository hygiene validation;
7. integrity validation.

## Authoritative and generated artifacts

Authoritative sources:

- model code under `src/`;
- validation and verification scripts under `scripts/`;
- tests under `tests/`;
- fixed experiment parameters;
- manuscript source.

Generated scientific artifacts:

- CSV tables under `data/`;
- PNG figures under `data/`;
- copied manuscript figures under `paper/figures/`;
- compiled manuscript PDF.

The exact HPP classification is exhaustive and computer-assisted. The continuous and ensemble studies are reproducible numerical demonstrations with explicitly stated horizons, seeds, and caps.
