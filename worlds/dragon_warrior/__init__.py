import threading
from typing import Any, Dict, List, Optional

import names
from items import DWItem, item_table, cursed_table, filler_table
from locations import location_table
from regions import create_regions, connect_regions
import settings
from BaseClasses import Item, ItemClassification, Location, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from rom import DRAGON_WARRIOR_HASH

class DWSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Dragon Warrior ROM"""
        description = "Dragon Warrior ROM File"
        copy_to: Optional[str] = "Dragon Warrior (USA) (Rev A).nes"
        md5s = DRAGON_WARRIOR_HASH
    
    rom_file: RomFile = RomFile(RomFile.copy_to)

class DWWebWorld(WebWorld):
    theme = "grassFlowers"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Dragon Warrior randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serp"]
        )
    ]


class DragonWarriorWorld(World):
    """
    The peace of fair Alefgard has been shattered by the appearance of the nefarious master of the night known as
    the Dragonlord, and the Sphere of Light, which for so long kept the forces of darkness in check, has been stolen!
    It is time for you, a young warrior through whose veins flows the blood of the legendary hero Erdrick, to set out
    on a quest to vanquish the Dragonlord, and save the land from darkness!
    """
    game = "Dragon Warrior"
    item_name_to_id = []
    location_name_to_id = []
    item_name_groups = []
    location_name_groups = []
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

        itempool = []

        total_locations = len(location_table)

        itempool += [self.create_item(names.silver_harp), 
                     self.create_item(names.staff_of_rain), 
                     self.create_item(names.stones_of_sunlight), 
                     self.create_item(names.magic_key)]

        while len(itempool) < len(total_locations):
            itempool += [self.create_item(self.get_filler_item_name())]

        self.multiworld.itempool += itempool


    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = DWItem(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(cursed_table.keys() + filler_table.keys()))

    def generate_basic(self) -> None:
        pass # TODO

    def set_rules(self):
        pass # TODO

    def fill_slot_data(self) -> Dict[str, Any]:
        return {}