# snatchernauts_fx_plugin/core/hotkeys.rpy
default snfx_hotkeys_enabled = True
default snfx_keymap = {
    "open_editor": "K_F10",
    "toggle_hud":  "K_F9",
    "prev":        "K_LEFT",
    "next":        "K_RIGHT",
}

screen snfx_hotkey_router():
    if snfx_hotkeys_enabled:
        key snfx_keymap["open_editor"] action Function(renpy.call_in_new_context, "snfx_open_editor_key")
        key snfx_keymap["toggle_hud"]  action If(renpy.get_screen("snfx_hud"), true=Hide("snfx_hud"), false=Show("snfx_hud"))
        key snfx_keymap["prev"]        action Function(renpy.call_in_new_context, "snfx_cycle_presets", -1)
        key snfx_keymap["next"]        action Function(renpy.call_in_new_context, "snfx_cycle_presets", +1)

label snfx_open_editor_key:
    $ snfx.open_editor()
    return

init python:
    if "snfx_hotkey_router" not in config.overlay_screens:
        config.overlay_screens.append("snfx_hotkey_router")
