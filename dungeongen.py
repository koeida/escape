from random import choice, randint
import bsp
import itertools
from tools import first, two_chunk, filter_dict, map_dict, get_coords
import pygame
import time
from copy import deepcopy
from sprites import Sprite
import world
import creatures


dungeon_viz = []
colors = [(randint(0,255), randint(0,255), randint(0,255)) for x in range(50)]

class Graphnode:
    def __init__ (self, name, value, neighbors=None):
        self.name = name
        self.value = value
        self.neighbors = set()
        
class Zone:
    def __init__ (self, name, rooms, x, y, w, h):
        self.name = name
        self.rooms = rooms
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.floor_tile = choice(filter_dict(lambda v: v.floor_tile, world.TILES.data))
        mapped = map_dict(lambda k,v: (k, v.matching_tile), world.TILES.data)
        filtered = list(filter(lambda t: t[1] != None, mapped))
        print("jadkLwj;jwoIDJWODJ;jwdoWJ;O" + str(filtered))
        self.wall_tile, self.top_tile = choice(filtered)
        
def make_room(w,h, floor_tile=0, wall_tile=1, top_tile=6):
    """Returns a list of lists of tile numbers"""
    results = []
    top_corner = wall_tile
    # Top row is always all 1s: 4 --> [1,1,1,1]
    top_row = [top_corner] + [top_tile for x in range(w - 2)] + [top_corner] #make_list_of_1s(w) 
    results.append(top_row)
    for x in range(h - 2):
        middle_row = make_middle(w, wall_tile, floor_tile)
        results.append(middle_row)
    bottom_row = [top_tile for x in range(w)]
    results.append(bottom_row)
    # Middle rows, first tile is 1
    v_cord = []
    for row in range(h):
        for column in range(w):
            if results[row][column] == wall_tile and not is_corner(column,row,w,h):
                v_cord.append([row , column])
    v = choice(v_cord)
    #results[v[0]][v[1]] = 3
    return results
def make_middle(n, wall_tile=1, floor_tile=0):
    l = [wall_tile]
    for x in range(n - 2):
        l.append(floor_tile)
    l.append(wall_tile)
    return l
def is_corner(x, y, w, h):
    if x == 0 and y == h:
        return True
    elif x == 0 and y == 0:
        return True
    elif x == w and y == 0:
        return True
    elif x == w and y == h:
        return True
    return False    
def make_list_of_1s(n):
    l = []
    for x in range(n):
       l.append(1)
    return l
    
def printmap(m):
    for row in m:
        r = list(map(str,row))
        print("".join(r))

def on_map(x,y,m):
    """Returns True if x,y is within map m"""
    return (x > 0 and x < len(m[0]) and y > 0 and y < len(m))
    
def stamp(x,y,s,m, ignore_tile=None):
    """Stamps s onto m at coordinates x,y"""
    for sy in range(len(s)):
        for sx in range(len(s[0])):
            if on_map(x + sx, y + sy, m):
                if s[sy][sx] != ignore_tile:
                    m[y + sy][x + sx] = s[sy][sx]

def adjacentcheck(r1, r2):
    #print("%s ==? %s" % (r1, r2))
    if r1.x + r1.w == r2.x and r1.y < r2.y + r2.h and r1.y + r1.h > r2.y:
        return (True, "lr")
    # r1.y
    if r1.y == r2.y + r2.h and r1.x < r2.x + r2.w and r1.x + r1.w > r2.x:
        return (True, "du")
    if r1.x == r2.x + r2.w and r1.y < r2.y + r2.h and r1.y + r1.h > r2.y:
        return (True, "rl")
    if r1.y + r1.h == r2.y and r1.x < r2.x + r2.w and r1.x + r1.w > r2.x:
        return (True, "ud")
   # print(r1)
    #print(r2)
    #print("")
    return (False, None)
    
