# snatchernauts_fx_plugin/core/presets_autotune.rpy
init -1 python:
    import os, json

    def _snfx_retarget_resolution_in_json(path, width, height):
        try:
            if not os.path.isabs(path):
                path = os.path.join(config.gamedir, path)
            if not os.path.exists(path):
                return False
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict):
                d["resolution"] = [int(width), int(height)]
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(d, f, ensure_ascii=False, indent=2)
                return True
        except Exception as e:
            renpy.log(":: [ SN FX ] - Preset retarget failed: %r" % e)
        return False

    def _snfx_autotune_apply_profile(d, look):
        # Adjust a dict in-place according to 'look' (cinematic/broadcast/retro/neon/neutral)
        L = (look or "cinematic").lower()
        cat = None
        # try to infer category by keys
        if "aspect" in d: cat="letterbox"
        elif "scanline_strength" in d: cat="crt"
        elif "downsample" in d: cat="grain"
        elif "ops" in d: cat="grade"
        elif "anim" in d and "threshold" in d: cat="bloom"
        elif "lights" in d and "ambient" in d: cat="lighting"

        if L=="cinematic":
            if cat=="letterbox": d["aspect"]="2.39:1"; d["speed"]="normal"; d["speed_custom"]=6.0; d["enable"]=True
            elif cat=="crt": d.update({"enable":True,"intensity":0.18,"vignette":0.18,"aberration":0.0015,"scanline_strength":0.22,"scanline_density":1.6,"glitch":0.0,"anim_type":"sine","anim_speed":0.9,"barrel":0.002})
            elif cat=="grain": d.update({"enable":True,"intensity":0.06,"size":1.1,"speed":1.0,"downsample":1.0})
            elif cat=="grade": d["ops"]=[{"op":"hue","value":0.02},{"op":"saturation","value":1.12},{"op":"contrast","value":1.08},{"op":"tint","r":1.03,"g":1.02,"b":0.98}]
            elif cat=="bloom": d.update({"enable":True,"threshold":0.72,"soft_knee":0.50,"intensity":0.90,"radius":2.0,"samples":15,"anamorphic":0.20,"anim":{"type":"pulse","speed":1.0,"amount":0.15}})
        elif L=="broadcast":
            if cat=="letterbox": d.update({"aspect":"16:9","enable":False})
            elif cat=="crt": d.update({"enable":False,"intensity":0.14,"vignette":0.10,"aberration":0.0010,"scanline_strength":0.20,"scanline_density":1.5,"glitch":0.0,"anim_type":"none","anim_speed":0.0,"barrel":0.002})
            elif cat=="grain": d.update({"enable":True,"intensity":0.04,"size":1.0,"speed":0.9,"downsample":1.0})
            elif cat=="grade": d["ops"]=[{"op":"saturation","value":1.05},{"op":"contrast","value":1.03}]
            elif cat=="bloom": d.update({"enable":True,"threshold":0.70,"soft_knee":0.50,"intensity":0.65,"radius":1.6,"samples":13,"anamorphic":0.0,"anim":{"type":"none","speed":0.0,"amount":0.0}})
        elif L=="retro":
            if cat=="letterbox": d.update({"aspect":"4:3","speed":"fast","speed_custom":10.0,"enable":True})
            elif cat=="crt": d.update({"enable":True,"intensity":0.30,"vignette":0.16,"aberration":0.0030,"scanline_strength":0.42,"scanline_density":1.8,"glitch":0.18,"anim_type":"rolling","anim_speed":1.2,"barrel":0.006})
            elif cat=="grain": d.update({"enable":True,"intensity":0.10,"size":1.8,"speed":0.9,"downsample":2.0})
            elif cat=="grade": d["ops"]=[{"op":"hue","value":-0.02},{"op":"saturation","value":1.05},{"op":"contrast","value":0.98}]
            elif cat=="bloom": d.update({"enable":True,"threshold":0.78,"soft_knee":0.35,"intensity":0.70,"radius":1.6,"samples":13,"anamorphic":0.00,"anim":{"type":"none","speed":0.0,"amount":0.0}})
        elif L=="neon":
            if cat=="letterbox": d.update({"aspect":"21:9","speed":"normal","speed_custom":6.0,"enable":True})
            elif cat=="crt": d.update({"enable":True,"intensity":0.22,"vignette":0.20,"aberration":0.0026,"scanline_strength":0.32,"scanline_density":1.8,"glitch":0.06,"anim_type":"sine","anim_speed":1.1,"barrel":0.004})
            elif cat=="grain": d.update({"enable":True,"intensity":0.07,"size":1.3,"speed":1.2,"downsample":1.3})
            elif cat=="grade": d["ops"]=[{"op":"tint","r":0.95,"g":1.02,"b":1.08},{"op":"saturation","value":1.15},{"op":"contrast","value":1.1},{"op":"hue","value":0.01}]
            elif cat=="bloom": d.update({"enable":True,"threshold":0.58,"soft_knee":0.42,"intensity":1.25,"radius":2.4,"samples":17,"anamorphic":0.30,"anim":{"type":"pulse","speed":1.2,"amount":0.20}})
        else: # neutral
            if cat=="letterbox": d.update({"aspect":"16:9","enable":False})
            elif cat=="crt": d.update({"enable":False,"intensity":0.12,"vignette":0.10,"aberration":0.0012,"scanline_strength":0.18,"scanline_density":1.4,"glitch":0.0,"anim_type":"none","anim_speed":0.0,"barrel":0.002})
            elif cat=="grain": d.update({"enable":True,"intensity":0.03,"size":1.0,"speed":1.0,"downsample":1.0})
            elif cat=="grade": d["ops"]=[{"op":"identity"}]
            elif cat=="bloom": d.update({"enable":True,"threshold":0.70,"soft_knee":0.50,"intensity":0.60,"radius":1.8,"samples":13,"anamorphic":0.0,"anim":{"type":"none","speed":0.0,"amount":0.0}})

    class SNFX_Presets_API(object):
        def __init__(self):
            self.look = getattr(store, "snfx_preset_look", "cinematic")

        def set_look(self, look):
            self.look = str(look).lower()
            store.snfx_preset_look = self.look
            snfx_log("Presets: look -> %s" % self.look)

        def autotune(self, look=None):
            look = (look or self.look or "cinematic").lower()
            W, H = config.screen_width, config.screen_height
            for cat in ("letterbox","crt","grain","grade","lighting","bloom"):
                path = os.path.join(config.gamedir, "snatchernauts_fx_plugin", "presets", "custom", cat)
                if not os.path.isdir(path): continue
                for n in os.listdir(path):
                    if not n.endswith(".json"): continue
                    jp = os.path.join(path, n)
                    try:
                        with open(jp, "r", encoding="utf-8") as f: d = json.load(f)
                        _snfx_autotune_apply_profile(d, look)
                        if isinstance(d, dict): d["resolution"] = [int(W), int(H)]
                        with open(jp, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
                    except Exception as e:
                        renpy.log(":: [ SN FX ] - Autotune error %r on %s" % (e, jp))
            snfx_log("Presets: autotuned for %dx%d (%s)" % (W,H,look))

    # attach
    snfx.presets = SNFX_Presets_API()

# Run once after install; set default look if not set
init 1 python:
    if not hasattr(persistent, "_snfx_autotuned"):
        try:
            snfx.presets.set_look(getattr(store,"snfx_preset_look","cinematic"))
            snfx.presets.autotune()
            persistent._snfx_autotuned = True
        except Exception as e:
            renpy.log(":: [ SN FX ] - Autotune init error: %r" % e)
