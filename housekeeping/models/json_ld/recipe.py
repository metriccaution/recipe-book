from __future__ import annotations

from typing import Annotated, Literal, Optional, Union

from pydantic import AfterValidator, BaseModel, Field

from ..time_range import TimeRange


def _is_interval(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    return TimeRange.parse(value).duration_string()


class HowToStep(BaseModel):
    ld_type: Literal["HowToStep"] = Field(alias="@type", default="HowToStep")
    text: str
    itemListElement: Optional[list["HowToStep"]] = None


HowToStep.model_rebuild()


class HowToSection(BaseModel):
    ld_type: Literal["HowToSection"] = Field(alias="@type", default="HowToSection")
    name: str
    itemListElement: list[HowToStep]


class Recipe(BaseModel):
    context: Literal["https://schema.org"] = Field(
        alias="@context", default="https://schema.org"
    )
    ld_type: Literal["Recipe"] = Field(alias="@type", default="Recipe")
    name: str
    description: Optional[str] = None
    recipeYield: Optional[str] = None

    # TODO - Tags
    # TODO - Source (author?)
    # TODO - Tool

    recipeCategory: Literal[
        "Baking",
        "Component",
        "Drink",
        "Main",
        "Pickle",
        "Side",
        "Snack",
        "Sweet",
    ]

    cookTime: Annotated[Optional[str], AfterValidator(_is_interval)] = None
    prepTime: Annotated[str, AfterValidator(_is_interval)]

    recipeIngredient: list[str]
    recipeInstructions: Union[list[HowToStep], list[HowToSection]]
