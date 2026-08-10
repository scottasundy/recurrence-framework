# Contributing

Contributions should preserve the distinction between analytical statements, exhaustive computer-assisted claims, and illustrative numerical experiments.

## Required checks

For ordinary source changes, run from the repository root:

```bash
python -m pytest
python scripts/verify_ambiguity.py
python scripts/validate.py data
python scripts/validate.py repository
python scripts/validate.py integrity
```

Before a release, or whenever generated scientific outputs change, also run:

```bash
python scripts/validate.py reproduction
python scripts/validate.py paper
python scripts/validate.py manifest
python scripts/validate.py integrity
```

The clean regeneration comparison is deliberately handled by a separate manual/release GitHub Actions workflow because it is computationally expensive. Do not weaken assertions to make a change pass. Any changed exact count must be explained scientifically and independently verified.

## Generated files

Edit authoritative source files rather than hand-editing generated CSV or figure outputs. Regenerate outputs with:

```bash
python scripts/validate.py reproduce
```

Commit regenerated scientific data only when the source change justifies them. Update `manifest.sha256` last, after all checks pass.

## Scientific terminology

Use `complete state`, `observation`, `predictive equivalence`, `least period`, `orbit`, `density word`, and `observationally indistinguishable` precisely. Do not equate equal density with equal microscopic state or physical indistinguishability.

## Privacy and repository hygiene

Do not commit credentials, local paths, virtual environments, caches, editor files, build logs, or document metadata. Do not add author, affiliation, funding, DOI, repository, or publication claims without documented evidence.

## Contribution licensing

By submitting a contribution, you agree that software contributions are provided under Apache-2.0 and contributions to the manuscript, documentation, data, and figures are provided under CC-BY-4.0, according to the scope in [`LICENSE.md`](LICENSE.md). Do not submit material you do not have the right to license on those terms.
