# snatchernauts_fx_plugin/core/editor.rpy
screen snfx_editor():
    modal True
    zorder 1000
    on "show" action Function(snfx_runtime_pause, True)
    on "hide" action Function(snfx_runtime_pause, False)
    default tab = snfx_state.active_tab
    drag:
        draggable True
        drag_handle (0.0, 0.0)
        frame style "snfx_window" at snfx_draggable:
            background Frame(Solid(snfx_bg_dark), 10, 10)
            has vbox
            hbox:
                spacing 12
                text "SNATCHERNAUTS FX — Editor" style "snfx_title"
                null width 12
                text ("Res: %dx%d" % (config.screen_width, config.screen_height)) style "snfx_text" color snfx_text_dim
                null width 12
                text "UI Transparency" style "snfx_label"
                bar style "snfx_bar" value VariableValue("snfx_ui_alpha", 0.5, 1.0)
                null width 12
                textbutton "Close" style "snfx_button_pink" action Hide("snfx_editor")
            null height 8
            hbox:
                spacing 10
                vbox:
                    spacing 6
                    textbutton "About / Help" style "snfx_button" action [SetScreenVariable("tab","About"), SetField(snfx_state,"active_tab","About")]
                    textbutton "Letterbox"    style "snfx_button" action [SetScreenVariable("tab","Letterbox"), SetField(snfx_state,"active_tab","Letterbox")]
                    textbutton "CRT"          style "snfx_button" action [SetScreenVariable("tab","CRT"), SetField(snfx_state,"active_tab","CRT")]
                    textbutton "Film Grain"   style "snfx_button" action [SetScreenVariable("tab","Grain"), SetField(snfx_state,"active_tab","Grain")]
                    textbutton "Color Grade"  style "snfx_button" action [SetScreenVariable("tab","Grade"), SetField(snfx_state,"active_tab","Grade")]
                    textbutton "Lighting (2D)"style "snfx_button" action [SetScreenVariable("tab","Lighting"), SetField(snfx_state,"active_tab","Lighting")]
                    textbutton "Bloom"        style "snfx_button" action [SetScreenVariable("tab","Bloom"), SetField(snfx_state,"active_tab","Bloom")]
                frame style "snfx_window" at snfx_draggable:
                    background Frame(Solid(snfx_bg_panel), 10, 10)
                    xmaximum int(config.screen_width * 0.55)
                    ymaximum int(config.screen_height * 0.65)
                    if tab == "About":      use snfx_about()
                    if tab == "Letterbox":  use snfx_ui_letterbox()
                    if tab == "CRT":        use snfx_ui_crt()
                    if tab == "Grain":      use snfx_ui_grain()
                    if tab == "Grade":      use snfx_ui_grade()
                    if tab == "Lighting":   use snfx_ui_lighting()
                    if tab == "Bloom":      use snfx_ui_bloom()

screen snfx_preset_picker(category, apply_fn):
    hbox:
        spacing 20
        vbox:
            label "Included" style "snfx_label"
            viewport:
                draggable True mousewheel True scrollbars "vertical" ymaximum int(config.screen_height * 0.35)
                vbox:
                    $ inc = snfx_list_included(category)
                    for p in inc:
                        $ d = snfx_load_json(p)
                        if d:
                            textbutton (d.get("name") or renpy.basename(p)) style "snfx_button" action Function(apply_fn, d)
        vbox:
            label "Custom" style "snfx_label"
            viewport:
                draggable True mousewheel True scrollbars "vertical" ymaximum int(config.screen_height * 0.35)
                vbox:
                    $ cus = snfx_list_custom(category)
                    for p in cus:
                        $ d = snfx_load_json(p)
                        if d:
                            textbutton (d.get("name") or renpy.basename(p)) style "snfx_button" action Function(apply_fn, d)

