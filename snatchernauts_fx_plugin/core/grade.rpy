# snatchernauts_fx_plugin/core/grade.rpy
init python:
    import renpy.display.im as im

    def SNFX_ops_to_matrix(ops):
        m = im.matrix.identity()
        for o in ops or []:
            t = (o.get("op") or "").lower()
            if t == "saturation": m = m * im.matrix.saturation(float(o.get("value",1.0)))
            elif t == "contrast": m = m * im.matrix.contrast(float(o.get("value",1.0)))
            elif t == "brightness": m = m * im.matrix.brightness(float(o.get("value",0.0)))
            elif t == "hue":      m = m * im.matrix.hue(float(o.get("value",0.0)))
            elif t == "tint":     m = m * im.matrix.tint(float(o.get("r",1.0)), float(o.get("g",1.0)), float(o.get("b",1.0)))
            elif t == "sepia":    m = m * im.matrix.sepia()
            elif t == "identity": m = m * im.matrix.identity()
        return m

transform snfx_grade_master_t():
    matrixcolor (snfx_state.grade_matrix if snfx_state.enable_grade else im.matrix.identity())

init python:
    config.layer_at_list.setdefault("master", [])
    _lst = config.layer_at_list["master"]
    for t in (snfx_crt_master_t, snfx_bloom_master_t, snfx_grade_master_t):
        if t not in _lst:
            _lst.append(t)
