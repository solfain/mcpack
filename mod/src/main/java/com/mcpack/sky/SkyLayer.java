package com.mcpack.sky;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Properties;

/**
 * One custom-sky layer, as described by an OptiFine/MCPatcher
 * {@code optifine/sky/world0/<name>.properties} file.
 *
 * <p>Times are stored as minutes-of-day (0..1440). Layers fade in over
 * {@code [startFadeIn, endFadeIn]} and out over {@code [startFadeOut, endFadeOut]},
 * wrapping around midnight when the window spans it.
 */
public final class SkyLayer {

    /** How the layer is composited over what is already in the sky. */
    public enum Blend {
        REPLACE, ADD, SUBTRACT, MULTIPLY, SCREEN, OVERLAY;

        static Blend parse(String raw, Blend fallback) {
            if (raw == null) {
                return fallback;
            }
            return switch (raw.trim().toLowerCase(Locale.ROOT)) {
                case "replace" -> REPLACE;
                case "add" -> ADD;
                case "subtract" -> SUBTRACT;
                case "multiply" -> MULTIPLY;
                case "screen" -> SCREEN;
                case "overlay" -> OVERLAY;
                default -> fallback;
            };
        }
    }

    public final String name;          // "sky3" - the properties file's base name
    public final String source;        // texture file name, e.g. "starfield03.png"
    public final int startFadeIn;
    public final int endFadeIn;
    public final int startFadeOut;
    public final int endFadeOut;
    public final Blend blend;
    public final boolean rotate;
    public final float speed;
    public final float[] axis;

    private SkyLayer(String name, String source, int startFadeIn, int endFadeIn,
                     int startFadeOut, int endFadeOut, Blend blend,
                     boolean rotate, float speed, float[] axis) {
        this.name = name;
        this.source = source;
        this.startFadeIn = startFadeIn;
        this.endFadeIn = endFadeIn;
        this.startFadeOut = startFadeOut;
        this.endFadeOut = endFadeOut;
        this.blend = blend;
        this.rotate = rotate;
        this.speed = speed;
        this.axis = axis;
    }

    /** "@HH:MM" / "HH:MM" / minutes / 0..1 fraction -> minutes of day. */
    public static int parseTime(String raw, int fallback) {
        if (raw == null || raw.isBlank()) {
            return fallback;
        }
        String s = raw.trim().replace("@", "");
        try {
            if (s.contains(":")) {
                String[] parts = s.split(":", 2);
                int h = Integer.parseInt(parts[0].trim());
                int m = (int) Float.parseFloat(parts[1].trim());
                return Math.floorMod(h * 60 + m, 1440);
            }
            float v = Float.parseFloat(s);
            // OptiFine also accepts a fraction of the day (0.0 - 1.0)
            return Math.floorMod(Math.round(v <= 1.0F && v > 0.0F ? v * 1440.0F : v), 1440);
        } catch (NumberFormatException e) {
            return fallback;
        }
    }

    private static float[] parseAxis(String raw) {
        if (raw == null || raw.isBlank()) {
            return new float[]{0.0F, 0.0F, 0.0F};
        }
        String[] parts = raw.trim().split("\\s+");
        float[] out = new float[]{0.0F, 0.0F, 0.0F};
        for (int i = 0; i < Math.min(3, parts.length); i++) {
            try {
                out[i] = Float.parseFloat(parts[i]);
            } catch (NumberFormatException ignored) {
                // leave as 0
            }
        }
        return out;
    }

    /**
     * @return the layer, or {@code null} when the file has no usable {@code source}
     *         (which is how the original pack describes layers it never shipped art for)
     */
    public static SkyLayer from(String name, Properties props, java.util.function.Predicate<String> textureExists) {
        String source = props.getProperty("source");
        if (source == null || source.isBlank()) {
            return null;
        }
        source = source.trim();
        // OptiFine allows "./file.png", "textures/...", or a bare name
        int slash = Math.max(source.lastIndexOf('/'), source.lastIndexOf('\\'));
        if (slash >= 0) {
            source = source.substring(slash + 1);
        }
        if (!textureExists.test(source)) {
            return null;
        }
        return new SkyLayer(
                name,
                source,
                parseTime(props.getProperty("startFadeIn"), 0),
                parseTime(props.getProperty("endFadeIn"), 0),
                parseTime(props.getProperty("startFadeOut"), 0),
                parseTime(props.getProperty("endFadeOut"), 0),
                Blend.parse(props.getProperty("blend"), Blend.REPLACE),
                Boolean.parseBoolean(props.getProperty("rotate", "false")),
                Float.parseFloat(props.getProperty("speed", "1.0")),
                parseAxis(props.getProperty("axis"))
        );
    }

    /** True when {@code t} is inside [from, to), tolerating windows that wrap midnight. */
    private static boolean inWindow(int t, int from, int to) {
        if (from == to) {
            return false;
        }
        return from < to ? (t >= from && t < to) : (t >= from || t < to);
    }

    /**
     * Opacity of this layer at the given time of day.
     *
     * @param timeOfDay minutes of day, 0..1440 (0 = sunrise, 6000 = noon in MC terms)
     */
    public float alphaAt(int timeOfDay) {
        int t = Math.floorMod(timeOfDay, 1440);
        if (startFadeIn != endFadeIn && inWindow(t, startFadeIn, endFadeIn)) {
            return fraction(t, startFadeIn, endFadeIn);      // fading in
        }
        if (startFadeOut != endFadeOut && inWindow(t, startFadeOut, endFadeOut)) {
            return 1.0F - fraction(t, startFadeOut, endFadeOut); // fading out
        }
        // Outside both windows: fully visible if the layer's window still covers this time
        boolean covered = inWindow(t, endFadeIn, startFadeOut) || inWindow(t, endFadeOut, startFadeIn);
        if (endFadeIn == startFadeOut || endFadeOut == startFadeIn) {
            covered = true;
        }
        return covered ? 1.0F : 0.0F;
    }

    private static float fraction(int t, int from, int to) {
        int span = Math.floorMod(to - from, 1440);
        int done = Math.floorMod(t - from, 1440);
        if (span == 0) {
            return 0.0F;
        }
        return Math.min(1.0F, Math.max(0.0F, (float) done / (float) span));
    }

    /** All layers of a world folder, in stable order, with unusable ones dropped. */
    public static List<SkyLayer> loadAll(java.util.Map<String, Properties> files,
                                        java.util.function.Predicate<String> textureExists,
                                        List<String> problems) {
        List<SkyLayer> layers = new ArrayList<>();
        files.entrySet().stream()
                .sorted(java.util.Map.Entry.comparingByKey())
                .forEach(e -> {
                    SkyLayer layer = from(e.getKey(), e.getValue(), textureExists);
                    if (layer == null) {
                        problems.add(e.getKey() + ": source='" + e.getValue().getProperty("source")
                                + "' is missing from the pack - layer skipped");
                    } else {
                        layers.add(layer);
                    }
                });
        return layers;
    }

    @Override
    public String toString() {
        return "SkyLayer[" + name + " -> " + source + ", blend=" + blend
                + ", fadeIn=" + startFadeIn + "-" + endFadeIn
                + ", fadeOut=" + startFadeOut + "-" + endFadeOut
                + ", rotate=" + rotate + "]";
    }
}
