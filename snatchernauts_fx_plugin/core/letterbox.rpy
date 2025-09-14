# snatchernauts_fx_plugin/core/letterbox.rpy
init python:
    renpy.register_property("lb_ratio", "u_ratio")
    renpy.register_property("lb_mix",   "u_mix")

    renpy.register_shader(
        "snfx.letterbox",
        variables = """
            uniform float u_ratio;
            uniform float u_mix;
            attribute vec2 a_position;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex = """
            v_tex_coord = a_tex_coord;
            gl_Position = vec4(a_position, 0.0, 1.0);
        """,
        fragment = """
            float halfbar = clamp(u_ratio * 0.5, 0.0, 0.5);
            float top    = step(v_tex_coord.y, halfbar);
            float bottom = step(1.0 - v_tex_coord.y, halfbar);
            float a = clamp((top + bottom) * u_mix, 0.0, 1.0);
            gl_FragColor = vec4(0.0, 0.0, 0.0, a);
        """
    )

transform snfx_letterbox_t():
    shader "snfx.letterbox"
    lb_ratio snfx_state.letterbox_ratio
    lb_mix   snfx_state.letterbox_mix

screen snfx_letterbox_screen():
    zorder 90
    if snfx_state.enable_letterbox and snfx_state.letterbox_ratio > 0.0:
        add Solid("#0000") at snfx_letterbox_t
