# Recipe Book

My collection of recipes, a mix of stuff in my regular rotation, special occasion stuff, and some old favourites from my childhood.

## Data

- Data's stored as YAML files in `/recipes/`
  - There's a custom recipe format, [defined in Pydantic models](./housekeeping/models/recipes.py)
  - There's ingredients stored as their own entities to keep things consistent, and to aid in tagging
- The recipes themselves are sourced from all over
  - They're generally re-edited for style, I've aimed for a concise, clear format, favouring more steps over longer individual steps
  - In terms of licensing, I believe that the facts of a recipe aren't protected by copyright, only the expression of them, with that in mind, I've re-written recipes into my own style, which, I believe _should_ be sufficient
