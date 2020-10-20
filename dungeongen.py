from random import choice, randint
import bsp
import itertools
from tools import first

class Graphnode:
    def __init__ (self, name, value, neighbors=None):
        self.name = name
        self.value = value
        self.neighbors = set()
        

def make_room(w,h, floor_tile=0, wall_tile=1):
    """Returns a list of lists of tile numbers"""
    results = []
    top_tile = 6
    top_corner = 1
    # Top row is always all 1s: 4 --> [1,1,1,1]
    top_row = [top_corner] + [top_tile for x in range(w - 2)] + [top_corner] #make_list_of_1s(w) 
    results.append(top_row)
    for x in range(h - 2):
        side_wall = 1
        middle_row = make_middle(w, side_wall, floor_tile)
        results.append(middle_row)
    bottom_row = [wall_tile for x in range(w)]
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
    if r1.x + r1.w == r2.x:
        return (True, "lr")
    # r1.y
    if r1.y == r2.y + r2.h:
        return (True, "du")
    if r1.x == r2.x + r2.w:
        return (True, "rl")
    if r1.y + r1.h == r2.y:
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

def stamp_hallway(r1, r2, atype, m):
    # if r1 is left of r2 then the atype will be lr
    # But, in terms of hallway building, if r1 is left of r2, 
    #   the door is on the right and the hallway digs to the right
    # Therefore, you need to swap directions (e.g, to rl) when thinking about digging.
    
    d1 = get_door(r1, atype[1])
    d2 = get_door(r2, atype[0])
    if d1 == None or d2 == None:
        return
    m[d1[1]][d1[0]] = 2 #if randint(1, 5) == 1 else 2
    m[d2[1]][d2[0]] = 2 #if randint(1, 5) == 1 else 2
    dir = atype[1]
    cur_x, cur_y = change_d(dir, d1)
    end = change_d(atype[0], d2)
    #m[end[1]][end[0]] = 4
    l = 0
    while True:
        m[cur_y][cur_x] = 4
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
            m[cur_y][cur_x] = 4
            return
         
        if m[cur_y][cur_x] not in [3, 14]:
            cur_x = old_x
            cur_y = old_y
            
        if cur_x == old_x and cur_y == old_y:
            l += 1 

testmap = [[3 for x in range(50)] for y in range(30)]    
r1 = bsp.Area(30,9,10,5)    
r2 = bsp.Area(11,16,10,10)
r1s = make_room(r1.w, r1.h)
r2s = make_room(r2.w, r2.h)
stamp(r1.x, r1.y, r1s, testmap)
stamp(r2.x, r2.y, r2s, testmap)
stamp_hallway(r1, r2, "du", testmap)
for row in testmap:
    r = list(map(str,row))
    print("".join(r)) 

def adjacent_zones(zones):
    results = []
    combos = itertools.combinations(zones, 2)
    for c in combos:
        roomstocheck = itertools.product(c[1], c[0])
        pairs = list(filter(lambda p: adjacentcheck(p[0], p[1])[0], roomstocheck))
        if pairs != []:
            results.append(c)
        else:
            pass
            #print("zone:")
            #for a in c[0]:
            #    print(str(a))
            #print("other zone:")
            #for b in c[1]:
            #    print(str(b))
            #exit()
    return results           

def make_graph(zone_pairs):
    cur_name = 0
    nodes = []
    for z1, z2 in zone_pairs:
        z1n = first(lambda n: n.value == z1, nodes)
        z2n = first(lambda n: n.value == z2, nodes)
        
        
        if z1n == None:
            z1n = Graphnode(cur_name, z1)
            cur_name += 1
            nodes.append(z1n)
        if z2n == None:
            z2n = Graphnode(cur_name, z2)
            cur_name += 1
            nodes.append(z2n)
        
        # These seem to reference the same neighbor list.
        
        assert(id(z1n.neighbors) != id(z2n.neighbors))
        z1n.neighbors.add(z2n)
        z2n.neighbors.add(z1n)
        
        
        #print(z1n.neighbors)
        
        #print("joining %s and %s" % (z1n.name, z2n.name))
        #for n in z1n.neighbors:
        #    print("\t%s" % n.name)
       
        
    
    for n in nodes:
        #print(n.name)
        for nb in n.neighbors:
            pass
            #print("\t%s", nb.name)
    #print()
    #print(len(zone_pairs))
    return nodes[0]
        
def make_dungeon(size):
    blank_tile = 3
    dungeon = [[blank_tile for x in range(size)] for y in range(size)]
    zones = bsp.make_bsp_rooms(size,size)
    azones = adjacent_zones(zones)
    #for a in azones:
    #    print(a)
 
    #exit()
    # Looks to me like adjacent zones is returning somewhat reasonable data (but with some weird island nodes)
    # Maybe the bug is in make_graph?
    make_graph(azones)
    for z in zones:
        make_zone(z, dungeon)
    return dungeon
    

    
def make_zone(rooms, dungeon):
    pairs = get_pairs(rooms)
    
    for r in rooms:
        r.x += 3
        r.y += 3
        r.w -= 6
        r.h -= 6
    
    for r in rooms:
        stamp(r.x, r.y, make_room(r.w, r.h, 0, 6), dungeon)
       #stamp(r.x + 5, r.y + 5, make_room(r.w - 10, r.h - 10, 0, 98), dungeon)
    for p in pairs:
        room_pair, adj_data = p
        r1, r2 = room_pair
        # print(r1)
        # print(r2)        
        # print(adj_data)
        # exit() 
        
        stamp_hallway(r1, r2, adj_data[1], dungeon)
    
    
            
    return dungeon

#make_dungeon(130)