.PHONY: install test certificate reproduce reproduction data paper repository manifest integrity all clean

install:
	python -m pip install -r requirements.txt -r requirements-dev.txt
	python -m pip install -e . --no-deps

test:
	python -m pytest

certificate:
	python scripts/verify_ambiguity.py

reproduce:
	python scripts/validate.py reproduce

reproduction:
	python scripts/validate.py reproduction

data:
	python scripts/validate.py data

paper:
	python scripts/validate.py paper

repository:
	python scripts/validate_repo.py

manifest:
	python scripts/validate.py manifest

integrity:
	python scripts/validate.py integrity

all:
	python scripts/validate.py all

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find src -maxdepth 1 -type d -name '*.egg-info' -prune -exec rm -rf {} +
	rm -f paper/*.aux paper/*.bbl paper/*.blg paper/*.fdb_latexmk paper/*.fls paper/*.log paper/*.out paper/*.toc
