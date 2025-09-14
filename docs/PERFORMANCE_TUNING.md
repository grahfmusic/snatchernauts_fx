# Performance Tuning

- **Bloom**: largest cost — lower `radius`/`samples` or reduce `intensity`/`anamorphic`.
- **CRT**: glitch + barrel cost more than base scanlines/aberration.
- **Grain**: overlay and inexpensive; using Downsample gives chunkier look at near-zero cost.
- **Lighting**: each light is a full-screen pass; keep typical 3–8. Prefer smaller radii and fewer overlapping big rects.
- **Resolution**: 1080p ideal; for 4K tweak bloom down.

Tip: build look with Bloom off, then dial Bloom back in cautiously.
