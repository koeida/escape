import pygame
from collections import namedtuple
from gamemap import get_map_coords
import world
from random import randint
from functools import reduce
from tools import first
import math

import particles as part

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
      

    
    
    
def hitbar(max,cur,screen):
    screen.fill((20,20,20),(35,35,max,30))
    screen.fill((0,150,30),(35,35,cur,30))
    
def sanebar(max,cur,screen):
    screen.fill((20,20,20),(600,300,10,max))
    screen.fill((255,0,0),(600,300,10,cur))
    
    

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
        if s.angle != None:
            nimg = pygame.transform.rotate(s.original_img, s.angle)
            r = s.simple_img.get_rect()
            r.x = s.x
            r.y = s.y
            nr = nimg.get_rect()
            nr.center = r.center
            nr.x -= c_left
            nr.y -= c_top
            screen.blit(nimg, nr)
        else:
            screen.blit(s.simple_img, (s.x - c_left, s.y - c_top))
    else:
        aname, width, height, aframes, adelay = s.animations[s.current_animation][s.facing]
        img = world.image_db[aname]
        ts = world.load_tileset(img, width, height)
        try:
            current_tile_number = aframes[s.current_frame]
        except:
            current_tile_number = aframes[0]
        tix, tiy = get_tile_coords(ts, current_tile_number) 
        screen.blit(img, (s.x - c_left, s.y - c_top), (tix, tiy, ts.tile_width, ts.tile_height))
        #hitbox_rect = pygame.Rect(s.x + s.hitbox.x - c_left, s.y + s.hitbox.y - c_top, s.hitbox.width, s.hitbox.height)
        #pygame.gfxdraw.rectangle(screen, hitbox_rect, (255,0,0))
                
def render_cam_sprites(screen, cam, sprites, ts, m, light_screen):
    c_left, c_top = get_camera_game_coords(cam, m, ts)
    for s in sprites:
        srect = s.get_rect()
        sw = srect.width
        sh = srect.height
        on_x = s.x >= c_left - sw and s.x < c_left + cam.width
        on_y = s.y >= c_top - sh and s.y < c_top + cam.height

        light_distance = 200
        on_x_light = s.x >= c_left - sw - light_distance and s.x < c_left + cam.width + light_distance
        on_y_light = s.y >= c_top - sh - light_distance and s.y < c_top + cam.height + light_distance

        if on_x and on_y:
            render_sprite(screen, c_left, c_top, s)

        if on_x_light and on_y_light and s.light:
            light_screen.blit(world.image_db["light"], (s.x - c_left - 150, s.y - c_top - 150), special_flags=pygame.BLEND_RGBA_SUB)
                
    return screen
    
def render_cam_particles(screen, cam, ts, m,sprites):
    c_left, c_top = get_camera_game_coords(cam, m, ts)
    for p in part.particles:
        on_x = p.x >= c_left and p.x < c_left + cam.width
        on_y = p.y >= c_top and p.y < c_top + cam.height
        if on_x and on_y:
            screen.fill(p.color, (p.x - c_left, p.y - c_top, p.size,p.size))
            
                
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

def render_camera(camera, ts, m, sprites, light_screen):
    result = render_camera_tiles(camera, ts, m)
    result = render_cam_sprites(result, camera, sprites, ts, m, light_screen)
    result = render_cam_particles(result, camera, ts, m,sprites)
    return result
    
def blit_text(screen, text, x, y, size, color=(255,255,255), font_type = None):
    text = str(text)
    if font_type == None:
        font = pygame.font.SysFont("Terminal", size)
    else:
        font = pygame.font.Font(font_type, size)
        
    text = font.render(text, True, color)
    screen.blit(text, (x,y))

def draw_inventory(screen, inventory):
    for y in range(2):
        for x in range(8):
            screen.blit(world.image_db["i_square"], (520+x*32, 32+y*32))


