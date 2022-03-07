test:
	python -m pytest -n auto

coverage:
	python -m pytest -n auto --cov htbcli/ --cov-report term-missing

pdb:
	python -m pytest -n auto --pdb

build:
	python -m build
