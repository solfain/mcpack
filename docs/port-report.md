# Legacy pack -> modern port report

* source: `build/vermeil`
* output: `build/port`
* target: Minecraft Java 1.21.11 (resource pack format 75)

| bucket | files |
|---|---|
| moved + renamed to modern path | 461 |
| already at a valid modern path | 545 |
| left out (no equivalent / junk) | 259 |
| **unresolved** | 0 |
| kept at legacy path (not read by target) | 49 |
| name collisions | 3 |

## Kept in the pack but not read by 1.21.11 (49 files)

These have no direct modern path (mostly pre-1.20.2 GUI sheets / sprite sheets). They are copied unchanged so nothing is lost; porting them needs slicing into individual sprites.

* `mcpatcher/anim/Inventario.properties` - legacy mcpatcher/anim kept as-is
* `mcpatcher/anim/tangiro.png` - legacy mcpatcher/anim kept as-is
* `textures/blocks/anvil_top_damaged_1.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/anvil_top_damaged_2.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/bed_feet_end.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/bed_feet_side.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/bed_feet_top.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/bed_head_end.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/bed_head_side.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/bed_head_top.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/coal_ore.png - Copy.mcmeta` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/dropper_top_vertical.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/flower_paeonia.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/leaves_acacia_opaque.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/leaves_big_oak_opaque.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/leaves_birch_opaque.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/leaves_jungle_opaque.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/leaves_oak_opaque.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/leaves_spruce_opaque.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/redstone_dust_cross.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/blocks/trip_wire_source.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/entity/chest/christmas_double.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/entity/chest/normal_double.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/entity/chest/trapped_double.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/environment/moon_phases.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/gui/achievement/achievement_background.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/gui/achievement/achievement_icons.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/gui/container/creative_inventory/tabs.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/gui/container/stats_icons.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/gui/icons.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/gui/options_background.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/gui/widgets.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/items/bed.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/empty_armor_slot_boots.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/empty_armor_slot_chestplate.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/empty_armor_slot_helmet.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/empty_armor_slot_leggings.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/redstone_dust.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/skull_creeper.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/skull_skeleton.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/skull_steve.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/skull_wither.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/skull_zombie.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/spawn_egg.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/items/spawn_egg_overlay.png` - no 1:1 modern equivalent - kept at legacy path
* `textures/map/map_icons.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/painting/paintings_kristoffer_zetterstrand.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/particle/footprint.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)
* `textures/particle/particles.png` - no modern vanilla path (GUI/HUD sheets are individual sprites now)

## Left out

