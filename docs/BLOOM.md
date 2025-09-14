# Bloom (Master Pass)

Fullscreen glow from bright areas. Order: **CRT → Bloom → Grade**.

## Controls
- Threshold, Soft Knee, Intensity
- Radius, Samples, Anamorphic stretch
- Animation: None / Pulse / Breathe

## API
```renpy
$ snfx.bloom.load("Bloom_Cinematic")
$ snfx.bloom.set(threshold=0.72, soft_knee=0.5, intensity=0.9, radius=2.0, samples=15, anamorphic=0.2)
$ snfx.bloom.set_anim(type="pulse", speed=1.0, amount=0.15)
```