def get_pairs(rooms):
    pairs = itertools.combinations(rooms, 2)
    pairs = list(map(lambda p: (p, adjacentcheck(p[0],p[1])), pairs))
    pairs = list(filter(lambda p: p[1][0], pairs))
    
    return pairs
    
def get_door(r, side):
    if side in ("l", "r"):
        l = range(r.y + 1, r.y + r.h - 1)
        if side == "l":
            l = list(map(lambda y: (r.x, y), l))
        else:
            l = list(map(lambda y: (r.x + r.w - 1, y), l))
    if side in ("u", "d"):
        l = range(r.x + 1, r.x + r.w - 1)
        if side == "u":
            l = list(map(lambda x: (x, r.y), l))
        else:
            l = list(map(lambda x: (x, r.y + r.h - 1), l))
    if l == []:
        return None
    return choice(l)
    
        
    pass
    
def change_d(dir, d):
    if dir == "u":
        cur_x = d[0]
        cur_y = d[1] - 1
    if dir == "d":
        cur_x = d[0]
        cur_y = d[1] + 1
    if dir == "l":
        cur_x = d[0] - 1
        cur_y = d[1] 
    if dir == "r":
        cur_x = d[0] + 1
        cur_y = d[1]
    return (cur_x, cur_y)

def stamp_hallway(r1, r2, atype, m, doortile=2, hall_tile=4):
    # if r1 is left of r2 then the atype will be lr
    # But, in terms of hallway building, if r1 is left of r2, 
    #   the door is on the right and the hallway digs to the right
    # Therefore, you need to swap directions (e.g, to rl) when thinking about digging.
    
    d1 = get_door(r1, atype[1])
    d2 = get_door(r2, atype[0])
    if d1 == None or d2 == None:
        return
    m[d1[1]][d1[0]] = doortile #if randint(1, 5) == 1 else 2
    m[d2[1]][d2[0]] = doortile #if randint(1, 5) == 1 else 2
    dir = atype[1]
    cur_x, cur_y = change_d(dir, d1)
    end = change_d(atype[0], d2)
    #m[end[1]][end[0]] = 4
    l = 0
    while True:
        m[cur_y][cur_x] = hall_tile
        old_x = cur_x
        old_y = cur_y
        if randint(1,2) == 1   :
            if cur_x < end[0]:
                cur_x += 1
            elif cur_x > end[0]: 
                cur_x -= 1
            else:
                cur_x += randint(-1, 1)
        else:
            if cur_y < end[1]:
                cur_y += 1
            elif cur_y > end[1]:
                cur_y -= 1
            else:
                cur_y += randint(-1, 1)
        
        if l == 100:
            #print("nub!")
            return
        if cur_x == end[0] and cur_y == end[1]:
            m[cur_y][cur_x] = hall_tile
            return
         
        if m[cur_y][cur_x] not in [3, 4]:
            cur_x = old_x
            cur_y = old_y
            
        if cur_x == old_x and cur_y == old_y:
            l += 1 

# testmap = [[3 for x in range(50)] for y in range(30)]    
# r1 = bsp.Area(30,9,10,5)    
# r2 = bsp.Area(11,16,10,10)
# r1s = make_room(r1.w, r1.h)
# r2s = make_room(r2.w, r2.h)
# stamp(r1.x, r1.y, r1s, testmap)
# stamp(r2.x, r2.y, r2s, testmap)
# stamp_hallway(r1, r2, "du", testmap)
# for row in testmap:
    # r = list(map(str,row))
    # print("".join(r)) 

def adjacent_zone_rooms(z1, z2):
    roomstocheck = itertools.product(z2.rooms, z1.rooms)
    pairs = list(filter(lambda p: adjacentcheck(p[0], p[1])[0], roomstocheck))
    return pairs
    
def adjacent_zones(zones):
    results = []
    combos = itertools.combinations(zones, 2)
    for c in combos:
        pairs = adjacent_zone_rooms(c[0], c[1])
        if pairs != []:
            results.append(c)
    return results           

