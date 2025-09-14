
# Snatchernauts FX Plugin 1.0
### Developed by Grahf (Dean Thomson) - September 2025

High‑quality **post‑processing & 2D lighting** pipeline for Ren’Py **8.4+ (GL2)** on desktop.  
Designed for cinematic visual novels and interactive fiction that want **letterbox**, **CRT**, **film grain**, **bloom**, **color grading**, and a **real‑time 2D lighting system** — all with an **in‑engine editor**, **preset JSONs**, and a **clean API**.

> **PC only.** Targets capable desktops (Win/macOS/Linux). Mobile & web are out of scope.

---

## ✨ Features

- **Post‑FX Stack** (top→bottom): Letterbox → CRT → Film Grain → Bloom → Color Grade
- **Advanced Ren’Py 8.4 shader path** (GL2), performance‑minded
- **In‑engine Editor** (draggable, dark UI with cyan/pink accents, MapleMono font)
- **First‑Run Setup Wizard**  
  Look Targets, Autotune to your resolution, Debug toggle, Hotkey binding with **conflict detection & auto‑fix**, profiles, and **Reset to defaults**
- **20 included presets per shader** + **20 lighting presets**
- **JSON preset system** (included & custom), auto‑load, save, edit
- **2D Lighting** (ambient, point, spot, rect) with per‑light animation (flicker / pulse / breathe)
- **Bloom** pass w/ animations (pulse / breathe) and anamorphic stretch
- **Tiny HUD overlay** for quick toggles
- **Rebindable hotkeys** with safe suggestions & profiles
- **Console logging** in your requested format: `:: [ SN FX ] - ...`

---

## 📦 Repository Layout

```
.
├─ snatchernauts_fx_plugin/
│  ├─ core/                       # all .rpy code (post stack, shaders, lights, editor, wizard, io, hud, hotkeys)
│  ├─ presets/
│  │  ├─ included/                # 20 presets per shader + 20 lighting + 20 bloom
│  │  └─ custom/                  # your presets (editor saves here)
│  ├─ ui/                         # rounded dark UI assets
│  └─ MapleMono-Regular.ttf       # bundled UI font
├─ docs/                          # full Markdown manual
└─ example_scene.rpy              # copy into your project to test
```

> If you ship as a drop‑in: put the whole `snatchernauts_fx_plugin/` folder under your game’s `game/` directory.

---

## 🚀 Installation

1) **Copy** the `snatchernauts_fx_plugin/` folder into your project at:
```
game/snatchernauts_fx_plugin/
```
2) (Optional) Add presets:
```
game/snatchernauts_fx_plugin/presets/included/
game/snatchernauts_fx_plugin/presets/custom/
```
3) Run the game. On the main menu the **First‑Run Setup Wizard** opens: pick a look, run **Autotune**, set hotkeys (with conflict detection), and optionally open the editor.

> Requires **Ren’Py 8.4+ (GL2)** on desktop with modern GPU drivers.

---

## 🧭 Quick Start

### Open the Editor
- Press **F10** (or your bound key), or call:
```renpy
$ snfx.open_editor()
```

### Apply a Look in Script
```renpy
label start:
    "Bootstrapping FX…"

    # Optional: resolve hotkey conflicts right away
    $ snfx.keys.bind(open_editor="K_F6", toggle_hud="K_F7", prev="K_a", next="K_d")

    # Optional: choose a look target and retarget presets to current resolution
    $ snfx.presets.set_look("cinematic")      # cinematic | broadcast | retro | neon | neutral
    $ snfx.presets.autotune()

    # Post-FX layers
    $ snfx.lb.load("Cine_Letterbox_Default")
    $ snfx.lb.speed("fast")        # UI: speed only; aspect lives in the preset
    $ snfx.lb.show(True)

    $ snfx.crt.load("Cine_CRT_Default")
    $ snfx.grain.load("Cine_Grain_Default")
    $ snfx.bloom.load("Cine_Bloom_Default")
    $ snfx.grade.load("Cine_Grade_Default")

    # Lighting
    $ snfx.lights.load("Cine_Lights_Default")

    "Ready."
    return
```

---

## 🧰 First‑Run Setup Wizard

- **Look Target** (cinematic / broadcast / retro / neon / neutral) → runs **Autotune** to stamp **custom** presets with your current resolution.
- **Hotkeys** with **live conflict detection** against `config.keymap`:
  - Fields highlight red on conflict and list offending actions.
  - **Suggest Non‑Conflicting Keys** picks safe keys automatically.
  - **Profiles**: save/load/delete mapped sets; **Reset to defaults** button included.
- **Debug logging** toggle and **Open editor after finish** option.
- “Don’t show again” persists. Re‑show anytime:
```renpy
$ persistent._snfx_setup_done = False
```

---

## 🎚️ Editor Overview

Tabs: **About**, **Letterbox**, **CRT**, **Film Grain**, **Bloom**, **Color Grade**, **Lighting**  
- **Letterbox**: *speed only* (very slow → very fast or numeric). Aspect comes from presets (2.39:1, 21:9, 16:9, 4:3, more).  
- **CRT**: vignette, chromatic aberration, scanlines, glitch, animation type/speed, barrel warp.  
- **Film Grain**: intensity, size, speed, downsample.  
- **Bloom**: threshold, soft knee, intensity, radius, samples, anamorphic, animations.  
- **Color Grade**: GPU `matrixcolor` ops (saturation, contrast, brightness, hue, tint, sepia/identity).  
- **Lighting (2D)**: ambient and multiple lights (point/spot/rect) front/behind, with flicker/pulse/breathe animation and draggable handles.

