import logging
import os
import platform
import sys
import zipfile
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
from .options import DWOptions, DWOptionGroups
from .client import DragonWarriorClient

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

    option_groups = DWOptionGroups


class DragonWarriorWorld(World):
    """
    The peace of fair Alefgard has been shattered by the appearance of the nefarious master of the night known as
    the Dragonlord, and the Sphere of Light, which for so long kept the forces of darkness in check, has been stolen!
    It is time for you, a young warrior through whose veins flows the blood of the legendary hero Erdrick, to set out
    on a quest to vanquish the Dragonlord, and save the land from darkness!
    """
    game = "Dragon Warrior"
    settings_key = "dw_options"
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

    @classmethod
    def stage_generate_early(cls, multiworld: MultiWorld):
        # Extract the dwr module from the .apworld depending on OS into a temp directory
        current_directory = os.getcwd()
        new_dir = os.path.join(current_directory, "dragon_warrior_randomizer")

        try:
            os.mkdir(new_dir)
        except FileExistsError:
            pass

        if platform.system() == "Windows":
            file = "dwr.cp312-win_amd64.pyd"
        else:
            file = "dwr.cpython-312-x86_64-linux-gnu.so"
        
        with zipfile.ZipFile(os.path.join(current_directory, "custom_worlds", "dragon_warrior.apworld")) as zf:
            zf.extract("dragon_warrior/" + file, path=new_dir)

        # Clean up format from zip file
        os.replace(os.path.join(new_dir, "dragon_warrior", file), os.path.join(new_dir, file))
        os.rmdir(os.path.join(new_dir, "dragon_warrior"))
        open(os.path.join(new_dir, "__init__.py"), "a")

        sys.path.append(new_dir)


    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

        itempool = []

        total_locations = len(location_table)

        itempool += [self.create_item(names.silver_harp), 
                     self.create_item(names.staff_of_rain), 
                     self.create_item(names.stones_of_sunlight),
                     self.create_item(names.magic_key),
                     self.create_item(names.erdricks_sword),
                     self.create_item(names.death_necklace),
                     self.create_item(names.cursed_belt)]

        while len(itempool) < total_locations:
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
        return self.multiworld.random.choice(list(filler_table.keys()))

    def generate_output(self, output_directory: str) -> None:
        # Created in stage_generate_early
        import dwr # type: ignore

        try:
            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.nes")

            # Write the patched ROM to the temp directory
            dwr_output_dir = os.path.join(os.getcwd(), "dragon_warrior_randomizer")
            flags = self.determine_flags()
            # Cython requires Python to pass strings in as bytes encoded in ascii, seed is an unsigned long long
            dwr.py_dwr_randomize(bytes(get_base_rom_path(), encoding="ascii"), self.multiworld.seed // 100, bytes(flags, encoding="ascii"), bytes(dwr_output_dir, encoding="ascii"))

            rom = LocalRom(os.path.join(dwr_output_dir, "Dragon Warrior (USA) (Rev A).nes"))
            patch_rom(self, rom)
            self.rom_name = rom.name
            rom.write_to_file(rompath)

            patch = DWDeltaPatch(os.path.splitext(rompath)[0] + ".apdw",
                            self.player, 
                            self.multiworld.player_name[self.player],
                            patched_path=os.path.splitext(rompath)[0] + ".nes")
            patch.write()
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()

    def determine_flags(self) -> str:
        default_flags = "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAUAAAAAA"
        # TODO
        return default_flags