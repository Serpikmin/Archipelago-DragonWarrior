# Dragon Warrior APWorld

## How do I generate a multiworld with Dragon Warrior?

You can install the `dragon_warrior.apworld` file in the Releases tab to your AP Launcher to generate a YAML, as well as a multiworld. Be sure to send the Dragon Warrior player the generated `.apdw` patch file so they can play!

<<<<<<< HEAD
* The Legend of Zelda: A Link to the Past
* Factorio
* Subnautica
* Risk of Rain 2
* The Legend of Zelda: Ocarina of Time
* Timespinner
* Super Metroid
* Secret of Evermore
* Final Fantasy
* VVVVVV
* Raft
* Super Mario 64
* Meritous
* Super Metroid/Link to the Past combo randomizer (SMZ3)
* ChecksFinder
* ArchipIDLE
* Hollow Knight
* The Witness
* Sonic Adventure 2: Battle
* Starcraft 2
* Donkey Kong Country 3
* Dark Souls 3
* Super Mario World
* Pokémon Red and Blue
* Hylics 2
* Overcooked! 2
* Zillion
* Lufia II Ancient Cave
* Blasphemous
* Wargroove
* Stardew Valley
* The Legend of Zelda
* The Messenger
* Kingdom Hearts 2
* The Legend of Zelda: Link's Awakening DX
* Adventure
* DLC Quest
* Noita
* Undertale
* Bumper Stickers
* Mega Man Battle Network 3: Blue Version
* Muse Dash
* DOOM 1993
* Terraria
* Lingo
* Pokémon Emerald
* DOOM II
* Shivers
* Heretic
* Landstalker: The Treasures of King Nole
* Final Fantasy Mystic Quest
* TUNIC
* Kirby's Dream Land 3
* Celeste 64
* Castlevania 64
* A Short Hike
* Yoshi's Island
* Mario & Luigi: Superstar Saga
* Bomb Rush Cyberfunk
* Aquaria
* Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006
* A Hat in Time
* Old School Runescape
* Kingdom Hearts 1
* Mega Man 2
* Yacht Dice
* Faxanadu
* Saving Princess
* Castlevania: Circle of the Moon
* Inscryption
* Civilization VI
* The Legend of Zelda: The Wind Waker
* Jak and Daxter: The Precursor Legacy
* Super Mario Land 2: 6 Golden Coins
* shapez
* Paint
=======
## How do I join a multiworld with Dragon Warrior?
>>>>>>> 0c91ffc7 (Update readme)

Your host should send you the `.apdw` patch file, ensure you have the Archipelago Launcher, and open the `.apdw` patch file using the "Open Patch" option in the launcher. **NOTE THAT DOUBLE CLICKING THE PATCH FILE WILL NOT WORK!!** (due to some under the hood stuff) After Bizhawk + Client open, be sure to type your multiworld's corresponding URL + port at the top and hit connect, you'll be prompted to type your player name (slot number), and then you're good!

## What does randomization do to this game?

Currently, only chests and their contents are randomized into the multiworld. Magic Key Vendors no longer sell them, instead, a single unbreakable Magic Key is shuffled into the multiworld as a progression item.

## What is the goal of Dragon Warrior when randomized?

In order to beat the game, you must receive the Staff of Rain + Stones of Sunlight, and take them to the Rainbow Shrine (alongside with Erdrick's Token, which is currently in it's vanilla location) in order to receive the Rainbow Drop and reach Charlock Castle. The completion condition is to defeat the Dragonlord.

## What items and locations get shuffled?

All items contained in chests are shuffled around.

## Which items can be in another player's world?

Any shuffled item can be in other players' worlds.

## What does another world's item look like in Dragon Warrior?

All items, both remote and local, appear in chests as "APItem".

## When the player receives an item, what happens?

Currently, items are silently added to the player's inventory. If it is full, a filler item will be dropped for a quest item. Otherwise the item is ignored.

## Future plans:

- (Nearly) Full suite of options from the [DWRandomizer](https://dwrandomizer.com/)
- Add the three search spots to the item/location pool (Fairy Flute, Erdrick's Token, Erdrick's Armor)
- Add equipment shop slots as locations and create progressive equipment
- Add boss kills as checks (Green Dragon, Golem, Knight Aberrant)
- Spellsanity/Levelsanity