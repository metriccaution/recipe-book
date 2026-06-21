from pathlib import Path
from typing import Union

import pytest

from housekeeping.commands.export_json_ld import recipe_to_json_ld
from housekeeping.models.json_ld.recipe import HowToSection, HowToStep
from housekeeping.models.json_ld.recipe import Recipe as JsonLdRecipe
from housekeeping.models.repository import RecipeRepository


def _load_converted() -> list[JsonLdRecipe]:
    repo = RecipeRepository.from_directory(Path("recipes"))
    return [recipe_to_json_ld(recipe) for recipe in repo.recipes]


_converted = _load_converted()


def _all_steps(
    instructions: list[Union[HowToStep, HowToSection]],
) -> list[HowToStep]:
    steps = []
    for item in instructions:
        if isinstance(item, HowToStep):
            steps.append(item)
            if item.itemListElement:
                steps.extend(item.itemListElement)
        elif isinstance(item, HowToSection):
            steps.extend(item.itemListElement)
    return steps


@pytest.mark.parametrize("recipe", _converted, ids=lambda r: r.name)
def test_name_non_empty(recipe: JsonLdRecipe):
    assert recipe.name.strip()


@pytest.mark.parametrize("recipe", _converted, ids=lambda r: r.name)
def test_has_ingredients(recipe: JsonLdRecipe):
    "schema.org marks recipeIngredient as recommended; an empty list is meaningless."
    assert len(recipe.recipeIngredient) > 0


@pytest.mark.parametrize("recipe", _converted, ids=lambda r: r.name)
def test_ingredient_text_non_empty(recipe: JsonLdRecipe):
    for ingredient in recipe.recipeIngredient:
        assert ingredient.strip()


@pytest.mark.parametrize("recipe", _converted, ids=lambda r: r.name)
def test_has_instructions(recipe: JsonLdRecipe):
    "schema.org marks recipeInstructions as recommended; an empty list is meaningless."
    assert len(recipe.recipeInstructions) > 0


@pytest.mark.parametrize("recipe", _converted, ids=lambda r: r.name)
def test_step_text_non_empty(recipe: JsonLdRecipe):
    for step in _all_steps(recipe.recipeInstructions):
        assert step.text.strip()


@pytest.mark.parametrize("recipe", _converted, ids=lambda r: r.name)
def test_sections_non_empty(recipe: JsonLdRecipe):
    "HowToSection with no steps is invalid — consumers skip or error on it."
    for item in recipe.recipeInstructions:
        if isinstance(item, HowToSection):
            assert item.name.strip()
            assert len(item.itemListElement) > 0


@pytest.mark.parametrize("recipe", _converted, ids=lambda r: r.name)
def test_instructions_not_mixed(recipe: JsonLdRecipe):
    "recipeInstructions must be all HowToStep or all HowToSection, not both."
    types = {type(item) for item in recipe.recipeInstructions}
    assert len(types) <= 1
