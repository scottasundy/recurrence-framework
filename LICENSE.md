# Licensing

Copyright (c) 2026 Scott A. Sundy.

This combined repository preserves the licenses of its component projects and applies explicit licenses to the new umbrella layer.

## New umbrella software — Apache-2.0

The following root-level material is licensed under Apache License 2.0:

- `scripts/`
- `tests/`
- `.github/workflows/`
- `Makefile`
- root testing/build configuration files

See `LICENSES/Apache-2.0.txt`.

## New umbrella scientific/documentation content — CC-BY-4.0

Unless otherwise stated, new root documentation is licensed under Creative Commons Attribution 4.0 International:

- `README.md`
- `docs/`
- `CHANGELOG.md`
- `RELEASE_NOTES.md`
- `CONTRIBUTING.md`
- `VERSIONS.md`

See `LICENSES/CC-BY-4.0.txt`.

## Bundled component projects

- `studies/dynamics/` retains its original split Apache-2.0 / CC-BY-4.0 licensing as defined by its own `LICENSE.md`.
- `studies/cosmology/` retains its original MIT / CC-BY-4.0 scoped licensing and DESI-derived-data terms as defined by its own `LICENSE`, `LICENSE-CODE`, `LICENSE-CONTENT`, acknowledgments, and provenance files.
- `studies/coordinate/` is bundled as the author's research artifact; the umbrella CC-BY-4.0 license applies to its original non-software content and Apache-2.0 to its coordinate utility for purposes of this combined distribution.

Third-party or derived data remain subject to their own terms. In particular, the DESI-derived posterior projection requires the acknowledgments/provenance terms recorded inside the CRPS module.
