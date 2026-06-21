from datetime import date
from enum import Enum
from operator import attrgetter
from re import compile, sub
from typing import Literal, Optional, Union
from urllib.parse import urlsplit
from uuid import uuid4

from pydantic import BaseModel, Field, computed_field, field_validator

from .isbn import validate_isbn
from .time_range import TimeRange

_whitespace_regex = compile("\\s+")


class Section(str, Enum):
    Main = "Main"
    Sweet = "Sweet"
    Side = "Side"
    Snack = "Snack"
    Baking = "Baking"
    Component = "Component"
    Pickle = "Pickle"
    Drink = "Drink"


class DescribedSource(BaseModel):
    "All I've got is a description"

    type: Literal["described"] = "described"
    description: str


class InternetSource(BaseModel):
    "A recipe from the internet"

    type: Literal["url"] = "url"
    url: str
    description: Optional[str] = None

    @field_validator("url")
    @classmethod
    def valid_url(cls, url: str) -> str:
        parsed = urlsplit(url)
        if parsed.scheme not in ["http", "https"]:
            raise ValueError(f"Invalid URL: {url}")
        return url


class BookSource(BaseModel):
    "A recipe from a book"

    type: Literal["book"] = "book"
    isbn: str
    page: Optional[int] = None
    description: str

    @field_validator("isbn")
    @classmethod
    def valid_isbn(cls, isbn: str) -> str:
        return validate_isbn(isbn)


class Ingredient(BaseModel):
    """A single ingredient."""

    quantity: str
    ingredient: str
    notes: Optional[str] = None


class IngredientGroup(BaseModel):
    """A group of ingredients.

    Lots of recipes will only have one of these, but some break out different
    parts of the recipe.

    If there's one group, its ok to not have a title, otherwise each group
    should have a unique title.
    """

    group: Optional[str] = None
    ingredients: list[Ingredient]

    @field_validator("ingredients")
    @classmethod
    def unique_ingredients(cls, items: list[Ingredient]) -> list[Ingredient]:
        names = [attrgetter("ingredient")(item) for item in items]
        if len(set(names)) != len(names):
            raise ValueError(f"Ingredients must be unique, but got: {','.join(names)}")
        return items


class InstructionStep(BaseModel):
    "A single step in the recipe - though it might have sub-steps."

    text: str
    substeps: Optional[list["InstructionStep"]] = None

    @field_validator("text")
    @classmethod
    def valid_text(cls, v: str) -> str:
        assert "\n" not in v
        return _whitespace_regex.sub(" ", v).strip()


class StepGroup(BaseModel):
    """A group of recipe steps - some recipes might have only one, some might
    break themselves down into groups.

    There's also an optional per-step description block.
    """

    title: Optional[str] = None
    text: Optional[str] = None
    steps: list[InstructionStep]

    @field_validator("steps")
    @classmethod
    def valid_steps(cls, v: list[InstructionStep]) -> list[InstructionStep]:
        assert len(v) > 0, "No steps"
        assert len(v) == len(set([i.text for i in v])), "Duplicate steps"
        return v


class Recipe(BaseModel):
    "A complete recipe"

    identifier: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    section: Section
    created_at: date
    tags: list[str]
    equipment: list[str]
    serves: Optional[int] = None
    prepTime: str
    cookingTime: Optional[str] = None
    source: Union[BookSource, InternetSource, DescribedSource]
    description: Optional[str] = None
    ingredients: list[IngredientGroup]
    steps: list[StepGroup]

    @computed_field
    @property
    def slug(self) -> str:
        return sub(r"^-|-$", "", sub(r"[^a-z0-9]+", "-", self.title.lower()))

    @field_validator("tags")
    @classmethod
    def valid_tags(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")

        return sorted(v)

    @field_validator("equipment")
    @classmethod
    def valid_equipment(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("Equipment must be unique")

        return sorted(v)

    @field_validator("cookingTime", "prepTime")
    @classmethod
    def valid_time_string(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        return TimeRange.parse(v).duration_string()

    @field_validator("ingredients")
    @classmethod
    def valid_ingredient_groups(cls, v: list[IngredientGroup]) -> list[IngredientGroup]:
        if len(v) == 0:
            raise ValueError("Recipe must have at least one ingredient group")
        if len(v) > 1:
            titles = [g.group for g in v]
            if any(t is None for t in titles):
                raise ValueError(
                    "All ingredient groups must have titles when there is more than one group"
                )
            if len(set(titles)) != len(titles):
                raise ValueError("Ingredient group titles must be unique")
        return v

    @field_validator("steps")
    @classmethod
    def valid_step_groups(cls, v: list[StepGroup]) -> list[StepGroup]:
        if len(v) == 0:
            raise ValueError("Recipe must have at least one step group")
        if len(v) > 1:
            titles = [g.title for g in v]
            if any(t is None for t in titles):
                raise ValueError(
                    "All step groups must have titles when there is more than one group"
                )
            if len(set(titles)) != len(titles):
                raise ValueError("Step group titles must be unique")
        return v

    # TODO - To markdown method
    # TODO - Camel case
