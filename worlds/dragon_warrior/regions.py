from BaseClasses import Entrance, Region
from worlds.AutoWorld import World
from typing import Dict, Optional, Callable

from . import locations
from . import names

"""
CHEST MEMORY NOTES:

ROM Data for chests starts at offset 0x5DDD, each are stored in 4 bytes
Format: Map ID, X, Y, Chest Contents

OFFSET |        MAP      | CONTENTS
-------|-----------------|---------
0x5DDD | Tantegel Castle |   ~10G
0x5DE1 | Tantegel Castle |   ~10G
0x5DE5 | Tantegel Castle |   ~10G
0x5DE9 | Tantegel Castle |   ~10G
0x5DED |   Throne Room   |   120G
0x5DF1 |   Throne Room   |   Torch
0x5DF5 |   Throne Room   |    Key
0x5DF9 |     Rimuldar    |   Wings
0x5DFD |     Garinham    |   ~10G
0x5E01 |     Garinham    |   Herb
0x5E05 |     Garinham    |   Torch
0x5E09 |    Dragonlord   |   Herb
0x5E0D |    Dragonlord   | High Gold
0x5E11 |    Dragonlord   |   Wings
0x5E15 |    Dragonlord   |    Key
0x5E19 |    Dragonlord   | Cursed Belt
0x5E1D |    Dragonlord   |   Herb
0x5E21 |    Sun Shrine   | St. of Sunl.
0x5E25 |   Rain Shrine   | St. of Rain
0x5E29 |  Garin Grave B1 |   Herb
0x5E2D |  Garin Grave B1 |   ~10G
0x5E31 |  Garin Grave B1 |   ~10G
0x5E35 |  Garin Grave B3 | Cursed Belt
0x5E39 |  Garin Grave B3 | Silv. Harp
0x5E3D |   Charlock B2   | Erdr. Sword
0x5E41 | MountainCave B2 |   ~107G
0x5E45 | MountainCave B2 |   Torch
0x5E49 | MountainCave B2 | Fight. Ring
0x5E4D | MountainCave B2 |   ~10G
0x5E51 | MountainCave B1 |   Herb
0x5E55 | Erdrick Cave B2 | Erd. Tablet

TODO: Find where code for opening chests is and hijack to not grant chest contents,
as well as send data to the client regarding which check was opened
"""

class DWRegion(Region):
    game = "Dragon Warrior"

def create_regions(world: World) -> None:
    menu_region = create_region(world, 'Menu', None)

    overworld_region = create_region(world, names.overworld, None)

    tantegel_throne_room_region = create_region(world, names.tantegel_throne_room, locations.throne_room_locations)
    
    tantegel_castle_region = create_region(world, names.tantegel_castle, locations.tantegel_castle_locations)

    brecconary_region = create_region(world, names.breconnary, locations.brecconary_locations)

    garinham_region = create_region(world, names.garinham, locations.garinham_locations)

    garinham_key_region = create_region(world, names.garinham_keys, locations.garinham_key_locations)

    kol_region = create_region(world, names.kol, locations.kol_locations)

    rimuldar_region = create_region(world, names.rimuldar, locations.rimuldar_locations)    

    rimuldar_key_region = create_region(world, names.rimuldar_keys, locations.rimuldar_key_locations)

    cantlin_region = create_region(world, names.cantlin, locations.cantlin_locations)

    mountain_cave_region = create_region(world, names.mountain_cave, locations.mountain_cave_locations)

    garins_grave_region = create_region(world, names.garins_grave, locations.garins_grave_locations)

    charlock_region = create_region(world, names.charlock_castle, locations.charlock_locations)

    hauksness_region = create_region(world, names.hauksness, locations.hauksness_locations)

    erdricks_cave_region = create_region(world, names.erdricks_cave, locations.erdricks_cave_locations)

    shrine_of_rain_region = create_region(world, names.staff_of_rain_shrine, locations.shrine_of_rain_locations)

    erdricks_token_region = create_region(world, names.erdricks_token_tile, locations.erdricks_token_locations)

    rainbow_shrine_region = create_region(world, names.rainbow_drop_shrine, locations.rainbow_shrine_locations)

    world.multiworld.regions += [
        menu_region,
        overworld_region,
        tantegel_throne_room_region,
        tantegel_castle_region,
        brecconary_region,
        garinham_region,
        garinham_key_region,
        kol_region,
        rimuldar_region,
        rimuldar_key_region,
        cantlin_region,
        mountain_cave_region,
        garins_grave_region,
        charlock_region,
        hauksness_region,
        erdricks_cave_region,
        shrine_of_rain_region,
        erdricks_token_region,
        rainbow_shrine_region
    ]


def connect_regions(world: World) -> None:
    region_names: Dict[str, int] = {}

    connect(world, world.player, region_names, 'Menu', names.tantegel_throne_room)
    connect(world, world.player, region_names, names.tantegel_throne_room, names.overworld)
    connect(world, world.player, region_names, names.overworld, names.breconnary)
    connect(world, world.player, region_names, names.overworld, names.garinham)
    connect(world, world.player, region_names, names.overworld, names.kol)             # Connect with gear later
    connect(world, world.player, region_names, names.overworld, names.rimuldar)        # Connect with gear later
    connect(world, world.player, region_names, names.overworld, names.hauksness)       # Connect with gear later
    connect(world, world.player, region_names, names.overworld, names.cantlin)         # Connect with gear & flute later
    connect(world, world.player, region_names, names.overworld, names.erdricks_cave)
    connect(world, world.player, region_names, names.overworld, names.mountain_cave)   # Connect with gear later

    connect(world, world.player, region_names, names.overworld, names.tantegel_castle, 
            lambda state: (state.has(names.magic_key, world.player)))
    connect(world, world.player, region_names, names.overworld, names.garinham_keys, 
            lambda state: (state.has(names.magic_key, world.player)))
    connect(world, world.player, region_names, names.overworld, names.rimuldar_keys,  # Connect with gear later
            lambda state: (state.has(names.magic_key, world.player)))
    connect(world, world.player, region_names, names.garinham_keys, names.garins_grave) # Connect with gear later
    connect(world, world.player, region_names, names.overworld, names.staff_of_rain_shrine, 
            lambda state: (state.has(names.silver_harp, world.player)))
    connect(world, world.player, region_names, names.overworld, names.erdricks_token_tile)  # Connect with gear later
    connect(world, world.player, region_names, names.overworld, names.rainbow_drop_shrine,  # Connect with gear later
            lambda state: (state.has(names.staff_of_rain, world.player) and 
                           state.has(names.stones_of_sunlight, world.player)))
    connect(world, world.player, region_names, names.overworld, names.charlock_castle,      # Connect with gear later
            lambda state: (state.has(names.rainbow_drop, world.player)))
    

def create_region(world: World, name: str, location_checks=None):
    ret = DWRegion(name, world.player, world.multiworld)
    if location_checks:
        for locName, locId in location_checks.items():
            location = locations.DWLocation(world.player, locName, locId, ret)
            ret.locations.append(location)

    return ret

def connect(world: World, player: int, used_names: Dict[str, int], source: str, target: str,
            rule: Optional[Callable] = None):
    source_region = world.multiworld.get_region(source, player)
    target_region = world.multiworld.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
