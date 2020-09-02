from random import randint

def get_map_coords(px, py, tile_width, tile_height):
    pxmod = pymod = 0
    if px < 0:
        pxmod = -1
    if py < 0:
        pymod = -1
    mx = int(px / tile_width) + pxmod
    my = int(py / tile_height) + pymod
    return (mx, my)    

def onscreen(mx,my,m):
    return mx >= 0 and mx < len(m[0]) and my >= 0 and my < len(m)
    
def walkable(mapx, mapy, m, ts):
    current_tile = m[mapy][mapx]
    if current_tile in ts.data:
        return ts.data[current_tile].walkable
    else:
        return True

def gen_test_map():
    game_map = [[0 for x in range(100)] for y in range(100)]
    for x in range(1000):
        game_map[randint(0,99)][randint(0,99)] = randint(0,7)
    
    for x in range(100):
        game_map[0][x] = 16 * 6 + 2
        game_map[len(game_map[0]) - 1][x] = 16 * 6 + 2
    
    
    for y in range(100):
        game_map[y][0] = 16 * 6 + 2
        game_map[y][len(game_map) - 1] = 16 * 6 + 2
        
    
    return game_map
