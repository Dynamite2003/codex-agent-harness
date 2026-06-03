PYTHON ?= python3

.PHONY: test lint typecheck check clean-runs

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests

lint:
	$(PYTHON) -m ruff check .

typecheck:
	PYTHONPATH=src $(PYTHON) -m mypy src tests

check: test lint typecheck

clean-runs:
	./harness clean-runs --keep 10
