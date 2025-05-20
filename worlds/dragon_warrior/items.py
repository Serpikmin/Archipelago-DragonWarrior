from typing import Dict, NamedTuple, Set
from BaseClasses import Item
from . import names


class ItemData(NamedTuple):
    code: int
    progression: bool = False
    useful: bool = False
    skip_balancing: bool = False


class DWItem(Item):
    game = "Dragon Warrior"

equipment_table = {
    names.progressive_weapon: ItemData(0x001, True),
    names.progressive_shield: ItemData(0x002, True),
    names.progressive_armor: ItemData(0x003, True),
    names.dragon_scale: ItemData(0x004),
    names.fighters_ring: ItemData(0x005)
}

important_table = {
    names.fairy_flute: ItemData(0x006, True),
    names.silver_harp: ItemData(0x007, True),
    names.gwaelins_love: ItemData(0x008, True),
    names.erdricks_token: ItemData(0x009, True),
    names.staff_of_rain: ItemData(0x00A, True),
    names.stones_of_sunlight: ItemData(0x00B, True),
    names.rainbow_drop: ItemData(0x00C, True, True),
    names.magic_key: ItemData(0x00D, True, True),
}

cursed_table = {
    names.cursed_belt: ItemData(0x00E),
    names.death_necklace: ItemData(0x00F)
}

filler_table = {
    names.herb: ItemData(0x010),
    names.chimaera_wing: ItemData(0x011),
    names.torch: ItemData(0x012),
    names.fairy_water: ItemData(0x013)
}

item_table = {
    **equipment_table,
    **important_table,
    **cursed_table,
    **filler_table,
}

item_names: Dict[str, Set[str]] = {
    "Equipment": Set(name for name in equipment_table.keys() + cursed_table.keys()),
    "Progression": Set(name for name in important_table.keys()),
    "Consumable": Set(name for name in filler_table.keys())
    }

lookup_item_to_id: Dict[str, int] = {item_name: data.code for item_name, data in item_table.items()}
lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}