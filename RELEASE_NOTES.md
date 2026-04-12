# DailyTrends 6.0.0 Release Notes

## Overview

Major modernization release. The project has been fully revived with updated dependencies,
a modern build system, bug fixes, and a comprehensive test suite.

## What's New

### Modernized Build System
- **Migrated from `setup.py` to `pyproject.toml`** with `hatchling` build backend
- **Fully `uv`-based development workflow** — no more pip/setuptools/twine manual management
- Added `ruff` for linting with import sorting and code quality checks
- Added `.gitignore` and `.python-version` for clean development setup

### Updated Dependencies
- `pandas` — from `>=0.24.2` to `>=2.0`
- `numpy` — from `>=1.16.4` to `>=1.24`
- `requests` — from `>=2.22.0` to `>=2.31`
- `tqdm` — from `>=4.35.0` to `>=4.66`
- `python-dateutil>=2.8` — **added as explicit dependency** (was used but never declared)
- Dropped old dev deps (`twine==1.14.0`, `pip==21.1`, `wheel==0.33.6`)

### Python Version Support
- Dropped Python 3.5 - 3.9 (end-of-life)
- Now targets **Python 3.10, 3.11, 3.12, 3.13**

### Bug Fixes
- **Fixed crash when Google Trends API doesn't return expected widget** (`request.py`) —
  `params_1` was set to `None` and used without checking, causing a `TypeError`.
  Now raises a clear `ValueError` with a descriptive message.
- **Fixed silent error swallowing in rescaler** (`rescale.py`) — bare `except` clause
  silently dropped data frames during aggregation. Now catches only `ValueError` and
  logs a warning instead of silently discarding data.
- **Fixed unreliable ratio calculation** (`rescale.py`) — changed from `value_counts().idxmax()`
  (mode) to `median()`, which is more robust for continuous ratio data.
- **Fixed deprecated pandas frequency string** — changed `"d"` to `"D"` to avoid
  `Pandas4Warning` deprecation warnings.
- **Fixed type checking** (`collect.py`) — replaced `type(q) != str` with `isinstance()`
  for proper subclass support.
- **Added validation** — `collect_data()` now validates that `dest` is provided
  when `save=True`, and validates all list items are strings.
- **Updated User-Agent** to a modern Chrome version to reduce API rejection risk.

### License Clarification
- LICENSE file says Apache 2.0; updated `pyproject.toml` classifiers to match
  (was incorrectly listed as GPL v3 in old `setup.py`).

### Testing
- Added **37 pytest tests** covering:
  - Interval generation logic (10 tests)
  - Rescaling/aggregation math (12 tests)
  - Input validation (7 tests)
  - API request mocking (4 tests)
  - Package imports and version (4 tests)
- Ported the old `test_rescaler.py` script into a proper parametric test with assertions

### Code Quality
- All code passes `ruff` linting with zero warnings
- Proper type hints using modern Python syntax (`str | list[str]` instead of `Union`)
- Added docstrings to all public functions
- Proper `__init__.py` with `__version__` and `__all__` exports

## Breaking Changes

- **Minimum Python version is now 3.10** (was 3.5)
- `collect_data()` now always returns a `DataFrame` (previously returned `None` when `save=True`)
- Bare `except` in `qAggr` replaced with specific `ValueError` handling — previously
  silently swallowed all errors, now only handles expected ratio calculation failures

## How to Upgrade

```bash
pip install --upgrade DailyTrends
```

Or with uv:

```bash
uv add DailyTrends --upgrade
```
