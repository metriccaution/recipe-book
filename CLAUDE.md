# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All Python tooling uses `uv run`. Run these from the repo root:

```bash
# Format and lint (always run before committing)
uv run ruff check --select I --fix .
uv run ruff check --fix
uv run ruff format

# Type-check
uv run pyright housekeeping/

# Run unit/model tests (excludes data tests)
uv run pytest --ignore=housekeeping/recipes_tests

# Normalise recipe data (validates + rewrites YAML files in-place)
uv run python -m housekeeping normalise

# Run data integrity tests (requires normalised data)
uv run pytest housekeeping/recipes_tests

# Run a single test file
uv run pytest housekeeping/models/time_range_test.py

# Full build (PDF + site)
./build.sh
```

The `test.sh` script runs formatting, unit tests, normalisation, and data tests in sequence. The `build.sh` script additionally exports JSON, compiles the Typst PDF, and builds the Astro static site.

## Architecture

This is a personal recipe book with three layers:

**Data** (`recipes/`) — YAML files organised by type:
- `recipes/<Section>/<Title>.yaml` — recipe files (sections: Main, Sweet, Side, Snack, Baking, Component, Pickle, Drink)
- `ingredients/<MeasureType>/<Name>.yaml` — ingredient metadata (measure types: volume, weight, spice, singles, can)

**Housekeeping** (`housekeeping/`) — Python tooling that manages the data:
- `models/recipes.py` — Pydantic models for the recipe YAML format (`Recipe`, `IngredientGroup`, `StepGroup`, etc.)
- `models/ingredients.py` — `IngredientMetadata` model; ingredients have synonyms and tags; the tag namespace drives which recipe tags are managed vs. manual (see data integrity rules below)
- `models/repository.py` — `RecipeRepository` loads/writes the full `recipes/` directory tree
- `models/json_ld/` — schema.org JSON-LD export models
- `commands/` — CLI subcommands: `normalise`, `export_json`, `export_typst`, `export_json_ld`
- `recipes_tests/` — pytest tests that validate the actual recipe data (not model unit tests)

**Site** (`site/`) — Astro static site that consumes `exported/full/repo.json`.

## Data integrity rules

- Recipe tags are a mix of **manual tags** (e.g. "Family Classics") and **ingredient-derived tags** (e.g. "Onion"). During `normalise`, any tag that appears in the ingredient metadata tag namespace is stripped from recipes and re-derived from the recipe's actual ingredients. Tags outside that namespace are preserved unchanged. Never manually add a tag that exists in any ingredient's `tags` list; run `normalise` instead.
- `normalise` rewrites the entire `recipes/` directory in place (`shutil.rmtree` then recreate). Always run tests before and after editing recipe YAML.
- Every ingredient used in a recipe must have a matching entry in `recipes/ingredients/`. The `test_ingredients_correct` test enforces this.
- Ingredient matching uses name + synonyms + optional units; the `IngredientMetadata.matches_ingredient` method is the authority.
- UUIDs (`identifier` fields) must be globally unique across all recipes and ingredients.

## Key constraints in the models

- `prepTime` / `cookingTime` are ISO 8601 duration strings (e.g. `PT30M`, `PT1H30M`), parsed and normalised by `TimeRange`.
- Ingredient names within a group must be unique; step text within a group must be unique.
- When a recipe has multiple ingredient groups or step groups, all groups must have titles.
- Tags and equipment lists are sorted and deduplicated on save.
