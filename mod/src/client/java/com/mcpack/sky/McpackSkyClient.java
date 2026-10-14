package com.mcpack.sky;

import net.fabricmc.api.ClientModInitializer;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.render.Camera;
import net.minecraft.resource.Resource;
import net.minecraft.resource.ResourceManager;
import net.minecraft.util.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

/**
 * mcpack-sky - renders the custom sky layers a resource pack describes in the
 * OptiFine/MCPatcher {@code optifine/sky/<world>/} layout, without OptiFine.
 *
 * <p>Deliberately depends on nothing but Fabric Loader, so the only install
 * requirements are Loader + this jar.
 */
public class McpackSkyClient implements ClientModInitializer {

    public static final String MOD_ID = "mcpacksky";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    /** Dimension folders, matching OptiFine's convention (world0 = overworld). */
    public static final String WORLD_OVERWORLD = "world0";

    private static final Map<String, List<SkyLayer>> LAYERS = new LinkedHashMap<>();
    private static final List<String> PROBLEMS = new ArrayList<>();

    private static Object lastWorld = null;
    private static boolean everLoaded = false;

    @Override
    public void onInitializeClient() {
        LOGGER.info("[mcpack-sky] initialising (custom skies without OptiFine)");
    }

    /**
     * Called from the sky render hook. Layer definitions are read once per world
     * entry, so nothing is parsed per frame.
     */
    public static void onSkyPass(Camera camera) {
        MinecraftClient client = MinecraftClient.getInstance();
        Object world = client.world;
        if (!everLoaded || world != lastWorld) {
            everLoaded = true;
            lastWorld = world;
            if (world != null) {
                loadLayers(client.getResourceManager());
            }
        }
    }

    /** Reads every {@code optifine/sky/<world>/*.properties} the loaded packs provide. */
    public static void loadLayers(ResourceManager manager) {
        LAYERS.clear();
        PROBLEMS.clear();

        Map<String, Properties> files = new LinkedHashMap<>();
        Map<Identifier, Resource> found = manager.findResources(
                "optifine/sky/" + WORLD_OVERWORLD,
                id -> id.getPath().endsWith(".properties"));
        for (Map.Entry<Identifier, Resource> entry : found.entrySet()) {
            try (InputStream in = entry.getValue().getInputStream()) {
                Properties props = new Properties();
                props.load(in);
                files.put(baseName(entry.getKey().getPath(), ".properties"), props);
            } catch (Exception e) {
                PROBLEMS.add(entry.getKey() + ": unreadable (" + e + ")");
            }
        }
        if (files.isEmpty()) {
            LOGGER.info("[mcpack-sky] no optifine/sky/{} definitions in the active pack set", WORLD_OVERWORLD);
            return;
        }

        Set<String> textures = new HashSet<>();
        for (Identifier id : manager.findResources(
                "optifine/sky/" + WORLD_OVERWORLD,
                id -> id.getPath().endsWith(".png")).keySet()) {
            textures.add(baseName(id.getPath(), ".png"));
        }

        List<SkyLayer> layers = SkyLayer.loadAll(files, textures::contains, PROBLEMS);
        LAYERS.put(WORLD_OVERWORLD, layers);
        LOGGER.info("[mcpack-sky] {}: {} layer(s) ready from {} file(s), {} texture(s) present",
                WORLD_OVERWORLD, layers.size(), files.size(), textures.size());
        for (SkyLayer layer : layers) {
            LOGGER.info("[mcpack-sky]   {}", layer);
        }
        for (String problem : PROBLEMS) {
            LOGGER.warn("[mcpack-sky] {}", problem);
        }
    }

    private static String baseName(String path, String suffix) {
        String name = path.substring(path.lastIndexOf('/') + 1);
        return name.endsWith(suffix) ? name.substring(0, name.length() - suffix.length()) : name;
    }

    public static List<SkyLayer> layers() {
        return LAYERS.getOrDefault(WORLD_OVERWORLD, List.of());
    }

    public static List<String> problems() {
        return List.copyOf(PROBLEMS);
    }
}