def make_graph(zone_pairs):
    cur_name = 0
    nodes = []
    for z1, z2 in zone_pairs:
        z1n = first(lambda n: n.value == z1, nodes)
        z2n = first(lambda n: n.value == z2, nodes)
        
        
        if z1n == None:
            z1n = Graphnode(z1.name, z1)
            nodes.append(z1n)
        if z2n == None:
            z2n = Graphnode(z2.name, z2)
            nodes.append(z2n)
    
        assert(id(z1n.neighbors) != id(z2n.neighbors))
        z1n.neighbors.add(z2n)
        z2n.neighbors.add(z1n)
       
        #print(z1n.neighbors)
        
        #print("joining %s and %s" % (z1n.name, z2n.name))
        #for n in z1n.neighbors:
        #    print("\t%s" % n.name)
       
        
    
    for n in nodes:
        print(n.name)
        for nb in n.neighbors:
            print("\t%s", nb.name)
    #print()
    #print(len(zone_pairs))
    return nodes[0]

def connect_zones(zones, node):
    walk = done_walk(node, len(zones))
    walk = list(map(lambda n: n.name, walk))
    end = zones[walk[-1]]
    start = zones[walk[0]]
    chunks = two_chunk(walk)

    results = []
    for c in chunks:
       pairs = adjacent_zone_rooms(zones[c[0]], zones[c[1]])
       r1, r2  = choice(pairs)
       direction = adjacentcheck(r1,r2)[1]
       results.append((r1, r2, direction))
    return results, start, end
    
def done_walk(cur_node, length):
    history = []
    while len(history) != length:
        history = drunken_walk([], cur_node)
    return history
    
    
def drunken_walk(history, cur_node):
    n = cur_node.neighbors
    n = list(filter(lambda x: x not in history, n))
    if n == []:
        return history
    else:
        node = choice(n)
        history.append(node)
        return drunken_walk(history, node)

def shrink_room(room):
    r = deepcopy(room)
    r.x += 3
    r.y += 3
    r.w -= 6
    r.h -= 6
    return r
    
def make_dungeon(size, viz_screen=None):
    blank_tile = 3
    dungeon = [[blank_tile for x in range(size)] for y in range(size)]
    zs, zone_sizes = bsp.make_bsp_rooms(size,size)
    tsize = 32
    zones = []
    for z in range(len(zs)):
        zdata = zone_sizes[z].name
        zx, zy, zw, zh = list(map(lambda x: x * tsize, [zdata.x, zdata.y, zdata.w, zdata.h]))
        zone = Zone(z, zs[z], zx, zy, zw, zh)
        zones.append(zone)
    azones = adjacent_zones(zones)

    zone_num = 0
    room_list = []
    if viz_screen != None:
        for z in zones:
            room_list += z.rooms
            draw_viz(viz_screen, room_list, "")
        #for z in zones:
            #for r in z:
            #    r.zone_num = zone_num
           # room_list += z
            #draw_viz(viz_screen, room_list, "")
            #draw_viz(viz_screen, room_list, "zone %d/%d" % (zone_num, len(zones.rooms)))
        #    zone_num += 1

    n = make_graph(azones)
    
    for z in zones:
        stamp_rooms(z, dungeon)
        
    joined_rooms, start, end = connect_zones(zones, n)
    for r1, r2, atype in joined_rooms:   
        stamp_hallway(shrink_room(r1), shrink_room(r2), atype,dungeon, 12, 10)

    line_hallways(size, dungeon)
    
    keys = []
    for z in zones:
        make_zone_hallways(z.rooms, dungeon)
        place_key(z, keys)
    
    trap_door_spawn(dungeon)
    return dungeon, keys, start, end, zones

def trap_door_spawn(m):
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == 16 and randint(1, 300) == 1:
                m[y][x] = 20
        

