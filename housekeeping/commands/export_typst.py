"""Export structured data for compiling the recipe book PDF."""

import json
from pathlib import Path

from housekeeping.models.recipes import Section
from housekeeping.models.repository import RecipeRepository
from housekeeping.models.time_range import TimeRange

# End up being excessively large exports
_overly_general_tags = [
    "Meat",
    "Nuts",
    "Onion",
    "Tomato",
]

# Don't really make sense for the exported PDF
_internal_tags = ["Complex"]


def typst_export(source_dir: Path, export_directory: Path):
    repo = RecipeRepository.from_directory(source_dir)

    printable_recipes = []
    tags = set()
    for recipe in sorted(repo.recipes, key=lambda r: r.title):
        printable_recipes.append(
            {
                **recipe.model_dump(mode="json", exclude_none=True),
                "prepTime": TimeRange.parse(recipe.prepTime).pretty_print()
                if recipe.prepTime
                else None,
                "cookingTime": TimeRange.parse(recipe.cookingTime).pretty_print()
                if recipe.cookingTime
                else None,
            }
        )

        for tag in recipe.tags:
            tags.add(tag)

    by_section = []
    for section in Section:
        by_section.append(
            {
                "section": section.value,
                "recipes": [
                    r for r in printable_recipes if r["section"] == section.value
                ],
            }
        )

    filter_tags = _overly_general_tags + _internal_tags

    by_tag = []
    for tag in sorted(tags):
        if tag in filter_tags:
            continue

        by_tag.append(
            {
                "title": tag,
                "items": sorted(
                    [
                        {
                            "label": r.identifier,
                            "text": r.title,
                        }
                        for r in repo.recipes
                        if tag in r.tags
                    ],
                    key=lambda r: r["text"],
                ),
            }
        )

    export_directory.mkdir(exist_ok=True, parents=True)

    with open(Path(export_directory, "recipes.json"), mode="w") as f:
        json.dump(printable_recipes, f, indent=2)

    with open(Path(export_directory, "recipes-by-section.json"), mode="w") as f:
        json.dump(by_section, f, indent=2)

    with open(Path(export_directory, "by-tag.json"), mode="w") as f:
        json.dump(by_tag, f, indent=2)
