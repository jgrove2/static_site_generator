# Test Suite

This directory contains unit tests for the static site generator.

## Running Tests

### Using the test runner script

```bash
python3 run_tests.py
```

### Using unittest directly

```bash
python3 -m unittest discover tests
```

### Using pytest (if installed)

```bash
pytest tests/
```

## Test Coverage

The test suite currently covers **34 total tests**:

### Logger Module (`tests/logger/test_logger.py`)

- **17 test cases** covering the `setup_logging` function
- Tests include:
  - Default configuration behavior
  - Custom log levels
  - Console and file handlers
  - Formatter configuration
  - Handler cleanup and management
  - Multiple logger setup calls
  - File creation and writing
  - Error handling

### Config Module (`tests/config/test_default.py`)

- **6 test cases** covering the default configuration constants
- Tests include:
  - Content directory configuration
  - Output directory configuration
  - Template file configuration
  - Logging configuration constants

### Builder Module (`tests/builder/test_html.py`)

- **7 test cases** covering the HTML builder functionality
- Tests include:
  - Module import verification
  - Function existence and callability
  - Return value validation (tuple of successful_conversions, error_count)
  - Content directory not found scenarios
  - No markdown files scenarios
  - Successful markdown to HTML conversion
  - Error handling during file processing

### Parser Module (`tests/parser/test_markdown.py`)

- **2 test cases** covering the markdown parser functionality
- Tests include:
  - Module import verification
  - Function existence and callability

### Templates Module (`tests/templates/test_loader.py`)

- **2 test cases** covering the template loader functionality
- Tests include:
  - Module import verification
  - Function existence and callability

## Test Structure

The test directory mirrors the source code structure:

```
tests/
├── __init__.py
├── logger/
│   ├── __init__.py
│   └── test_logger.py
├── config/
│   ├── __init__.py
│   └── test_default.py
├── builder/
│   ├── __init__.py
│   └── test_html.py
├── parser/
│   ├── __init__.py
│   └── test_markdown.py
├── templates/
│   ├── __init__.py
│   └── test_loader.py
└── README.md
```

- `run_tests.py` - Test runner script
- `requirements-test.txt` - Testing dependencies

## Adding New Tests

1. Create test files in the appropriate module directory (e.g., `tests/logger/` for logger tests)
2. Name test files with the pattern `test_*.py`
3. Inherit from `unittest.TestCase`
4. Use descriptive test method names starting with `test_`
5. Include docstrings explaining what each test does
6. Use `setUp()` and `tearDown()` for test fixtures
7. Import from the corresponding `src` module (e.g., `from src.logger.logger import setup_logging`)

## Test Dependencies

Install testing dependencies with:

```bash
pip install -r requirements-test.txt
```

## Continuous Integration

The tests can be integrated into CI/CD pipelines by running:

```bash
python3 run_tests.py
```

The script returns exit code 0 on success, 1 on failure.
