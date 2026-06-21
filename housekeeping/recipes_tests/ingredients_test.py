from pathlib import Path

import pytest

from housekeeping.models.ingredients import IngredientMetadata
from housekeeping.models.recipes import Recipe
from housekeeping.models.repository import RecipeRepository

_repo = RecipeRepository.from_directory(Path("recipes"))

_ingredients = set()
for i in _repo.ingredients:
    _ingredients.add(i.name)
    for synonym in i.synonyms:
        _ingredients.add(synonym)


def test_loads():
    "Check we actually have data."

    assert len(_repo.ingredients) > 0
    assert len(_repo.recipes) > 0


@pytest.mark.parametrize("recipe", _repo.recipes, ids=lambda r: r.title)
def test_ingredients_correct(recipe: Recipe):
    for group in recipe.ingredients:
        for full_ingredient in group.ingredients:
            assert any(
                ingredient.matches_ingredient(full_ingredient)
                for ingredient in _repo.ingredients
            ), f"{full_ingredient!r} in {recipe.title}"


@pytest.mark.parametrize("ingredient", _repo.ingredients, ids=lambda r: r.name)
def test_ingredients_are_used(ingredient: IngredientMetadata):
    "Check each ingredient has a listing"

    for recipe in _repo.recipes:
        for group in recipe.ingredients:
            for full_ingredient in group.ingredients:
                if ingredient.matches_ingredient(full_ingredient):
                    return
    assert False, f"No recipe uses {ingredient.name}"


def test_uuids_unique():
    uuids = {}

    for recipe in _repo.recipes:
        if recipe.identifier not in uuids:
            uuids[recipe.identifier] = []
        uuids[recipe.identifier].append(recipe.title)

    for ingredient in _repo.ingredients:
        if ingredient.identifier not in uuids:
            uuids[ingredient.identifier] = []
        uuids[ingredient.identifier].append(ingredient.name)

    duplicate_ids = [v for v in uuids.values() if len(v) > 1]
    assert len(duplicate_ids) == 0


@pytest.mark.parametrize(
    "search_string,tag,exclusions",
    [
        ("Salad", "Salad", []),
        ("Stew", "Stew", []),
        ("Pie", "Pie", ["Saag Aloo Shepherds Pie", "Mince Pie Tiffin"]),
        ("Tart", "Pie", []),
        ("Biscuit", "Biscuit", []),
        ("Cookie", "Biscuit", []),
        ("Sauce", "Sauce", []),
        ("Bread", "Bread", ["Bread Sauce", "Bread and Butter Pudding", "Gingerbread"]),
    ],
)
def test_recipes_with_titles_have_tags(
    search_string: str,
    tag: str,
    exclusions: list[str],
):
    for recipe in _repo.recipes:
        if search_string.lower() not in recipe.title.lower():
            continue

        if recipe.title in exclusions:
            continue

        assert tag in recipe.tags, f"{recipe.title} should be tagged with {tag}"
