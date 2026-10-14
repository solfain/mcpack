package com.mcpack.sky.mixin;

import com.mcpack.sky.McpackSkyClient;
import com.mojang.blaze3d.buffers.GpuBufferSlice;
import com.mojang.blaze3d.framegraph.FrameGraphBuilder;
import net.minecraft.client.Camera;
import net.minecraft.client.renderer.LevelRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Hook point for custom sky rendering.
 *
 * <p>{@code addSkyPass} is the same frame-graph entry point vanilla uses to add its
 * sky rendering pass, which is where a replacement sky has to be injected. This runs
 * at HEAD so the custom layers can be drawn into the sky pass before/alongside vanilla's.
 */
@Mixin(LevelRenderer.class)
public abstract class LevelRendererMixin {

    @Inject(
            method = "addSkyPass(Lcom/mojang/blaze3d/framegraph/FrameGraphBuilder;Lnet/minecraft/client/Camera;Lcom/mojang/blaze3d/buffers/GpuBufferSlice;)V",
            at = @At("HEAD")
    )
    private void mcpacksky$skyPass(FrameGraphBuilder frameGraphBuilder, Camera camera, GpuBufferSlice fogParameters, CallbackInfo ci) {
        McpackSkyClient.onSkyPass(camera);
    }
}
