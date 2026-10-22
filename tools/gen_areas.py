"""Generate the YAML for 12 configurable areas: HA settings (text + select) and the Areas page rows.

usage: gen_areas.py <out-dir>   writes cfg_entities.yaml, icon_selects.yaml, area_rows.yaml
"""
import os
import sys

out = sys.argv[1]

# (name, icon option, lights, scenes, sensors) as the panel has them today
AREAS = [
    ("Kitchen", "Kitchen", "light.kokken_spots, light.spisebord_kokken",
     "scene.kokken_50_50, scene.aftensmad, scene.kokken_morgen",
     "climate.danfoss_icon_2_gulvvarme_7, sensor.danfoss_icon_2_gulvvarme_humidity_7"),
    ("Living Room", "Living room",
     "light.stue_lights_effective, light.stue_bord_lampe, light.stue_gulv_lampe, light.stander_lampe",
     "scene.normal_stue, scene.hygge, scene.stue_amme_scene",
     "climate.danfoss_icon_2_gulvvarme_9, sensor.danfoss_icon_2_gulvvarme_humidity_9"),
    ("sove værelse", "Bedroom",
     "light.sovevaerelse_leklint, light.sovevaerelse_loft_lampe_white, light.sovevaerelse_loft_lampe_rgb", "",
     "sensor.alpstuga_air_quality_monitor_temperature_2, sensor.alpstuga_air_quality_monitor_humidity_2, "
     "sensor.alpstuga_air_quality_monitor_carbon_dioxide_2"),
    ("badeværelse stort", "Bathroom", "light.badevaerelse_stort_spots", "",
     "climate.danfoss_icon_2_gulvvarme_11, sensor.danfoss_icon_2_gulvvarme_humidity_11"),
    ("kontor", "Office", "light.kontor_loft_lampe_white, light.kontor_loft_lampe_rgb", "",
     "sensor.alpstuga_air_quality_monitor_temperature, sensor.alpstuga_air_quality_monitor_humidity, "
     "sensor.alpstuga_air_quality_monitor_carbon_dioxide"),
    ("bryggers", "Laundry", "light.bryggers_loft_z2m_group", "",
     "climate.danfoss_icon_2_gulvvarme_2, sensor.danfoss_icon_2_gulvvarme_humidity_2"),
    ("værelse 1 vejen", "Bed", "light.vaerelse_1_vejen_paere, light.vaerelse_1_vejen_bord_lampe", "",
     "climate.danfoss_icon_2_gulvvarme_6, sensor.danfoss_icon_2_gulvvarme_humidity_6"),
    ("værelse 2 have", "Bed", "light.vaerelse_2_haven_paere", "",
     "climate.danfoss_icon_2_gulvvarme_3, sensor.danfoss_icon_2_gulvvarme_humidity_3"),
    ("entre", "Box", "light.entre, light.entre_spots_mqtt", "",
     "climate.danfoss_icon_2_gulvvarme_4, sensor.danfoss_icon_2_gulvvarme_humidity_4"),
    ("garage", "Garage", "light.garage_2, light.garage_paneler_z2m_group", "",
     "climate.danfoss_icon_2_gulvvarme_1, sensor.danfoss_icon_2_gulvvarme_humidity_1"),
    ("terrasse baghave", "Box", "light.lys_udhaeng_tresse", "", ""),
    ("indkørsel", "Box", "light.lys_udhaeng_indkorsel", "", ""),
]

# Icon options (same order as the glyph table in cfg_apply)
ICONS = [
    ("Box", "F0FE6"), ("Home", "F02DC"), ("Kitchen", "F0290"), ("Dining", "F0A70"),
    ("Living room", "F04B9"), ("TV", "F0502"), ("Bedroom", "F0FD4"), ("Bed", "F02E3"),
    ("Toys", "F1288"), ("Bathroom", "F09AB"), ("Shower", "F09A0"), ("Bathtub", "F1818"),
    ("Office", "F0F48"), ("Desk", "F1239"), ("Laundry", "F072A"), ("Wardrobe", "F0F90"),
    ("Hallway", "F081A"), ("Entrance", "F081C"), ("Stairs", "F04CD"), ("Garage", "F06D9"),
    ("Car", "F010B"), ("Garden", "F0531"), ("Flowers", "F024A"), ("Terrace", "F1817"),
    ("Outdoor lamp", "F1054"), ("Gate", "F0299"), ("Pool", "F0606"), ("Gym", "F01E6"),
    ("Lamp", "F06B5"), ("Ceiling light", "F0769"),
]
NAMES = [n for n, _ in ICONS]


