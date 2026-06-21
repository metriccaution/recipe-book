set -e

# Source code housekeeping
uv run ruff check --select I --fix .
uv run ruff check --fix
uv run ruff format

# Rewrite the data to a validated version of itself
uv run python -m housekeeping normalise

# Check the code, check the data
uv run pytest
