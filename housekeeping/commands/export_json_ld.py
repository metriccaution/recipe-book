"""Convert the main repo files into JSON-LD based files."""

from pathlib import Path

from housekeeping.models.json_ld.recipe import HowToSection, HowToStep
from housekeeping.models.json_ld.recipe import Recipe as JsonLdRecipe
from housekeeping.models.recipes import InstructionStep
from housekeeping.models.recipes import Recipe as SourceRecipe
from housekeeping.models.repository import RecipeRepository


def _convert_step(source: InstructionStep) -> HowToStep:
    if source.substeps and len(source.substeps) > 0:
        return HowToStep(
            text=source.text,
            itemListElement=[_convert_step(step) for step in source.substeps],
        )
    else:
        return HowToStep(text=source.text)


def recipe_to_json_ld(recipe: SourceRecipe) -> JsonLdRecipe:
    ingredients = []
    for ingredient_group in recipe.ingredients:
        for ingredient in ingredient_group.ingredients:
            text = f"{ingredient.quantity} {ingredient.ingredient}"
            if ingredient.notes:
                text += f" ({ingredient.notes})"
            ingredients.append(text)

    instructions = []
    if len(recipe.steps) == 1:
        for step in recipe.steps[0].steps:
            instructions.append(_convert_step(step))
    else:
        for step_group in recipe.steps:
            assert len(step_group.title) > 0, "No title on group"
            instructions.append(
                HowToSection(
                    name=step_group.title,
                    itemListElement=[_convert_step(step) for step in step_group.steps],
                )
            )

    return JsonLdRecipe(
        name=recipe.title,
        description=recipe.description if recipe.description else None,
        recipeYield=f"Serves {recipe.serves}" if recipe.serves else None,
        recipeCategory=recipe.section.value,
        prepTime=recipe.prepTime,
        cookTime=recipe.cookingTime,
        recipeIngredient=ingredients,
        recipeInstructions=instructions,
    )


def json_ld_export(source_dir: Path, output_dir: Path) -> None:
    for recipe in RecipeRepository.from_directory(source_dir).recipes:
        converted = recipe_to_json_ld(recipe)

        output_dir.mkdir(exist_ok=True, parents=True)

        with open(Path(output_dir, f"{converted.name}.json"), mode="w") as f:
            f.write(
                converted.model_dump_json(
                    by_alias=True,
                    exclude_none=True,
                    indent=2,
                )
            )