screen snfx_about():
    viewport:
        draggable True mousewheel True scrollbars "vertical"
        vbox:
            spacing 6
            text "About" style "snfx_title"
            text "Post-FX stack: Letterbox, CRT, Film Grain, Bloom, Color Grade. 2D Lighting with ambient/point/spot/rect." style "snfx_text"
            text "Order: UI → Letterbox/Grain overlays → MASTER (CRT → Bloom → Grade) → World → Lights. UI not graded." style "snfx_text"
            text "Presets live in: snatchernauts_fx_plugin/presets/(included|custom)/<category>/*.json" style "snfx_text"
            text "Hotkeys:  F10 Editor   F9 HUD   ←/→ cycle presets in active tab" style "snfx_label" color snfx_accent_cyan

screen snfx_ui_letterbox():
    default save_name = ""
    vbox:
        spacing 8
        text "Letterbox Presets" style "snfx_title"
        use snfx_preset_picker("letterbox", snfx_apply_letterbox_json)
        null height 4
        hbox:
            spacing 10
            text "Enabled" style "snfx_label"
            togglebutton value VariableValue("snfx_state.enable_letterbox", True) style "snfx_button"
        text "Ease In/Out Speed" style "snfx_label"
        hbox:
            spacing 6
            textbutton "Very Slow" style "snfx_button" action Function(snfx_state.set_letterbox_speed, 1.5)
            textbutton "Slow"      style "snfx_button" action Function(snfx_state.set_letterbox_speed, 3.0)
            textbutton "Normal"    style "snfx_button" action Function(snfx_state.set_letterbox_speed, 6.0)
            textbutton "Fast"      style "snfx_button" action Function(snfx_state.set_letterbox_speed, 10.0)
            textbutton "Very Fast" style "snfx_button" action Function(snfx_state.set_letterbox_speed, 20.0)
        bar style "snfx_bar" value FieldValue(snfx_state, "._lb_speed", 0.0, 20.0)
        hbox:
            spacing 10
            textbutton "Show (preview)" style "snfx_button" action Function(snfx_state.animate_letterbox, True)
            textbutton "Hide (preview)" style "snfx_button" action Function(snfx_state.animate_letterbox, False)
        null height 8
        text "Save Custom" style "snfx_label" color snfx_accent_pink
        input style "snfx_input" value VariableInputValue("save_name") length 32
        $ _lb = {"name":save_name or "MyLetterbox", "resolution":[config.screen_width,config.screen_height],
                 "enable":snfx_state.enable_letterbox, "aspect":"16:9", "speed":"normal",
                 "speed_custom":snfx_state._lb_speed, "mix":1.0}
        textbutton "Save" style "snfx_button_pink" action Function(snfx_save_json, "letterbox", save_name or "MyLetterbox", _lb)

