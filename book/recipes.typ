#import "@preview/cmarker:0.1.1"
#import "helpers/recipe.typ": recipe
#import "helpers/title.typ": title-page

#set document(
  title: [Recipe Book],
)
#set text(
  font: "Libertinus Serif",
)
#set page(
  paper: "a4",
)
#set par(
  justify: true,
)

#title-page(
  title: "Cookbook",
  subtitle: "A recipe collection",
  date: datetime.today(),
)

// Table of contents
#set page(numbering: "(i)")
#counter(page).update(1)
#outline(indent: 2em, depth: 3)

#pagebreak()

#set page(footer: context [
  #h(1fr)
  #counter(page).display(
    "1/1",
    both: false,
  )
])
#set page(numbering: "1")
#counter(page).update(1)

#for section in json("data/recipes-by-section.json") [
  #pagebreak()
  = #section.section

  #cmarker.render(read("extras/sections/" + section.section + ".md"))

  #for r in section.recipes [
    #pagebreak()
    #recipe(r, level: 3)
  ]
]

#pagebreak()

#set ref(form: "page")

= Index

#columns(2, gutter: 16pt)[
  #for section in json("data/by-tag.json") [
    == #section.title

    #for item in section.items {
      [
        #link(label(item.label))[#item.text]#box(width: 1fr, repeat[.])#ref(label(item.label))
        #linebreak()
      ]
    }
  ]
]
