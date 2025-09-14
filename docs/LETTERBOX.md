# Letterbox

Overlay shader that draws black bars with animated ease in/out.

## Why
- Cinematic framing without scaling or cropping your scene.

## Use
```renpy
$ snfx.lb.load("LB_2.39:1")   # or any preset name
$ snfx.lb.speed("fast")       # Very Slow | Slow | Normal | Fast | Very Fast | numeric
$ snfx.lb.show(True)          # animate in (False → out)
```

## Preset JSON
```json
{
  "name": "LB_2.39:1",
  "resolution": [1920,1080],
  "enable": true,
  "aspect": "2.39:1",
  "speed": "normal",
  "speed_custom": 6.0,
  "mix": 1.0
}
```

> In the **Editor**, only the **speed** is editable; aspect comes from the preset.
