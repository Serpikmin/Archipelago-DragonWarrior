import logging
from worlds._bizhawk.client import BizHawkClient
from NetUtils import ClientStatus, NetworkItem, color
from typing import List, Optional, TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
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
        
        current_map, chests_array, recv_count, inventory_bytes, \
            dragonlord_dead = await read(ctx.bizhawk_ctx, [
            (0x45, 1, "RAM"),
            (0x601C, 16, "System Bus"),
            (0x0E, 1, "RAM"),
            (0xC1, 4, "RAM"),
            (0xE4, 1, "RAM")
        ])

        dragonlord_dead = dragonlord_dead & 0x4
        
        # Game Completion
        if not ctx.finished_game and dragonlord_dead:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

        # Search for new location checks
        new_checks = []

        # See locations.py for an explanation
        for i in range(0, 16, 2):
            chest = chests_array[i:i + 2]
            location_data = int(hex((current_map << 16) | chest), 16)
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
        # Compare items_received index in the RAM at 0x0E to len(ctx.items_received)
        # If smaller, we should grant the missing items
        writes = []
        important_items = [0x5, 0x7, 0x8, 0xA, 0xC, 0xD, 0xE]
        filler_items = [0x0, 0x1, 0x2, 0x3, 0x4, 0x6, 0x9, 0xB]

        recv_index = recv_count[0]

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            if item.item in important_items:  # Add item to inventory no matter what

                found_space = False

                for i in range(len(inventory_bytes)):
                    slot = inventory_bytes[i]
                    hi_item = ((slot & 0xF0) >> 4)
                    lo_item = slot & 0xF

                    if hi_item == 0:
                        new_byte = (item.item << 4) + lo_item
                        found_space = True
                    elif lo_item == 0:
                        new_byte = slot + lo_item
                        found_space = True
                    if found_space:
                        writes.append(0xC1 + i, new_byte.to_bytes(1, 'little'), "RAM")
                        break

                if not found_space:  # No free space found, kick out a filler item
                    for i in range(len(inventory_bytes)):
                        slot = inventory_bytes[i]
                        hi_item = ((slot & 0xF0) >> 4)
                        lo_item = slot & 0xF

                        if hi_item in filler_items:
                            new_byte = (item.item << 4) + lo_item
                            found_space = True
                        elif lo_item in filler_items:
                            new_byte = slot + lo_item
                            found_space = True
                        if found_space:
                            writes.append(0xC1 + i, new_byte.to_bytes(1, 'little'), "RAM")
                            break

            elif item.item == 0xD4:  # Magic Key
                writes.append((0xBF, bytes(1), "RAM"))

            elif item.item < 0xF: 
                
                found_space = False

                for i in range(len(inventory_bytes)):
                    slot = inventory_bytes[i]
                    hi_item = ((slot & 0xF0) >> 4)
                    lo_item = slot & 0xF

                    if hi_item == 0:
                        new_byte = (item.item << 4) + lo_item
                        found_space = True
                    elif lo_item == 0:
                        new_byte = slot + lo_item
                        found_space = True
                    if found_space:
                        writes.append(0xC1 + i, new_byte.to_bytes(1, 'little'), "RAM")
                        break
                # For now, skip adding if no inventory space found
            else:
                pass # Progressive Equipment

            recv_index += 1
            writes.append((0x0E, recv_index.to_bytes(1, 'little'), "RAM"))
        
        await write(ctx.bizhawk_ctx, writes)

        
