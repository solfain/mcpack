package com.mcpack.sky.mixin;

import com.mcpack.sky.McpackSkyClient;
import com.mojang.blaze3d.buffers.GpuBufferSlice;
import net.minecraft.client.render.Camera;
import net.minecraft.client.render.FrameGraphBuilder;
import net.minecraft.client.render.WorldRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Hook point for custom sky rendering.
 *
 * <p>{@code WorldRenderer.renderSky} is where 1.21.11 builds the sky pass
 * ({@code FrameGraphBuilder}, {@code Camera}, fog buffer). Custom sky layers get
 * injected here, which is also where a replacement sky would take over from vanilla's.
 */
@Mixin(WorldRenderer.class)
public abstract class WorldRendererMixin {

    @Inject(
            method = "renderSky(Lnet/minecraft/client/render/FrameGraphBuilder;Lnet/minecraft/client/render/Camera;Lcom/mojang/blaze3d/buffers/GpuBufferSlice;)V",
            at = @At("HEAD")
    )
    private void mcpacksky$skyPass(FrameGraphBuilder frameGraphBuilder, Camera camera, GpuBufferSlice fogBuffer, CallbackInfo ci) {
        McpackSkyClient.onSkyPass(camera);
    }
}
