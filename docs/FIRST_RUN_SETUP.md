# First-Run Setup Wizard

On first launch (main menu), configure the plugin quickly.

## Flow
1. Pick a **Look Target** → runs **Autotune** to stamp custom presets for your resolution.
2. Toggle **Debug Logging** and **Open editor after finish**.
3. Bind **Hotkeys** with **live conflict detection** (red highlight + explanation).
4. Manage **Hotkey Profiles** (save/load/delete) and **Reset to Defaults**.

## Profiles
- Save your current mapping as a named profile.
- Load a saved profile to instantly swap mappings.
- Delete removes it from persistence.
- The applied profile becomes the active profile and persists across sessions.

## Reset
- **Reset to Defaults** sets: `K_F10` (open), `K_F9` (HUD), `K_LEFT`/`K_RIGHT` (prev/next), enables hotkeys.
- You can also request conflict-free keys with **Suggest Non-Conflicting Keys**.

You can script the same:
```renpy
# Reset to defaults
$ snfx.keys.reset_defaults()

# Profiles
$ snfx.keys.save_profile("MyEditKeys")
$ snfx.keys.list_profiles()
$ snfx.keys.load_profile("MyEditKeys")
$ snfx.keys.delete_profile("MyEditKeys")
```
