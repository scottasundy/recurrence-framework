.PHONY: install test verify reproduce full manifest

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest -q

verify:
	python scripts/verify.py

reproduce:
	python run.py

full:
	python run.py --full

manifest:
	python scripts/manifest.py