def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ---- text entities
t = []
for i, (name, icon, lights, scenes, sensors) in enumerate(AREAS, start=1):
    first = i == 1
    for key, label, mdi, maxlen, init in (
        ("name", "name", "mdi:form-textbox", 40, name),
        ("lights", "lights", "mdi:lightbulb-group", 255, lights),
        ("scenes", "scenes", "mdi:palette", 255, scenes),
        ("sensors", "sensors", "mdi:thermometer", 255, sensors),
    ):
        t.append(f"  - platform: template\n")
        t.append(f"    id: a{i}_{key}\n")
        t.append(f"    name: \"Area {i} {label}\"\n")
        t.append(f"    icon: {mdi}\n")
        t.append(f"    mode: text\n")
        t.append(f"    max_length: {maxlen}\n")
        t.append(f"    initial_value: {q(init)}\n")
        t.append(f"    optimistic: true\n")
        t.append(f"    restore_value: true\n")
        t.append(f"    entity_category: config\n")
        if first and key == "name":
            t.append(f"    on_value: &area_cfg_changed\n")
            t.append(f"      - script.execute: cfg_changed\n")
        else:
            t.append(f"    on_value: *area_cfg_changed\n")
open(os.path.join(out, "cfg_entities.yaml"), "w", encoding="utf-8", newline="\n").write("".join(t))

# ---- icon selects
s = []
for i, (name, icon, *_rest) in enumerate(AREAS, start=1):
    assert icon in NAMES, icon
    s.append(f"  - platform: template\n")
    s.append(f"    id: a{i}_icon\n")
    s.append(f"    name: \"Area {i} icon\"\n")
    s.append(f"    icon: mdi:shape\n")
    s.append(f"    entity_category: config\n")
    s.append(f"    optimistic: true\n")
    s.append(f"    restore_value: true\n")
    s.append(f"    initial_option: {q(icon)}\n")
    if i == 1:
        s.append(f"    options: &area_icons\n")
        for n in NAMES:
            s.append(f"      - {q(n)}\n")
    else:
        s.append(f"    options: *area_icons\n")
    s.append(f"    on_value: *area_cfg_changed\n")
open(os.path.join(out, "icon_selects.yaml"), "w", encoding="utf-8", newline="\n").write("".join(s))

# ---- Areas page rows
r = []
for k in range(12):
    r.append(f"""              # ---- area {k + 1}
              - obj:
                  id: ar_row{k}
                  styles: row_style
                  width: 100%
                  height: 61
                  scrollable: false
                  layout: {{ type: FLEX, flex_flow: ROW, flex_align_cross: CENTER, flex_align_track: CENTER }}
                  on_press:
                    - script.execute: use_area_hold
                  on_short_click:
                    - script.execute: {{ id: area_tap, idx: {k} }}
                  on_long_press:
                    - script.execute: {{ id: open_area, idx: {k} }}
                  widgets:
                    - label: {{ id: ar_icon{k}, styles: area_icon, text: "\\U000F0FE6" }}
                    - obj:
                        styles: plain
                        flex_grow: 1
                        height: SIZE_CONTENT
                        scrollable: false
                        clickable: false
                        layout: {{ type: FLEX, flex_flow: COLUMN, pad_row: 2 }}
                        widgets:
                          - label: {{ id: ar_name{k}, styles: area_name, text: "", width: 100%, long_mode: DOT }}
                          - label: {{ id: ar_sub{k}, styles: area_sub, text: "", width: 100%, long_mode: DOT }}
                    - button:
                        id: ar_btn{k}
                        width: 72
                        height: 48
                        clickable: false
                        widgets:
                          - label: {{ id: ar_bulb{k}, styles: bulb_icon, align: CENTER, text: "\\U000F0E50" }}
""")
    if k < 11:
        r.append("\n")
open(os.path.join(out, "area_rows.yaml"), "w", encoding="utf-8", newline="\n").write("".join(r))

# glyph table for the lambda and the font
print("glyphs:", ", ".join(f'"\\U000{g}"' for _, g in ICONS))
for n, g in ICONS:
    print(f'      - "\\U000{g}" # {n}')
