# RL vs SLK Randomizer Tool

A somewhat poorly-written tool for randomly generating Pokemon teams from sample movelists. This tool was created mainly for custom movesets, should work for any list of Pokemon. Despite the rough shape it is currently in, polishing up this tool would likely require it to be completely redone.

# Usage

`__TEAMS_OUTPUT__.txt`: Pokemon Showdown/Pokepaste data for generated teams.

`config.ini`: 'omit_first_x_tiers' will exclude the top x amount of tiers used when randomly generating teams (see `tiers.txt`). 'original_stats' will use the stats from the teams_list.txt file. The other options in this file do nothing since they have not been coded in.

`pokemon_index.txt`: A list of a pokemon's full moveset. Does not need to be in alphabetical order but it helps when adding in new mons. Format is:

 - 1st line: Nickname (Pokemon Species+Forme)

 - 2nd line: Ability: ability_name, ability_name2...

 - 3rd line: move1, move2, move3, move4...

 - 4th line: blank line

Repeat as many times as you like.

`tiers.txt`: Tiers are the only line with a tab. Make sure they have a tab, but the tiers can be named whatever you want.

`teams_list.txt`: Pokemon Showdown/Pokepaste data, it can be exported from a save editor to showdown, then from showdown to a txt file.

don't have any of the following sequences in your pokemon's names or else it won't work:
 - ' -'
 - '('

# Limitations

 - This tool does not take into account move compatibility.
 - The code is set up so that seeds can be reused, but this compatibility is not coded in.
 - Will run into scaling issues since the tool parses files start to finish for everything.
 - Will sometimes have two of the same Pokemon on the same team when generating.
