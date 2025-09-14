# snatchernauts_fx_plugin/core/io.rpy
init python:
    import os, json
    from renpy.display import im

    SNFX_INCLUDED = "snatchernauts_fx_plugin/presets/included"
    SNFX_CUSTOM   = "snatchernauts_fx_plugin/presets/custom"

    def snfx_ensure_dirs():
        for cat in ("letterbox","crt","grain","grade","lighting","bloom"):
            renpy.mkdir(os.path.join(config.gamedir, SNFX_CUSTOM, cat))

    def snfx_list_included(category):
        pref = f"{SNFX_INCLUDED}/{category}/"
        pack = [f for f in renpy.list_files() if f.startswith(pref) and f.endswith(".json")]
        disk = []
        disk_dir = os.path.join(config.gamedir, pref)
        if os.path.isdir(disk_dir):
            for n in os.listdir(disk_dir):
                if n.endswith(".json"):
                    disk.append(os.path.join(pref, n))
        return pack + disk

    def snfx_list_custom(category):
        disk_dir = os.path.join(config.gamedir, SNFX_CUSTOM, category)
        if not os.path.isdir(disk_dir):
            return []
        return [os.path.join(SNFX_CUSTOM, category, n) for n in os.listdir(disk_dir) if n.endswith(".json")]

    def snfx_load_json(path):
        try:
            if not os.path.isabs(path) and not path.startswith(config.gamedir):
                with renpy.file(path) as f:
                    return json.load(f)
            with open(os.path.join(config.gamedir, path), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            renpy.log(f":: [ SN FX ] - load failed {path}: {e}")
            return None

    def snfx_save_json(category, name, data):
        snfx_ensure_dirs()
        path = os.path.join(config.gamedir, SNFX_CUSTOM, category, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        renpy.notify(f"Saved {category} preset: {name}")
        snfx_log(f"Saved preset {category}:{name}")
        return path

    SNFX_SPEEDS = {
        "very slow":1.5, "slow":3.0, "normal":6.0, "fast":10.0, "very fast":20.0
    }

    def snfx_apply_letterbox_json(d):
        if not d: return
        snfx_state.enable_letterbox = bool(d.get("enable", True))
        snfx_state.set_letterbox_aspect(d.get("aspect","2.39:1"))
        sp = d.get("speed","normal")
        snfx_state.set_letterbox_speed(float(d.get("speed_custom", SNFX_SPEEDS.get(sp,6.0))))
        snfx_state.animate_letterbox(True)
        snfx_log("Letterbox: " + ("On" if snfx_state.enable_letterbox else "Off"))

    def snfx_apply_crt_json(d):
        if not d: return
        snfx_state.enable_crt        = bool(d.get("enable",True))
        snfx_state.crt_intensity     = float(d.get("intensity",0.22))
        snfx_state.crt_vignette      = float(d.get("vignette",0.18))
        snfx_state.crt_aberration    = float(d.get("aberration",0.0025))
        snfx_state.crt_scan_strength = float(d.get("scanline_strength",0.25))
        snfx_state.crt_scan_density  = float(d.get("scanline_density",1.75))
        snfx_state.crt_glitch        = float(d.get("glitch",0.0))
        snfx_state.crt_anim_type     = {"none":0,"sine":1,"tri":2,"rolling":3}.get(str(d.get("anim_type","sine")).lower(),1)
        snfx_state.crt_anim_speed    = float(d.get("anim_speed",1.0))
        snfx_state.crt_barrel        = float(d.get("barrel",0.0))
        snfx_log(f"CRT: {'On' if snfx_state.enable_crt else 'Off'} ({d.get('name','')})")

    def snfx_apply_grain_json(d):
        if not d: return
        snfx_state.enable_grain     = bool(d.get("enable",True))
        snfx_state.grain_intensity  = float(d.get("intensity",0.06))
        snfx_state.grain_size       = float(d.get("size",1.0))
        snfx_state.grain_speed      = float(d.get("speed",1.0))
        snfx_state.grain_downsample = float(d.get("downsample",1.0))
        snfx_log(f"Grain: {'On' if snfx_state.enable_grain else 'Off'}")

    def snfx_apply_grade_json(d):
        if not d: return
        snfx_state.enable_grade   = bool(d.get("enable",True))
        snfx_state.grade_matrix   = SNFX_ops_to_matrix(d.get("ops") or [{"op":"identity"}])
        snfx_log(f"Grade: {'On' if snfx_state.enable_grade else 'Off'}")

    def snfx_apply_bloom_json(d):
        if not d: return
        snfx_state.enable_bloom   = bool(d.get("enable",True))
        snfx_state.bloom_threshold= float(d.get("threshold",0.7))
        snfx_state.bloom_knee     = float(d.get("soft_knee",0.5))
        snfx_state.bloom_intensity= float(d.get("intensity",0.8))
        snfx_state.bloom_radius   = float(d.get("radius",1.8))
        snfx_state.bloom_samples  = int(d.get("samples",13))
        snfx_state.bloom_anam     = float(d.get("anamorphic",0.0))
        a = d.get("anim", {"type":"none","speed":1.0,"amount":0.0})
        snfx_state.bloom_anim_type = {"none":0,"pulse":1,"breath":2}.get(str(a.get("type","none")).lower(),0)
        snfx_state.bloom_anim_speed= float(a.get("speed",1.0))
        snfx_state.bloom_anim_amt  = float(a.get("amount",0.0))
        snfx_log(f"Bloom: {'On' if snfx_state.enable_bloom else 'Off'}")

    def snfx_apply_lighting_json(d):
        if not d: return
        snfx_lights.clear()
        amb = d.get("ambient",[0,0,0,0])
        snfx_lights.set_ambient(amb[0],amb[1],amb[2],amb[3])
        for L in d.get("lights",[]):
            typ = L.get("type","point")
            if typ == "point":
                lit = snfx_lights.add_point(L["pos"][0], L["pos"][1],
                                            color=L.get("color",[1,1,1]),
                                            intensity=L.get("intensity",1.0),
                                            radius=L.get("radius",0.3),
                                            falloff=L.get("falloff",1.0),
                                            front=L.get("front",False))
            elif typ == "spot":
                lit = snfx_lights.add_spot(L["pos"][0], L["pos"][1],
                                           dir=L.get("dir",[0,-1]),
                                           angle=L.get("angle",35),
                                           color=L.get("color",[1,1,1]),
                                           intensity=L.get("intensity",1.0),
                                           radius=L.get("radius",0.6),
                                           falloff=L.get("falloff",1.0),
                                           front=L.get("front",False))
            else:
                ss = L.get("size",[0.3,0.15])
                lit = snfx_lights.add_rect(L["pos"][0], L["pos"][1],
                                           ss[0], ss[1],
                                           color=L.get("color",[1,1,1]),
                                           intensity=L.get("intensity",1.0),
                                           falloff=L.get("falloff",1.0),
                                           front=L.get("front",False))
            an = L.get("anim", {"type":"none","speed":1.0,"amount":0.0})
            snfx_lights.set_anim(lit, type=an.get("type","none"),
                                       speed=an.get("speed",1.0),
                                       amount=an.get("amount",0.0))
        snfx_log(f"Lighting: Loaded '{d.get('name','')}', lights={len(snfx_lights.lights)}")
