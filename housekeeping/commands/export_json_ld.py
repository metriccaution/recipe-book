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
    ingredients: list[str] = []
    for ingredient_group in recipe.ingredients:
        for ingredient in ingredient_group.ingredients:
            text = f"{ingredient.quantity} {' or '.join(ingredient.alternate_ingredients())}"
            if ingredient.notes:
                text += f" ({ingredient.notes})"
            ingredients.append(text)

    instructions: list[HowToStep] | list[HowToSection]
    if len(recipe.steps) == 1:
        instructions = [_convert_step(step) for step in recipe.steps[0].steps]
    else:
        section_list: list[HowToSection] = []
        for step_group in recipe.steps:
            title = step_group.title
            if title is None or len(title) == 0:
                raise ValueError("No title on group")
            section_list.append(
                HowToSection(
                    name=title,
                    itemListElement=[_convert_step(step) for step in step_group.steps],
                )
            )
        instructions = section_list

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
