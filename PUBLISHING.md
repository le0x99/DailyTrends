# Publishing DailyTrends to PyPI

## Prerequisites

1. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create a PyPI account at https://pypi.org/account/register/

3. Create a PyPI API token at https://pypi.org/manage/account/token/
   - Scope: limit to the `DailyTrends` project (or use account-wide for first publish)

## Steps to Publish

### 1. Ensure tests pass

```bash
uv sync
uv run pytest -v
uv run ruff check .
```

### 2. Build the package

```bash
uv build
```

This creates both a source distribution (`.tar.gz`) and a wheel (`.whl`) in the `dist/` directory.

### 3. Test on TestPyPI first (recommended)

```bash
uv publish --publish-url https://test.pypi.org/simple/ --token YOUR_TEST_PYPI_TOKEN
```

Verify the test release:
```bash
uv pip install --index-url https://test.pypi.org/simple/ DailyTrends==6.0.0
```

### 4. Publish to PyPI

```bash
uv publish --token YOUR_PYPI_TOKEN
```

Or set the token as an environment variable:
```bash
export UV_PUBLISH_TOKEN=pypi-YOUR_TOKEN_HERE
uv publish
```

### 5. Create a GitHub release

After pushing the tag:
```bash
git tag v6.0.0
git push origin v6.0.0
```

Then create a release on GitHub using the contents of `RELEASE_NOTES.md`.

## Version Bumping

For future releases, update the version in two places:
1. `pyproject.toml` — the `version` field under `[project]`
2. `DailyTrends/__init__.py` — the `__version__` variable

Then repeat the build and publish steps above.