Every tab can **load included/custom presets**, **preview**, and **save** to `presets/custom/<category>/*.json`.

---

## 🧾 Presets & JSON

- **20 included presets per shader** (Letterbox, CRT, Grain, Bloom, Grade) + **20 lighting presets**.  
- **Custom presets**: duplicate a template, tweak, and the editor will pick it up.
- **Look Targets & Autotune**: custom presets get resolution‑stamped and harmonized.

Minimal examples (see full schemas in `docs/SCHEMA_REFERENCE.md`):

```jsonc
// Letterbox
{ "name":"LB_2.39:1", "resolution":[1920,1080], "enable":true, "aspect":"2.39:1", "speed":"normal", "speed_custom":6.0, "mix":1.0 }

// CRT
{ "name":"CRT_Arcade", "resolution":[1920,1080], "enable":true,
  "intensity":0.28, "vignette":0.20, "aberration":0.0025,
  "scanline_strength":0.35, "scanline_density":1.8,
  "glitch":0.08, "anim_type":"sine", "anim_speed":1.1, "barrel":0.004 }

// Bloom
{ "name":"Bloom_Cinematic", "resolution":[1920,1080], "enable":true,
  "threshold":0.72, "soft_knee":0.50, "intensity":0.90, "radius":2.0,
  "samples":15, "anamorphic":0.20, "anim":{"type":"pulse","speed":1.0,"amount":0.15} }
```

---

## 🔌 API Cheat Sheet

```renpy
# System
$ snfx.open_editor()            # opens the editor (pauses gameplay)
$ snfx.pause(True/False)        # force pause/resume
$ snfx.debug(True/False)        # console logs ":: [ SN FX ] - ..."

# Look targets & autotune
$ snfx.presets.set_look("neon") # cinematic|broadcast|retro|neon|neutral
$ snfx.presets.autotune()       # retarget custom JSONs to current resolution

# Letterbox
$ snfx.lb.load("LB_2.39:1")
$ snfx.lb.speed("fast")         # or a number
$ snfx.lb.show(True/False)

# CRT / Grain / Bloom / Grade
$ snfx.crt.load("CRT_Arcade")
$ snfx.grain.load("Cinema_35mm_Soft")
$ snfx.bloom.load("Bloom_Cinematic")
$ snfx.grade.load("Teal_Orange")

# Lighting
$ snfx.lights.clear()
$ snfx.lights.set_ambient(0.12,0.12,0.15, 0.55)
$ L = snfx.lights.add_point(0.5,0.6, color=(1.0,0.9,0.7), intensity=1.15, radius=0.35, falloff=1.1, front=False)
$ snfx.lights.set_anim(L, type="flicker", speed=1.6, amount=0.2)
$ snfx.lights.save("MyScene")
$ snfx.lights.load("Lights_Studio")

# Hotkeys
$ snfx.keys.enable(True/False)
$ snfx.keys.bind(open_editor="K_F6", toggle_hud="K_F7", prev="K_a", next="K_d")
$ snfx.keys.conflicts(["K_F6","K_F7","K_a","K_d"])
$ sug = snfx.keys.suggest()
$ snfx.keys.save_profile("MyProfile")
$ snfx.keys.load_profile("MyProfile")
$ snfx.keys.reset_defaults()
```

---

## 🐛 Debug & Logging

Enable:
```renpy
$ snfx.debug(True)
```
Output format:
```
:: [ SN FX ] - Letterbox: On
:: [ SN FX ] - CRT: On (CRT_Arcade)
:: [ SN FX ] - Setup: look=neon, debug=On, keys={...}
```
Disable:
```renpy
$ snfx.debug(False)
```

---

## ⚙️ Performance Notes

- **Bloom** is the heaviest pass. Start low (radius/samples) and increase gradually.
- **CRT** glitch + barrel are costlier than base scanlines/aberration.
- **Grain** overlay is cheap; downsample can give chunkier look nearly free.
- **Lights**: each is a fullscreen eval; 3–8 typical. Prefer smaller radii and avoid large overlapping rects.
- 1080p is a sweet spot; for 4K, reduce bloom intensity/radius and light count.

See `docs/PERFORMANCE_TUNING.md` for tips.

---

## 🧩 Compatibility

- **Ren’Py 8.4+ (GL2)** desktop builds (Windows/macOS/Linux)
- Uses advanced shaders & screen language; do **not** target mobile/web.

Hotkey collisions? The wizard & APIs handle detection and suggestions.

---

## 📚 Documentation

Full manual in **`/docs`** (also published in releases):
- `INSTALLATION.md`
- `GETTING_STARTED.md` (scene integration)
- `EDITOR.md` (all tabs)
- `LETTERBOX.md`, `CRT.md`, `FILM_GRAIN.md`, `BLOOM.md`, `COLOR_GRADING.md`
- `LIGHTING.md` (2D lights)
- `PRESETS.md` & `SCHEMA_REFERENCE.md`
- `LOOK_TARGETS_AUTOTUNE.md`
- `API_REFERENCE.md`
- `HOTKEYS_AND_INPUT.md`
- `DEBUG_AND_LOGGING.md`
- `PERFORMANCE_TUNING.md`
- `TROUBLESHOOTING.md`

---

## 🤝 Contributing

Issues and PRs welcome! If you add presets, please include:
- A short description & preview notes
- JSON in the correct category folder
- Tested on Ren’Py 8.4+ desktop

---

## 📄 License

Choose the license that fits your project (MIT recommended for permissive use). Add your `LICENSE` file at repo root.

---

## 💬 Credits

Built for **Snatchernauts** projects and the VN community — enjoy the glow ✨
