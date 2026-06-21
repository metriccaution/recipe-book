"""Export structured data for compiling the recipe book PDF."""

import json
from pathlib import Path
from typing import Any

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


def typst_export(source_dir: Path, export_directory: Path) -> None:
    repo = RecipeRepository.from_directory(source_dir)

    printable_recipes: list[dict[str, Any]] = []
    recipes_by_tag: dict[str, list[dict[str, str]]] = {}
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

        entry = {"label": recipe.identifier, "text": recipe.title}
        for tag in recipe.tags:
            recipes_by_tag.setdefault(tag, []).append(entry)

    by_section: list[dict[str, Any]] = []
    for section in Section:
        by_section.append(
            {
                "section": section.value,
                "recipes": [
                    r for r in printable_recipes if r["section"] == section.value
                ],
            }
        )

    filter_tags = set(_overly_general_tags + _internal_tags)

    by_tag = [
        {
            "title": tag,
            "items": sorted(recipes_by_tag[tag], key=lambda r: r["text"]),
        }
        for tag in sorted(recipes_by_tag)
        if tag not in filter_tags
    ]

    export_directory.mkdir(exist_ok=True, parents=True)

    with open(Path(export_directory, "recipes.json"), mode="w") as f:
        json.dump(printable_recipes, f, indent=2)

    with open(Path(export_directory, "recipes-by-section.json"), mode="w") as f:
        json.dump(by_section, f, indent=2)

    with open(Path(export_directory, "by-tag.json"), mode="w") as f:
        json.dump(by_tag, f, indent=2)
