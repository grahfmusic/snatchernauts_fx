# Hotkeys & Input

Default bindings:
- **F10** — open Editor
- **F9** — toggle HUD
- **←/→** — cycle presets for the active editor tab

Conflicts? Use the **First-Run Wizard** or check in script:
```renpy
$ snfx.keys.enable(True)
$ conflicts = snfx.keys.conflicts(["K_F6","K_F7","K_a","K_d"])
if conflicts:
    $ sug = snfx.keys.suggest()
    $ snfx.keys.bind(open_editor=sug["open"], toggle_hud=sug["hud"], prev=sug["prev"], next=sug["next"])
else:
    $ snfx.keys.bind(open_editor="K_F6", toggle_hud="K_F7", prev="K_a", next="K_d")
```
