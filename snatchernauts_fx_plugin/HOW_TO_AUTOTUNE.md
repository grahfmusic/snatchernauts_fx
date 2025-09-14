# Auto-Tuned Custom Presets (Look Targets)

This pack includes ready-made custom presets for five **look targets** and an `.rpy` helper that
automatically retargets the JSON `resolution` to your game's current size and harmonizes values.

**Look targets:**
- `cinematic` (default)
- `broadcast`
- `retro`
- `neon`
- `neutral`

## Install
Copy these into your project:
```
game/snatchernauts_fx_plugin/core/presets_autotune.rpy
game/snatchernauts_fx_plugin/presets/custom/<category>/*.json
```

## Choose a Look
In script (before loading presets), set and (optionally) re-run autotune:
```renpy
$ snfx.presets.set_look("neon")     # or cinematic/broadcast/retro/neutral
$ snfx.presets.autotune()           # rewrites custom JSONs to current resolution + look
```

If you don't call anything, it defaults to `cinematic` and runs once on first launch.

## Use in Scene
```renpy
$ snfx.lb.load("Cine_Letterbox_Default")
$ snfx.crt.load("Cine_CRT_Default")
$ snfx.grain.load("Cine_Grain_Default")
$ snfx.bloom.load("Cine_Bloom_Default")
$ snfx.grade.load("Cine_Grade_Default")
$ snfx.lights.load("Cine_Lights_Default")
```
Change the `Cine_` prefix to `TV_`, `Retro_`, `Neon_`, or `Neutral_` for other looks.
