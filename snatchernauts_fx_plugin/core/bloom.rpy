# snatchernauts_fx_plugin/core/bloom.rpy
init python:
    for _p in ("u_time","u_thr","u_knee","u_inten","u_rad","u_anam","u_anim","u_aspeed","u_aamt","u_res"):
        renpy.register_property(_p[2:], _p)

    renpy.register_shader(
        "snfx.bloom_master",
        variables = """
            uniform sampler2D tex0;
            uniform vec2  u_res;
            uniform float u_time;
            uniform float u_thr;
            uniform float u_knee;
            uniform float u_inten;
            uniform float u_rad;
            uniform float u_anam;
            uniform float u_anim;
            uniform float u_aspeed;
            uniform float u_aamt;
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

            float t = u_time * u_aspeed;
            float anim = 0.0;
            if (u_anim > 0.5 && u_anim < 1.5) anim = sin(t) * u_aamt;
            else if (u_anim > 1.5)            anim = (sin(t*0.7)*0.5+0.5) * u_aamt;

            float thr  = clamp(u_thr + anim*0.1, 0.0, 1.0);
            float knee = clamp(u_knee, 0.0, 1.0);
            float intensity = max(0.0, u_inten + anim*0.25);

            vec3 src = texture2D(tex0, uv).rgb;
            float luma = max(max(src.r, src.g), src.b);
            float soft = clamp((luma - thr + knee) / (2.0*knee), 0.0, 1.0);
            float bright = max(luma - thr, 0.0) * soft;

            vec2 px = vec2(1.0 / u_res.x, 1.0 / u_res.y);
            float r = 1.5 * u_rad;
            vec2 dirs[4];
            dirs[0] = vec2(1.0 + u_anam, 0.0);
            dirs[1] = vec2(0.0, 1.0);
            dirs[2] = normalize(vec2(1.0 + u_anam, 1.0));
            dirs[3] = normalize(vec2(1.0 + u_anam,-1.0));

            vec3 bloom = vec3(0.0);
            float weights[5];
            weights[0]=0.227; weights[1]=0.194; weights[2]=0.121; weights[3]=0.054; weights[4]=0.016;

            for (int d=0; d<4; d++) {
                vec2 dir = dirs[d] * px * r;
                vec3 c = texture2D(tex0, uv).rgb * weights[0];
                for (int i=1; i<5; i++) {
                    c += texture2D(tex0, uv + dir * float(i)).rgb * weights[i];
                    c += texture2D(tex0, uv - dir * float(i)).rgb * weights[i];
                }
                bloom += c * (bright);
            }
            bloom /= 4.0;

            vec3 outc = src + bloom * intensity;
            gl_FragColor = vec4(outc, 1.0);
        """
    )

transform snfx_bloom_master_t():
    shader "snfx.bloom_master"
    res    (config.screen_width, config.screen_height)
    time   time
    thr    snfx_state.bloom_threshold if snfx_state.enable_bloom else 2.0
    knee   snfx_state.bloom_knee
    inten  snfx_state.bloom_intensity
    rad    snfx_state.bloom_radius
    anam   snfx_state.bloom_anam
    anim   snfx_state.bloom_anim_type
    aspeed snfx_state.bloom_anim_speed
    aamt   snfx_state.bloom_anim_amt
