# Look Targets & Autotune

To make presets portable across projects/resolutions, the plugin offers **Look Targets** and an **autotune** helper
that stamp presets to your current `config.screen_width/height` and harmonize parameter ranges.

## Installing the Helper
Ensure this file exists:
```
game/snatchernauts_fx_plugin/core/presets_autotune.rpy
```
and you have custom presets in:
```
game/snatchernauts_fx_plugin/presets/custom/<category>/*.json
```

## Picking a Look
Available looks:
- `cinematic` (scope framing, subtle CRT, soft grain, pulsing bloom, teal/orange grade)
- `broadcast` (neutral 16:9, minimal CRT off, gentle grain, soft bloom)
- `retro` (4:3, strong scanlines + rolling glitch, coarse grain, low bloom)
- `neon` (21:9, lively CRT, crisp grain, anamorphic bloom, cyber grade)
- `neutral` (clean, CRT off, minimal grade/bloom)

## API
```renpy
$ snfx.presets.set_look("neon")   # or cinematic/broadcast/retro/neutral
$ snfx.presets.autotune()         # retargets all custom JSONs to current resolution + look
```
The helper runs once on first launch (defaults to `"cinematic"`). Re-run any time after a resolution change.

## Which Files Are Modified?
Only **custom** presets are rewritten in-place. Included presets remain read‑only.
