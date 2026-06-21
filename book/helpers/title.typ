#let title-page(title: "Recipe Book", subtitle: none, date: none) = {
  set page(margin: 0pt)

  place(
    top + left,
    dx: 60pt,
    dy: 60pt,
    box(
      width: 4pt,
      height: 220pt,
      fill: rgb("#c8a96e"),
    ),
  )

  place(
    top + left,
    dx: 80pt,
    dy: 60pt,
    box(height: 220pt)[
      #set align(horizon)
      #set text(fill: rgb("#1a1a1a"))
      #v(1fr)
      #text(size: 48pt, weight: "bold", stretch: 75%)[#title]
      #v(8pt)
      #if subtitle != none {
        text(size: 16pt, style: "italic", fill: rgb("#555555"))[#subtitle]
      }
      #v(1fr)
    ],
  )

  place(
    bottom + right,
    dx: -60pt,
    dy: -60pt,
    box[
      #set text(size: 9pt, fill: rgb("#999999"), tracking: 2pt)
      #if date != none { upper(date.display("[day]-[month]-[year]")) }
    ],
  )
}
