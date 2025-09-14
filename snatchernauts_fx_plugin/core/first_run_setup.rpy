# snatchernauts_fx_plugin/core/first_run_setup.rpy
# First-run setup wizard v6: Look target, Autotune, Debug, Editor, Hotkey binding
# with conflict detection, visual highlights, Apply gating, Reset to defaults,
# and hotkey profiles (save/load/delete).

default persistent._snfx_setup_done = False
default persistent._snfx_key_profiles = {}
default persistent._snfx_key_profile_active = "Default"

init -2 python:
    # Styles for conflict highlighting (fallbacks if theme didn't define)
    try:
        style.snfx_input_frame
    except Exception:
        style.snfx_input_frame = Style(style.frame)
        style.snfx_input_frame.background = Frame(Solid("#1b1e24"), 8, 8)
        style.snfx_input_frame.xpadding = 6
        style.snfx_input_frame.ypadding = 2

    try:
        style.snfx_input_frame_error
    except Exception:
        style.snfx_input_frame_error = Style(style.snfx_input_frame)
        style.snfx_input_frame_error.background = Frame(Solid("#3a1b1b"), 8, 8)

init -1 python:
    import collections

    # --- Keymap scan & suggest ---
    def snfx_scan_keymap():
        used = collections.defaultdict(list)
        try:
            km = config.keymap or {}
        except Exception:
            km = {}
        for action, binds in km.items():
            try:
                for b in binds:
                    k = str(b)
                    used[k].append(str(action))
            except Exception:
                pass
        return dict(used)

    def snfx_conflicts(keys):
        """Return { key: [actions...] } for any collisions with config.keymap, excluding our own SNFX actions."""
        used = snfx_scan_keymap()
        out = {}
        for k in (keys or []):
            acts = list(used.get(str(k), []))
            acts = [a for a in acts if not a.lower().startswith("snfx")]
            if acts:
                out[str(k)] = acts
        return out

    def snfx_suggest_hotkeys():
        """Suggest a set of conflict-free defaults (best-effort)."""
        used = set(snfx_scan_keymap().keys())
        func = ["K_F4","K_F5","K_F6","K_F7","K_F8","K_F9","K_F10","K_F11","K_F12"]
        letters = ["K_q","K_w","K_e","K_r","K_t","K_y","K_u","K_i","K_o","K_p",
                   "K_a","K_s","K_d","K_f","K_g","K_h","K_j","K_k","K_l"]

        def first_free(pool, avoid=set()):
            for k in pool:
                if (k not in used) and (k not in avoid):
                    return k
            return pool[0]

        open_key = first_free(func)
        hud_key  = first_free(func, {open_key})
        prev_key = first_free(["K_a","K_LEFT"] + letters, {open_key, hud_key})
        next_key = first_free(["K_d","K_RIGHT"] + letters, {open_key, hud_key, prev_key})

        return {"open": open_key, "hud": hud_key, "prev": prev_key, "next": next_key}

    # --- Profiles storage ---
    def snfx_keys_profile_save(name, mapping, enabled=True):
        if not name: return False
        p = getattr(persistent, "_snfx_key_profiles", {}) or {}
        p[str(name)] = {"open":mapping.get("open"), "hud":mapping.get("hud"),
                        "prev":mapping.get("prev"), "next":mapping.get("next"),
                        "enabled": bool(enabled)}
        persistent._snfx_key_profiles = p
        persistent._snfx_key_profile_active = str(name)
        try: renpy.save_persistent()
        except Exception: pass
        return True

    def snfx_keys_profile_load(name):
        p = getattr(persistent, "_snfx_key_profiles", {}) or {}
        m = p.get(str(name))
        if not m: return False
        try:
            snfx.keys.bind(open_editor=m.get("open","K_F10"),
                           toggle_hud=m.get("hud","K_F9"),
                           prev=m.get("prev","K_LEFT"),
                           next=m.get("next","K_RIGHT"))
            snfx.keys.enable(bool(m.get("enabled", True)))
            persistent._snfx_key_profile_active = str(name)
            try: renpy.save_persistent()
            except Exception: pass
            return True
        except Exception:
            return False

    def snfx_keys_profile_delete(name):
        p = getattr(persistent, "_snfx_key_profiles", {}) or {}
        if str(name) in p:
            del p[str(name)]
            persistent._snfx_key_profiles = p
            try: renpy.save_persistent()
            except Exception: pass
            return True
        return False

    def snfx_keys_profiles():
        p = getattr(persistent, "_snfx_key_profiles", {}) or {}
        return sorted(p.keys())

    def snfx_keys_reset_defaults():
        snfx.keys.bind(open_editor="K_F10", toggle_hud="K_F9", prev="K_LEFT", next="K_RIGHT")
        snfx.keys.enable(True)
        return {"open":"K_F10","hud":"K_F9","prev":"K_LEFT","next":"K_RIGHT"}

    # Expose helpers on snfx.keys
    try:
        if not hasattr(snfx, "keys"): pass
    except Exception:
        pass
    else:
        try:
            if not hasattr(snfx.keys, "conflicts"):
                snfx.keys.conflicts = lambda seq: snfx_conflicts(seq)
            if not hasattr(snfx.keys, "suggest"):
                snfx.keys.suggest = lambda: snfx_suggest_hotkeys()
            if not hasattr(snfx.keys, "save_profile"):
                snfx.keys.save_profile = lambda name, mapping=None, enabled=True: snfx_keys_profile_save(name, mapping or getattr(store, "snfx_keymap", {}), enabled)
            if not hasattr(snfx.keys, "load_profile"):
                snfx.keys.load_profile = snfx_keys_profile_load
            if not hasattr(snfx.keys, "delete_profile"):
                snfx.keys.delete_profile = snfx_keys_profile_delete
            if not hasattr(snfx.keys, "list_profiles"):
                snfx.keys.list_profiles = snfx_keys_profiles
            if not hasattr(snfx.keys, "reset_defaults"):
                snfx.keys.reset_defaults = snfx_keys_reset_defaults
        except Exception:
            pass

