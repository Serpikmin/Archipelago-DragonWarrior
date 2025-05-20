from typing import Dict, Set
from BaseClasses import Location
import names


class DWLocation(Location):
    game = "Dragon Warrior"

throne_room_locations = {
    names.tantegel_throne_room_gold_chest: 0x001,
    names.tantegel_throne_room_key_chest: 0x002,
    names.tantegel_throne_room_torch_chest: 0x003,
}

tantegel_castle_locations = {
    names.tantegel_castle_gold_chest_1: 0x004,
    names.tantegel_castle_gold_chest_2: 0x005,
    names.tantegel_castle_gold_chest_3: 0x006,
    names.tantegel_castle_gold_chest_4: 0x007,
    names.tantegel_castle_basement: 0x008,
}

brecconary_locations = {
    names.brecconary_equip_shop_1: 0x009,
    names.brecconary_equip_shop_2: 0x00A,
    names.brecconary_equip_shop_3: 0x00B,
    names.brecconary_equip_shop_4: 0x00C,
    names.brecconary_equip_shop_5: 0x00D,
    names.brecconary_equip_shop_6: 0x00E,

    names.brecconary_item_shop_1: 0x00F,
    names.brecconary_item_shop_2: 0x010,
    names.brecconary_item_shop_3: 0x011,

    names.brecconary_fairy_water: 0x012,
}

garinham_locations = {
    names.garinham_equip_shop_1: 0x013,
    names.garinham_equip_shop_2: 0x014,
    names.garinham_equip_shop_3: 0x015,
    names.garinham_equip_shop_4: 0x016,
    names.garinham_equip_shop_5: 0x017,
    names.garinham_equip_shop_6: 0x018,
    names.garinham_equip_shop_7: 0x019,

    names.garinham_item_shop_1: 0x01A,
    names.garinham_item_shop_2: 0x01B,
    names.garinham_item_shop_3: 0x01C,

    names.garinham_chest_1: 0x01D,
    names.garinham_chest_2: 0x01E,
    names.garinham_chest_3: 0x01F,
}

kol_locations = {
    names.kol_equip_shop_1: 0x020,
    names.kol_equip_shop_2: 0x021,
    names.kol_equip_shop_3: 0x022,
    names.kol_equip_shop_4: 0x023,
    names.kol_equip_shop_5: 0x024,

    names.kol_item_shop_1: 0x025,
    names.kol_item_shop_2: 0x026,
    names.kol_item_shop_3: 0x027,
    names.kol_item_shop_4: 0x028,

    names.kol_fairy_flute: 0x029,
}

rimuldar_locations = {
    names.rimuldar_equip_shop_1: 0x02A,
    names.rimuldar_equip_shop_2: 0x02B,
    names.rimuldar_equip_shop_3: 0x02C,
    names.rimuldar_equip_shop_4: 0x02D,
    names.rimuldar_equip_shop_5: 0x02E,
    names.rimuldar_equip_shop_6: 0x02F,

    names.rimuldar_inn_chest: 0x030,
    names.rimuldar_magic_key_vendor: 0x031,
}

cantlin_locations = {
    names.cantlin_equip_shop_1_1: 0x032,
    names.cantlin_equip_shop_1_2: 0x033,
    names.cantlin_equip_shop_1_3: 0x034,
    names.cantlin_equip_shop_1_4: 0x035,
    names.cantlin_equip_shop_1_5: 0x036,
    names.cantlin_equip_shop_1_6: 0x037,

    names.cantlin_equip_shop_2_1: 0x038,
    names.cantlin_equip_shop_2_2: 0x039,

    names.cantlin_equip_shop_3_1: 0x03A,
    names.cantlin_equip_shop_3_2: 0x03B,
    names.cantlin_equip_shop_3_3: 0x03C,
    names.cantlin_equip_shop_3_4: 0x03D,

    names.cantlin_item_shop_1_1: 0x03E,
    names.cantlin_item_shop_1_2: 0x03F,

    names.cantlin_equip_shop_1_1: 0x040,
    names.cantlin_equip_shop_1_2: 0x041,

    names.cantlin_magic_key_vendor: 0x042,
    names.cantlin_fairy_water_vendor: 0x043,
}

mountain_cave_locations = {
    names.mountain_cave_1_chest: 0x044,

    names.mountain_cave_2_chest_1: 0x045,
    names.mountain_cave_2_chest_2: 0x046,
    names.mountain_cave_2_chest_3: 0x047,
    names.mountain_cave_2_chest_4: 0x048,
}

garins_grave_locations = {
    names.garins_grave_1_chest_1: 0x049,
    names.garins_grave_1_chest_2: 0x04A,
    names.garins_grave_1_chest_3: 0x04B,

    names.garins_grave_3_chest_1: 0x04C,
    names.garins_grave_3_chest_1: 0x04D,
}

charlock_locations = {
    names.charlock_castle_erdrick_sword: 0x04E,

    names.charlock_castle_chest_1: 0x04F,
    names.charlock_castle_chest_2: 0x050,
    names.charlock_castle_chest_3: 0x051,
    names.charlock_castle_chest_4: 0x052,
    names.charlock_castle_chest_5: 0x053,
    names.charlock_castle_chest_6: 0x054,
}

misc_locations = {
    names.hauksness_erdrick_armor: 0x055,
    names.erdrick_tablet: 0x056,
    names.staff_of_rain_location: 0x057,
    names.erdricks_token_location: 0x058,
    names.rainbow_drop_location: 0x059
}

location_table = {
    **throne_room_locations,
    **tantegel_castle_locations,
    **brecconary_locations,
    **garinham_locations,
    **kol_locations,
    **rimuldar_locations,
    **cantlin_locations,
    **mountain_cave_locations,
    **garins_grave_locations,
    **charlock_locations,
    **misc_locations
}

location_names: Dict[str, Set[str]] = { 
    "Tantegel Castle": Set(name for name in throne_room_locations.keys() + tantegel_castle_locations.keys()),
    "Brecconary": Set(name for name in brecconary_locations.keys()),
    "Garinham": Set(name for name in garinham_locations.keys()),
    "Kol": Set(name for name in kol_locations.keys()),
    "Rimuldar": Set(name for name in rimuldar_locations.keys()),
    "Cantlin": Set(name for name in cantlin_locations.keys()),
    "Mountain Cave": Set(name for name in mountain_cave_locations.keys()),
    "Garin's Grave": Set(name for name in garins_grave_locations.keys()),
    "Charlock": Set(name for name in charlock_locations.keys()),
    "Hauksness": Set([names.hauksness_erdrick_armor]),
    "Erdrick's Grave": Set([names.erdrick_tablet]),
    "Staff of Rain Shrine": Set([names.staff_of_rain_location]),
    "Erdrick's Token": Set([names.erdricks_token_location]),
    "Rainbow Drop Shrine": Set([names.rainbow_drop_location])
}

lookup_location_to_id: Dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}