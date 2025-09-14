# snatchernauts_fx_plugin/core/lights.rpy
init python:
    import math, json, os
    from collections import namedtuple

    class Light(object):
        def __init__(self, kind, **kw):
            self.type = kind
            self.pos  = list(kw.get("pos", [0.5,0.5]))
            self.color= list(kw.get("color", [1.0,1.0,1.0]))
            self.intensity = float(kw.get("intensity", 1.0))
            self.radius    = float(kw.get("radius", 0.3))
            self.falloff   = float(kw.get("falloff",1.0))
            self.front     = bool(kw.get("front", False))
            self.dir   = list(kw.get("dir", [0.0,-1.0]))
            self.angle = float(kw.get("angle", 35.0))
            self.size  = list(kw.get("size", [0.3,0.15]))
            self.anim  = dict(kw.get("anim", {"type":"none","speed":1.0,"amount":0.0}))
            self.runtime = {"phase":0.0}

    class LightsManager(object):
        def __init__(self):
            self.ambient = [0.0,0.0,0.0, 0.0]
            self.lights = []
            self.enabled = True

        def clear(self): self.lights[:] = []
        def set_ambient(self, r,g,b,intensity): self.ambient = [float(r),float(g),float(b),float(intensity)]
        def add_point(self, x,y, **kw):
            L = Light("point", pos=[x,y], **kw); self.lights.append(L); return L
        def add_spot(self, x,y, dir=(0,-1), angle=35, **kw):
            L = Light("spot", pos=[x,y], dir=list(dir), angle=angle, **kw); self.lights.append(L); return L
        def add_rect(self, x,y, w,h, **kw):
            L = Light("rect", pos=[x,y], size=[w,h], **kw); self.lights.append(L); return L
        def remove(self, L):
            if L in self.lights: self.lights.remove(L)
        def set_anim(self, L, type="none", speed=1.0, amount=0.0):
            L.anim = {"type":type, "speed":float(speed), "amount":float(amount)}
        def update(self, dt):
            for L in self.lights:
                L.runtime["phase"] = (L.runtime.get("phase",0.0) + dt * float(L.anim.get("speed",1.0))) % 1000.0
                a = L.anim.get("amount",0.0); t = L.runtime["phase"]
                typ = (L.anim.get("type") or "none").lower()
                if typ == "flicker":
                    v = 0.5 + 0.5 * math.sin(t*12.3) + 0.25*math.sin(t*7.1)
                    L.runtime["anim_mul"] = 1.0 + (v-0.5) * a
                elif typ == "pulse":
                    v = 0.5 + 0.5 * math.sin(t*6.28)
                    L.runtime["anim_mul"] = 1.0 + (v-0.5) * a
                else:
                    L.runtime["anim_mul"] = 1.0

    snfx_lights = LightsManager()

screen snfx_lights_driver():
    zorder 0
    timer 0.016 repeat True action Function(snfx_lights.update, 0.016)

init python:
    config.start_callbacks.append(lambda : renpy.show_screen("snfx_lights_driver"))
    config.after_load_callbacks.append(lambda : renpy.show_screen("snfx_lights_driver"))

