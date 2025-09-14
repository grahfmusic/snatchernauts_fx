# 2D Lighting System

Real-time 2D lights rendered on the master layer (so Bloom/Grade affect them).

## Types
- Ambient (RGBAi), Point, Spot (dir/angle), Rect (soft area)

## Per-Light
- pos (normalized), color, intensity, radius/size, falloff, front/behind, animation (flicker/pulse/breathe)

## API
```renpy
$ snfx.lights.clear()
$ snfx.lights.set_ambient(0.15,0.15,0.18, 0.6)
$ lid = snfx.lights.add_point(0.5,0.6, color=(1.0,0.9,0.7), intensity=1.0, radius=0.3, falloff=1.0, front=False)
$ snfx.lights.set_anim(lid, type="flicker", speed=1.6, amount=0.2)
$ snfx.lights.save("MyScene")
$ snfx.lights.load("Lights_Studio")
```
