from copy import copy
from math import sqrt
from random import random
from random import randint
from random import randrange
from random import choice

class DungeonSqr:
    def __init__(self, sqr):
        self.sqr = sqr

    def get_ch(self):
        return self.sqr

class Room:
    def __init__(self, r, c, h, w):
        self.row = r
        self.col = c
        self.height = h
        self.width = w

class RLDungeonGenerator:
    def __init__(self, w, h):
        self.MAX = 15 # Cutoff for when we want to stop dividing sections
        self.width = w
        self.height = h
        self.leaves = []
        self.dungeon = []
        self.rooms = []

        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(DungeonSqr('#'))

            self.dungeon.append(row)

    def random_split(self, min_row, min_col, max_row, max_col):
        # We want to keep splitting until the sections get down to the threshold
        seg_height = max_row - min_row
        seg_width = max_col - min_col

        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_row, min_col, max_row, max_col))
        elif seg_height < self.MAX and seg_width >= self.MAX:
            self.split_on_vertical(min_row, min_col, max_row, max_col)
        elif seg_height >= self.MAX and seg_width < self.MAX:
            self.split_on_horizontal(min_row, min_col, max_row, max_col)
        else:
                if random() < 0.5:
                    self.split_on_horizontal(min_row, min_col, max_row, max_col)
                else:
                    self.split_on_vertical(min_row, min_col, max_row, max_col)
     
    def split_on_horizontal(self, min_row, min_col, max_row, max_col):
        split = (min_row + max_row) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, split, max_col)
        self.random_split(split + 1, min_col, max_row, max_col)

    def split_on_vertical(self, min_row, min_col, max_row, max_col):        
        split = (min_col + max_col) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, max_row, split)
        self.random_split(min_row, split + 1, max_row, max_col)

    def carve_rooms(self):
        for leaf in self.leaves:
            # We don't want to fill in every possible room or the 
            # dungeon looks too uniform
            if random() > 0.80: continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            if section_height < 5 or section_width < 5:
                continue

            room_width = round(randrange(60, 100) / 100 * section_width)
            room_height = round(randrange(60, 100) / 100 * section_height)

            # If the room doesn't occupy the entire section we are carving it from,
            # 'jiggle' it a bit in the square
            if section_height > room_height:
                room_start_row = leaf[0] + randrange(section_height - room_height)
            else:
                room_start_row = leaf[0]

            if section_width > room_width:
                room_start_col = leaf[1] + randrange(section_width - room_width)
            else:
                room_start_col = leaf[1]
    
            self.rooms.append(Room(room_start_row, room_start_col, room_height, room_width))
            for r in range(room_start_row, room_start_row + room_height):
                for c in range(room_start_col, room_start_col + room_width):
                    self.dungeon[r][c] = DungeonSqr('.')

    def are_rooms_adjacent(self, room1, room2):
        adj_rows = []
        adj_cols = []
        for r in range(room1.row, room1.row + room1.height):
            if r >= room2.row and r < room2.row + room2.height:
                adj_rows.append(r)

        for c in range(room1.col, room1.col + room1.width):
            if c >= room2.col and c < room2.col + room2.width:
                adj_cols.append(c)

        return (adj_rows, adj_cols)

    def distance_between_rooms(self, room1, room2):
        centre1 = (room1.row + room1.height // 2, room1.col + room1.width // 2)
        centre2 = (room2.row + room2.height // 2, room2.col + room2.width // 2)

        return sqrt((centre1[0] - centre2[0]) ** 2 + (centre1[1] - centre2[1]) ** 2)

    def carve_corridor_between_rooms(self, room1, room2):
        if room2[2] == 'rows':
            row = choice(room2[1])
            # Figure out which room is to the left of the other
            if room1.col + room1.width < room2[0].col:
                start_col = room1.col + room1.width
                end_col = room2[0].col
            else:
                start_col = room2[0].col + room2[0].width
                end_col = room1.col                
            for c in range(start_col, end_col):
                self.dungeon[row][c] = DungeonSqr('.')
        else:
            col = choice(room2[1])
            # Figure out which room is above the other
            if room1.row + room1.height < room2[0].row:
                start_row = room1.row + room1.height
                end_row = room2[0].row
            else:
                start_row = room2[0].row + room2[0].height
                end_row = room1.row

            for r in range(start_row, end_row):
                self.dungeon[r][col] = DungeonSqr('.')

    # check each room, find the room with the closest room from another group
    def find_nearest_room_from_other_group(self, start_group, groups):
        pass
    # To make the dungeon fully reachable, group connected rooms together 
    # (we start off with all the rooms in a group of 1). Look for the nearest
    # room that is in a different group.
    
    def connect_rooms(self):
        groups = {}
        for j in range(len(self.rooms)):
            groups[j] = [self.rooms[j]]

        # Find the smallest group

        # ACTUALLY WHAT I SHOULD BE DOING!
        # - first go through all the rooms and calculate their distances to other adjacent rooms
        #   since I'll be using that over and over.
        #
        # - Until all the rooms are joined, loop over the groups, link the rooms that are closest,
        #   adjacent. Marge those groups, continue onward.
        smallest = 99999
        smallest_k = None
        for k in groups.keys():
            if len(groups[k]) < smallest:
                smallest = len(groups[k])
                smallest_k = k
            
        print(smallest_k)

        return
        unjoined = copy(self.rooms)

        while len(unjoined) > 1:
            room = choice(unjoined)
            unjoined.remove(room)
            
            #print(room.row, room.col, room.row + room.height, room.col + room.width)
            #for r in range(room.row, room.row + room.height):
            #    for c in range(room.col, room.col + room.width):
            #        self.dungeon[r][c] = DungeonSqr('1')
            
            nearest = 99999
            nearest_room = None

            # find candidate
            for candidate in unjoined:
                adj = self.are_rooms_adjacent(room, candidate)
                if len(adj[0]) > 0 or len(adj[1]) > 0:
                    d = self.distance_between_rooms(room, candidate)
                    if d < nearest:
                        nearest = d
                        if len(adj[0]) > 0:
                            nearest_room = (candidate, adj[0], 'rows')
                        else:
                            nearest_room = (candidate, adj[1], 'cols')

            #for r in range(nearest_room[0].row, nearest_room[0].row + nearest_room[0].height):
            #    for c in range(nearest_room[0].col, nearest_room[0].col + nearest_room[0].width):
            #        self.dungeon[r][c] = DungeonSqr('2')

            self.carve_corridor_between_rooms(room, nearest_room)
            unjoined.remove(nearest_room[0])
            
            

    def generate_map(self):
        self.random_split(1, 1, self.height - 1, self.width - 1)
        self.carve_rooms()
        self.connect_rooms()

    def print_map(self):
        for r in range(self.height):
            row = ''
            for c in range(self.width):
                row += self.dungeon[r][c].get_ch()
            print(row)

dg = RLDungeonGenerator(90, 45)
dg.generate_map()
dg.print_map()
