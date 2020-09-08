from random import choice, randint
import bsp
import itertools

def make_room(w,h, floor_tile=0, wall_tile=1):
    """Returns a list of lists of tile numbers"""
    results = []
    # Top row is always all 1s: 4 --> [1,1,1,1]
    top_row = [wall_tile for x in range(w)]#make_list_of_1s(w) 
    results.append(top_row)
    for x in range(h - 2):
        middle_row = make_middle(w, wall_tile, floor_tile)
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
        return (True, "rl")
    if r1.y == r2.y + r2.h:
        return (True, "ud")
    if r1.x == r2.x + r2.w:
        return (True, "lr")
    if r1.y + r1.h == r2.y:
        return (True, "du")
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
            l = list(map(lambda y: (r.x + r.w, y), l))
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

def stamp_hallway(r1, r2, atype, m):
    d1 = get_door(r1, atype[0])
    d2 = get_door(r2, atype[1])
    if d1 == None or d2 == None:
        return
    m[d1[1]][d1[0]] = 5
    m[d2[1]][d2[0]] = 5
    dir = atype[0]
    if dir == "u":
        cur_x = d1[0]
        cur_y = d1[1] - 1
    if dir == "d":
        cur_x = d1[0]
        cur_y = d1[1] + 1
    if dir == "l":
        cur_x = d1[0] - 1
        cur_y = d1[1] 
    if dir == "r":
        cur_x = d1[0] + 1
        cur_y = d1[1]
    while True:
        m[cur_y][cur_x] = 10
        if randint(1,2) == 1   :
            if cur_x < d2[0]:
                cur_x += 1
            elif cur_x > d2[0]: 
                cur_x -= 1
            else:
                cur_x += randint(-1, 1)
        else:
            if cur_y < d2[1]:
                cur_y += 1
            elif cur_y > d2[1]:
                cur_y -= 1
            else:
                cur_y += randint(-1, 1)
        if cur_x == d2[0] and cur_y == d2[1]:
            return
def make_dungeon(size):
    blank_tile = 33
    dungeon = [[blank_tile for x in range(size)] for y in range(size)]
    rooms = bsp.make_bsp_rooms(size,size)
    pairs = get_pairs(rooms)
    
    #roompair, atype = pairs[0]
    # r1, r2 = roompair
    # atype = atype[1]
    # print(r1)
    # print(r2)
    # print(atype)
    #print(atype[1])
        
    #print(r)
    #print(get_door(r, "r"))

    
    for r in rooms:
        r.x += 5
        r.y += 5
        r.w -= 10
        r.h -= 10
    
    for r in rooms:
        stamp(r.x, r.y, make_room(r.w, r.h, 0, 98), dungeon)
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


