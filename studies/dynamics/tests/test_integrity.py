from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.sha256"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_files() -> set[str]:
    excluded_suffixes = {".aux", ".log", ".out", ".toc"}
    files: set[str] = set()
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == MANIFEST.name:
            continue
        if any(part in {".git", ".pytest_cache", "__pycache__", ".venv", "venv"} for part in path.parts):
            continue
        if any(part.endswith(".egg-info") for part in path.parts):
            continue
        if path.suffix in excluded_suffixes:
            continue
        files.add(path.relative_to(ROOT).as_posix())
    return files


def test_integrity_manifest_is_complete_and_current():
    listed: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        expected, relative = line.split("  ", 1)
        assert relative not in listed
        listed[relative] = expected

    assert set(listed) == repository_files()
    for relative, expected in listed.items():
        assert sha256(ROOT / relative) == expected
