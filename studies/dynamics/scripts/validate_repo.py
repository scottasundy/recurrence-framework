#!/usr/bin/env python3
"""Validate repository links, privacy, metadata, and release hygiene."""

from __future__ import annotations

import re
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".tex",
    ".csv",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
    ".cff",
    ".json",
    ".gitignore",
    ".gitattributes",
}
EXCLUDED_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "*.egg-info"}


def repository_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", ".venv", "venv", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        if any(part.endswith(".egg-info") for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def validate_text_hygiene(files: list[Path]) -> None:
    forbidden = [
        "Chat" + "GPT",
        "Open" + "AI",
        "generated" + "-by",
        "generated" + " by",
        "hidden" + " prompt",
        "language" + " model",
        "/mnt/" + "data/",
        "/home/" + "oai/",
        "C:\\" + "Users\\",
    ]
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".gitignore", ".gitattributes"}:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if not relative.parts or relative.parts[0] != "LICENSES":
            for token in forbidden:
                assert token.lower() not in text.lower(), f"forbidden text {token!r} in {relative}"
        assert "\r" not in text, f"non-Unix line ending in {relative}"


def validate_markdown_links(files: list[Path]) -> None:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            resolved = (path.parent / target).resolve()
            assert ROOT.resolve() in (resolved, *resolved.parents), f"link escapes repository: {path} -> {target}"
            assert resolved.exists(), f"broken link: {path.relative_to(ROOT)} -> {target}"


def validate_tex_figures(files: list[Path]) -> None:
    pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
    for path in files:
        if path.suffix.lower() != ".tex":
            continue
        text = path.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            resolved = path.parent / target
            if resolved.suffix:
                assert resolved.is_file(), f"missing TeX figure: {target}"
            else:
                assert any((resolved.with_suffix(ext)).is_file() for ext in (".png", ".pdf", ".jpg", ".jpeg")), (
                    f"missing TeX figure: {target}"
                )


def validate_png_metadata(files: list[Path]) -> None:
    from PIL import Image

    for path in files:
        if path.suffix.lower() != ".png":
            continue
        with Image.open(path) as image:
            assert not image.info, f"PNG textual metadata present: {path.relative_to(ROOT)}"


def validate_pdf_metadata(files: list[Path]) -> None:
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        return
    for path in files:
        if path.suffix.lower() != ".pdf":
            continue
        completed = subprocess.run(
            [pdfinfo, str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        metadata = {}
        for line in completed.stdout.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
        for key in ("Author", "Creator", "Producer", "CreationDate", "ModDate", "Subject", "Keywords"):
            assert not metadata.get(key, ""), f"PDF metadata {key} present in {path.relative_to(ROOT)}"


def validate_release_hygiene(files: list[Path]) -> None:
    forbidden_names = {".DS_Store", "Thumbs.db"}
    forbidden_suffixes = {".pyc", ".pyo", ".swp", ".swo", ".bak", ".tmp", ".zip"}
    for path in files:
        relative = path.relative_to(ROOT)
        assert path.name not in forbidden_names, f"operating-system file present: {relative}"
        assert path.suffix.lower() not in forbidden_suffixes, f"temporary or nested archive present: {relative}"
        assert not path.is_symlink(), f"symbolic link present: {relative}"
    required = [
        "README.md",
        "LICENSE.md",
        "LICENSES/Apache-2.0.txt",
        "LICENSES/CC-BY-4.0.txt",
        "CITATION.cff",
        "docs/framework.md",
        "CONTRIBUTING.md",
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        ".gitignore",
        ".gitattributes",
        ".github/workflows/tests.yml",
        ".github/workflows/reproduce.yml",
        "scripts/verify_ambiguity.py",
        "scripts/verify_periods.py",
        "scripts/generate_periods.py",
        "docs/periods.md",
        "data/periods/5x5-summary.csv",
        "data/hpp/ambiguity.csv",
        "paper/paper.tex",
        "paper/paper.pdf",
    ]
    for relative in required:
        assert (ROOT / relative).is_file(), f"required repository file missing: {relative}"


def main() -> int:
    try:
        files = repository_files()
        validate_text_hygiene(files)
        validate_markdown_links(files)
        validate_tex_figures(files)
        validate_png_metadata(files)
        validate_pdf_metadata(files)
        validate_release_hygiene(files)
    except (AssertionError, OSError, UnicodeDecodeError, subprocess.CalledProcessError) as exc:
        print(f"Repository validation: FAIL - {exc}", file=sys.stderr)
        return 1
    print("Repository validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
