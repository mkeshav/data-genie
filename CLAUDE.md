# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Data Genie is a Python library for generating synthetic test data in multiple formats: fixed-width, delimited (CSV), and JSON. It also provides a data quality checking DSL through the `dqc` module that operates on pandas DataFrames.

**Python Version**: 3.5+
**Package Name**: data-genie (published to PyPI)
**Documentation**: https://data-genie.readthedocs.io

## Development Environment

### Docker-based Workflow (Recommended)

All development commands should be run through Docker Compose:

```bash
# Build test container
docker-compose build test

# Run all tests (uses tox for multi-version testing)
docker-compose run --rm test

# Run tests inside container (after getting shell)
docker-compose run --rm test bash
python setup.py develop && pytest

# Run single test
docker-compose run --rm test bash -c "python setup.py develop && pytest tests/test_fw.py -k 'test_float'"

# Type checking with mypy
docker-compose run --rm test bash -c "mypy genie_pkg"

# Smoke test (tests installed package)
docker-compose run --rm smoke_test
```

### Local Development

If working outside Docker:

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements_dev.txt

# Install package in development mode
python setup.py develop

# Run tests
pytest

# Run tests for specific Python versions
tox

# Type checking
mypy genie_pkg
```

## Architecture

### Core Modules

The package is organized around three data format generators plus utilities:

1. **fw_genie.py** - Fixed-width file generation
   - Generates fixed-length fields with precise width specifications
   - Supports encoding variations (UTF-8, ASCII)
   - Provides `generate()` and `anonymise_columns()` functions

2. **delimited_genie.py** - CSV/delimited file generation
   - Generates delimiter-separated values (default: comma)
   - Provides `generate()` and `anonymise_columns()` functions
   - Handles special cases like geo coordinates that expand to multiple columns

3. **json_genie.py** - JSON data generation using Jinja2 templates
   - Template-based generation with custom functions injected into Jinja environment
   - All generator functions exposed as template globals (e.g., `random_integer`, `random_email_id`)
   - Use `generate()` with template string or `generate_with_custom_template_function()` for custom templates

4. **generators.py** - Shared random data generators
   - Core random data generation functions used by all format generators
   - Includes: emails, IPs, credit cards, dates, geo coordinates, UUIDs, etc.
   - Uses Markov chain (`markovify`) for text generation from `wonderland.txt`

5. **dqc.py** - Data Quality Checker
   - Pandas DataFrame accessor (use as `df.dqc.run(check_spec)`)
   - Custom DSL parsed with Lark grammar (`data/dqc_grammar.lark`)
   - Supports checks: row_count, is_unique, not_null, is_positive, has_one_of, quantile, is_date, percent_value_length, when_row_identified_by, has_columns
   - Returns list of tuples: `(check_name, column_name, passed: bool)`

6. **australia.py** - Australian address data
   - Provides random OZ addresses using postcode data (`data/oz_postcodes.json`)
   - Methods: `get_random_state()`, `get_random_city_postcode()`, `get_city()`, `get_random_geo_coordinate()`

7. **validators.py** - Data validation utilities
   - Currently provides credit card validation using Luhn algorithm

### Package Data Files

Located in `genie_pkg/data/`:
- `dqc_grammar.lark` - Grammar definition for data quality DSL
- `oz_postcodes.json` - Australian postcode/locality database
- `wonderland.txt` - Source text for Markov chain text generation

These files are included via `package_data` in setup.py and accessed using `pkg_resources.resource_string()`.

## Testing

Tests use pytest with hypothesis for property-based testing. Test files mirror the module structure:
- `test_fw.py` - Fixed-width generation tests
- `test_delimited.py` - CSV/delimited generation tests
- `test_json.py` - JSON generation tests
- `test_dqc.py` - Data quality checker tests
- `test_generators.py` - Core generator function tests
- `test_validators.py` - Validator tests
- `test_australia.py` - Australia module tests

## Release Process

1. Update version in `genie_pkg/__init__.py`
2. Commit with message (use `[skip release]` prefix to skip release)
3. Run `./tag-master` to create git tag
4. Push to master: `git push origin master`
5. CircleCI workflow runs: test → type_check → hold (manual approval) → package_pypi_upload → smoke_test
6. Manually approve the hold step in CircleCI web UI to trigger PyPI upload
7. If documentation updated, manually trigger build on readthedocs

**Pre-push Hook**: Copy `pre-push` script to `.git/hooks/pre-push` after cloning

## CI/CD

CircleCI configuration (`.circleci/config.yml`) defines:
- **test**: Runs tox for multi-version testing
- **type_check**: Runs mypy type checking
- **package_pypi_upload**: Uploads to PyPI (requires manual approval, skipped if commit contains "[skip release]")
- **smoke_test**: Tests installed package from PyPI

Environment variables required in CircleCI:
- `PYPI_API_TOKEN` - PyPI project API token for package publishing
- `CODACY_PROJECT_TOKEN` - For code quality reporting during builds

## Common Patterns

### Column Specifications

All generators use tuple-based column specifications:

**Fixed-width**: `(length, type, *optional_args)`
```python
[(10, 'int'), (15, 'email', 'example.com'), (10, 'date', '%Y/%m/%d', 2)]
```

**Delimited**: `(type, *optional_args)`
```python
[('int', 1, 100), ('email', 20, 'test.com'), ('geo_coord', center, radius)]
```

### Data Types

Common types across generators: `int`, `float`, `str`, `date`, `email`, `one_of`, `special_string`, `geo_coord`, `cc_mastercard`, `cc_visacard`

### Anonymization

Both fw_genie and delimited_genie support anonymizing existing data:
- `anonymise_columns()` takes row bytes and column specs to replace specific columns with generated data

### DQC Usage

```python
import pandas as pd

df = pd.read_csv('data.csv')
check_spec = """
row_count > 100
column_name is_unique
column_name not_null
"""
results = df.dqc.run(check_spec, ignore_column_case=True)
# Returns: [(check_type, column_name, passed)]
```

## Dependencies

**Runtime** (requirements.txt):
- numpy<2
- pandas==2.2.2
- jinja2==3.1.3
- markovify==0.9.0
- lark-parser==0.11.3
- data-science-types==0.2.23

**Development** (requirements_dev.txt):
- pytest, pytest-sugar, pytest-html, pytest-cov
- hypothesis[pandas] - for property-based testing
- jsonschema
- sphinx - for documentation
- pipdeptree
