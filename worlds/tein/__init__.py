from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World


class TEINWebWorld(WebWorld):
    theme = "stone"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the The End is Nigh randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serp"]
        )
    ]

    # option_groups = TEINOptionGroups


class TEINWorld(World):
    """
    The End Is Nigh is a sprawling adventure platformer where you die a lot, 
    but thats ok because you are probably already dead anyway.
    """
    game = "The End is Nigh"
    authors = ["Serp"]
    # options_dataclass = TEINOptions
    # options: TEINOptions
    # item_name_to_id = lookup_name_to_id
    # item_name_groups = item_names
    # location_name_to_id = all_locations
    # location_name_groups = location_names
    web = TEINWebWorld()

    def create_regions(self):
        return super().create_regions()
    
    def create_item(self, name):
        return super().create_item(name)
    
    def get_filler_item_name(self):
        return super().get_filler_item_name()
    
    def fill_slot_data(self):
        return super().fill_slot_data()
    
    