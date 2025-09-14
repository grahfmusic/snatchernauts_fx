# snatchernauts_fx_plugin/core/ui_theme.rpy
default snfx_ui_alpha = 0.90
default snfx_accent_cyan = "#44e0e0"
default snfx_accent_pink = "#ff3c7f"
default snfx_bg_dark     = "#111111"
default snfx_bg_panel    = "#1a1a1a"
default snfx_text_main   = "#eeeeee"
default snfx_text_dim    = "#c8c8c8"

init -1 python:
    def snfx_scale():
        return max(0.75, min(1.25, min(config.screen_width/1920.0, config.screen_height/1080.0)))

    SNFX_FONT = "snatchernauts_fx_plugin/MapleMono-Regular.ttf"
    try: _ = renpy.file(SNFX_FONT)
    except: SNFX_FONT = "DejaVuSans.ttf"

    s = snfx_scale()
    size_small = int(round(10 * s))
    size_body  = int(round(11 * s))
    size_title = int(round(12 * s))

    panel9  = Frame("snatchernauts_fx_plugin/ui/panel.png", 12, 12)
    button9 = Frame("snatchernauts_fx_plugin/ui/button.png", 10, 10)
    bhov_cy = Frame("snatchernauts_fx_plugin/ui/button_hover_cyan.png", 10, 10)
    bhov_pk = Frame("snatchernauts_fx_plugin/ui/button_hover_pink.png", 10, 10)
    input9  = Frame("snatchernauts_fx_plugin/ui/input.png", 10, 10)
    thumb_i = Frame("snatchernauts_fx_plugin/ui/thumb.png", 4, 4)

    style.snfx_window = Style(style.default)
    style.snfx_window.background = panel9
    style.snfx_window.padding = 10
    style.snfx_window.outlines = []
    style.snfx_window.xminimum = int(config.screen_width * 0.32)
    style.snfx_window.yminimum = int(config.screen_height * 0.32)

    style.snfx_title = Style(style.default)
    style.snfx_title.font = SNFX_FONT
    style.snfx_title.size = size_title
    style.snfx_title.color = snfx_text_main

    style.snfx_label = Style(style.default)
    style.snfx_label.font = SNFX_FONT
    style.snfx_label.size = size_body
    style.snfx_label.color = snfx_text_main

    style.snfx_text = Style(style.default)
    style.snfx_text.font = SNFX_FONT
    style.snfx_text.size = size_small
    style.snfx_text.color = snfx_text_main

    style.snfx_button = Style(style.button)
    style.snfx_button.font = SNFX_FONT
    style.snfx_button.size = size_small
    style.snfx_button.color = snfx_text_main
    style.snfx_button.background = button9
    style.snfx_button.hover_background = bhov_cy
    style.snfx_button.selected_background = bhov_pk
    style.snfx_button.hover_color = "#111"
    style.snfx_button.padding = (8, 6)

    style.snfx_button_pink = Style(style.snfx_button)
    style.snfx_button_pink.hover_background = bhov_pk

    style.snfx_bar = Style(style.bar)
    style.snfx_bar.left_bar  = Solid(snfx_accent_cyan)
    style.snfx_bar.right_bar = Solid("#333")
    style.snfx_bar.thumb = thumb_i
    style.snfx_bar.thumb_offset = 0
    style.snfx_bar.xmaximum = int(260 * s)

    style.snfx_input = Style(style.input)
    style.snfx_input.font = SNFX_FONT
    style.snfx_input.size = size_small
    style.snfx_input.color = snfx_text_main
    style.snfx_input.background = input9
    style.snfx_input.hover_background = input9
    style.snfx_input.xmaximum = int(260 * s)

transform snfx_draggable:
    on show: alpha snfx_ui_alpha
    on replace: alpha snfx_ui_alpha