def trap_door_room(player):
    sprites = []
    m = [[3 for x in range(1000)] for y in range(1000)]
    floor_tiles = filter_dict(lambda x: x.floor_tile, world.TILES.data)
    room = make_room(15, 15, choice(floor_tiles), 1, 6)
    stamp(35, 35, room, m)
    sprites.append(player.shield)
    if randint(1, 1) == 1:
        key_anim = { "walking": {"down": ("keyanimation", 32, 32, [0,1,2,3,4], 4)}}
        key = Sprite(1152, 1152, "key", key_anim)
        key.alive = True
        key.hitpoints = 2
        key.item = True
        sprites.append(key)
    
    ladder = Sprite(1152, 1152, "ladder", simple_img=world.image_db["chest"])
    ladder.topx = player.x
    ladder.topy = player.y
    sprites.append(ladder)
    
    spawnpoints = get_coords(m, filter_dict(lambda x: x.floor_tile, world.TILES.data))
    
    for x in range(2):
        sprites.append(creatures.make_borg(m, spawnpoints, player))
    
    for x in range(2):
        sprites.append(creatures.make_vlation(m, spawnpoints, player))
        
    for x in range(1):
        sprites.append(creatures.make_skreet(m, spawnpoints, player))
    
    
    for x in range(1):
        sprites.append(creatures.make_gloub(m, spawnpoints, player))
    
    return m, sprites
    
def add_shadow(d, sprites):
    for y in range(len(d)):
        for x in range(len(d[0])):
            floor_tiles = filter_dict(lambda x: x.floor_tile, world.TILES.data)
            if d[y][x] in floor_tiles:
                if d[y - 1][x] not in floor_tiles and d[y][x + 1] not in floor_tiles:
                    shadow = Sprite(x * 32, y * 32, "shadow", simple_img=world.image_db["cornershadow"])
                    sprites.insert(0, shadow)
                elif d[y - 1][x] not in floor_tiles:
                    shadow = Sprite(x * 32, y * 32, "shadow", simple_img=world.image_db["topshadow"])
                    sprites.insert(0, shadow)
                elif d[y][x + 1] not in floor_tiles:
                    shadow = Sprite(x * 32, y * 32, "shadow", simple_img=world.image_db["sideshadow"])
                    sprites.insert(0, shadow)
                
    
def line_hallways(size, dungeon):
    for y in range(size):
        for x in range(size):
            try:
                adjacenttiles = [dungeon[y + 1][x], dungeon[y - 1][x], dungeon[y][x + 1], dungeon[y][x - 1], dungeon[y + 1][x + 1], dungeon[y - 1][x - 1], dungeon[y + 1][x - 1], dungeon[y - 1][x + 1]]

                if dungeon[y][x] == 3 and 10 in adjacenttiles:
                   dungeon[y][x] = 1
            except:
                pass
    for y in range(size):
        for x in range(size):
            if dungeon[y][x] == 10:
                dungeon[y][x] = 4
                
def stamp_rooms(z, dungeon):
    shrunk_rooms = map(shrink_room, z.rooms)
    
    for r in shrunk_rooms:
        stamp(r.x, r.y, make_room(r.w, r.h, z.floor_tile, z.wall_tile, z.top_tile), dungeon) 

def place_key(z, keys):   
    r = choice(z.rooms)
    for x in range(1):
        x = randint(r.x + 4, r.x + r.w - 5) * 32
        y = randint(r.y + 4, r.y + r.h - 5) * 32
        key_anim = { "walking": {"down": ("keyanimation", 32, 32, [0,1,2,3,4], 4)}}
        key = Sprite(x, y, "key", key_anim)
        key.alive = True
        key.hitpoints = 2
        key.item = True
        keys.append(key)
    
