import hashlib
import os
import threading
from typing import Any, ClassVar, Dict, List, Optional, Sequence, Tuple

from . import names
from .items import DWItem, item_table, cursed_table, filler_table, lookup_name_to_id, item_names
from .locations import location_table, lookup_location_to_id, location_names
from .regions import create_regions, connect_regions
import settings
from BaseClasses import Item, ItemClassification, Location, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from .rom import DRAGON_WARRIOR_HASH, LocalRom, get_base_rom_path, DWDeltaPatch, patch_rom
from .options import DWOptions
import dwr  # Package in requirements.txt

class DWSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Dragon Warrior ROM"""
        description = "Dragon Warrior ROM File"
        copy_to: Optional[str] = "Dragon Warrior (USA) (Rev A).nes"
        md5s = [DRAGON_WARRIOR_HASH]
    
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
    settings: ClassVar[DWSettings]
    options_dataclass = DWOptions
    options: DWOptions
    item_name_to_id = lookup_name_to_id
    location_name_to_id = lookup_location_to_id
    item_name_groups = item_names
    location_name_groups = location_names
    web = DWWebWorld()
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

    def generate_output(self, output_directory: str) -> None:
        try:
            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.nes")

            # Patch rom with dwrandomizer
            flags = self.determine_flags()
            dwr.py_dwr_randomize(get_base_rom_path(), self.multiworld.seed, flags, rompath)

            rom = LocalRom(rompath)
            patch_rom(rom)
            self.rom_name = rom.name

            patch = DWDeltaPatch(os.path.splitext(rompath)[0]+DWDeltaPatch.patch_file_ending, player=self.player,
                                   player_name=self.multiworld.player_name[self.player], patched_path=rompath)
            patch.write()
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()

    def determine_flags(self) -> str:
        default_flags = "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAUAAAAAA"
        # TODO
        return default_flags