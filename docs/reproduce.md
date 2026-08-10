# Reproducibility

## Environment

The master repository is tested on CPython 3.13.

Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

## Verify all automated tests

```bash
python scripts/verify.py
```

This runs:

1. root cross-study integration tests;
2. Recurrence Dynamics tests;
3. Cosmological Recurrence Study tests;
4. Observer Indistinguishability tests;
5. cross-study consistency checks.

## Reproduce the main numerical outputs

```bash
python run.py
```

This regenerates:

- the observer-indistinguishability outputs;
- the cosmology CSV outputs and figures;
- the coordinate console calculation;
- all automated verification suites.

## Full deterministic regeneration

```bash
python run.py --full
```

The full mode additionally invokes the complete Recurrence Dynamics validation/regeneration path:

```bash
cd studies/dynamics
python scripts/validate.py all
```

That path includes unit tests, the independent HPP ambiguity verifier, deterministic data checks, period-navigation verification, repository integrity checks, and other bundled validations.

## Individual studies

### Dynamics

```bash
cd studies/dynamics
python -m pytest
python scripts/validate.py all
```

### Observer indistinguishability

```bash
cd studies/observer
python run.py
python -m pytest
```

### Cosmology

```bash
cd studies/cosmology
python run.py
python -m pytest
```

The default cosmology run uses the bundled compact projection of the official DESI posterior, so the main regeneration does not require network access.

### Cosmic coordinate

```bash
cd studies/coordinate
python clock.py
```

The reference output begins with:

```text
M3 / Phi_C=0.7376 / t_ref=13.787 Gyr
```

## Integrity

`manifest.sha256` files are regenerated after repository assembly. They provide machine-checkable hashes for the packaged files. Generated Python caches, virtual environments, and test caches are excluded.