def make_zone_hallways(rooms, dungeon):
    pairs = get_pairs(rooms)
    
       #stamp(r.x + 5, r.y + 5, make_room(r.w - 10, r.h - 10, 0, 98), dungeon)
    for p in pairs:
        room_pair, adj_data = p
        r1, r2 = room_pair
        # print(r1)
        # print(r2)        
        # print(adj_data)
        # exit() 
        
        stamp_hallway(shrink_room(r1), shrink_room(r2), adj_data[1], dungeon)
    
    
def make_dungeon_keeg(size, viz_screen=None):
    global dungeon_viz

    blank_tile = 3
    dungeon = [[blank_tile for x in range(size)] for y in range(size)]
    zones = bsp.make_bsp_rooms(size,size)
    zone_num = 1
    room_list = []
    if viz_screen != None:
        for z in zones:
            for r in z:
                r.zone_num = zone_num
            room_list += z
            #draw_viz(viz_screen, room_list, "zone %d/%d" % (zone_num, len(zones)))
            zone_num += 1

    if viz_screen != None:
        draw_viz(viz_screen, room_list, "shrunked") 

    room_list = deepcopy(room_list)
    shrink_rooms(room_list)

    for z in zones:
        make_zone(z, dungeon, viz_screen, room_list)
    
    if viz_screen != None:
        draw_viz(viz_screen, room_list, "shrunked") 

    return dungeon
    

def shrink_rooms_keeg(rooms):
    for r in rooms:
        r.x += 3
        r.y += 3
        r.w -= 6
        r.h -= 6

    
def make_zone_keeg(rooms, dungeon, viz_screen=None, room_list=[]):
    pairs = get_pairs(rooms)

    shrink_rooms(rooms)

    for r in rooms:
        stamp(r.x, r.y, make_room(r.w, r.h, 0, 7), dungeon)
    for p in pairs:
        room_pair, adj_data = p
        r1, r2 = room_pair
        
        stamp_hallway(r1, r2, adj_data[1], dungeon)
            
    if viz_screen != None:
        draw_viz(viz_screen, room_list, "hallway %s -> %s (%s)" % (r1, r2, adj_data[1]), dungeon)
    return dungeon


#make_dungeon(130)

def waitforkey():
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                return

def write_text(screen, x, y, size, t, color=(255,255,255)):
    font = pygame.font.SysFont(None, size)
    img = font.render(t, True, color)
    screen.blit(img, (x, y))

def draw_all_rooms(screen, rooms, tw):
    for r in rooms:
        x = r.x
        y = r.y
        screen.fill(r.color, (x * tw, y * tw, r.w*tw, r.h*tw))
        write_text(screen, r.x * tw,r.y * tw, 12, str(r))
        write_text(screen, r.x * tw,r.y * tw + 12, 24, str(r.zone_num))
        #screen.fill((255,0,0), (y*tile_width,x*tile_width,r.w * tile_width,r.h * tile_width))

def draw_viz(screen, rooms, msg="", dungeon=[]):
    screen.fill((0,0,0))        
    tw = 4

    draw_all_rooms(screen, rooms, tw)
    if dungeon != []:
        for y in range(len(dungeon)):
            for x in range(len(dungeon)):
                if dungeon[y][x] == 4:
                    print("filly!")
                    screen.fill((255,255,255), (x*tw, y*tw, tw, tw))
    write_text(screen, 10, 1000, 24, msg)

    pygame.display.flip()
    waitforkey()


def visualize_gen(screen):   
    clock = pygame.time.Clock()
    running = True
    make_dungeon(140, screen)

def drawy():
    test_map = [[0 for x in range(70)] for y in range(70)]

    r1 = make_room(11, 30, floor_tile=0, wall_tile=1)
    r2 = make_room(12, 26, floor_tile=0, wall_tile=1)

    stamp(3, 3, r1, test_map)
    stamp(17, 39, r1, test_map)
    #stamp_hallway(r1, r2, 

    for r in test_map:
        r = list(map(str,r))
        print("".join(r))
