# snatchernauts_fx_plugin/core/api.rpy
init python:
    class SNFX_API(object):
        def open_editor(self): renpy.call_screen("snfx_editor")
        def debug(self, enable=True):
            store.snfx_debug_enabled = bool(enable)
            snfx_log("Debug: " + ("On" if enable else "Off"))
        def pause(self, state=True):
            snfx_runtime_pause(state)

        class Keys(object):
            def enable(self, e=True):
                store.snfx_hotkeys_enabled = bool(e)
                snfx_log("Hotkeys: " + ("Enabled" if e else "Disabled"))
            def bind(self, open_editor=None, toggle_hud=None, prev=None, next=None):
                if open_editor: store.snfx_keymap["open_editor"] = open_editor
                if toggle_hud:  store.snfx_keymap["toggle_hud"]  = toggle_hud
                if prev:        store.snfx_keymap["prev"]        = prev
                if next:        store.snfx_keymap["next"]        = next
                snfx_log(f"Hotkeys: {store.snfx_keymap}")
        keys = Keys()

        class LB(object):
            def load(self, name): return snfx_apply_letterbox_json(snfx_find_json("letterbox", name))
            def set_aspect(self, aspect): snfx_state.set_letterbox_aspect(aspect)
            def speed(self, v):
                if isinstance(v, basestring):
                    m = {"very slow":1.5,"slow":3.0,"normal":6.0,"fast":10.0,"very fast":20.0}; snfx_state.set_letterbox_speed(m.get(v.lower(),6.0))
                else: snfx_state.set_letterbox_speed(float(v))
            def show(self, s=True):
                snfx_state.animate_letterbox(s)
                snfx_log("Letterbox: " + ("On" if s else "Off"))
        class CRT(object):
            def load(self, name): return snfx_apply_crt_json(snfx_find_json("crt", name))
            def enable(self, e=True): snfx_state.enable_crt = bool(e); snfx_log("CRT: " + ("On" if e else "Off"))
            def set(self, **kw):
                for k,v in kw.items():
                    if hasattr(snfx_state, "crt_"+k): setattr(snfx_state, "crt_"+k, v)
        class Grain(object):
            def load(self, name): return snfx_apply_grain_json(snfx_find_json("grain", name))
            def set(self, **kw):
                for k,v in kw.items():
                    if hasattr(snfx_state, "grain_"+k): setattr(snfx_state, "grain_"+k, v)
        class Grade(object):
            def load(self, name): return snfx_apply_grade_json(snfx_find_json("grade", name))
            def apply_ops(self, ops): snfx_state.grade_matrix = SNFX_ops_to_matrix(ops); snfx_log("Grade: Applied ops")
        class Lights(object):
            def clear(self): snfx_lights.clear(); snfx_log("Lights: Cleared")
            def set_ambient(self, r,g,b,intensity): snfx_lights.set_ambient(r,g,b,intensity); snfx_log("Lights: Ambient set")
            def add_point(self, x,y, **kw): L=snfx_lights.add_point(x,y, **kw); snfx_log("Lights: Add point"); return L
            def add_spot(self, x,y, dir=(0,-1), angle=35, **kw): L=snfx_lights.add_spot(x,y, dir=dir, angle=angle, **kw); snfx_log("Lights: Add spot"); return L
            def add_rect(self, x,y, w,h, **kw): L=snfx_lights.add_rect(x,y, w,h, **kw); snfx_log("Lights: Add rect"); return L
            def set_anim(self, L, **kw): snfx_lights.set_anim(L, **kw); snfx_log("Lights: Anim set")
            def load(self, name): snfx_log(f"Lights: Load {name}"); return snfx_apply_lighting_json(snfx_find_json("lighting", name))
            def save(self, name):
                d = {"name":name,"resolution":[config.screen_width,config.screen_height],
                     "ambient":snfx_lights.ambient,
                     "lights":[
                         {"type":L.type,"pos":L.pos,"color":L.color,"intensity":L.intensity,"radius":L.radius,"falloff":L.falloff,"front":L.front,"dir":L.dir,"angle":L.angle,"size":L.size,"anim":L.anim}
                         for L in snfx_lights.lights
                     ]}
                snfx_log(f"Lights: Save {name}")
                return snfx_save_json("lighting", name, d)
        class Bloom(object):
            def load(self, name): return snfx_apply_bloom_json(snfx_find_json("bloom", name))
            def set(self, **kw):
                for k,v in kw.items():
                    if hasattr(snfx_state, "bloom_"+k): setattr(snfx_state, "bloom_"+k, v)
                snfx_log("Bloom: Set")
            def set_anim(self, **kw):
                if "type" in kw: snfx_state.bloom_anim_type = {"none":0,"pulse":1,"breath":2}.get(str(kw["type"]).lower(),0)
                if "speed" in kw: snfx_state.bloom_anim_speed = float(kw["speed"])
                if "amount"in kw: snfx_state.bloom_anim_amt   = float(kw["amount"])
                snfx_log("Bloom: Anim set")
            def save(self, name):
                d = {"name":name,"resolution":[config.screen_width,config.screen_height],
                     "enable":snfx_state.enable_bloom,"threshold":snfx_state.bloom_threshold,
                     "soft_knee":snfx_state.bloom_knee,"intensity":snfx_state.bloom_intensity,
                     "radius":snfx_state.bloom_radius,"samples":snfx_state.bloom_samples,
                     "anamorphic":snfx_state.bloom_anam,
                     "anim":{"type":{0:"none",1:"pulse",2:"breath"}[snfx_state.bloom_anim_type],
                             "speed":snfx_state.bloom_anim_speed,"amount":snfx_state.bloom_anim_amt}}
                snfx_log(f"Bloom: Save {name}")
                return snfx_save_json("bloom", name, d)

        def cycle_active_tab(self, step):
            tab = snfx_state.active_tab
            cat = {"Letterbox":"letterbox","CRT":"crt","Grain":"grain","Grade":"grade","Lighting":"lighting","Bloom":"bloom"}.get(tab)
            if not cat: return
            pool = [snfx_load_json(p) for p in snfx_list_included(cat)]
            pool = [d for d in pool if d]
            if not pool: return
            pool.sort(key=lambda d: d.get("name",""))
            idx = 0 if step>0 else -1
            d = pool[idx]
            {"letterbox":snfx_apply_letterbox_json,"crt":snfx_apply_crt_json,"grain":snfx_apply_grain_json,
             "grade":snfx_apply_grade_json,"lighting":snfx_apply_lighting_json,"bloom":snfx_apply_bloom_json}[cat](d)

    def snfx_find_json(category, name):
        for p in snfx_list_custom(category):
            d = snfx_load_json(p);  n = (d or {}).get("name")
            if n == name: return d
        for p in snfx_list_included(category):
            d = snfx_load_json(p);  n = (d or {}).get("name")
            if n == name: return d

    snfx = SNFX_API()
    snfx.lb     = SNFX_API.LB()
    snfx.crt    = SNFX_API.CRT()
    snfx.grain  = SNFX_API.Grain()
    snfx.grade  = SNFX_API.Grade()
    snfx.lights = SNFX_API.Lights()
    snfx.bloom  = SNFX_API.Bloom()
