# Variables
PYTHON = python3
PIP = pip
MAIN = a_maze_ing.py
CONFIG = config/default_config.txt


.PHONY: help install run debug clean lint lint-strict test

help:
	@echo "A-Maze-ing Project Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install     - Install project dependencies"
	@echo "  run          - Execute the main script"
	@echo "  debug        - Run in debug mode with pdb"
	@echo "  clean        - Remove temporary files and caches"
	@echo "  lint         - Run flake8 and mypy checks"
	@echo "  lint-strict  - Run strict mypy checks"
	@echo "  test         - Run pytest tests"

install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed successfully!"

run:
	@echo "Running main script..."
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	@echo "Running in debug mode..."
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@echo "$()Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/
	@echo "Cleanup complete!"

lint:
	@echo "Running flake8..."
	flake8 .
	@echo "Running mypy..."
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "Linting complete!"

lint-strict:
	@echo "Running flake8..."
	flake8 .
	@echo "Running mypy (strict)..."
	mypy . --strict
	@echo "Strict linting complete!"

test:
	@echo "Running tests..."
	pytest tests/ -v
	@echo "Tests complete!"