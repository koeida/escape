from random import randint

def get_map_coords(px, py, tile_width, tile_height):
    mx = int(px / tile_width)
    my = int(py / tile_height)
    return (mx, my)
    

    
    