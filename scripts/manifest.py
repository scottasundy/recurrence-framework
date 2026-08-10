#!/usr/bin/env python3
"""Build a SHA-256 manifest for the complete combined repository."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manifest.sha256"
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}


def include(path: Path) -> bool:
    if path == OUT or not path.is_file():
        return False
    return not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    files = sorted((p for p in ROOT.rglob("*") if include(p)), key=lambda p: p.as_posix())
    lines = [f"{sha256(p)}  {p.relative_to(ROOT).as_posix()}" for p in files]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {OUT.name} with {len(lines)} entries")


if __name__ == "__main__":
    main()
