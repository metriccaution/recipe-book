set -e

# Source code housekeeping
uv run ruff check --select I --fix .
uv run ruff check --fix
uv run ruff format

# Check the code
uv run pytest --ignore=housekeeping/recipes_tests

# Rewrite the data to a validated version of itself
uv run python -m housekeeping normalise

# Check the data
uv run pytest housekeeping/recipes_tests
