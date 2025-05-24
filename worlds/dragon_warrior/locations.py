from typing import Dict, Set
from BaseClasses import Location
import names


class DWLocation(Location):
    game = "Dragon Warrior"

# Chests in DQ1 are stored as 4 bytes in the ROM, Map ID,X,Y,Contents. There is nothing stored to determine if a chest
# ever been opened before if it contains gold or a consumable, only that certain chests with key items don't spawn if
# the player has them in their inventory. However, data for chests opened on the CURRENT MAP are stored in the
# NES System Bus from address 0x601C to 0x602B, where each two bytes are the X and Y coords of the checked chest. The
# game compares these values with the current map to determine which chests to unload. Using this, we can set the
# location checks for these chests to be a 3 byte ID, building it from the Map ID stored in the RAM at 0x0045 with
# the two location bytes stored in the System Bus between 0x601C to 0x602B.

# TODO: Figure out shops

throne_room_locations = {
    names.tantegel_throne_room_gold_chest: 0x050404,
    names.tantegel_throne_room_key_chest: 0x050601,
    names.tantegel_throne_room_torch_chest: 0x050504,
}

tantegel_castle_locations = {
    names.tantegel_castle_gold_chest_1: 0x04010D,  # Need Key
    names.tantegel_castle_gold_chest_2: 0x04010F,  # Need Key
    names.tantegel_castle_gold_chest_3: 0x04020E,  # Need Key
    names.tantegel_castle_gold_chest_4: 0x04030F,  # Need Key
    names.tantegel_castle_basement: 0x0C0405,      # Need Key
}

brecconary_locations = {
    # names.brecconary_equip_shop_1: 0x009,
    # names.brecconary_equip_shop_2: 0x00A,
    # names.brecconary_equip_shop_3: 0x00B,
    # names.brecconary_equip_shop_4: 0x00C,
    # names.brecconary_equip_shop_5: 0x00D,
    # names.brecconary_equip_shop_6: 0x00E,

    # names.brecconary_item_shop_1: 0x00F,
    # names.brecconary_item_shop_2: 0x010,
    # names.brecconary_item_shop_3: 0x011,

    # names.brecconary_fairy_water: 0x012,
}

garinham_locations = {
    # names.garinham_equip_shop_1: 0x013,
    # names.garinham_equip_shop_2: 0x014,
    # names.garinham_equip_shop_3: 0x015,
    # names.garinham_equip_shop_4: 0x016,
    # names.garinham_equip_shop_5: 0x017,
    # names.garinham_equip_shop_6: 0x018,
    # names.garinham_equip_shop_7: 0x019,

    # names.garinham_item_shop_1: 0x01A,
    # names.garinham_item_shop_2: 0x01B,
    # names.garinham_item_shop_3: 0x01C,
}

garinham_key_locations = {
    names.garinham_chest_1: 0x090805,   # Need Key
    names.garinham_chest_2: 0x090806,   # Need Key
    names.garinham_chest_3: 0x090905,   # Need Key
}

kol_locations = {
    # names.kol_equip_shop_1: 0x020,
    # names.kol_equip_shop_2: 0x021,
    # names.kol_equip_shop_3: 0x022,
    # names.kol_equip_shop_4: 0x023,
    # names.kol_equip_shop_5: 0x024,

    # names.kol_item_shop_1: 0x025,
    # names.kol_item_shop_2: 0x026,
    # names.kol_item_shop_3: 0x027,
    # names.kol_item_shop_4: 0x028,

    # names.kol_fairy_flute: 0x029,
}

rimuldar_locations = {
    # names.rimuldar_equip_shop_1: 0x02A,
    # names.rimuldar_equip_shop_2: 0x02B,
    # names.rimuldar_equip_shop_3: 0x02C,
    # names.rimuldar_equip_shop_4: 0x02D,
    # names.rimuldar_equip_shop_5: 0x02E,
    # names.rimuldar_equip_shop_6: 0x02F,

    # names.rimuldar_magic_key_vendor: 0x031,
}

rimuldar_key_locations = {
    names.rimuldar_inn_chest: 0x0B1817,   # Need Key
}

