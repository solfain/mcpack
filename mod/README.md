# mcpack-sky

A **Fabric client mod** that renders custom sky layers described by resource packs in the
OptiFine/MCPatcher layout (`assets/minecraft/optifine/sky/<world>/*.properties`), so packs like
Vermeil get their sky back **without OptiFine**.

Requirements: **Fabric Loader** + this jar. No Fabric API, no OptiFine.

Build: pushed automatically by `.github/workflows/build-mod.yml` → jar lands in `dist/mod/`.
Locally: `cd mod && gradle build` (needs JDK 21; Gradle 8.14 or newer).

## Status

* [x] project skeleton + CI build
* [x] OptiFine sky `.properties` parsing (fade windows, blend mode, rotation, axis)
* [x] hook into the sky render pass (1.21.11 frame-graph entry point)
* [ ] drawing the layers (render pipeline + core shaders) — in progress

## Notes

The mixin hooks `LevelRenderer#addSkyPass(FrameGraphBuilder, Camera, GpuBufferSlice)`, the same
entry point vanilla and other 1.21.11 sky mods use; layer loading is lazy and re-runs whenever the
enabled resource-pack set changes.

Sky file format reference: the OptiFine custom-sky properties documented by MCPatcher/OptiFine
(`source`, `startFadeIn`, `endFadeIn`, `startFadeOut`, `endFadeOut`, `blend`, `rotate`, `speed`, `axis`).

MIT licensed. API usage (frame-graph sky pass + the 1.21.11 render pipeline calls) was cross-checked
against [Nuit](https://github.com/FlashyReese/nuit) (MIT), the maintained custom-sky mod for this
version; no Nuit code is copied.
