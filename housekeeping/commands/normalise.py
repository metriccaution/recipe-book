import shutil
from pathlib import Path

from housekeeping.models.repository import RecipeRepository


def normalise(source_dir: Path) -> None:
    """Re-load and re-write the existing sources.

    This makes sure all the data is valid, and in the correct format.
    """

    repo = RecipeRepository.from_directory(source_dir)

    tags_by_ingredient: dict[str, list[str]] = {}
    # If removing a tag, put it in here to get it removed from recipes
    ingredient_tags: set[str] = set()
    for i in repo.ingredients:
        tags_by_ingredient[i.name] = i.tags
        for alias in i.synonyms:
            tags_by_ingredient[alias] = i.tags
        for t in i.tags:
            ingredient_tags.add(t)

    for r in repo.recipes:
        tags = [t for t in r.tags if t not in ingredient_tags]
        extra_tags: list[str] = []
        for ig in r.ingredients:
            for il in ig.ingredients:
                for i in il.alternate_ingredients():
                    extra_tags += tags_by_ingredient.get(i, [])

        r.tags = list(set(tags + extra_tags))
        r.tags.sort()

    shutil.rmtree(source_dir)
    repo.to_directory(source_dir)
