# Color Grading (MatrixColor)

Final pass using Ren'Py `im.MatrixColor` ops.

## Common Ops
- saturation, contrast, brightness
- hue, tint(r,g,b)
- identity, sepia

## API
```renpy
$ snfx.grade.load("Teal_Orange")
$ snfx.grade.apply_ops([
  {"op":"contrast","value":1.1},
  {"op":"tint","r":1.03,"g":1.02,"b":0.98}
])
```
