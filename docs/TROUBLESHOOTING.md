# Troubleshooting

**Editor doesn’t open**  
Hotkey conflict — rebind:
```renpy
$ snfx.keys.bind(open_editor="K_F6")
```

**Autotune didn’t change my presets**  
Only **custom** presets are rewritten. Ensure your files live under `presets/custom/` and that `core/presets_autotune.rpy` exists. Then:
```renpy
$ snfx.presets.autotune()
```

**Black screen or shader error**  
Require **Ren'Py 8.4+ (GL2)** on desktop; update GPU drivers.

**Lights not visible**  
Check `intensity`, `front/behind`, and confirm Bloom/Grade aren’t overpowering subtle light colors.

**Logs too noisy**  
```renpy
$ snfx.debug(False)
```
