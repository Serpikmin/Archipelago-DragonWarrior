import threading
from typing import Any, Dict, List, Optional

from items import DWItem
import settings
from BaseClasses import Item, Location, MultiWorld, Tutorial
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
        pass # TODO

    def create_item(self, name: str) -> DWItem:
        pass # TODO

    def get_filler_item_name(self) -> str:
        pass # TODO

    def create_items(self) -> None:
        pass # TODO

    def generate_early(self) -> None:
        pass # TODO

    def generate_basic(self) -> None:
        pass # TODO

    def fill_hook(self, 
                  progitempool: List["Item"], 
                  usefulitempool: List["Item"], 
                  filleritempool: List["Item"], 
                  fill_locations: List["Location"]) -> None:
        pass # TODO

    def generate_output(self, output_directory: str) -> None:
        pass # TODO

    def fill_slot_data(self) -> Dict[str, Any]:
        return {}