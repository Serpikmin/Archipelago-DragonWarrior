# Dragon Warrior APWorld

## How do I generate a multiworld with Dragon Warrior?

You can install the `dragon_warrior.apworld` file in the Releases tab to your AP Launcher to generate a YAML, as well as a multiworld. Be sure to send the Dragon Warrior player the generated `.apdw` patch file so they can play!

## How do I join a multiworld with Dragon Warrior?

Your host should send you the `.apdw` patch file, ensure you have the Archipelago Launcher, and open the `.apdw` patch file using the "Open Patch" option in the launcher. **NOTE THAT DOUBLE CLICKING THE PATCH FILE WILL NOT WORK!!** (due to some under the hood stuff) After Bizhawk + Client open, be sure to type your multiworld's corresponding URL + port at the top and hit connect, you'll be prompted to type your player name (slot number), and then you're good!

## What does randomization do to this game?

Opening chests and search spots are checks by default. There's also a YAML option to make level-ups checks up to level 30 (default 16)
Items include any of the randomized key items, cursed items, medicinal herbs, and gold
Magic Key Vendors no longer sell them, instead, a single unbreakable Magic Key is shuffled into the multiworld as a progression item.

## What is the goal of Dragon Warrior when randomized?

In order to beat the game, you must receive the Staff of Rain, Stones of Sunlight, and Erdrick's Token, then take them to the Rainbow Shrine (alongside with Erdrick's Token, which is currently in it's vanilla location) in order to receive the Rainbow Drop and reach Charlock Castle. The completion condition is to defeat the Dragonlord.

## What items and locations get shuffled?

All items contained in chests and search spots are shuffled around. Level-ups additionally can count as location checks with extra filler gold/herbs filled in.

## Which items can be in another player's world?

Any shuffled item can be in other players' worlds.

## What does another world's item look like in Dragon Warrior?

All items, both remote and local, appear in chests as "APItem".

## When the player receives an item, what happens?

Currently, items are silently added to the player's inventory. If it is full, a filler item will be dropped for a quest item. Otherwise the item is ignored.

## Future plans (roughly ordered):

- Add equipment shop slots as locations and create progressive equipment
- Add some remaining map/goal options from [DWRandomizer](https://dwrandomizer.com/)
- Deathlink