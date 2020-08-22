from random import randint

def get_map_coords(px, py, tile_width, tile_height):
    mx = int(px / tile_width)
    my = int(py / tile_height)
    return (mx, my)    

def onscreen(mx,my,m):
    return mx >= 0 and mx < len(m[0]) and my >= 0 and my < len(m)
    
def walkable(mapx, mapy, m, ts):
    current_tile = m[mapy][mapx]
    if current_tile in ts.data:
        return ts.data[current_tile].walkable
    else:
        return True
    

    
    