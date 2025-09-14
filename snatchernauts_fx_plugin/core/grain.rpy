# snatchernauts_fx_plugin/core/grain.rpy
init python:
    for _p in ("u_time","u_gint","u_gsize","u_gspeed","u_down"):
        renpy.register_property(_p[2:], _p)

    renpy.register_shader(
        "snfx.grain",
        variables = """
            uniform float u_time, u_gint, u_gsize, u_gspeed, u_down;
            attribute vec2 a_position;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex = """
            v_tex_coord = a_tex_coord;
            gl_Position = vec4(a_position, 0.0, 1.0);
        """,
        fragment = """
            vec2 uv = floor(v_tex_coord * max(1.0, u_down)) / max(1.0, u_down);
            float t = u_time * u_gspeed;
            float n = fract(sin(dot(uv * (300.0 / max(0.0001, u_gsize)) + t, vec2(12.9898,78.233))) * 43758.5453);
            float g = n * 0.6 + 0.2;
            gl_FragColor = vec4(vec3(g), clamp(u_gint, 0.0, 1.0));
        """
    )

transform snfx_grain_t():
    shader "snfx.grain"
    time   time
    gint   snfx_state.grain_intensity
    gsize  snfx_state.grain_size
    gspeed snfx_state.grain_speed
    down   snfx_state.grain_downsample

screen snfx_grain_screen():
    zorder 60
    if snfx_state.enable_grain and snfx_state.grain_intensity > 0.0:
        add Solid("#0000") at snfx_grain_t