screen snfx_ui_crt():
    default save_name = ""
    vbox:
        spacing 8
        text "CRT Presets" style "snfx_title"
        use snfx_preset_picker("crt", snfx_apply_crt_json)
        null height 6
        grid 2 6:
            transpose True
            spacing 6
            text "Enabled" style "snfx_label"; togglebutton value VariableValue("snfx_state.enable_crt", True) style "snfx_button"
            text "Intensity" style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".crt_intensity", 0.0, 1.0)
            text "Vignette"  style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".crt_vignette", 0.0, 1.0)
            text "Aberration"style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".crt_aberration", 0.0, 0.01)
            text "Scan Strength" style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".crt_scan_strength", 0.0, 1.0)
            text "Scan Density"  style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".crt_scan_density", 0.5, 3.0)
            text "Glitch"   style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".crt_glitch", 0.0, 1.0)
            text "Anim Speed" style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".crt_anim_speed", 0.1, 3.0)
        hbox:
            spacing 6
            text "Anim Type" style "snfx_label"
            textbutton "None" style "snfx_button" action SetField(snfx_state, "crt_anim_type", 0)
            textbutton "Sine" style "snfx_button" action SetField(snfx_state, "crt_anim_type", 1)
            textbutton "Tri"  style "snfx_button" action SetField(snfx_state, "crt_anim_type", 2)
            textbutton "Roll" style "snfx_button" action SetField(snfx_state, "crt_anim_type", 3)
        text "Barrel Warp" style "snfx_label"
        bar style "snfx_bar" value FieldValue(snfx_state, ".crt_barrel", 0.0, 0.02)
        null height 8
        text "Save Custom" style "snfx_label" color snfx_accent_pink
        input style "snfx_input" value VariableInputValue("save_name") length 40
        $ _crt = {"name":save_name or "MyCRT","resolution":[config.screen_width,config.screen_height],
                  "enable":snfx_state.enable_crt,"intensity":snfx_state.crt_intensity,"vignette":snfx_state.crt_vignette,
                  "aberration":snfx_state.crt_aberration,"scanline_strength":snfx_state.crt_scan_strength,
                  "scanline_density":snfx_state.crt_scan_density,"glitch":snfx_state.crt_glitch,
                  "anim_type":{0:"none",1:"sine",2:"tri",3:"rolling"}[snfx_state.crt_anim_type],
                  "anim_speed":snfx_state.crt_anim_speed,"barrel":snfx_state.crt_barrel}
        textbutton "Save" style "snfx_button_pink" action Function(snfx_save_json, "crt", save_name or "MyCRT", _crt)

screen snfx_ui_grain():
    default save_name = ""
    vbox:
        spacing 8
        text "Film Grain Presets" style "snfx_title"
        use snfx_preset_picker("grain", snfx_apply_grain_json)
        null height 6
        grid 2 4:
            transpose True
            spacing 6
            text "Enabled"  style "snfx_label"; togglebutton value VariableValue("snfx_state.enable_grain", True) style "snfx_button"
            text "Intensity"style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".grain_intensity", 0.0, 1.0)
            text "Size"     style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".grain_size", 0.5, 2.5)
            text "Speed"    style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".grain_speed", 0.2, 3.0)
            text "Downsample" style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".grain_downsample", 1.0, 3.0)
        null height 8
        text "Save Custom" style "snfx_label" color snfx_accent_pink
        input style "snfx_input" value VariableInputValue("save_name") length 40
        $ _g = {"name":save_name or "MyGrain","resolution":[config.screen_width,config.screen_height],
                "enable":snfx_state.enable_grain,"intensity":snfx_state.grain_intensity,"size":snfx_state.grain_size,
                "speed":snfx_state.grain_speed,"downsample":snfx_state.grain_downsample}
        textbutton "Save" style "snfx_button_pink" action Function(snfx_save_json, "grain", save_name or "MyGrain", _g)

