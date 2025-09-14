# Getting Started

The plugin self‑registers when the folder is under `game/`. No imports needed.

## Opening the Editor
- Press **F10** (default), or:
  ```renpy
  $ snfx.open_editor()
  ```
The Editor **pauses gameplay** while open; closing resumes.

## Including the Plugin in a Scene

Minimal example:
```renpy
label start:
    "Scene begins."

    # Optional: resolve hotkey conflicts
    $ snfx.keys.bind(open_editor="K_F6", toggle_hud="K_F7", prev="K_a", next="K_d")

    # Optional: pick a look and retarget custom presets to your current resolution
    $ snfx.presets.set_look("cinematic")   # cinematic | broadcast | retro | neon | neutral
    $ snfx.presets.autotune()

    # Use Editor to explore and save presets
    $ snfx.open_editor()

    # Apply looks programmatically
    $ snfx.lb.load("Cine_Letterbox_Default")
    $ snfx.lb.speed("fast")
    $ snfx.lb.show(True)

    $ snfx.crt.load("Cine_CRT_Default")
    $ snfx.grain.load("Cine_Grain_Default")
    $ snfx.bloom.load("Cine_Bloom_Default")
    $ snfx.grade.load("Cine_Grade_Default")

    # Lighting scene
    $ snfx.lights.load("Cine_Lights_Default")

    "Continue..."
    return
```

## Recommended Stack Order
- Overlays: **Letterbox**, **Film Grain**
- Master chain on `master` layer: **CRT → Bloom → Color Grade**
- Lights render on `master` so Bloom/Grade affect them.
