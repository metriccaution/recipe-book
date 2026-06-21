#import "@preview/cmarker:0.1.1"

// The source section of a recipe
#let source(item, level: 3) = [
  #if "isbn" in item [
    From - #item.description (ISBN: #item.isbn)
  ] else if "url" in item [
    From - #item.description (#link(item.url))
  ] else [
    From - #item.description
  ]
  // TODO - More details
]

// The ingredients list
#let ingredients(itemList, level: 3) = [
  #heading("Ingredients", level: level)
  #for group in itemList [
    #if "group" in group [
      #heading(group.group, level: level + 1)
    ]

    #for ingredient in group.ingredients [
      #if "notes" in ingredient [
        - #ingredient.quantity #ingredient.ingredient (#ingredient.notes)
      ] else [
        - #ingredient.quantity #ingredient.ingredient
      ]
    ]
  ]
]

// Renders step text + any sub-steps as a nested bullet list
#let render-step(s) = {
  let text = cmarker.render(s.text)
  if "substeps" in s {
    text + block(above: 0.5em, below: 0.5em, enum(..s.substeps.map(sub => enum.item(render-step(sub)))))
  } else {
    text
  }
}

// Full instruction list
#let steps(itemList, level: 3) = [
  #heading("Instructions", level: level)

  #for group in itemList [
    #if "title" in group [
      #heading(group.title, level: level + 1)
    ]

    #enum(..group.steps.map(step => enum.item(render-step(step))))
  ]
]

// Format an ISO date string (YYYY-MM-DD) as "D Month YYYY"
#let format-date(d) = {
  let parts = d.split("-")
  let dt = datetime(year: int(parts.at(0)), month: int(parts.at(1)), day: int(parts.at(2)))
  dt.display("[day] [month repr:long] [year]")
}

// A full recipe
#let recipe(item, level: 2) = [
  #heading(item.title, level: level) #label(item.identifier)

  #source(item.source, level: level + 1)

  #if "serves" in item [
    Serves - #item.serves
  ]

  #if "prepTime" in item and "cookingTime" in item [
    Preparation time: #item.prepTime, Cooking time: #item.cookingTime
  ] else if "prepTime" in item [
    Preparation time: #item.prepTime
  ] else if "cookingTime" in item [
    Cooking time: #item.cookingTime
  ]

  #if "created_at" in item [
    Added at: #format-date(item.created_at)
  ]

  #cmarker.render(item.at("description", default: ""))

  #ingredients(item.ingredients, level: level + 1)
  #steps(item.steps, level: level + 1)
]
