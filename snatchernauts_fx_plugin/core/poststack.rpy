# snatchernauts_fx_plugin/core/poststack.rpy
# Core wiring, layers, per-frame driver, state, pause logic, logging

init -100 python:
    # Force GL2 pipeline (desktop only)
    config.gl2 = True

default snfx_debug_enabled = True
default snfx_game_paused = False

init python:
    import renpy
    import renpy.display.im as im

    # ---- Logging ----
    def snfx_log(msg):
        if snfx_debug_enabled:
            renpy.log(":: [ SN FX ] - %s" % msg)

    # ---- Pause/Resume gameplay while editor is open ----
    def snfx_runtime_pause(state=True):
        global snfx_game_paused
        try:
            if state:
                snfx_log("Editor: Pause gameplay")
                # pause audio channels
                for ch in ("music", "voice", "sound", "sfx"):
                    try: renpy.music.set_pause(True, channel=ch)
                    except: pass
                # auto-forward off
                try:
                    store._snfx_prev_afm = getattr(store.preferences, "afm_enable", None)
                    if store._snfx_prev_afm is not None:
                        store.preferences.afm_enable = False
                except: pass
                snfx_game_paused = True
            else:
                snfx_log("Editor: Resume gameplay")
                for ch in ("music", "voice", "sound", "sfx"):
                    try: renpy.music.set_pause(False, channel=ch)
                    except: pass
                try:
                    if getattr(store, "_snfx_prev_afm", None) is not None:
                        store.preferences.afm_enable = store._snfx_prev_afm
                except: pass
                snfx_game_paused = False
        except Exception as e:
            renpy.log(":: [ SN FX ] - Pause Error: %r" % e)

    # ---- Layers for overlay FX ----
    _layers = list(config.layers)
    def _ins(layer_name, before="screens"):
        if layer_name not in _layers:
            idx = _layers.index(before) if before in _layers else len(_layers)
            _layers.insert(idx, layer_name)
    _ins("snfx_letterbox")
    _ins("snfx_grain")
    config.layers = _layers

    # ---- Helpers ----
    def _screen_aspect(): return float(config.screen_width) / float(config.screen_height)

    def _letterbox_ratio_for_aspect(target_aspect):
        S = _screen_aspect()
        try:
            ta = float(target_aspect)
        except:
            ta = target_aspect
        if not isinstance(ta, (int,float)):
            if isinstance(target_aspect, basestring) and ":" in target_aspect:
                x,y = target_aspect.split(":"); ta = float(x)/float(y)
            else:
                ta = 2.39
        if ta <= 0 or ta <= S:
            return 0.0
        visible = S / float(ta)
        return max(0.0, min(1.0, 1.0 - visible))

    # ---- State ----
    class SNFX(object):
        def __init__(self):
            self.enable_letterbox = True
            self.enable_grain     = True
            self.enable_crt   = True
            self.enable_bloom = True
            self.enable_grade = True

            # letterbox
            self.letterbox_ratio  = 0.0
            self.letterbox_mix    = 0.0
            self._lb_target       = 0.0
            self._lb_speed        = 6.0

            # grain
            self.grain_intensity  = 0.06
            self.grain_size       = 1.0
            self.grain_speed      = 1.0
            self.grain_downsample = 1.0

            # crt
            self.crt_intensity     = 0.22
            self.crt_vignette      = 0.18
            self.crt_aberration    = 0.0025
            self.crt_scan_density  = 1.75
            self.crt_scan_strength = 0.25
            self.crt_glitch        = 0.0
            self.crt_anim_type     = 1
            self.crt_anim_speed    = 1.0
            self.crt_barrel        = 0.0

            # bloom
            self.bloom_threshold = 0.7
            self.bloom_knee      = 0.5
            self.bloom_intensity = 0.8
            self.bloom_radius    = 1.8
            self.bloom_samples   = 13
            self.bloom_anam      = 0.0
            self.bloom_anim_type = 0
            self.bloom_anim_speed= 1.0
            self.bloom_anim_amt  = 0.0

            # grade
            self.grade_matrix   = im.matrix.identity()

            self.active_tab = "About"

        # letterbox
        def set_letterbox_aspect(self, aspect):
            if isinstance(aspect, (int, float)): a = float(aspect)
            else:
                try:
                    if ":" in str(aspect):
                        x, y = str(aspect).split(":"); a = float(x)/float(y)
                    else: a = float(aspect)
                except: a = 2.39
            self.letterbox_ratio = _letterbox_ratio_for_aspect(a)

        def set_letterbox_speed(self, v):
            self._lb_speed = max(0.0, float(v))

        def animate_letterbox(self, showing=True):
            self._lb_target = 1.0 if showing else 0.0

        def update(self, dt):
            self.letterbox_mix += (self._lb_target - self.letterbox_mix) * min(1.0, self._lb_speed * dt)

    snfx_state = SNFX()

# per-frame driver
screen snfx_driver():
    zorder 0
    timer 0.016 repeat True action Function(snfx_state.update, 0.016)

init python:
    def _snfx_boot():
        renpy.show_screen("snfx_driver")
        renpy.show_screen("snfx_letterbox_screen", _layer="snfx_letterbox")
        renpy.show_screen("snfx_grain_screen",     _layer="snfx_grain")
    config.start_callbacks.append(_snfx_boot)
    config.after_load_callbacks.append(_snfx_boot)
