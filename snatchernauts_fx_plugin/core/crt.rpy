# snatchernauts_fx_plugin/core/crt.rpy
init python:
    for _p in ("u_time","u_res","u_inten","u_vign","u_ab","u_scan_den","u_scan_str","u_glitch","u_anim","u_speed","u_barrel"):
        renpy.register_property(_p[2:], _p)

    renpy.register_shader(
        "snfx.crt_master",
        variables = """
            uniform sampler2D tex0;
            uniform vec2  u_res;
            uniform float u_time;
            uniform float u_inten;
            uniform float u_vign;
            uniform float u_ab;
            uniform float u_scan_den;
            uniform float u_scan_str;
            uniform float u_glitch;
            uniform float u_anim;
            uniform float u_speed;
            uniform float u_barrel;
            attribute vec2 a_position;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex = """
            v_tex_coord = a_tex_coord;
            gl_Position = vec4(a_position, 0.0, 1.0);
        """,
        fragment = """
            vec2 uv = v_tex_coord;

            if (u_barrel > 0.0001) {
                vec2 c = uv - 0.5;
                float r2 = dot(c,c);
                uv = 0.5 + c * (1.0 + u_barrel * r2);
            }

            float t = u_time * u_speed;
            float line = floor(uv.y * u_res.y);
            float rnd  = fract(sin(line * 12.9898 + t * 78.233) * 43758.5453);
            float jitter = (u_glitch > 0.0) ? ((rnd - 0.5) * 0.006 * u_glitch) : 0.0;
            uv.x += jitter;

            float phase = uv.y * (u_res.y * 3.14159 / max(1.0, u_scan_den));
            float animS;
            if (u_anim < 0.5)       animS = 1.0;
            else if (u_anim < 1.5)  animS = 0.5 + 0.5 * sin(phase + t*6.0);
            else if (u_anim < 2.5)  { float x = mod(phase + t*6.0, 6.283); animS = 1.0 - abs((x/3.14159)-2.0)/2.0; }
            else                    animS = fract(phase * 0.05 + t*0.3);

            vec2 off = vec2(u_ab, 0.0);
            vec3 base;
            base.r = texture2D(tex0, uv + off).r;
            base.g = texture2D(tex0, uv      ).g;
            base.b = texture2D(tex0, uv - off).b;

            float scan = clamp(u_scan_str * animS, 0.0, 1.0);
            vec2  d = v_tex_coord - vec2(0.5);
            float vig = smoothstep(0.4, 1.0, length(d)*1.25) * u_vign;

            vec3 col = base;
            float dark = clamp(scan + vig, 0.0, 1.0) * u_inten;
            col *= (1.0 - dark);

            gl_FragColor = vec4(col, 1.0);
        """
    )

transform snfx_crt_master_t():
    shader "snfx.crt_master"
    res     (config.screen_width, config.screen_height)
    time    time
    inten   snfx_state.crt_intensity if snfx_state.enable_crt else 0.0
    vign    snfx_state.crt_vignette
    ab      snfx_state.crt_aberration
    scan_den snfx_state.crt_scan_density
    scan_str snfx_state.crt_scan_strength
    glitch   snfx_state.crt_glitch
    anim     snfx_state.crt_anim_type
    speed    snfx_state.crt_anim_speed
    barrel   snfx_state.crt_barrel
