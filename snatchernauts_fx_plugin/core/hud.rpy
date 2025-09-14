# snatchernauts_fx_plugin/core/hud.rpy
screen snfx_hud():
    zorder 999
    frame style "snfx_window" at snfx_draggable:
        background Frame(Solid("#000a"), 10, 10)
        vbox:
            text "SNFX HUD" style "snfx_title"
            text ("Tab: " + snfx_state.active_tab) style "snfx_text" color snfx_accent_cyan
            text ("Res: %dx%d" % (config.screen_width, config.screen_height)) style "snfx_text" color snfx_text_dim

label snfx_cycle_presets(step=1):
    $ snfx.cycle_active_tab(step)
    return
