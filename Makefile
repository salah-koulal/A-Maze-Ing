# Variables
PYTHON = python3
PIP = pip
MAIN = a_maze_ing.py
CONFIG = config/default_config.txt


.PHONY: help install run clean lint

help:
	@echo "A-Maze-ing Project Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install     - Install project dependencies"
	@echo "  run          - Execute the main script"
	@echo "  clean        - Remove temporary files and caches"
	@echo "  lint         - Run flake8 and mypy checks"

install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed successfully!"

run:
	@echo "Running main script..."
	PYTHONPATH=src $(PYTHON) $(MAIN) $(CONFIG)

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
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
	@echo "Linting complete!"

