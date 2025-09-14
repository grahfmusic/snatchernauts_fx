# API Reference

Everything hangs off the global `snfx` object.

## System
```renpy
$ snfx.open_editor()       # open editor (pauses gameplay until closed)
$ snfx.pause(True/False)   # force pause/resume gameplay logic
$ snfx.debug(True/False)   # toggle console logging ":: [ SN FX ] - ..."
```

## Hotkeys
```renpy
$ snfx.keys.enable(True/False)
$ snfx.keys.bind(open_editor="K_F10", toggle_hud="K_F9", prev="K_LEFT", next="K_RIGHT")
```

## Presets (Look Targets & Autotune)
```renpy
$ snfx.presets.set_look("cinematic" | "broadcast" | "retro" | "neon" | "neutral")
$ snfx.presets.autotune()    # stamp custom JSONs with current resolution + adjust ranges
```

## Letterbox
```renpy
$ snfx.lb.load(name)
$ snfx.lb.speed("fast")      # or number
$ snfx.lb.show(True/False)
```

## CRT
```renpy
$ snfx.crt.load(name)
$ snfx.crt.enable(True/False)
$ snfx.crt.set(intensity=..., vignette=..., aberration=..., scan_strength=..., scan_density=..., glitch=..., anim_type=..., anim_speed=..., barrel=...)
```

## Film Grain
```renpy
$ snfx.grain.load(name)
$ snfx.grain.set(intensity=..., size=..., speed=..., downsample=...)
```

## Color Grade
```renpy
$ snfx.grade.load(name)
$ snfx.grade.apply_ops([ ... ])  # list of {op,value} dicts
```

## Lighting
```renpy
$ snfx.lights.clear()
$ snfx.lights.set_ambient(r,g,b,intensity)
$ L = snfx.lights.add_point(x,y, color=(r,g,b), intensity=1.0, radius=0.3, falloff=1.0, front=False)
$ snfx.lights.add_spot(x,y, dir=(dx,dy), angle=35, color=(r,g,b), intensity=1.0, radius=0.6, falloff=1.0, front=False)
$ snfx.lights.add_rect(x,y, w,h, color=(r,g,b), intensity=0.8, falloff=1.0, front=False)
$ snfx.lights.set_anim(L, type="flicker|pulse|breathe", speed=1.6, amount=0.2)
$ snfx.lights.load(name)
$ snfx.lights.save(name)
```

## Bloom
```renpy
$ snfx.bloom.load(name)
$ snfx.bloom.set(enable=True, threshold=..., soft_knee=..., intensity=..., radius=..., samples=..., anamorphic=...)
$ snfx.bloom.set_anim(type="pulse", speed=..., amount=...)
$ snfx.bloom.save(name)
```


## Hotkey Profiles & Utilities
```renpy
$ snfx.keys.reset_defaults()

$ snfx.keys.save_profile("MyProfile")         # saves current mapping (or pass a mapping as 2nd arg)
$ snfx.keys.list_profiles()                    # -> ["Default","MyProfile",...]
$ snfx.keys.load_profile("MyProfile")
$ snfx.keys.delete_profile("MyProfile")

$ snfx.keys.conflicts(["K_F6","K_F7","K_a","K_d"])   # -> { "K_F6": ["some_action", ...], ... }
$ sug = snfx.keys.suggest()                          # -> {"open":"K_F6","hud":"K_F7","prev":"K_a","next":"K_d"}
```
