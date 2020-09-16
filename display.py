import pygame
from collections import namedtuple
from gamemap import get_map_coords
import world
from random import randint
from functools import reduce
from tools import first
import math

Tileset = namedtuple("Tileset", "image tile_width tile_height tiles_per_line rows data")

class Camera:
    def __init__(self, target, x, y, width, height):
        self.target = target
        self.width = width
        self.height = height
        self.shake = 0
        self.x = x
        self.y = y
    def set_shake(self, x):
        self.shake = x

class TileInfo:
    pass
    
def tile(walkable=True):
    results = TileInfo()
    results.walkable = walkable
    return results

def load_tileset(tileset_img, tile_width, tile_height):
    img_width = tileset_img.get_rect().width   
    img_height = tileset_img.get_rect().height    
    tiles_per_line = int(img_width / tile_width)
    rows = int(img_height / tile_height)   
    
    data = {1: tile(False),
            3: tile(False),
            6: tile(False),
            12: tile(False)} 
   
    return Tileset(tileset_img, tile_width, tile_height, tiles_per_line, rows, data)
    
def hitbar(max,cur,screen):
    screen.fill((20,20,20),(35,35,max,30))
    screen.fill((0,150,30),(35,35,cur,30))
    
    

def draw_tile(screen, tileset, tile_number, x, y):
    tile_y = int(tile_number / tileset.tiles_per_line)
    tile_x = int(tile_number % tileset.tiles_per_line)
    
    tix = tile_x * tileset.tile_width
    tiy = tile_y * tileset.tile_width    
    
    screen.blit(tileset.image, (x,y), (tix, tiy, tileset.tile_width, tileset.tile_height))

def stack_spritesheets(ss):
    def blitreturn(s1,s2):
        s1.blit(s2,(0,0))
        return s1

    
    width = world.image_db[ss[0]].get_rect().width
    height = world.image_db[ss[0]].get_rect().height
    blanksurf = pygame.Surface((width,height), pygame.SRCALPHA)
    
    ss = list(map(lambda s: world.image_db[s], ss))

    return reduce(blitreturn, [blanksurf] + ss)
    
        
def get_sprite_cur_img(s):
    aname, width, height, aframes, adelay = s.animations[s.current_animation]
    img = world.image_db[aname]
    return img

def get_tile_coords(tileset, tile_number):
    tile_y = int(tile_number / tileset.tiles_per_line)
    tile_x = int(tile_number % tileset.tiles_per_line)
    
    tix = tile_x * tileset.tile_width
    tiy = tile_y * tileset.tile_width    
    return (tix, tiy)

def render_sprite(screen, c_left, c_top, s):
    if s.simple_img != None:
        screen.blit(s.simple_img, (s.x - c_left, s.y - c_top))
    else:
        aname, width, height, aframes, adelay = s.animations[s.current_animation][s.facing]
        img = world.image_db[aname]
        ts = load_tileset(img, width, height)
        try:
            current_tile_number = aframes[s.current_frame]
        except:
            current_tile_number = aframes[0]
        tix, tiy = get_tile_coords(ts, current_tile_number) 
        screen.blit(img, (s.x - c_left, s.y - c_top), (tix, tiy, ts.tile_width, ts.tile_height))
        hitbox_rect = pygame.Rect(s.x + s.hitbox.x - c_left, s.y + s.hitbox.y - c_top, s.hitbox.width, s.hitbox.height)
        pygame.gfxdraw.rectangle(screen, hitbox_rect, (255,0,0))
                
def render_cam_sprites(screen, cam, sprites, ts, m):
    c_left, c_top = get_camera_game_coords(cam, m, ts)
    for s in sprites:
        srect = s.get_rect()
        sw = srect.width
        sh = srect.height
        on_x = s.x >= c_left - sw and s.x < c_left + cam.width
        on_y = s.y >= c_top - sh and s.y < c_top + cam.height
        if on_x and on_y:
            render_sprite(screen, c_left, c_top, s)
                
    return screen
        
        
""" Returns the absolute x/y coordinates of the camera's left(x) and top(y) pixels """
def get_camera_game_coords(camera, m, ts):
    tgtx = camera.target.x + int(camera.target.get_rect().width / 2)
    tgty = camera.target.y + int(camera.target.get_rect().height / 2)
   
    centerx = int(camera.width / 2)
    centery = int(camera.height / 2)
    
    c_left = tgtx - centerx + randint(0, camera.shake)
    c_top = tgty - centery + randint(0, camera.shake)
    
    return (c_left, c_top)
    
def clip_tiles(tile_surf, c_left, c_top, ts, camera):
    xgap = c_left % ts.tile_width
    ygap = c_top % ts.tile_height
    clipped = pygame.Surface((camera.width, camera.height))
    clipped.blit(tile_surf, (0,0), (xgap, ygap, camera.width, camera.height)) 
    return clipped
    
def render_camera_tiles(camera, ts, m):
    tw = ts.tile_width
    th = ts.tile_height
    c_left, c_top = get_camera_game_coords(camera, m, ts)
    start_mx, start_my = get_map_coords(c_left, c_top, ts.tile_width, ts.tile_height)
    num_tiles_wide = int(camera.width / ts.tile_width)  
    num_tiles_high= int(camera.width / ts.tile_width) 
    
    tiles = [(x * tw, y * th, m[y + start_my][x + start_mx])
             for x in range(num_tiles_wide + 1)
             for y in range(num_tiles_high + 1)
             if y + start_my >= 0 and y + start_my < len(m) and 
                x + start_mx >= 0 and x + start_mx < len(m[0])]
    result = pygame.Surface((camera.width + ts.tile_width, camera.height + ts.tile_height))    
    
    for tx, ty, tnum in tiles:
        draw_tile(result, ts, tnum, tx, ty)

    
    return clip_tiles(result, c_left, c_top, ts, camera)

def render_camera(camera, ts, m, sprites):
    result = render_camera_tiles(camera, ts, m)
    result = render_cam_sprites(result, camera, sprites, ts, m)
    return result
    
def draw_interface(screen, cam, ts, game_map, sprites):
    # Draw the camera
    cam_surface = render_camera(cam, ts, game_map, sprites)
    screen.blit(cam_surface, (cam.x, cam.y))
    player = first(lambda s: s.kind =="player",sprites) 
    hitbar(100,player.hitpoints,screen)
    # TASK: Maybe draw a pretty border around the camera, I dunno
    # TASK: Draw player stats
    # TASK: Draw inventory? 
    # TASK: Brainstorm other things that should go on the screen
    
def calc_screen_coords(game_coords, camrect, cam, m, ts):
    gx,gy = game_coords
    camx, camy, camw, camh = camrect
    cam_left_game, cam_top_game = get_camera_game_coords(cam, m, ts)
    gx_oncam = cam_left_game - gx
    gy_oncam = cam_top_game - gy
    #meh
    
    
def render_shield(player_sx, playersy, mouse_x, mouse_y, swidth):
    cam_size = 32*9
    cam_pos = 50
    rel_x, rel_y = mouse_x - cam_pos - cam_size, mouse_y - cam_pos - cam_size
    #angle = math.atan2(rel_y, rel_x)
    angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
    shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    sangle = 90 / 2
    smiddle = 100
    pygame.gfxdraw.arc(shield_surface, smiddle, smiddle, 45, 
                       int(angle - sangle), int(angle + sangle),
                       (255, 255, 255))  
    return shield_surface
    