screen snfx_ui_grade():
    default save_name = ""
    default gd_sat = 1.0
    default gd_con = 1.0
    default gd_bri = 0.0
    default gd_hue = 0.0
    default gd_tr  = 1.0
    default gd_tg  = 1.0
    default gd_tb  = 1.0
    vbox:
        spacing 8
        text "Color Grade Presets" style "snfx_title"
        use snfx_preset_picker("grade", snfx_apply_grade_json)
        null height 6
        hbox: spacing 10
        text "Enabled" style "snfx_label"
        togglebutton value VariableValue("snfx_state.enable_grade", True) style "snfx_button"
        grid 2 7:
            transpose True
            spacing 6
            text "Saturation" style "snfx_label"; bar style "snfx_bar" value VariableValue("gd_sat", 1.0)
            text "Contrast"   style "snfx_label"; bar style "snfx_bar" value VariableValue("gd_con", 1.0)
            text "Brightness" style "snfx_label"; bar style "snfx_bar" value VariableValue("gd_bri", 0.0)
            text "Hue"        style "snfx_label"; bar style "snfx_bar" value VariableValue("gd_hue", 0.0)
            text "Tint R"     style "snfx_label"; bar style "snfx_bar" value VariableValue("gd_tr",  1.0)
            text "Tint G"     style "snfx_label"; bar style "snfx_bar" value VariableValue("gd_tg",  1.0)
            text "Tint B"     style "snfx_label"; bar style "snfx_bar" value VariableValue("gd_tb",  1.0)
        hbox:
            textbutton "Apply To Scene" style "snfx_button" action SetField(snfx_state, "grade_matrix",
                SNFX_ops_to_matrix([{"op":"saturation","value":gd_sat},
                                    {"op":"contrast","value":gd_con},
                                    {"op":"brightness","value":gd_bri},
                                    {"op":"hue","value":gd_hue},
                                    {"op":"tint","r":gd_tr,"g":gd_tg,"b":gd_tb}]))
        null height 8
        text "Save Custom" style "snfx_label" color snfx_accent_pink
        input style "snfx_input" value VariableInputValue("save_name") length 40
        $ _ops=[{"op":"saturation","value":gd_sat},{"op":"contrast","value":gd_con},
                {"op":"brightness","value":gd_bri},{"op":"hue","value":gd_hue},
                {"op":"tint","r":gd_tr,"g":gd_tg,"b":gd_tb}]
        textbutton "Save" style "snfx_button_pink" action Function(snfx_save_json, "grade", save_name or "MyGrade",
            {"name":save_name or "MyGrade","enable":True,"ops":_ops})

screen snfx_ui_lighting():
    default save_name = ""
    vbox:
        spacing 8
        text "Lighting Presets" style "snfx_title"
        use snfx_preset_picker("lighting", snfx_apply_lighting_json)
        null height 6
        hbox:
            spacing 10
            text "Enabled" style "snfx_label"
            togglebutton value VariableValue("snfx_lights.enabled", True) style "snfx_button"
            text "Ambient (RGBAi)" style "snfx_label" color snfx_text_dim
        hbox:
            spacing 6
            text "R" style "snfx_text"; bar style "snfx_bar" value VariableValue("ambient_r", snfx_lights.ambient[0] if snfx_lights.ambient else 0.0)
            text "G" style "snfx_text"; bar style "snfx_bar" value VariableValue("ambient_g", snfx_lights.ambient[1] if snfx_lights.ambient else 0.0)
            text "B" style "snfx_text"; bar style "snfx_bar" value VariableValue("ambient_b", snfx_lights.ambient[2] if snfx_lights.ambient else 0.0)
            text "I" style "snfx_text"; bar style "snfx_bar" value VariableValue("ambient_i", snfx_lights.ambient[3] if snfx_lights.ambient else 0.0)
            textbutton "Apply" style "snfx_button" action Function(snfx_lights.set_ambient, ambient_r,ambient_g,ambient_b,ambient_i)
        hbox:
            spacing 6
            textbutton "Add Point" style "snfx_button" action Function(snfx_lights.add_point, 0.5,0.5, intensity=1.0, radius=0.3, falloff=1.0, color=[1.0,0.95,0.8], front=False)
            textbutton "Add Spot"  style "snfx_button" action Function(snfx_lights.add_spot, 0.5,0.8, dir=(0,-1), angle=35, intensity=1.0, radius=0.6, falloff=1.0, color=[0.8,0.9,1.0], front=False)
            textbutton "Add Rect"  style "snfx_button" action Function(snfx_lights.add_rect, 0.5,0.6, 0.3,0.15, intensity=0.8, falloff=1.0, color=[1.0,0.8,0.6], front=False)
            textbutton "Clear"     style "snfx_button_pink" action Function(snfx_lights.clear)
        null height 6
        frame style "snfx_window":
            background Frame(Solid("#0a0a0a"), 10, 10)
            xmaximum int(config.screen_width * 0.52)
            ymaximum int(config.screen_height * 0.35)
            has fixed
            for L in snfx_lights.lights:
                drag:
                    draggable True
                    xpos L.pos[0] * config.screen_width
                    ypos L.pos[1] * config.screen_height
                    drag_handle (0.5,0.5)
                    xanchor 0.5 yanchor 0.5
                    child Frame(Solid(snfx_accent_cyan), 6, 6)
                    dragged SetField(L, "pos", [ max(0.0, min(1.0, _drag_pos[0]/config.screen_width)),
                                                 max(0.0, min(1.0, _drag_pos[1]/config.screen_height)) ])
            text "Drag dots to move lights" style "snfx_text" color snfx_text_dim xpos 8 ypos 8
        null height 8
        text "Save Custom" style "snfx_label" color snfx_accent_pink
        input style "snfx_input" value VariableInputValue("save_name") length 40
        $ _lights_json = {"name":save_name or "MyLights","resolution":[config.screen_width,config.screen_height],
                          "ambient":snfx_lights.ambient,
                          "lights":[
                              {"type":L.type,"pos":L.pos,"color":L.color,"intensity":L.intensity,"radius":L.radius,"falloff":L.falloff,
                               "front":L.front,"dir":L.dir,"angle":L.angle,"size":L.size,"anim":L.anim}
                              for L in snfx_lights.lights
                          ]}
        textbutton "Save" style "snfx_button_pink" action Function(snfx_save_json, "lighting", save_name or "MyLights", _lights_json)

