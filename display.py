import pygame
from collections import namedtuple
from gamemap import get_map_coords
import world
from random import randint

Tileset = namedtuple("Tileset", "image tile_width tile_height tiles_per_line rows data")
Camera = namedtuple("Camera", "target width height")

class Camera:
    def __init__(self, target, width, height):
        self.target = target
        self.width = width
        self.height = height
        self.shake = 0
    def set_shake(self, x):
        self.shake = x

class TileInfo:
    pass
    
def tile(walkable=True):
    results = TileInfo()
    results.walkable = walkable
    return results

def load_tileset(f, tile_width, tile_height):
    tileset_img = pygame.image.load(f)
    img_width = tileset_img.get_rect().width   
    img_height = tileset_img.get_rect().height    
    tiles_per_line = int(img_width / tile_width)
    rows = int(img_height / tile_height)   
    
    data = {98: tile(False)} 
    
   
    return Tileset(tileset_img, tile_width, tile_height, tiles_per_line, rows, data)

def draw_tile(screen, tileset, tile_number, x, y):
    tile_y = int(tile_number / tileset.tiles_per_line)
    tile_x = tile_number % tileset.tiles_per_line    
    
    tix = tile_x * tileset.tile_width
    tiy = tile_y * tileset.tile_width    
    
   
    screen.blit(tileset.image, (x,y), (tix, tiy, tileset.tile_width, tileset.tile_height))
        
        
def draw_sprite(screen, s, cam_left, cam_top, croprect=None):
    aname, aframes, adelay = s.animations[s.current_animation]
    img = world.image_db[aname]
    img_rect = img.get_rect()
    croprect = croprect if croprect != None else (0, 0, img_rect.width, img_rect.height)
    screen.blit(img, (s.x - cam_left, s.y - cam_top), croprect)
    
    
def draw_cam_sprites(screen, camera, sprites, c_left, c_top):
    for s in sprites:
        if s.x > c_left and s.x < c_left + camera.width:
            if s.y > c_top and s.y < c_top + camera.height:
                draw_sprite(screen,s, c_left, c_top)                
    

def draw_camera(screen, camera, ts, m, sx, sy, sprites):
    tgtx = camera.target.x
    tgty = camera.target.y
    
    if camera.target.x <= int(camera.width / 2):
        tgtx = int(camera.width / 2)
    if camera.target.y <= int(camera.width / 2):
        tgty = int(camera.width / 2)
        
    
    c_left = tgtx - int(camera.width / 2) + randint(0, camera.shake)
    c_top = tgty - int(camera.height / 2) + randint(0, camera.shake)
        
    xgap = c_left % ts.tile_width
    ygap = c_top % ts.tile_height
    
    start_mx, start_my = get_map_coords(c_left, c_top, ts.tile_width, ts.tile_height)
    
    num_tiles_wide = int(camera.width / ts.tile_width)  
    num_tiles_high = int(camera.width / ts.tile_width) 
    
    result = pygame.Surface((camera.width + ts.tile_width, camera.height + ts.tile_height))
    
    for y in range(num_tiles_high + 1):
        for x in range(num_tiles_wide + 1):
            yindex = y + start_my
            xindex = x + start_mx
            if yindex >= 0 and yindex < len(m) and xindex >= 0 and xindex < len(m[0]): 
                cur_tile = m[yindex][xindex]
                draw_tile(result, ts, cur_tile, x * ts.tile_width, y * ts.tile_height)
    
    
    screen.blit(result, (sx, sy), (xgap, ygap, camera.width, camera.height))
    draw_cam_sprites(screen, camera, sprites, c_left, c_top)
    
