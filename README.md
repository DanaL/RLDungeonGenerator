This is a proof of concept for a new type of dungeon map that I'm intending on using in crashRun to generate some maps. However, I thought perhaps I'd written this stand-alone python file, I'd post it on github by itself in case it is useful for someone.

While crashRun already had a few difference kinds of maps (caves, mazes, tightly packed 'boxes' of rooms), I also wanted one that was
a little closer to the original rogue, in the sense that it is rooms connected by longer tunnels.

One thing I'm not sure I like is that the map doesn't generate loops. It's an acyclic graph. I might experiment with adding a few
superfluous tunnels to make potential loops.

Finally, the levels of the dungeon I intend to use this generator for will have rooms connected by teleporters. In that case, 
for a handful of rooms, I'll pick two rooms from random, different groups and skip carving tunnels, instead connecting them 
with teleporters.

The generator works by binary space partitioning, splitting the map into smaller and smaller sections until we reach sections
that are approximately the size of a room. I then carve a room out in the space (skipping a handful of sections to avoid an
overly uniform-looking dungeon). To connect the rooms together, I calculate which rooms are adjacent to each other (either
horizontally or vertically) and calculate how far apart they are. Then, I group the rooms together, find nearby rooms, draw
a tunnel between them, then merge them into the same group. I do this until there is only one room remaining. If a tunnel connecting
rooms is four or greater squares long (or exactly one square long), I put doors at either end of the corridor.

Example output to show what the dungeon maps it creates look like:

```
##########################################################################################
################.......###########.........###############################################
#..........#####.......###########.........################.......########################
#..........#####.......##.......##.........################.......#####........###########
#..........#####.......##..................##...........###.......#####........###########
#..........#####.......##.......##.........##...........###.......#####........###########
#..........#####.......##.......##.........##...........###.......#####........###########
#..........#####................##.........##...........######.########........###########
#..........#####.......##.......##.........##...........######.########........###########
#..........#####.......##.......##.........##...........######.###########.###############
#.##############.......##.......##.........##...........###.....##########.###############
#.###########################+####.........##...........###.....####........##############
#.........###################.######################+######.....####........##..........##
#.........###################.######################.######.....####....................##
#.........###################+######################.######.....####........##..........##
#.........#################.......##......##########+######.....####........##..........##
#.........#################.......##......###.............+.....####........##..........##
#.........#################.......##......###.............#.....####........##..........##
#.........#################...............###.............##########........##..........##
#.........#################.......##......###.............##########........########.#####
#.........#################.......##......###.............##########........########.#####
#.........#################.......##......................############+#############.#####
#.........##################.################.............##########...........##......###
########.###################.#####################.########.......##...........##......###
########.###################.#####################.########.......##...........##......###
#........################......###.......#####..........###.......##...........##......###
#........##...........###................#####..........###.......##...........##......###
#........##...........###......###.......#####..........###....................##......###
#........##....................###.......#####..........###.......##...........##......###
#........##...........###......###.......#####..........###.......##...........###########
#........##...........###......###.......#####..........###.......##...........###########
#........##...........###......###.......#####..........########.###...........###########
#........##...........###......###.......#####..........########.#########################
#........##...........###......###.......#######.##########.......###############......###
##.############.#############.####.......#######.##########.......##..........###......###
##.############.#############.####+#############.........##.......##..........###......###
#........##......######.........##.........#####.........##.......##..........###......###
#................######.........##.........#####.........##.......##..........###......###
#........##......######.........##.........#####.........##.......##...................###
#........##......######.........##.........#####.........##.......##..........###......###
#........##......######.........##.........#####.........##...................###......###
#........##......######.........##.........#####..................##..........###......###
###########......######.........##.........#####.........##.......###############......###
#######################.........###########################.......########################
##########################################################################################
```

This code is released into the Public Domain.
