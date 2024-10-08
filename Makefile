install:
	sage -pip install -e .
	rm -r build
	#rm -r homogeneous.egg-info

test:
	sage -t young

coverage:
	sage --coverage young

docs: docs/Makefile
	cd docs && make html
	cd docs && make latexpdf

docs-clean:
	cd docs && make clean

lint:
	black young
	isort --profile black young
	flake8 --extend-ignore=E741 --max-line-length 88 young
	ruff check --ignore=E741 young

.PHONY: install test coverage docs-clean docs lint
