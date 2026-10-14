#!/usr/bin/env python3
"""
port_pack.py - port a legacy (pre-1.13 "textures/blocks" era) Minecraft Java
resource pack to a modern version (default target: 1.21.11).

WHAT IT DOES
  * rewrites pack.mcmeta to the modern format (pack_format / min_format / max_format)
  * moves + renames every texture to the path modern Minecraft actually reads
    (textures/block, textures/item, textures/entity/..., textures/entity/equipment, ...)
  * converts mcpatcher/ folders to the optifine/ paths modern loaders read
  * (optionally) writes a font/default.json so legacy unicode_page_*.png glyph
    sheets are actually used by the game
  * drops OS junk (Thumbs.db, .DS_Store) and reports everything it could not map

IMAGE PIXELS ARE NEVER MODIFIED - this tool only moves/renames files.

Usage:
    python3 tools/port_pack.py --src <legacy pack dir> --out <output dir> \
        [--pack-format 75] [--vanilla-paths <txt of 1.21.11 asset paths>] \
        [--fonts] [--report <file.md>] [--zip <file.zip>]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import struct
import sys
import zipfile
from pathlib import Path

# --------------------------------------------------------------------------
# name translation tables
# --------------------------------------------------------------------------

# legacy dye/wool/glass/terracotta colour name -> modern colour name
COLOR = {
    "white": "white", "orange": "orange", "magenta": "magenta",
    "light_blue": "light_blue", "yellow": "yellow", "lime": "lime",
    "pink": "pink", "gray": "gray", "silver": "light_gray", "cyan": "cyan",
    "purple": "purple", "blue": "blue", "brown": "brown", "green": "green",
    "red": "red", "black": "black",
}
C = "{color}"
M = "{modern}"

# legacy wood names -> modern wood names
WOOD = {
    "oak": "oak", "spruce": "spruce", "birch": "birch", "jungle": "jungle",
    "acacia": "acacia", "big_oak": "dark_oak", "dark_oak": "dark_oak",
    "roofed_oak": "dark_oak",
}
W = "{wood}"
MW = "{modern}"


def expand(template: str, table: dict, key: str, token: str, out_token: str) -> dict:
    """'wool_colored_{color}' + COLOR table -> {'wool_colored_red': 'red_wool', ...}"""
    result = {}
    for k, v in table.items():
        result[template.replace(token, k).format(**{token.strip("{}"): k})] = (
            template.replace(token, k).replace(out_token, v).replace(f"{{{key}}}", v)
        )
    return result


def build_colour_map(template: str, replacement: str) -> dict:
    """template/replacement use {color} for legacy and {modern} for modern colour."""
    out = {}
    for legacy, modern in COLOR.items():
        out[template.format(color=legacy)] = replacement.format(modern=modern)
    return out


def build_wood_map(template: str, replacement: str) -> dict:
    out = {}
    for legacy, modern in WOOD.items():
        out[template.format(wood=legacy)] = replacement.format(modern=modern)
    return out


# --------------------------------------------------------------------------
# BLOCK textures  (textures/blocks -> textures/block)
# --------------------------------------------------------------------------
BLOCK_MAP: dict[str, str] = {}
for tmpl, repl in [
    ("wool_colored_{color}", "{modern}_wool"),
    ("hardened_clay_stained_{color}", "{modern}_terracotta"),
    ("stained_hardened_clay_{color}", "{modern}_terracotta"),
    ("glass_pane_top_{color}", "{modern}_stained_glass_pane_top"),
    ("glass_{color}", "{modern}_stained_glass"),
    ("stained_glass_pane_{color}_top", "{modern}_stained_glass_pane_top"),
    ("stained_glass_{color}", "{modern}_stained_glass"),
]:
    BLOCK_MAP.update(build_colour_map(tmpl, repl))

for tmpl, repl in [
    ("planks_{wood}", "{modern}_planks"),
    ("log_{wood}_top", "{modern}_log_top"),
    ("log_{wood}", "{modern}_log"),
    ("sapling_{wood}", "{modern}_sapling"),
    ("leaves_{wood}", "{modern}_leaves"),
    ("door_{wood}_upper", "{modern}_door_top"),
    ("door_{wood}_lower", "{modern}_door_bottom"),
    ("trapdoor_{wood}", "{modern}_trapdoor"),
]:
    BLOCK_MAP.update(build_wood_map(tmpl, repl))

BLOCK_MAP.update({
    # ---- renamed 1:1 ----
    "hardened_clay": "terracotta",
    "cobblestone_mossy": "mossy_cobblestone",
    "stonebrick": "stone_bricks",
    "stonebrick_carved": "chiseled_stone_bricks",
    "stonebrick_cracked": "cracked_stone_bricks",
    "stonebrick_mossy": "mossy_stone_bricks",
    "brick": "bricks",
    "nether_brick": "nether_bricks",
    "red_nether_brick": "red_nether_bricks",
    "end_bricks": "end_stone_bricks",
    "stone_granite": "granite",
    "stone_granite_smooth": "polished_granite",
    "stone_diorite": "diorite",
    "stone_diorite_smooth": "polished_diorite",
    "stone_andesite": "andesite",
    "stone_andesite_smooth": "polished_andesite",
    "stone_slab_side": "smooth_stone_slab_side",
    "stone_slab_top": "smooth_stone",
    "dirt_podzol_side": "podzol_side",
    "dirt_podzol_top": "podzol_top",
    "grass_side": "grass_block_side",
    "grass_side_overlay": "grass_block_side_overlay",
    "grass_side_snowed": "grass_block_snow",
    "grass_top": "grass_block_top",
    "farmland_dry": "farmland",
    "farmland_wet": "farmland_moist",
    "sandstone_normal": "sandstone",
    "sandstone_carved": "chiseled_sandstone",
    "sandstone_smooth": "cut_sandstone",
    "red_sandstone_normal": "red_sandstone",
    "red_sandstone_carved": "chiseled_red_sandstone",
    "red_sandstone_smooth": "cut_red_sandstone",
    "quartz_block_chiseled": "chiseled_quartz_block",
    "quartz_block_chiseled_top": "chiseled_quartz_block_top",
    "quartz_block_lines": "quartz_pillar",
    "quartz_block_lines_top": "quartz_pillar_top",
    "quartz_ore": "nether_quartz_ore",
    "endframe_top": "end_portal_frame_top",
    "endframe_side": "end_portal_frame_side",
    "endframe_eye": "end_portal_frame_eye",
    "anvil_base": "anvil",
    "bed_feet_end": "KEEP", "bed_feet_side": "KEEP", "bed_feet_top": "KEEP",
    "bed_head_end": "KEEP", "bed_head_side": "KEEP", "bed_head_top": "KEEP",
    "mushroom_block_skin_brown": "brown_mushroom_block",
    "mushroom_block_skin_red": "red_mushroom_block",
    "mushroom_block_skin_stem": "mushroom_stem",
    "mushroom_brown": "brown_mushroom",
    "mushroom_red": "red_mushroom",
    "ice_packed": "packed_ice",
    "sponge_wet": "wet_sponge",
    "redstone_lamp_off": "redstone_lamp",
    "torch_on": "torch",
    "redstone_torch_on": "redstone_torch",
    "redstone_torch_off": "redstone_torch_off",
    "piston_top_normal": "piston_top",
    "piston_stop_sticky": None,
    "command_block": ["command_block_side", "command_block_front", "command_block_back"],
    "comparator_off": "comparator",
    "repeater_off": "repeater",
    "furnace_front_off": "furnace_front",
    "anvil_top_damaged_0": "anvil_top",
    "anvil_top_damaged_1": "KEEP",
    "anvil_top_damaged_2": "KEEP",
    "dropper_top_vertical": "KEEP",
    "redstone_dust_cross": "KEEP",
    "redstone_dust_cross_overlay": "redstone_dust_overlay",
    "redstone_dust_line": ["redstone_dust_line0", "redstone_dust_line1"],
    "redstone_dust_line_overlay": "redstone_dust_overlay",
    "trip_wire_source": "KEEP",
    "clay_ball": None,
    "mob_spawner": "spawner",
    "noteblock": "note_block",
    "slime": "slime_block",
    "portal": "nether_portal",
    "flower_paeonia": "KEEP",
    "door_wood_upper": "oak_door_top",
    "door_wood_lower": "oak_door_bottom",
    "door_iron_upper": "iron_door_top",
    "door_iron_lower": "iron_door_bottom",
    "rail_normal": "rail",
    "rail_normal_turned": "rail_corner",
    "rail_detector": "detector_rail",
    "rail_detector_powered": "detector_rail_on",
    "rail_golden": "powered_rail",
    "rail_golden_powered": "powered_rail_on",
    "rail_activator": "activator_rail",
    "rail_activator_powered": "activator_rail_on",
    "trapdoor": "oak_trapdoor",
    "waterlily": "lily_pad",
    "web": "cobweb",
    "deadbush": "dead_bush",
    "tallgrass": "short_grass",
    "reeds": "sugar_cane",
    "prismarine_rough": "prismarine",
    "prismarine_dark": "dark_prismarine",
    "sealantern": "sea_lantern",
    "melon_stem_connected": "attached_melon_stem",
    "melon_stem_disconnected": "melon_stem",
    "pumpkin_stem_connected": "attached_pumpkin_stem",
    "pumpkin_stem_disconnected": "pumpkin_stem",
    "pumpkin_face_off": "carved_pumpkin",
    "pumpkin_face_on": "jack_o_lantern",
    "trip_wire": "tripwire",
    "dispenser_front_horizontal": "dispenser_front",
    "dropper_front_horizontal": "dropper_front",
    "enchanting_table_book": "@entity/enchanting_table_book",
    "itemframe_background": "item_frame",
    "fire_layer_0": None,
    "fire_layer_1": None,
    # water / lava still images
    "water": "water_still",
    "lava": "lava_still",
    # obsolete leftovers in this pack (duplicates / never-loaded names)
    "furnace_front_off 2": None,
    "furnace_front_on2": None,
    "furnace_side2": None,
    "furnace_top2": None,
    "repeater_off copy": None,
    "glass_pane_top_yellow---Copie": None,
    "sandstone_carved2": None,
    "whiteStone": None,
    "enchantment_bottom": None,
    "enchantment_side": None,
    "enchantment_top": None,
    "custom_lava_flowing": None,
    "custom_lava_still": None,
    "custom_water_flowing": None,
    "custom_water_still": None,
})
# flowers / double plants
BLOCK_MAP.update({
    "flower_dandelion": "dandelion",
    "flower_rose": "poppy",
    "flower_blue_orchid": "blue_orchid",
    "flower_houstonia": "azure_bluet",
    "flower_oxeye_daisy": "oxeye_daisy",
    "flower_paeonia": "KEEP",
    "flower_allium": "allium",
    "flower_tulip_orange": "orange_tulip",
    "flower_tulip_pink": "pink_tulip",
    "flower_tulip_red": "red_tulip",
    "flower_tulip_white": "white_tulip",
    "double_plant_fern_bottom": "large_fern_bottom",
    "double_plant_fern_top": "large_fern_top",
    "double_plant_grass_bottom": "tall_grass_bottom",
    "double_plant_grass_top": "tall_grass_top",
    "double_plant_paeonia_bottom": "peony_bottom",
    "double_plant_paeonia_top": "peony_top",
    "double_plant_rose_bottom": "rose_bush_bottom",
    "double_plant_rose_top": "rose_bush_top",
    "double_plant_sunflower_back": "sunflower_back",
    "double_plant_sunflower_bottom": "sunflower_bottom",
    "double_plant_sunflower_front": "sunflower_front",
    "double_plant_sunflower_top": "sunflower_top",
    "double_plant_syringa_bottom": "lilac_bottom",
    "double_plant_syringa_top": "lilac_top",
})
# crop growth stages: carrots_stage_0 -> carrots_stage0
for crop in ("carrots", "potatoes", "nether_wart", "cocoa", "wheat", "beetroots"):
    for i in range(8):
        if crop in ("wheat",):
            BLOCK_MAP[f"wheat_stage_{i}"] = f"wheat_stage{i}"
        else:
            BLOCK_MAP[f"{crop}_stage_{i}"] = f"{crop}_stage{i}"

# --------------------------------------------------------------------------
# ITEM textures  (textures/items -> textures/item)
# --------------------------------------------------------------------------
ITEM_MAP: dict[str, str] = {}
for legacy, modern in COLOR.items():
    ITEM_MAP[f"dye_powder_{legacy}"] = f"{modern}_dye"

ITEM_MAP.update({
    "apple_golden": "golden_apple",
    "bed": "KEEP",
    "beef_cooked": "cooked_beef",
    "beef_raw": "beef",
    "boat": "oak_boat",
    "book_enchanted": "enchanted_book",
    "book_normal": "book",
    "book_writable": "writable_book",
    "book_written": "written_book",
    "bow_standby": "bow",
    "bucket_empty": "bucket",
    "bucket_lava": "lava_bucket",
    "bucket_milk": "milk_bucket",
    "bucket_water": "water_bucket",
    "carrot_golden": "golden_carrot",
    "chicken_cooked": "cooked_chicken",
    "chicken_raw": "chicken",
    "door_iron": "iron_door",
    "door_wood": "oak_door",
    "fireball": "fire_charge",
    "fireworks": "firework_rocket",
    "fireworks_charge": "firework_star",
    "fireworks_charge_overlay": "firework_star_overlay",
    "fish_clownfish_raw": "tropical_fish",
    "fish_cod_cooked": "cooked_cod",
    "fish_cod_raw": "cod",
    "fish_pufferfish_raw": "pufferfish",
    "fish_salmon_cooked": "cooked_salmon",
    "fish_salmon_raw": "salmon",
    "fishing_rod_uncast": "fishing_rod",
    "map_empty": "map",
    "map_filled": "filled_map",
    "melon_speckled": "glistering_melon_slice",
    "minecart_chest": "chest_minecart",
    "minecart_command_block": "command_block_minecart",
    "minecart_furnace": "furnace_minecart",
    "minecart_hopper": "hopper_minecart",
    "minecart_normal": "minecart",
    "minecart_tnt": "tnt_minecart",
    "netherbrick": "nether_brick",
    "porkchop_cooked": "cooked_porkchop",
    "porkchop_raw": "porkchop",
    "potato_baked": "baked_potato",
    "potato_poisonous": "poisonous_potato",
    "potion_bottle_drinkable": "potion",
    "potion_bottle_empty": "glass_bottle",
    "potion_bottle_overlay": "potion_overlay",
    "potion_bottle_splash": "splash_potion",
    "reeds": "sugar_cane",
    "seeds_melon": "melon_seeds",
    "seeds_pumpkin": "pumpkin_seeds",
    "seeds_wheat": "wheat_seeds",
    "sign": "oak_sign",
    "skull_creeper": "KEEP", "skull_skeleton": "KEEP", "skull_steve": "KEEP",
    "skull_wither": "KEEP", "skull_zombie": "KEEP",
    "slimeball": "slime_ball",
    "spider_eye_fermented": "fermented_spider_eye",
    "spawn_egg": "KEEP",
    "melon": "melon_slice",
    "spawn_egg_overlay": "KEEP",
    "wood_axe": "wooden_axe",
    "gold_axe": "golden_axe",
    "gold_boots": "golden_boots",
    "gold_chestplate": "golden_chestplate",
    "gold_helmet": "golden_helmet",
    "gold_hoe": "golden_hoe",
    "gold_horse_armor": "golden_horse_armor",
    "gold_leggings": "golden_leggings",
    "gold_pickaxe": "golden_pickaxe",
    "gold_shovel": "golden_shovel",
    "gold_sword": "golden_sword",

    "wood_hoe": "wooden_hoe",
    "wood_pickaxe": "wooden_pickaxe",
    "wood_shovel": "wooden_shovel",
    "wood_sword": "wooden_sword",
    # leftovers with no modern vanilla equivalent
    "quiver": None,
    "ruby": None,
    "empty_armor_slot_boots": "KEEP",
    "empty_armor_slot_chestplate": "KEEP",
    "empty_armor_slot_helmet": "KEEP",
    "empty_armor_slot_leggings": "KEEP",
})
for n in ("11", "13", "blocks", "cat", "chirp", "far", "mall", "mellohi",
          "stal", "strad", "wait", "ward"):
    ITEM_MAP[f"record_{n}"] = f"music_disc_{n}"

# --------------------------------------------------------------------------
# ENTITY textures
# --------------------------------------------------------------------------
ENTITY_MAP = {
    "endercrystal/endercrystal": "end_crystal/end_crystal",
    "endercrystal/endercrystal_beam": "end_crystal/end_crystal_beam",
    "zombie_pigman": "piglin/zombified_piglin",
    "cow/cow": ["cow/temperate_cow", "cow/cold_cow", "cow/warm_cow"],
    "cow/mooshroom": ["cow/red_mooshroom", "cow/brown_mooshroom"],
    "steve": "player/wide/steve",
    "snowman": "snow_golem",
    "chicken": ["chicken/temperate_chicken", "chicken/cold_chicken", "chicken/warm_chicken"],
    "pig/pig": ["pig/temperate_pig", "pig/cold_pig", "pig/warm_pig"],
    "pig/pig_saddle": "equipment/pig_saddle/saddle",
    "squid": "squid/squid",
    "zombie/zombie_villager": "zombie_villager/zombie_villager",
    "iron_golem": "iron_golem/iron_golem",
    "sign": "signs/oak",
    "boat": "boat/oak",
    "experience_orb": "experience_orb",
    "lead_knot": "lead_knot",
    "explosion": None,          # no longer a texture in 1.21.x
    "arrow": None,              # moved to entity/projectiles/arrow.png (handled below)
    "sheep/sheep_fur": "sheep/sheep_wool",
    "horse/armor/horse_armor_iron": "equipment/horse_body/iron",
    "horse/armor/horse_armor_gold": "equipment/horse_body/gold",
    "horse/armor/horse_armor_diamond": "equipment/horse_body/diamond",
    "villager/butcher": "villager/profession/butcher",
    "villager/farmer": "villager/profession/farmer",
    "villager/librarian": "villager/profession/librarian",
    "villager/priest": "villager/profession/cleric",
    "villager/smith": "villager/profession/weaponsmith",
    "villager/villager": "villager/type/plains",
    "chest/normal_double": "KEEP",
    "chest/christmas_double": "KEEP",
    "chest/trapped_double": "KEEP",
    "chest/ender_double": "KEEP",
}
ENTITY_MAP["arrow"] = "projectiles/arrow"

# models/armor/<material>_layer_N.png -> entity/equipment/...
ARMOR_MAP = {
    "leather_layer_1": "equipment/humanoid/leather",
    "leather_layer_1_overlay": "equipment/humanoid/leather_overlay",
    "leather_layer_2": "equipment/humanoid_leggings/leather",
    "leather_layer_2_overlay": "equipment/humanoid_leggings/leather_overlay",
    "chainmail_layer_1": "equipment/humanoid/chainmail",
    "chainmail_layer_2": "equipment/humanoid_leggings/chainmail",
    "iron_layer_1": "equipment/humanoid/iron",
    "iron_layer_2": "equipment/humanoid_leggings/iron",
    "gold_layer_1": "equipment/humanoid/gold",
    "gold_layer_2": "equipment/humanoid_leggings/gold",
    "diamond_layer_1": "equipment/humanoid/diamond",
    "diamond_layer_2": "equipment/humanoid_leggings/diamond",
}

# --------------------------------------------------------------------------
# mcpatcher/ -> optifine/  (paths modern OptiFine / Continuity / Fusion read)
# --------------------------------------------------------------------------
OTHER_MAP = {
    "textures/environment/sun": "textures/environment/celestial/sun",
    "textures/misc/enchanted_item_glint": "textures/misc/enchanted_glint_item",
}

# legacy animated item strips now shipped as one file per frame
STRIP_SLICES = {
    "textures/items/clock.png":   ("textures/item", "clock_", 64),
    "textures/items/compass.png": ("textures/item", "compass_", 32),
}

MCPATCHER_MAP = {
    "mcpatcher/anim": "KEEP",             # legacy custom animation format, kept as-is
    "mcpatcher/color.properties": "optifine/color.properties",
    "mcpatcher/colormap": "optifine/colormap",
    "mcpatcher/ctm": "optifine/ctm",
    "mcpatcher/font": None,               # duplicate of textures/font
    "mcpatcher/lightmap": "optifine/lightmap",
    "mcpatcher/sky": "optifine/sky",
}

JUNK = {"thumbs.db", ".ds_store", "desktop.ini"}


def shape_of(path: Path):
    try:
        with open(path, "rb") as fh:
            head = fh.read(26)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return struct.unpack(">II", head[16:24])
    except OSError:
        return None


class Porter:
    def __init__(self, src: Path, out: Path, vanilla: set[str] | None,
                 pack_format: int, min_format, max_format):
        self.src = src
        self.out = out
        self.vanilla = vanilla
        self.pack_format = pack_format
        self.min_format = min_format
        self.max_format = max_format
        self.mapped: list[tuple[str, str]] = []
        self.identity: list[str] = []
        self.dropped: list[tuple[str, str]] = []
        self.unknown: list[str] = []
        self.missing_target: list[tuple[str, str]] = []
        self.kept_legacy: list[tuple[str, str]] = []
        self.collisions: list[tuple[str, str, str]] = []
        self.written: set[str] = set()

    # ---------------- helpers ----------------
    def exists_in_vanilla(self, rel: str) -> bool:
        if not self.vanilla:
            return True
        if rel.startswith("assets/minecraft/"):
            rel = rel[len("assets/minecraft/"):]
        return f"assets/minecraft/{rel}" in self.vanilla

    def write(self, rel: str, data: bytes, src_rel: str = ""):
        dest = self.out / rel
        if rel in self.written:
            self.collisions.append((rel, src_rel, "already written"))
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        self.written.add(rel)

    def copy(self, src_file: Path, rel_dest: str, src_rel: str):
        if rel_dest in self.written:
            self.collisions.append((rel_dest, src_rel, "destination taken"))
            return
        dest = self.out / rel_dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest)
        self.written.add(rel_dest)

    # ---------------- top level ----------------
    def run(self, want_fonts: bool):
        assets = self.src / "assets" / "minecraft"
        for path in sorted(assets.rglob("*")):
            if path.is_dir():
                continue
            if path.name.lower() in JUNK:
                self.dropped.append((str(path.relative_to(self.src)), "OS junk file"))
                continue
            rel = str(path.relative_to(assets)).replace("\\", "/")
            if rel in STRIP_SLICES:
                self.slice_strip(path, rel, *STRIP_SLICES[rel])
            elif rel in (k + ".mcmeta" for k in STRIP_SLICES):
                self.dropped.append((rel, "animation metadata no longer needed - the strip is sliced into frames"))
            elif rel.startswith("textures/blocks/"):
                self.do_texture(path, rel, rel[len("textures/blocks/"):], "textures/block", BLOCK_MAP)
            elif rel.startswith("textures/items/"):
                self.do_texture(path, rel, rel[len("textures/items/"):], "textures/item", ITEM_MAP)
            elif rel.startswith("textures/entity/"):
                self.do_texture(path, rel, rel[len("textures/entity/"):], "textures/entity", ENTITY_MAP,
                                extra_map=ARMOR_MAP, extra_prefix="textures/models/armor/")
            elif rel.startswith("textures/models/armor/"):
                name = rel[len("textures/models/armor/"):]
                self.do_texture(path, rel, name, "textures/models/armor/", ARMOR_MAP)
            elif rel.startswith("mcpatcher/"):
                self.do_mcpatcher(path, rel)
            else:
                self.do_other(path, rel)
        if want_fonts:
            self.write_font_json()
        self.write_mcmeta()
        # copy pack.png / any other root files
        for extra in ("pack.png",):
            p = self.src / extra
            if p.exists():
                shutil.copy2(p, self.out / extra)

    # ---------------- per-area handlers ----------------
    def do_texture(self, path: Path, src_rel: str, name: str, legacy_dir: str,
                   table: dict, extra_map: dict | None = None, extra_prefix: str = ""):
        """name is relative to legacy_dir, e.g. 'wool_colored_red.png' or 'wolf/wolf.png'"""
        suffix = ""
        base = name
        for ext in (".png.mcmeta", ".mcmeta", ".png"):
            if base.endswith(ext):
                base, suffix = base[:-len(ext)], ext
                break
        else:
            self.unknown.append(src_rel)
            return

        key = base
        raw = "__ABSENT__"
        if key in table:
            raw = table[key]
        elif extra_map and key in extra_map:
            raw = extra_map[key]

        if raw == "__ABSENT__":
            # no rule: keep the same name if modern vanilla has it
            rel_dest = f"assets/minecraft/{legacy_dir}/{key}{suffix}"
            if self.exists_in_vanilla(self.probe(rel_dest, suffix)):
                self.identity.append(rel_dest)
                self.copy(path, rel_dest, src_rel)
            else:
                self.keep_legacy(path, src_rel)
            return

        if raw is None:
            self.dropped.append((src_rel, "obsolete name / duplicate with no modern path"))
            return
        if raw == "KEEP":
            self.keep_legacy(path, src_rel)
            return

        dests = raw if isinstance(raw, (list, tuple)) else [raw]
        for dest in dests:
            if dest.startswith("@entity/"):
                rel_dest = f"assets/minecraft/textures/entity/{dest[len('@entity/'):]}{suffix}"
            elif legacy_dir == "textures/models/armor/":
                rel_dest = f"assets/minecraft/textures/entity/{dest}{suffix}"
            else:
                rel_dest = f"assets/minecraft/{legacy_dir}/{dest}{suffix}"
            if not self.exists_in_vanilla(self.probe(rel_dest, suffix)):
                self.missing_target.append((src_rel, rel_dest))
                continue
            self.mapped.append((src_rel, rel_dest))
            self.copy(path, rel_dest, src_rel)

    @staticmethod
    def probe(rel_dest: str, suffix: str) -> str:
        """.mcmeta sidecars may accompany a texture that exists - validate the texture."""
        if suffix in (".mcmeta", ".png.mcmeta"):
            return rel_dest[: -len(suffix)] + ".png"
        return rel_dest

    def keep_legacy(self, path: Path, src_rel: str):
        self.kept_legacy.append((src_rel, "no 1:1 modern equivalent - kept at legacy path"))
        self.copy(path, "assets/minecraft/" + src_rel.replace(os.sep, "/"), src_rel)

    def slice_strip(self, path: Path, src_rel: str, dest_dir: str, prefix: str, frames: int):
        """legacy animated texture strip (N frames stacked vertically) -> modern one file per frame"""
        try:
            from PIL import Image
        except ImportError:
            self.kept_legacy.append((src_rel, "needs Pillow to slice the animation strip (pip install pillow)"))
            self.copy(path, "assets/minecraft/" + src_rel, src_rel)
            return
        img = Image.open(path).convert("RGBA")
        frame_h = img.height // frames
        if frame_h * frames != img.height:
            self.kept_legacy.append((src_rel, f"strip height {img.height} is not divisible into {frames} frames"))
            self.copy(path, "assets/minecraft/" + src_rel, src_rel)
            return
        for i in range(frames):
            frame = img.crop((0, i * frame_h, img.width, (i + 1) * frame_h))
            rel_dest = f"assets/minecraft/{dest_dir}/{prefix}{i:02d}.png"
            dest = self.out / rel_dest
            dest.parent.mkdir(parents=True, exist_ok=True)
            frame.save(dest)
            self.written.add(rel_dest)
        self.mapped.append((src_rel, f"{dest_dir}/{prefix}00..{prefix}{frames-1:02d}.png ({frames} frames)"))

    def do_mcpatcher(self, path: Path, rel: str):
        sub = rel[len("mcpatcher/"):].split("/")[0]
        new = MCPATCHER_MAP.get(f"mcpatcher/{sub}", "UNSET")
        if new == "KEEP":
            self.kept_legacy.append((rel, f"legacy mcpatcher/{sub} kept as-is"))
            self.copy(path, f"assets/minecraft/{rel}", rel)
            return
        if new is None:
            self.dropped.append((rel, f"legacy mcpatcher/{sub} has no modern vanilla equivalent"))
            return
        rel_dest = f"assets/minecraft/{new}/" + "/".join(rel.split("/")[2:])
        self.mapped.append((rel, rel_dest))
        self.copy(path, rel_dest, rel)

    def do_other(self, path: Path, rel: str):
        """textures/{gui,misc,environment,font,map,painting,particle} and everything else"""
        # split name for potential png / mcmeta handling
        base, suffix = rel, ""
        for ext in (".png.mcmeta", ".mcmeta", ".png"):
            if rel.endswith(ext):
                base, suffix = rel[:-len(ext)], ext
                break
        new_base = OTHER_MAP.get(base, base)
        rel_dest = f"assets/minecraft/{new_base}{suffix}"
        is_font = new_base.startswith("textures/font/")
        if self.exists_in_vanilla(f"{new_base}{suffix}") or is_font:
            if new_base != base:
                self.mapped.append((rel, rel_dest))
            else:
                self.identity.append(rel_dest)
            self.copy(path, rel_dest, rel)
        else:
            self.kept_legacy.append((rel, "no modern vanilla path (GUI/HUD sheets are individual sprites now)"))
            self.copy(path, f"assets/minecraft/{rel}", rel)

    # ---------------- generated files ----------------
    def write_font_json(self):
        """Legacy unicode_page_*.png sheets are only usable via bitmap providers
        (the legacy_unicode provider was removed in 1.20), and the pack's sheets are
        2x resolution, so glyph metrics must be stated explicitly or text renders
        double size."""
        fontdir = self.out / "assets" / "minecraft" / "textures" / "font"
        if not fontdir.exists():
            return
        pages = sorted(fontdir.glob("unicode_page_*.png"))
        ascii_sheet = (fontdir / "ascii.png").exists()
        reported = []

        providers = [{"type": "reference", "id": "minecraft:include/space"}]
        if ascii_sheet:
            providers.append({"type": "bitmap", "file": "minecraft:font/ascii.png",
                              "height": 8, "ascent": 7})
            reported.append("ascii.png @ 8px (2x art)")

        # vanilla providers fill in accented / nonlatin glyphs we do not ship
        providers.append({"type": "reference", "id": "minecraft:include/default"})

        for page in pages:
            try:
                page_no = int(page.stem.split("_")[-1], 16)
            except ValueError:
                continue
            if 0xD8 <= page_no <= 0xDF:      # surrogate pages are not addressable
                continue
            chars = ["".join(chr(page_no * 256 + row * 16 + col) for col in range(16))
                     for row in range(16)]
            providers.append({
                "type": "bitmap",
                "file": f"minecraft:font/{page.stem}.png",
                "height": 8,
                "ascent": 7,
                "chars": chars,
            })
        providers.append({"type": "reference", "id": "minecraft:include/unifont"})

        (self.out / "assets" / "minecraft" / "font").mkdir(parents=True, exist_ok=True)
        (self.out / "assets" / "minecraft" / "font" / "default.json").write_text(
            json.dumps({"providers": providers}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        # the galactic-alphabet font references our 2x ascii_sga.png, so pin its metrics too
        if (fontdir / "ascii_sga.png").exists():
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            rows = []
            for r in range(16):
                row = []
                for c in range(16):
                    ch = "\u0000"
                    if r == 4 and 1 <= c <= 15:
                        ch = letters[c - 1]
                    elif r == 5 and 1 <= c <= 11:
                        ch = letters[15 + c - 1]
                    elif r == 6 and 1 <= c <= 15:
                        ch = letters[c - 1].lower()
                    elif r == 7 and 1 <= c <= 11:
                        ch = letters[15 + c - 1].lower()
                    row.append(ch)
                rows.append("".join(row))
            alt = {"providers": [
                {"type": "reference", "id": "minecraft:include/space"},
                {"type": "bitmap", "file": "minecraft:font/ascii_sga.png",
                 "height": 8, "ascent": 7, "chars": rows},
            ]}
            (self.out / "assets" / "minecraft" / "font" / "alt.json").write_text(
                json.dumps(alt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            reported.append("ascii_sga.png via font/alt.json @ 8px")

        reported.append(f"{len(pages)} unicode_page sheets @ 8px")
        self.mapped.append(("<generated>", "assets/minecraft/font/default.json - " + ", ".join(reported)))

    def write_mcmeta(self):
        desc = "§eBy: §dTanjiroCraft §7on §fYou§cTube"
        old = self.src / "pack.mcmeta"
        if old.exists():
            try:
                desc = json.loads(old.read_text(encoding="utf-8-sig"))["pack"].get("description", desc)
            except Exception:
                pass
        mcmeta = {
            "pack": {
                "pack_format": self.pack_format,
                "min_format": [self.pack_format, 0],
                "max_format": self.max_format,
                "description": desc,
            }
        }
        (self.out / "pack.mcmeta").write_text(json.dumps(mcmeta, ensure_ascii=False, indent=2) + "\n",
                                              encoding="utf-8")

    # ---------------- report ----------------
    def report(self, target_desc: str) -> str:
        L = []
        L.append("# Legacy pack -> modern port report\n")
        L.append(f"* source: `{self.src}`")
        L.append(f"* output: `{self.out}`")
        L.append(f"* target: {target_desc}\n")
        L.append(f"| bucket | files |\n|---|---|")
        L.append(f"| moved + renamed to modern path | {len(self.mapped)} |")
        L.append(f"| already at a valid modern path | {len(self.identity)} |")
        L.append(f"| left out (no equivalent / junk) | {len(self.dropped)} |")
        L.append(f"| **unresolved** | {len(self.unknown)} |")
        L.append(f"| kept at legacy path (not read by target) | {len(self.kept_legacy)} |")
        L.append(f"| name collisions | {len(self.collisions)} |")
        if self.missing_target:
            L.append("\n## Mapped to a name that does not exist in the target version\n")
            for src, dest in self.missing_target:
                L.append(f"* `{src}` -> `{dest}` (dropped)")
        if self.kept_legacy:
            L.append(f"\n## Kept in the pack but not read by 1.21.11 ({len(self.kept_legacy)} files)\n")
            L.append("These have no direct modern path (mostly pre-1.20.2 GUI sheets / sprite sheets). "
                     "They are copied unchanged so nothing is lost; porting them needs slicing into "
                     "individual sprites.\n")
            for src, why in self.kept_legacy:
                L.append(f"* `{src}` - {why}")
        if self.unknown:
            L.append("\n## Unresolved files (kept in the original pack, not written out)\n")
            for u in self.unknown:
                L.append(f"* `{u}`")
        if self.dropped:
            L.append("\n## Left out\n")
            for src, why in self.dropped:
                L.append(f"* `{src}` - {why}")
        if self.collisions:
            L.append("\n## Collisions (second file skipped)\n")
            for dest, src, why in self.collisions:
                L.append(f"* `{dest}` <- `{src}` ({why})")
        return "\n".join(L) + "\n"


def load_vanilla(path: str | None) -> set[str] | None:
    if not path:
        return None
    with open(path, encoding="utf-8") as fh:
        return {line.strip() for line in fh if line.strip()}


def make_zip(pack_dir: Path, zip_path: Path):
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(pack_dir.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(pack_dir))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Port a legacy resource pack to a modern Minecraft version")
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pack-format", type=int, default=75)
    ap.add_argument("--max-format", default="86,0")
    ap.add_argument("--vanilla-paths")
    ap.add_argument("--fonts", action="store_true", help="generate font/default.json for legacy unicode pages")
    ap.add_argument("--report")
    ap.add_argument("--zip")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    src, out = Path(args.src), Path(args.out)
    if out.exists():
        if not args.force:
            sys.exit(f"output {out} exists (use --force)")
        shutil.rmtree(out)
    out.mkdir(parents=True)

    max_format = [int(x) for x in args.max_format.split(",")]
    porter = Porter(src, out, load_vanilla(args.vanilla_paths), args.pack_format, None, max_format)
    porter.run(args.fonts)

    report = porter.report(f"Minecraft Java 1.21.11 (resource pack format {args.pack_format})")
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
    print(report)
    if args.zip:
        make_zip(out, Path(args.zip))
        print(f"\nwrote {args.zip} ({Path(args.zip).stat().st_size/1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