* `assets/minecraft/mcpatcher/ctm/.DS_Store` - OS junk file
* `assets/minecraft/mcpatcher/ctm/glass/.DS_Store` - OS junk file
* `assets/minecraft/mcpatcher/font/Thumbs.db` - OS junk file
* `mcpatcher/font/ascii.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/ascii_sga.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_00.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_01.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_02.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_03.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_04.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_05.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_06.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_07.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_09.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_0a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_0b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_0c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_0d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_0e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_0f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_10.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_11.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_12.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_13.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_14.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_15.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_16.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_17.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_18.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_19.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_1a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_1b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_1c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_1d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_1e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_1f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_20.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_21.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_22.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_23.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_24.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_25.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_26.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_27.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_28.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_29.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_2a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_2b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_2c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_2d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_2e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_2f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_30.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_31.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_32.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_33.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_34.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_35.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_36.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_37.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_38.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_39.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_3a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_3b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_3c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_3d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_3e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_3f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_40.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_41.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_42.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_43.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_44.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_45.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_46.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_47.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_48.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_49.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_4a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_4b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_4c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_4d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_4e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_4f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_50.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_51.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_52.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_53.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_54.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_55.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_56.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_57.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_58.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_59.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_5a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_5b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_5c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_5d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_5e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_5f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_60.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_61.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_62.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_63.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_64.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_65.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_66.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_67.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_68.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_69.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_6a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_6b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_6c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_6d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_6e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_6f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_70.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_71.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_72.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_73.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_74.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_75.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_76.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_77.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_78.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_79.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_7a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_7b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_7c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_7d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_7e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_7f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_80.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_81.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_82.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_83.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_84.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_85.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_86.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_87.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_88.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_89.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_8a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_8b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_8c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_8d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_8e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_8f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_90.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_91.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_92.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_93.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_94.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_95.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_96.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_97.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_98.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_99.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_9a.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_9b.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_9c.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_9d.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_9e.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_9f.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a0.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a1.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a2.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a3.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a4.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a5.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a6.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a7.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a8.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_a9.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_aa.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ab.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ac.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ad.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ae.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_af.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b0.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b1.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b2.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b3.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b4.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b5.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b6.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b7.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b8.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_b9.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ba.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_bb.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_bc.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_bd.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_be.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_bf.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c0.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c1.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c2.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c3.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c4.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c5.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c6.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c7.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c8.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_c9.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ca.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_cb.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_cc.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_cd.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ce.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_cf.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d0.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d1.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d2.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d3.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d4.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d5.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d6.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_d7.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_f9.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_fa.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_fb.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_fc.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_fd.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_fe.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `mcpatcher/font/unicode_page_ff.png` - legacy mcpatcher/font has no modern vanilla equivalent
* `assets/minecraft/mcpatcher/lightmap/.DS_Store` - OS junk file
* `assets/minecraft/mcpatcher/sky/world0/Thumbs.db` - OS junk file
* `assets/minecraft/textures/blocks/Thumbs.db` - OS junk file
* `textures/blocks/clay_ball.png` - obsolete name / duplicate with no modern path
* `textures/blocks/custom_lava_flowing.png` - obsolete name / duplicate with no modern path
* `textures/blocks/custom_lava_still.png` - obsolete name / duplicate with no modern path
* `textures/blocks/custom_water_flowing.png` - obsolete name / duplicate with no modern path
* `textures/blocks/custom_water_still.png` - obsolete name / duplicate with no modern path
* `textures/blocks/enchantment_bottom.png` - obsolete name / duplicate with no modern path
* `textures/blocks/enchantment_side.png` - obsolete name / duplicate with no modern path
* `textures/blocks/enchantment_top.png` - obsolete name / duplicate with no modern path
* `textures/blocks/fire_layer_0.png` - obsolete name / duplicate with no modern path
* `textures/blocks/fire_layer_0.png.mcmeta` - obsolete name / duplicate with no modern path
* `textures/blocks/fire_layer_1.png` - obsolete name / duplicate with no modern path
* `textures/blocks/fire_layer_1.png.mcmeta` - obsolete name / duplicate with no modern path
* `textures/blocks/furnace_front_off 2.png` - obsolete name / duplicate with no modern path
* `textures/blocks/furnace_front_on2.png` - obsolete name / duplicate with no modern path
* `textures/blocks/furnace_side2.png` - obsolete name / duplicate with no modern path
* `textures/blocks/furnace_top2.png` - obsolete name / duplicate with no modern path
* `textures/blocks/glass_pane_top_yellow---Copie.png` - obsolete name / duplicate with no modern path
* `textures/blocks/piston_stop_sticky.png` - obsolete name / duplicate with no modern path
* `textures/blocks/repeater_off copy.png` - obsolete name / duplicate with no modern path
* `textures/blocks/sandstone_carved2.png` - obsolete name / duplicate with no modern path
* `textures/blocks/whiteStone.png` - obsolete name / duplicate with no modern path
* `textures/entity/explosion.png` - obsolete name / duplicate with no modern path
* `assets/minecraft/textures/font/Thumbs.db` - OS junk file
* `textures/items/clock.png.mcmeta` - animation metadata no longer needed - the strip is sliced into frames
* `textures/items/compass.png.mcmeta` - animation metadata no longer needed - the strip is sliced into frames
* `assets/minecraft/textures/items/desktop.ini` - OS junk file
* `textures/items/quiver.png` - obsolete name / duplicate with no modern path
* `textures/items/ruby.png` - obsolete name / duplicate with no modern path
* `assets/minecraft/textures/models/armor/Thumbs.db` - OS junk file

## Collisions (second file skipped)

* `assets/minecraft/textures/block/lava_still.png` <- `textures/blocks/lava_still.png` (destination taken)
* `assets/minecraft/textures/block/redstone_dust_overlay.png` <- `textures/blocks/redstone_dust_line_overlay.png` (destination taken)
* `assets/minecraft/textures/block/water_still.png` <- `textures/blocks/water_still.png` (destination taken)
