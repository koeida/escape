import pygame
from collections import namedtuple
from gamemap import get_map_coords

Tileset = namedtuple("Tileset", "image tile_width tile_height tiles_per_line rows")
Camera = namedtuple("Camera", "target width height")

def load_tileset(f, tile_width, tile_height):
    tileset_img = pygame.image.load(f)
    img_width = tileset_img.get_rect().width   
    img_height = tileset_img.get_rect().height    
    tiles_per_line = int(img_width / tile_width)
    rows = int(img_height / tile_height)   
   
    return Tileset(tileset_img, tile_width, tile_height, tiles_per_line, rows)

def draw_tile(screen, tileset, tile_number, x, y):
    tile_y = int(tile_number / tileset.tiles_per_line)
    tile_x = tile_number % tileset.tiles_per_line    
    
    tix = tile_x * tileset.tile_width
    tiy = tile_y * tileset.tile_width    
    
   
    screen.blit(tileset.image, (x,y), (tix, tiy, tileset.tile_width, tileset.tile_height))
        
    
    

def draw_camera(screen, camera, ts, m, sx, sy):
    c_left = camera.target.x - int(camera.width / 2)
    c_top = camera.target.y - int(camera.height / 2)
    xgap = c_left % ts.tile_width
    ygap = c_top % ts.tile_height      
    
    start_mx, start_my = get_map_coords(c_left, c_top, ts.tile_width, ts.tile_height)
    
    num_tiles_wide = int(camera.width / ts.tile_width)  
    num_tiles_high = int(camera.width / ts.tile_width) 
    
    result = pygame.Surface((camera.width + ts.tile_width, camera.height + ts.tile_height))
    
    for y in range(num_tiles_high + 1):
        for x in range(num_tiles_wide + 1):
            cur_tile = m[y + start_my][x + start_mx]
            draw_tile(result, ts, cur_tile, x * ts.tile_width, y * ts.tile_height)
    
    
    screen.blit(result, (sx, sy), (xgap, ygap, camera.width, camera.height))
    
