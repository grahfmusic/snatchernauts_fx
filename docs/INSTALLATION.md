# Installation

> Requires **Ren'Py 8.4+ (GL2)** on desktop (Windows/macOS/Linux). The plugin targets capable PCs. Mobile/web not supported.

## 1) Drop the Plugin
Place the folder in your project's `game/`:
```
game/snatchernauts_fx_plugin/
```

Structure should include:
```
snatchernauts_fx_plugin/
  core/           # .rpy code
  presets/
    included/     # shipped presets (optional pack)
    custom/       # your presets
  ui/             # rounded UI assets
  MapleMono-Regular.ttf
```

## 2) Presets (Optional but Recommended)
- **Included Starter Pack (20 each):** unzip into  
  `game/snatchernauts_fx_plugin/presets/included/`
- **Custom Templates:** unzip into  
  `game/snatchernauts_fx_plugin/presets/custom/`
- **Auto‑Tuned Custom Pack + Helper:** unzip into  
  `game/snatchernauts_fx_plugin/` (adds `core/presets_autotune.rpy` and ready defaults).

## 3) Verify
Run your game:
- **F10** (or rebound key) → open Editor (auto‑pauses gameplay).
- **F9** → toggle tiny HUD.
If a key conflicts, rebind (see [Hotkeys & Input](HOTKEYS_AND_INPUT.md)).
