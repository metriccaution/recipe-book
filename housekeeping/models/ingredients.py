from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from .recipes import Ingredient

# TODO - Sorting out units for everything


class MeasureType(str, Enum):
    "Different kinds of measurements - To allow normalisation"

    Volume = "volume"
    Weight = "weight"
    Spice = "spice"
    Singles = "singles"
    Can = "can"


class Units(str, Enum):
    Can = "can"

    def matches_quantity(self, value: str) -> bool:
        # TODO - Probably wants a list of patterns
        return value.endswith(self.value)


class IngredientMetadata(BaseModel):
    """Information about allowed ingredients.

    Mostly exists so I can make sure I have consistency across recipes.
    """

    identifier: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    include_in_shopping: bool = True
    synonyms: list[str]
    measure: MeasureType
    tags: list[str] = []
    units: Optional[list[Units]] = None

    @field_validator("name", "synonyms", mode="before")
    @classmethod
    def no_slash(cls, v: str | list[str]) -> str | list[str]:
        values = v if isinstance(v, list) else [v]
        for value in values:
            if "/" in value:
                raise ValueError(
                    f"Ingredient name must not contain '/': {value!r}, as that's used to indicate alternate ingredients."
                )
        return v

    @field_validator("tags")
    @classmethod
    def valid_tags(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")

        # Sort it for neatness
        v.sort()

        return v

    def matches_ingredient(self, ingredient: Ingredient) -> bool:
        "Does this ingredient match the reference data."

        parts = ingredient.alternate_ingredients()
        matches_name = any(part == self.name or part in self.synonyms for part in parts)
        if not matches_name:
            return False

        if self.units:
            return any(
                unit.matches_quantity(ingredient.quantity) for unit in self.units
            )

        return True
