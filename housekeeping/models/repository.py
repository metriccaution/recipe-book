"""Everything as one big data model."""

from pathlib import Path

from pydantic import BaseModel
from yaml import SafeLoader, dump, load

from .ingredients import IngredientMetadata
from .recipes import Recipe


class RecipeRepository(BaseModel):
    "All of the data together"

    ingredients: list[IngredientMetadata]
    recipes: list[Recipe]

    @classmethod
    def from_directory(cls, source_directory: Path) -> "RecipeRepository":
        "Load up a directory to structure data. See also, `to_directory`."
        ingredients = []
        recipes = []

        for ingredient_file in Path(source_directory, "ingredients").rglob("*.yaml"):
            with open(ingredient_file) as f:
                ingredients.append(IngredientMetadata(**load(f, Loader=SafeLoader)))

        for recipe_file in Path(source_directory, "recipes").rglob("*.yaml"):
            with open(recipe_file) as f:
                try:
                    recipes.append(Recipe(**load(f, Loader=SafeLoader)))
                except Exception as e:
                    print(recipe_file)
                    raise e

        return RecipeRepository(ingredients=ingredients, recipes=recipes)

    def to_directory(self, export_directory: Path):
        "Write structured data to a directory. See also, `from_directory`."

        export_directory.mkdir(parents=True, exist_ok=True)

        for ingredient in self.ingredients:
            write_to = Path(
                export_directory,
                "ingredients",
                ingredient.measure,
                f"{ingredient.name}.yaml",
            )
            write_to.parent.mkdir(parents=True, exist_ok=True)
            with open(write_to, mode="w") as f:
                dump(
                    ingredient.model_dump(
                        exclude_none=True,
                        mode="json",
                    ),
                    f,
                    sort_keys=False,
                )

        for recipe in self.recipes:
            write_to = Path(
                export_directory,
                "recipes",
                recipe.section,
                f"{recipe.title}.yaml",
            )
            write_to.parent.mkdir(parents=True, exist_ok=True)
            with open(write_to, mode="w") as f:
                dump(
                    recipe.model_dump(
                        exclude_none=True,
                        exclude={"slug"},
                        mode="json",
                    ),
                    f,
                    sort_keys=False,
                )
