# CRT (Master Pass)

Applies a retro display look over the whole scene. Renders before Bloom and Color Grade.

## Controls
- **Intensity** (overall), **Vignette**, **Chromatic Aberration**
- **Scan Strength/Density**, **Glitch**, **Animation Type** (None/Sine/Tri/Roll), **Anim Speed**
- **Barrel Warp** for subtle curvature

## API
```renpy
$ snfx.crt.load("CRT_Arcade")
$ snfx.crt.enable(True)
$ snfx.crt.set(intensity=0.28, vignette=0.2, aberration=0.002,
               scan_strength=0.35, scan_density=1.8,
               glitch=0.08, anim_type=1, anim_speed=1.1, barrel=0.004)
```
