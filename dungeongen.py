from random import choice, randint
import bsp
import itertools
import pygame
import time

dungeon_viz = []
colors = [(randint(0,255), randint(0,255), randint(0,255)) for x in range(50)]

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
    d1 = get_door(r1, atype[0])
    d2 = get_door(r2, atype[1])
    if d1 == None or d2 == None:
        return
    m[d1[1]][d1[0]] = 12 if randint(1, 5) == 1 else 2
    m[d2[1]][d2[0]] = 12 if randint(1, 5) == 1 else 2
    dir = atype[0]
    cur_x, cur_y = change_d(dir, d1)
    end = change_d(atype[1], d2)
    m[end[1]][end[0]] = 4
    l = 0
    while True:
        l += 1
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
            return
        if cur_x == end[0] and cur_y == end[1]:
            return
         
        if m[cur_y][cur_x] not in [3, 14]:
            cur_x = old_x
            cur_y = old_y

        
def make_dungeon(size, viz_screen=None):
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

    draw_viz(viz_screen, room_list, "shrunked") 

    for z in zones:
        make_zone(z, dungeon, viz_screen)
    
    draw_viz(viz_screen, room_list, "shrunked") 

    return dungeon
    

def shrink_rooms(rooms):
    for r in rooms:
        r.x += 3
        r.y += 3
        r.w -= 6
        r.h -= 6

    
def make_zone(rooms, dungeon, viz_screen=None):
    pairs = get_pairs(rooms)
    
    shrink_rooms(rooms)

    for r in rooms:
        stamp(r.x, r.y, make_room(r.w, r.h, 0, 6), dungeon)
    for p in pairs:
        room_pair, adj_data = p
        r1, r2 = room_pair
        
        stamp_hallway(r1, r2, adj_data[1], dungeon)
            
    return dungeon

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

def draw_all_rooms(screen, rooms):
    tw = 4
    for r in rooms:
        x = r.x
        y = r.y
        screen.fill(r.color, (x * tw, y * tw, r.w*tw, r.h*tw))
        write_text(screen, r.x * tw,r.y * tw, 12, str(r))
        write_text(screen, r.x * tw,r.y * tw + 12, 24, str(r.zone_num))
        #screen.fill((255,0,0), (y*tile_width,x*tile_width,r.w * tile_width,r.h * tile_width))

def draw_viz(screen, rooms, msg=""):
    screen.fill((0,0,0))        

    draw_all_rooms(screen, rooms)
    write_text(screen, 10, 1000, 24, msg)


    pygame.display.flip()
    waitforkey()


def visualize_gen(screen):   
    clock = pygame.time.Clock()
    running = True
    make_dungeon(120, screen)


pygame.init()
screen = pygame.display.set_mode((1280, 1024))
try:
    visualize_gen(screen)
except Exception as e:
    print(e)
    pygame.display.quit()

                

        

