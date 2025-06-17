.PHONY: clean test lint format build-wheel clean-wheel

# Development
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete

# Testing
test:
	poetry run pytest tests/ -v --cov=tarsier --cov-report=term-missing --cov-report=xml

test-watch:
	poetry run pytest tests/ -v --cov=tarsier --cov-report=term-missing -f

# Linting and Formatting
lint:
	poetry run black --check tarsier/ tests/
	poetry run isort --check-only tarsier/ tests/
	poetry run mypy tarsier/ tests/

format:
	poetry run black tarsier/ tests/
	poetry run isort tarsier/ tests/

# Wheel building
build-wheel:
	poetry build -f wheel

clean-wheel:
	rm -rf dist/ build/ *.egg-info/

# Development environment setup
setup-dev: format lint test

# Clean and rebuild everything
rebuild: clean clean-wheel build-wheel

# Help
help:
	@echo "Available commands:"
	@echo "  make clean          - Remove all Python cache files and build artifacts"
	@echo "  make test          - Run tests with coverage"
	@echo "  make test-watch    - Run tests in watch mode"
	@echo "  make lint          - Run linters (black, isort, mypy)"
	@echo "  make format        - Format code using black and isort"
	@echo "  make build-wheel   - Build Python wheel package"
	@echo "  make clean-wheel   - Remove wheel build artifacts"
	@echo "  make setup-dev     - Setup development environment"
	@echo "  make rebuild       - Clean and rebuild everything"
	@echo ""
	@echo "Simple Poetry commands (use directly):"
	@echo "  poetry install     - Install dependencies"
	@echo "  poetry add         - Add new dependencies"
	@echo "  poetry remove      - Remove dependencies"
	@echo "  poetry shell       - Activate virtual environment" 