cantlin_locations = {
    # names.cantlin_equip_shop_1_1: 0x032,
    # names.cantlin_equip_shop_1_2: 0x033,
    # names.cantlin_equip_shop_1_3: 0x034,
    # names.cantlin_equip_shop_1_4: 0x035,
    # names.cantlin_equip_shop_1_5: 0x036,
    # names.cantlin_equip_shop_1_6: 0x037,

    # names.cantlin_equip_shop_2_1: 0x038,
    # names.cantlin_equip_shop_2_2: 0x039,

    # names.cantlin_equip_shop_3_1: 0x03A,
    # names.cantlin_equip_shop_3_2: 0x03B,
    # names.cantlin_equip_shop_3_3: 0x03C,
    # names.cantlin_equip_shop_3_4: 0x03D,

    # names.cantlin_item_shop_1_1: 0x03E,
    # names.cantlin_item_shop_1_2: 0x03F,

    # names.cantlin_equip_shop_1_1: 0x040,
    # names.cantlin_equip_shop_1_2: 0x041,

    # names.cantlin_magic_key_vendor: 0x042,
    # names.cantlin_fairy_water_vendor: 0x043,
}

mountain_cave_locations = {
    names.mountain_cave_1_chest: 0x160D05,

    names.mountain_cave_2_chest_1: 0x170106,
    names.mountain_cave_2_chest_2: 0x170302,
    names.mountain_cave_2_chest_3: 0x170202,
    names.mountain_cave_2_chest_4: 0x170A09,
}

garins_grave_locations = {
    names.garins_grave_1_chest_1: 0x180B00,   # Need Key
    names.garins_grave_1_chest_2: 0x180C00,   # Need Key
    names.garins_grave_1_chest_3: 0x180D00,   # Need Key

    names.garins_grave_3_chest_1: 0x1A0101,   # Need Key
    names.garins_grave_3_chest_2: 0x1A0D06,   # Need Key
}

charlock_locations = {
    names.charlock_castle_erdrick_sword: 0x100505,   # Need Rainbow Drop

    names.charlock_castle_chest_1: 0x140B0B,  # Need Rainbow Drop
    names.charlock_castle_chest_2: 0x140B0C,  # Need Rainbow Drop
    names.charlock_castle_chest_3: 0x140B0D,  # Need Rainbow Drop
    names.charlock_castle_chest_4: 0x140C0C,  # Need Rainbow Drop
    names.charlock_castle_chest_5: 0x140C0D,  # Need Rainbow Drop
    names.charlock_castle_chest_6: 0x140D0D,  # Need Rainbow Drop
}

hauksness_locations = {
    # names.hauksness_erdrick_armor: 0x055,
}

erdricks_cave_locations = {
    names.erdrick_tablet: 0x1D0903,
}

shrine_of_rain_locations = {
    names.staff_of_rain_location: 0x0D0304,  # Need Silver Harp
}

erdricks_token_locations = {
    # names.erdricks_token_location: 0x058,
}

rainbow_shrine_locations = {
    # names.rainbow_drop_location: 0x059     # Need Stones of Sunlight & Staff of Rain
}

location_table = {
    **throne_room_locations,
    **tantegel_castle_locations,
    **brecconary_locations,
    **garinham_locations,
    **garinham_key_locations,
    **kol_locations,
    **rimuldar_locations,
    **rimuldar_key_locations,
    **cantlin_locations,
    **mountain_cave_locations,
    **garins_grave_locations,
    **charlock_locations,
    **hauksness_locations,
    **erdricks_grave_locations,
    **shrine_of_rain_locations,
    **erdricks_token_locations,
    **rainbow_shrine_locations
}

location_names: Dict[str, Set[str]] = { 
    "Tantegel Castle": Set(name for name in throne_room_locations.keys() + tantegel_castle_locations.keys()),
    "Brecconary": Set(name for name in brecconary_locations.keys()),
    "Garinham": Set(name for name in garinham_locations.keys() + garinham_key_locations.keys()),
    "Kol": Set(name for name in kol_locations.keys()),
    "Rimuldar": Set(name for name in rimuldar_locations.keys() + rimuldar_key_locations.keys()),
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