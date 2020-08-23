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
        
def get_sprite_cur_img(s):
    aname, aframes, adelay = s.animations[s.current_animation]
    img = world.image_db[aname]
    return img
                
def render_cam_sprites(screen, cam, sprites, ts, m):
    c_left, c_top = get_camera_game_coords(cam, m, ts)
    for s in sprites:
        srect = s.get_rect()
        sw = srect.width
        sh = srect.height
        on_x = s.x >= c_left - sw and s.x < c_left + cam.width
        on_y = s.y >= c_top - sh and s.y < c_top + cam.height
        if on_x and on_y:
            img = s.simple_img if s.simple_img != None else get_sprite_cur_img(s)            
            screen.blit(img, (s.x - c_left, s.y - c_top))
                
    return screen
        
def get_camera_game_coords(camera, m, ts):
    tgtx = camera.target.x
    tgty = camera.target.y
   
    centerx = int(camera.width / 2)
    centery = int(camera.height / 2)
    
    maxx = len(m[0]) * ts.tile_width - centerx
    maxy = len(m) * ts.tile_width - centery
    
    if tgtx <= centerx:
        tgtx = centerx        
    if tgty <= centery:
        tgty = centery
    if tgtx >= maxx:
        tgtx = maxx
    if tgty >= maxy:
        tgty = maxy
    
    c_left = tgtx - centerx + randint(0, camera.shake)
    c_top = tgty - centery + randint(0, camera.shake)
    
    return (c_left, c_top)

def render_camera_tiles(camera, ts, m):   
    c_left, c_top = get_camera_game_coords(camera, m, ts)
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
    
    xgap = c_left % ts.tile_width
    ygap = c_top % ts.tile_height
    clipped = pygame.Surface((camera.width, camera.height))
    clipped.blit(result, (0,0), (xgap, ygap, camera.width, camera.height)) 
    return clipped

def render_camera(camera, ts, m, sprites):
    result = render_camera_tiles(camera, ts, m)
    result = render_cam_sprites(result, camera, sprites, ts, m)
    return result
    
def draw_interface(screen, cam, ts, game_map, sprites):
    # Draw the camera
    CAMX = 50
    CAMY = 50
    cam_surface = render_camera(cam, ts, game_map, sprites)
    screen.blit(cam_surface, (CAMX, CAMY))
    # TASK: Maybe draw a pretty border around the camera, I dunno
    # TASK: Draw player stats
    # TASK: Draw inventory? 
    # TASK: Brainstorm other things that should go on the screen
    
   
    