def draw_interface(screen, cam, ts, game_map, sprites):
    # Draw the camera
    dark_surface = pygame.Surface((cam.width, cam.height), pygame.SRCALPHA)
    dark_surface.fill((0,0,0))
    cam_surface = render_camera(cam,  ts, game_map, sprites, dark_surface)
    screen.blit(cam_surface, (cam.x, cam.y))
    #screen.blit(world.image_db["darkscreen"],(cam.x,cam.y))
    screen.blit(dark_surface, (cam.x, cam.y))
    player = first(lambda s: s.kind == "player", sprites) 
    if player != None:
        hitbar(100, player.hitpoints,screen)
        sanebar(200,player.sanity,screen)
    if world.mode == "dialogue":
        dialoguebox(screen, 100, 100, 200, 100, world.dialogue_message)
        if world.choice != "":
            dialoguebox(screen, 100, 225, 200, 32, world.choice)
    # TASK: Maybe draw a pretty border around the camera, I dunno
    # TASK: Draw player stats
    screen.blit(world.image_db["coin"], (0, 510))
    blit_text(screen, player.money, 50, 512, 48)
    # TASK: Draw inventory?
    draw_inventory(screen, player.inventory)
    # TASK: Brainstorm other things that should go on the screen
    
def calc_screen_coords(game_coords, camrect, cam, m, ts):
    gx,gy = game_coords
    camx, camy, camw, camh = camrect
    cam_left_game, cam_top_game = get_camera_game_coords(cam, m, ts)
    gx_oncam = cam_left_game - gx
    gy_oncam = cam_top_game - gy
    #meh
    
    
def render_shield(mouse_x, mouse_y, swidth, shield):
    cam_size = 32*9
    cam_pos = 50
    rel_x, rel_y = mouse_x - cam_pos - cam_size, mouse_y - cam_pos - cam_size
    #angle = math.atan2(rel_y, rel_x)
    angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
    shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    sangle = shield.width / 2
    smiddle = 50
    pygame.gfxdraw.arc(shield_surface, smiddle, smiddle, 45, 
                       int(angle - sangle), int(angle + sangle),
                       (255, 255, 255))  
    return shield_surface
  

def text_lines(lpl, message):
    lines = []
    message += " " 
    while message != "":
        line = message[:lpl]
        other = ""
        while line[-1] != " ":
            other += line[-1]
            line = line[:-1]
        message = other[::-1] + message[lpl:]
        lines.append(line)
    return lines


  
def dialoguebox(screen, x, y, w, h, message):
    pygame.font.init()
    
    myfont = pygame.font.SysFont('Lucida Console', 18) 
    lpb = 56
    boxes = text_lines(lpb, message)
    message = boxes[0]
    message += " "
    rx, ry, rw, rh = rect = (x - 10, y - 10, w + 20, h + 20)
    screen.fill((0, 0, 0), (rx + 32, ry + 32, rw - 64, rh - 64))
    for n in range(int(rect[2]/32)):
        rex = (n * 32) + x
        screen.blit(world.image_db["dbt"], (rex, rect[1]))
        screen.blit(world.image_db["dbb"], (rex, rect[1] + rect[3] - 32))
    
    for n in range(int(rect[3]/32)):
        rey = (n * 32) + y
        screen.blit(world.image_db["dbl"], (rect[0], rey))
        screen.blit(world.image_db["dbr"], (rect[0] + rect[2] - 32, rey))
    screen.blit(world.image_db["dbtl"], (rect[0], rect[1]))
    screen.blit(world.image_db["dbtr"], (rect[0] + rect[2] - 32, rect[1]))
    screen.blit(world.image_db["dbbl"], (rect[0], rect[1] + rect[3] - 32))
    screen.blit(world.image_db["dbbr"], (rect[0] + rect[2] - 32, rect[1] + rect[3] - 32))
    letter_width = 20
    lpl = int(w/letter_width * 2)
    lines = text_lines(lpl, message)
    cury = y
    for l in lines:
        textsurface = myfont.render(l, False, (255, 255, 255))
        screen.blit(textsurface, (x, cury))
        cury += 25
        