screen snfx_first_run_trigger():
    if main_menu and not persistent._snfx_setup_done:
        timer 0.20 action Show("snfx_first_run_wizard")

screen snfx_first_run_wizard():
    modal True
    zorder 2000
    default look = getattr(store, "snfx_preset_look", "cinematic")
    default enable_debug = snfx_debug_enabled
    default open_editor_after = True
    default dont_show_again = True
    default enable_hotkeys = True

    # initialize hotkey fields from current map when screen constructs
    default hk_open = (snfx_keymap["open_editor"] if "snfx_keymap" in store else "K_F10")
    default hk_hud  = (snfx_keymap["toggle_hud"]  if "snfx_keymap" in store else "K_F9")
    default hk_prev = (snfx_keymap["prev"]        if "snfx_keymap" in store else "K_LEFT")
    default hk_next = (snfx_keymap["next"]        if "snfx_keymap" in store else "K_RIGHT")

    # Profiles UI state
    default profile_name = persistent._snfx_key_profile_active or "Default"
    default new_profile_name = ""

    # live conflict check
    $ conflicts = snfx_conflicts([hk_open, hk_hud, hk_prev, hk_next])
    $ open_conf = conflicts.get(hk_open, [])
    $ hud_conf  = conflicts.get(hk_hud,  [])
    $ prev_conf = conflicts.get(hk_prev, [])
    $ next_conf = conflicts.get(hk_next, [])
    $ has_conflict = bool(open_conf or hud_conf or prev_conf or next_conf)

    python:
        # Quick-pick pools
        _snfx_quick_func_keys = ["K_F4","K_F5","K_F6","K_F7","K_F8","K_F9","K_F10","K_F11","K_F12"]
        _snfx_quick_letters   = ["K_q","K_w","K_e","K_r","K_t","K_y","K_u","K_i","K_o","K_p",
                                 "K_a","K_s","K_d","K_f","K_g","K_h","K_j","K_k","K_l"]
        _snfx_suggestion = snfx_suggest_hotkeys()
        _snfx_profiles = snfx_keys_profiles()

    drag:
        draggable True
        drag_handle (0.0, 0.0)
        frame style "snfx_window":
            background Frame(Solid(snfx_bg_dark), 10, 10)
            has vbox
            hbox:
                spacing 12
                text "SNATCHERNAUTS FX — First Run Setup" style "snfx_title"
                null width 20
                text ("Detected Resolution: %dx%d" % (config.screen_width, config.screen_height)) style "snfx_text" color snfx_text_dim
                null width 10
                textbutton "Skip" style "snfx_button" action [SetField(persistent, "_snfx_setup_done", True), Hide("snfx_first_run_wizard")]
            null height 10

            hbox:
                spacing 18

                vbox:
                    spacing 8
                    text "Choose a Look Target" style "snfx_label"
                    text "These presets will be auto-tuned to your current resolution." style "snfx_text" color snfx_text_dim
                    null height 6
                    $ looks = [("cinematic","Cinematic (scope, filmic)"),
                               ("broadcast","Broadcast (neutral 16:9)"),
                               ("retro","Retro (4:3, scanlines)"),
                               ("neon","Neon (21:9, stylized)"),
                               ("neutral","Neutral (clean)")]
                    for key,label in looks:
                        textbutton label style "snfx_button" action SetScreenVariable("look", key) selected (look==key)

                    null height 12
                    text "Options" style "snfx_label"
                    hbox:
                        text "Enable debug log" style "snfx_text"
                        togglebutton value VariableValue("enable_debug", True) style "snfx_button"
                    hbox:
                        text "Open editor after finish" style "snfx_text"
                        togglebutton value VariableValue("open_editor_after", True) style "snfx_button"
                    hbox:
                        text "Don't show again" style "snfx_text"
                        togglebutton value VariableValue("dont_show_again", True) style "snfx_button"

                null width 24

                vbox:
                    spacing 8
                    text "Hotkeys" style "snfx_label"
                    text "Set keys now; conflicting fields are highlighted. You can save them as a profile." style "snfx_text" color snfx_text_dim

                    grid 3 4:
                        transpose True
                        spacing 6
                        text "Enable Hotkeys" style "snfx_text"; togglebutton value VariableValue("enable_hotkeys", True) style "snfx_button"; null

                        text "Open Editor" style "snfx_text"
                        frame style ( "snfx_input_frame_error" if open_conf else "snfx_input_frame" ):
                            input style "snfx_input" value VariableInputValue("hk_open") length 16
                        if open_conf:
                            text ("⚠ Used by: " + ", ".join(open_conf)) style "snfx_text" color "#ff6b6b"
                        else:
                            text "✓ No conflict" style "snfx_text" color "#7cd992"

                        text "Toggle HUD" style "snfx_text"
                        frame style ( "snfx_input_frame_error" if hud_conf else "snfx_input_frame" ):
                            input style "snfx_input" value VariableInputValue("hk_hud") length 16
                        if hud_conf:
                            text ("⚠ Used by: " + ", ".join(hud_conf)) style "snfx_text" color "#ff6b6b"
                        else:
                            text "✓ No conflict" style "snfx_text" color "#7cd992"

                        text "Prev Preset" style "snfx_text"
                        frame style ( "snfx_input_frame_error" if prev_conf else "snfx_input_frame" ):
                            input style "snfx_input" value VariableInputValue("hk_prev") length 16
                        if prev_conf:
                            text ("⚠ Used by: " + ", ".join(prev_conf)) style "snfx_text" color "#ff6b6b"
                        else:
                            text "✓ No conflict" style "snfx_text" color "#7cd992"

                        text "Next Preset" style "snfx_text"
                        frame style ( "snfx_input_frame_error" if next_conf else "snfx_input_frame" ):
                            input style "snfx_input" value VariableInputValue("hk_next") length 16
                        if next_conf:
                            text ("⚠ Used by: " + ", ".join(next_conf)) style "snfx_text" color "#ff6b6b"
                        else:
                            text "✓ No conflict" style "snfx_text" color "#7cd992"

                    null height 6
                    hbox:
                        spacing 10
                        text "Quick Picks:" style "snfx_text" color snfx_text_dim
                        for k in _snfx_quick_func_keys:
                            textbutton k[2:] style "snfx_button" action [
                                SetScreenVariable("hk_open", k if hk_open!=k else hk_open),
                                SetScreenVariable("hk_hud",  "K_F7" if k=="K_F6" else "K_F6")
                            ]
                        null width 10
                        for k in _snfx_quick_letters[:6]:
                            textbutton k[2:].upper() style "snfx_button" action [
                                SetScreenVariable("hk_prev", k if hk_prev!=k else hk_prev),
                                SetScreenVariable("hk_next", "K_d" if k!="K_d" else "K_f")
                            ]

                    null height 8
                    hbox:
                        spacing 10
                        text "Auto-fix:" style "snfx_text" color snfx_text_dim
                        textbutton "Suggest Non-Conflicting Keys" style "snfx_button_cyan" action [
                            SetScreenVariable("hk_open", _snfx_suggestion["open"]),
                            SetScreenVariable("hk_hud",  _snfx_suggestion["hud"]),
                            SetScreenVariable("hk_prev", _snfx_suggestion["prev"]),
                            SetScreenVariable("hk_next", _snfx_suggestion["next"])
                        ]
                        textbutton "Reset to Defaults" style "snfx_button" action [
                            SetScreenVariable("hk_open", "K_F10"),
                            SetScreenVariable("hk_hud",  "K_F9"),
                            SetScreenVariable("hk_prev", "K_LEFT"),
                            SetScreenVariable("hk_next", "K_RIGHT"),
                            SetScreenVariable("enable_hotkeys", True)
                        ]

                    null height 10
                    text "Profiles" style "snfx_label"
                    hbox:
                        spacing 8
                        text "Active:" style "snfx_text"
                        if _snfx_profiles:
                            viewport:
                                xmaximum 180
                                mousewheel True
                                has vbox
                                for n in _snfx_profiles:
                                    textbutton n style "snfx_button" action [ SetScreenVariable("profile_name", n) ] selected (profile_name==n)
                        else:
                            text "No profiles saved yet." style "snfx_text" color snfx_text_dim

                        null width 18
                        vbox:
                            spacing 6
                            hbox:
                                spacing 6
                                text "Save As:" style "snfx_text"
                                input style "snfx_input" value VariableInputValue("new_profile_name") length 24
                                textbutton "Save" style "snfx_button_cyan" action [
                                    Function(snfx_keys_profile_save, (new_profile_name or "Profile"), {"open":hk_open,"hud":hk_hud,"prev":hk_prev,"next":hk_next}, enable_hotkeys),
                                    SetScreenVariable("profile_name", (new_profile_name or "Profile")),
                                    SetScreenVariable("new_profile_name", ""),
                                    Function(renpy.notify, "SN FX: Profile saved")
                                ]
                            hbox:
                                spacing 6
                                textbutton "Load Selected" style "snfx_button" sensitive (_snfx_profiles and profile_name in _snfx_profiles) action [
                                    Function(snfx_keys_profile_load, profile_name),
                                    SetScreenVariable("hk_open", persistent._snfx_key_profiles.get(profile_name,{}).get("open", hk_open)),
                                    SetScreenVariable("hk_hud",  persistent._snfx_key_profiles.get(profile_name,{}).get("hud", hk_hud)),
                                    SetScreenVariable("hk_prev", persistent._snfx_key_profiles.get(profile_name,{}).get("prev", hk_prev)),
                                    SetScreenVariable("hk_next", persistent._snfx_key_profiles.get(profile_name,{}).get("next", hk_next)),
                                    Function(renpy.notify, "SN FX: Profile loaded")
                                ]
                                textbutton "Delete Selected" style "snfx_button_pink" sensitive (_snfx_profiles and profile_name in _snfx_profiles) action [
                                    Function(snfx_keys_profile_delete, profile_name),
                                    SetScreenVariable("profile_name", "Default"),
                                    Function(renpy.notify, "SN FX: Profile deleted")
                                ]

                    null height 14
                    text "Summary" style "snfx_label"
                    text ("Look: %s" % look.title()) style "snfx_text"
                    text ("Autotune → %dx%d" % (config.screen_width, config.screen_height)) style "snfx_text"
                    text ("Debug: %s" % ("On" if enable_debug else "Off")) style "snfx_text"
                    text ("Hotkeys: %s / %s / %s / %s" % (hk_open, hk_hud, hk_prev, hk_next)) style "snfx_text"
                    if has_conflict:
                        text "Resolve hotkey conflicts to enable Apply." style "snfx_text" color "#ffb4b4"

                    null height 18
                    textbutton "Apply & Continue" style "snfx_button_pink" sensitive (not has_conflict) action [
                        Function(snfx.presets.set_look, look),
                        Function(snfx.presets.autotune),
                        Function(snfx.debug, enable_debug),
                        Function(snfx.keys.enable, enable_hotkeys),
                        Function(snfx.keys.bind, open_editor=hk_open, toggle_hud=hk_hud, prev=hk_prev, next=hk_next),
                        Function(snfx_keys_profile_save, profile_name or "Default", {"open":hk_open,"hud":hk_hud,"prev":hk_prev,"next":hk_next}, enable_hotkeys),
                        SetField(persistent, "_snfx_key_profile_active", profile_name or "Default"),
                        If(dont_show_again, true=SetField(persistent, "_snfx_setup_done", True)),
                        Hide("snfx_first_run_wizard"),
                        If(open_editor_after, true=Function(snfx.open_editor)),
                        Function(renpy.notify, "SN FX setup complete"),
                        Function(renpy.log, ":: [ SN FX ] - Setup: look=%s, debug=%s, profile=%s, keys=%s" % (look, ("On" if enable_debug else "Off"), (profile_name or "Default"), {"open":hk_open,"hud":hk_hud,"prev":hk_prev,"next":hk_next}))
                    ]
