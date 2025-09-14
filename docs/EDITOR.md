# Editor Guide

Open with **F10**. Professional dark UI with rounded panels, MapleMono font, scale-aware.

## Global
- **UI Transparency** slider for panel opacity.
- Tabs: **About**, **Letterbox**, **CRT**, **Film Grain**, **Color Grade**, **Lighting**, **Bloom**.
- Each tab: **Included** and **Custom** preset lists; you can **Save** current settings to `presets/custom/<category>/Name.json`.

## Letterbox (Speed Only)
- Choose preset to set **aspect** (ratios live in presets). In the UI you control **animation speed only**.
- Preview **Show/Hide** easing (Very Slow → Very Fast or numeric).

## CRT
- Intensity, Vignette, Chromatic Aberration, Scan Strength/Density, Glitch, Animation Type (None/Sine/Tri/Roll), Speed, Barrel Warp.

## Film Grain
- Intensity, Size, Speed, Downsample (for chunkier texture). Overlay is performance-friendly.

## Color Grade
- GPU `matrixcolor` ops: Saturation, Contrast, Brightness, Hue, RGB Tint.
- Apply to scene and save as preset.

## Lighting (2D)
- Ambient RGBAi along the top.
- Add **Point**, **Spot**, **Rect** lights. Drag handles to move in normalized space.
- Per-light: intensity, radius/size, falloff, front/behind, animation (flicker/pulse/breathe).
- Save a whole lighting setup as a preset.

## Bloom
- Threshold, Soft Knee, Intensity, Radius, Samples, Anamorphic stretch; Animations (None/Pulse/Breathe).