screen snfx_ui_bloom():
    default save_name = ""
    vbox:
        spacing 8
        text "Bloom Presets" style "snfx_title"
        use snfx_preset_picker("bloom", snfx_apply_bloom_json)
        null height 6
        grid 2 7:
            transpose True
            spacing 6
            text "Enabled"   style "snfx_label"; togglebutton value VariableValue("snfx_state.enable_bloom", True) style "snfx_button"
            text "Threshold" style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".bloom_threshold", 0.0, 1.0)
            text "Soft Knee" style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".bloom_knee", 0.0, 1.0)
            text "Intensity" style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".bloom_intensity", 0.0, 2.0)
            text "Radius"    style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".bloom_radius", 0.5, 3.0)
            text "Anamorphic"style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".bloom_anam", 0.0, 0.6)
            text "Anim Speed"style "snfx_label"; bar style "snfx_bar" value FieldValue(snfx_state, ".bloom_anim_speed", 0.1, 3.0)
        hbox:
            spacing 6
            text "Anim Type" style "snfx_label"
            textbutton "None"   style "snfx_button" action SetField(snfx_state, "bloom_anim_type", 0)
            textbutton "Pulse"  style "snfx_button" action SetField(snfx_state, "bloom_anim_type", 1)
            textbutton "Breathe"style "snfx_button" action SetField(snfx_state, "bloom_anim_type", 2)
        text "Anim Amount" style "snfx_label"
        bar style "snfx_bar" value FieldValue(snfx_state, ".bloom_anim_amt", 0.0, 0.5)
        null height 8
        text "Save Custom" style "snfx_label" color snfx_accent_pink
        input style "snfx_input" value VariableInputValue("save_name") length 40
        $ _b = {"name":save_name or "MyBloom","resolution":[config.screen_width,config.screen_height],
                "enable":snfx_state.enable_bloom,"threshold":snfx_state.bloom_threshold,
                "soft_knee":snfx_state.bloom_knee,"intensity":snfx_state.bloom_intensity,
                "radius":snfx_state.bloom_radius,"samples":snfx_state.bloom_samples,
                "anamorphic":snfx_state.bloom_anam,
                "anim":{"type":{0:"none",1:"pulse",2:"breath"}[snfx_state.bloom_anim_type],
                        "speed":snfx_state.bloom_anim_speed,"amount":snfx_state.bloom_anim_amt}}
        textbutton "Save" style "snfx_button_pink" action Function(snfx_save_json, "bloom", save_name or "MyBloom", _b)
