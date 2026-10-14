# mcpack-sky

A **Fabric client mod** that renders custom sky layers described by resource packs in the
OptiFine/MCPatcher layout (`assets/minecraft/optifine/sky/<world>/*.properties`), so packs like
Vermeil get their sky back **without OptiFine**.

Requirements: **Fabric Loader** + this jar. No Fabric API, no OptiFine.

Build: pushed automatically by `.github/workflows/build-mod.yml` → jar lands in `dist/mod/`.
Locally: `cd mod && gradle build` (needs JDK 21; Gradle 8.14 or newer).

## Status

* [x] project skeleton + CI build (`dist/mod/mcpack-sky-0.1.0.jar`, 12 KB)
* [x] OptiFine sky `.properties` parsing (fade windows, blend mode, rotation, axis)
* [x] hook into the sky render pass — `WorldRenderer.renderSky(FrameGraphBuilder, Camera, GpuBufferSlice)`
* [ ] drawing the layers (render pipeline + core shaders) — **not implemented yet**

**What the current jar does:** on entering a world it reads every `optifine/sky/world0/*.properties`
from the active packs, parses them, and logs what it found (including any layer whose texture is
missing from the pack). It does not draw anything yet, so it is a test build for validating the
loading path — check the log for `[mcpack-sky]` lines.

## Toolchain notes (learned the hard way)

* 1.21.11 still needs remapping: the plain `net.fabricmc.fabric-loom` plugin is the **no-remap**
  variant used for the unobfuscated 26.x game; this project uses the era-matching
  `fabric-loom` **1.12-SNAPSHOT** with Yarn `1.21.11+build.6`.
* Build with **JDK 21** and **Gradle 8.14** (Loom 1.18/Gradle 9.x target the newer game and will
  leave the 1.21.11 jar obfuscated).
* Client classes (rendering) must live in `src/client/java`; the common classpath has no
  client-only classes in 1.21.9+.
* Loom 1.12 disables the legacy Mixin annotation processor: do **not** add `sponge-mixin` as an
  `annotationProcessor`, or mixin target remapping fails at compile time.

## Notes

The mixin hooks `LevelRenderer#addSkyPass(FrameGraphBuilder, Camera, GpuBufferSlice)`, the same
entry point vanilla and other 1.21.11 sky mods use; layer loading is lazy and re-runs whenever the
enabled resource-pack set changes.

Sky file format reference: the OptiFine custom-sky properties documented by MCPatcher/OptiFine
(`source`, `startFadeIn`, `endFadeIn`, `startFadeOut`, `endFadeOut`, `blend`, `rotate`, `speed`, `axis`).

MIT licensed. API usage (frame-graph sky pass + the 1.21.11 render pipeline calls) was cross-checked
against [Nuit](https://github.com/FlashyReese/nuit) (MIT), the maintained custom-sky mod for this
version; no Nuit code is copied.
