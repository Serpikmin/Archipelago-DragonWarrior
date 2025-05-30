import logging
from worlds._bizhawk.client import BizHawkClient
from NetUtils import NetworkItem
from typing import List, Optional
import worlds._bizhawk as bizhawk

from worlds._bizhawk.context import BizHawkClientContext

nes_logger = logging.getLogger("NES")
logger = logging.getLogger("Client")

EXPECTED_ROM_NAME = b"DRAGON WARRIOR"

class DragonWarriorClient(BizHawkClient):
    game = "Dragon Warrior"
    system = "NES"
    patch_suffix = ".apdw"
    item_queue: List[NetworkItem] = []
    rom: Optional[bytes] = None

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (
                await bizhawk.read(ctx.bizhawk_ctx, [(0xFFF0, 14, "PRG ROM")])
            )[0]

            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode(
                "ascii"
            )
            if not rom_name.startswith(EXPECTED_ROM_NAME):
                logger.info(
                    "ERROR: Rom is not valid!"
                )
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111

        return True
    
    async def game_watcher(self, ctx):
        from worlds._bizhawk import read, write

        if ctx.server is None or ctx.slot is None:
            return
        
        # Game Completion

        # Search for new location checks
        new_checks = []

        # Check for opened chests
        current_map = await read(ctx.bizhawk_ctx, [
            (0x45, 1, "RAM")
        ])
        chests_array = await read(ctx.bizhawk_ctx, [
            (0x601C, 16, "System Bus")
        ])

        # See locations.py for an explanation
        for i in range(0, 16, 2):
            chest = chests_array[i:i + 2]
            location_data = hex((current_map << 16) | chest)
            if location_data not in ctx.checked_locations:
                new_checks.append(location_data)

        # Send found checks
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            nes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])


        # Receive Items
        # Compare an items_received index in the ROM to len(ctx.items_received)
        # If smaller, we should grant the missing items