init python:
    for _p in ("u_pos","u_col","u_inten","u_rad","u_fall","u_res"):
        renpy.register_property(_p[2:], _p)
    renpy.register_shader(
        "snfx.light_point",
        variables = """
            uniform vec2  u_pos;
            uniform vec3  u_col;
            uniform float u_inten;
            uniform float u_rad;
            uniform float u_fall;
            uniform vec2  u_res;
            attribute vec2 a_position;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex = "v_tex_coord=a_tex_coord; gl_Position=vec4(a_position,0.0,1.0);",
        fragment = """
            vec2 p = u_pos;
            float d = distance(v_tex_coord, p) / max(0.0001, u_rad);
            float fall = pow(clamp(1.0 - d, 0.0, 1.0), max(0.1, u_fall));
            vec3 c = u_col * (u_inten * fall);
            gl_FragColor = vec4(c, fall);
        """
    )

    for _p in ("u_pos","u_dir","u_angle","u_col","u_inten","u_rad","u_fall","u_res"):
        renpy.register_property(_p[2:], _p)
    renpy.register_shader(
        "snfx.light_spot",
        variables = """
            uniform vec2  u_pos;
            uniform vec2  u_dir;
            uniform float u_angle;
            uniform vec3  u_col;
            uniform float u_inten;
            uniform float u_rad;
            uniform float u_fall;
            uniform vec2  u_res;
            attribute vec2 a_position;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex = "v_tex_coord=a_tex_coord; gl_Position=vec4(a_position,0.0,1.0);",
        fragment = """
            vec2  toP = normalize(v_tex_coord - u_pos);
            float ang = radians(u_angle);
            float cd  = dot(normalize(u_dir), toP);
            float cone = smoothstep(cos(ang), cos(ang*0.6), cd);
            float d = distance(v_tex_coord, u_pos) / max(0.0001, u_rad);
            float fall = pow(clamp(1.0 - d, 0.0, 1.0), max(0.1, u_fall));
            float m = cone * fall;
            vec3 c = u_col * (u_inten * m);
            gl_FragColor = vec4(c, m);
        """
    )

    for _p in ("u_pos","u_size","u_col","u_inten","u_fall","u_res"):
        renpy.register_property(_p[2:], _p)
    renpy.register_shader(
        "snfx.light_rect",
        variables = """
            uniform vec2  u_pos;
            uniform vec2  u_size;
            uniform vec3  u_col;
            uniform float u_inten;
            uniform float u_fall;
            uniform vec2  u_res;
            attribute vec2 a_position;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex = "v_tex_coord=a_tex_coord; gl_Position=vec4(a_position,0.0,1.0);",
        fragment = """
            vec2 d = abs(v_tex_coord - u_pos) / (u_size*0.5);
            vec2 edge = clamp(1.0 - d, 0.0, 1.0);
            float m = pow(edge.x * edge.y, max(0.1, u_fall));
            vec3 c = u_col * (u_inten * m);
            gl_FragColor = vec4(c, m);
        """
    )

screen snfx_light_point(L):
    zorder (95 if L.front else 5)
    add Solid("#0000"):
        at Transform(shader="snfx.light_point",
                     properties={"pos":tuple(L.pos),
                                 "col":tuple(L.color),
                                 "inten":L.intensity * L.runtime.get("anim_mul",1.0),
                                 "rad":L.radius, "fall":L.falloff,
                                 "res":(config.screen_width, config.screen_height)},
                     blend="add")

screen snfx_light_spot(L):
    zorder (95 if L.front else 5)
    add Solid("#0000"):
        at Transform(shader="snfx.light_spot",
                     properties={"pos":tuple(L.pos),
                                 "dir":tuple(L.dir),
                                 "angle":L.angle,
                                 "col":tuple(L.color),
                                 "inten":L.intensity * L.runtime.get("anim_mul",1.0),
                                 "rad":L.radius, "fall":L.falloff,
                                 "res":(config.screen_width, config.screen_height)},
                     blend="add")

screen snfx_light_rect(L):
    zorder (95 if L.front else 5)
    add Solid("#0000"):
        at Transform(shader="snfx.light_rect",
                     properties={"pos":tuple(L.pos),
                                 "size":tuple(L.size),
                                 "col":tuple(L.color),
                                 "inten":L.intensity * L.runtime.get("anim_mul",1.0),
                                 "fall":L.falloff,
                                 "res":(config.screen_width, config.screen_height)},
                     blend="add")

screen snfx_light_ambient():
    zorder 4
    if snfx_lights.ambient[3] > 0.0:
        $ r,g,b,i = snfx_lights.ambient
        add Solid("#0000"):
            at Transform(matrixcolor=im.matrix.tint(r,g,b) * im.matrix.brightness(i-0.5),
                         blend="add")

screen snfx_lights_screen():
    use snfx_light_ambient
    for L in snfx_lights.lights:
        if L.type == "point":
            use snfx_light_point(L)
        elif L.type == "spot":
            use snfx_light_spot(L)
        elif L.type == "rect":
            use snfx_light_rect(L)

init python:
    def _snfx_light_boot():
        renpy.show_screen("snfx_lights_screen", _layer="master")
    config.start_callbacks.append(_snfx_light_boot)
    config.after_load_callbacks.append(_snfx_light_boot)
