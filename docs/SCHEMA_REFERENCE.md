# JSON Schema Reference

### Letterbox
```json
{ "name":"...", "resolution":[W,H], "enable":true, "aspect":"2.39:1", "speed":"normal", "speed_custom":6.0, "mix":1.0 }
```

### CRT
```json
{ "name":"...", "resolution":[W,H], "enable":true, "intensity":0.22, "vignette":0.18, "aberration":0.0025,
  "scanline_strength":0.25, "scanline_density":1.75, "glitch":0.0, "anim_type":"sine", "anim_speed":1.0, "barrel":0.003 }
```

### Film Grain
```json
{ "name":"...", "resolution":[W,H], "enable":true, "intensity":0.06, "size":1.2, "speed":1.2, "downsample":1.0 }
```

### Color Grade
```json
{ "name":"...", "enable":true, "ops":[{"op":"contrast","value":1.1},{"op":"tint","r":1.02,"g":1.0,"b":0.98}] }
```

### Lighting
```json
{ "name":"...", "resolution":[W,H], "ambient":[r,g,b,intensity], "lights":[
  { "type":"point|spot|rect", "pos":[x,y], "color":[r,g,b], "intensity":1.0, "radius":0.3, "falloff":1.0,
    "front":false, "dir":[dx,dy], "angle":35, "size":[w,h],
    "anim":{"type":"none|flicker|pulse|breathe","speed":1.0,"amount":0.2}
}]}
```

### Bloom
```json
{ "name":"...", "resolution":[W,H], "enable":true, "threshold":0.72, "soft_knee":0.5, "intensity":0.9,
  "radius":2.0, "samples":15, "anamorphic":0.2,
  "anim":{"type":"none|pulse|breathe","speed":1.0,"amount":0.15} }
```
