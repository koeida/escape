from gamemap import get_map_coords, onscreen, walkable
import world
import display
import pygame

from tools import distance,get_coords, clamp, filter_dict
from random import randint, uniform,choice

import collisions
from sprites import Sprite
           
def switch_anim(s, anim_name):
    if s.current_animation == anim_name:
        return
    if s.current_animation in ["walking", "standing"]:
        s.next_anim = None
        s.current_frame = 0
        s.cur_anim_timer = 0
        s.current_animation = anim_name
    else:
        s.next_anim = anim_name

def tick_anim(s):
    if s.anim_timer == None:
        return
    s.cur_anim_timer += 1
    if s.cur_anim_timer > s.anim_timer:
        current_anim = s.animations[s.current_animation][s.facing]
        s.cur_anim_timer = 0
        s.current_frame = s.current_frame + 1 if s.current_frame < len(current_anim[3]) - 1 else 0
        if s.current_frame == 0 and s.next_anim != None:
            s.current_animation = s.next_anim
            s.next_anim = None
            
def randomspawn(s, m, spawnpoints=[]):
    if spawnpoints == []:
        spawnpoints = get_coords(m, filter_dict(lambda x: x.floor_tile, world.TILES.data))
    bad = True
    while(bad):
        spawn_x, spawn_y = choice(spawnpoints)
        gts = filter_dict(lambda x: x.floor_tile, world.TILES.data)
        try:
            if m[spawn_y][spawn_x + 1] in gts and m[spawn_y+1][spawn_x + 1] in gts and m[spawn_y + 1][spawn_x] in gts:
                bad = False
        except:
            bad = True

        s.x = spawn_x * 32
        s.y = spawn_y * 32
    

def portal_tick(p, m, ts, sprites):
        p.angle += 5
        
def generic_tick(p, m, ts, sprites):
    attempt_walk(p,m,ts)
    
def tick_puke(p, m, ts, sprites):
    hx = p.target.x + 31
    hy = p.target.y + 43 
    
    if hx > p.x:
        p.vx += 0.1
    if hx < p.x:
        p.vx -= 0.1
    if hy > p.y:
        p.vy += 0.1
        #p.facing ="down"
    if hy < p.y:
        p.vy -=0.1
        #p.facing ="up"
    max_vel = 2
    min_vel = -2    
    if p.deflected_timer > 0 or p.is_wild == True:
        p.deflected_timer -= 1
        max_vel = 5
        min_vel = -5

    p.vy = clamp(p.vy, min_vel, max_vel)
    p.vx = clamp(p.vx, min_vel, max_vel)
    attempt_walk(p,m,ts)
    p.lifespan -= 1

    if p.lifespan < 0:
        p.alive = False
            
def tick_player(p, m, ts, sprites):
    attempt_walk(p, m, ts)
    


def tick_borgalon(borgalon, m, ts, sprites):
    if borgalon.mode == "chase":
        if borgalon.target.x > borgalon.x:
            borgalon.vx = 1
            borgalon.facing ="right"
        if borgalon.target.x < borgalon.x:
            borgalon.vx = -1
            borgalon.facing ="left"
        if borgalon.target.y > borgalon.y:
            borgalon.vy = 1
            #borgalon.facing ="down"
        if borgalon.target.y < borgalon.y:
            borgalon.vy = -1
            #borgalon.facing ="up"
        attempt_walk(borgalon, m, ts)
        
        if distance(borgalon,borgalon.target) <= 200:
            borgalon.mode = "attack"
            borgalon.vx = 0
            borgalon.vy = 0
        if distance(borgalon,borgalon.target) >= 1000:
            borgalon.mode = "cheel"
            
    if borgalon.mode == "cheel":
        if distance(borgalon,borgalon.target) <=500:
            borgalon.mode = "chase"
            
    if borgalon.mode == "attack":
        if randint(1,10) == 1:
            puke_anim = { "walking": {"down": ("puke", 20, 20, [0, 1], 3)}}
            puke = Sprite(borgalon.x, borgalon.y, "puke", puke_anim)
            puke.target = borgalon.target
            puke.vy = uniform(-2,4)
            puke.vx = uniform(-5, 5)
            puke.lifespan = randint(50,250)
            puke.tick = tick_puke
            puke.is_wild = False
            sprites.append(puke)
        if distance(borgalon,borgalon.target) >=500:
            borgalon.mode = "chase"
        #borgalon.facing = "down"
    #if distance(borgalon,borgalon.target) < 300:
    #    borgalon.targeszt = borgalon.target.y - 100
def tick_vlation(vlation, m, ts, sprites):
    if vlation.mode == "chase":
        if vlation.target.x > vlation.x:
            vlation.vx = 2
            vlation.facing ="right"
        if vlation.target.x < vlation.x:
            vlation.vx = -2
            vlation.facing ="left"
        if vlation.target.y > vlation.y:
            vlation.vy = 2
            #vlation.facing ="down"
        if vlation.target.y < vlation.y:
            vlation.vy = -2
            #vlation.facing ="up"
        attempt_walk(vlation, m, ts)
        
        if distance(vlation,vlation.target) <= 200:
            vlation.mode = "attack"
            vlation.vx = 0
            vlation.vy = 0
        if distance(vlation,vlation.target) >= 1000:
            vlation.mode = "cheel"
            
    if vlation.mode == "cheel":
        if distance(vlation,vlation.target) <=500:
            vlation.mode = "chase"
            
            
    if vlation.mode == "attack":
        if randint(1,5) == 1:
            loogie_anim = { "walking": {"down": ("bloodyloodies", 20, 20, [0, 1], 3)}}
            bloodyloodie = Sprite(vlation.x, vlation.y, "bloodyloodies", loogie_anim)
            bloodyloodie.target = vlation.target
            bloodyloodie.vy = 3
            bloodyloodie.vx = uniform(-3, 3)
            bloodyloodie.lifespan = randint(50,250)
            bloodyloodie.tick = tick_puke
            bloodyloodie.is_wild = False
            sprites.append(bloodyloodie)
        if distance(vlation,vlation.target) >=500:
            vlation.mode = "chase"  
            
def tick_skreet(skreet, m, ts, sprites):
    if skreet.mode == "chase":
        if skreet.target.x > skreet.x:
            skreet.vx = 2
            skreet.facing ="right"
        if skreet.target.x < skreet.x:
            skreet.vx = -2
            skreet.facing ="left"
        if skreet.target.y > skreet.y:
            skreet.vy = 2
            #skreet.facing ="down"
        if skreet.target.y < skreet.y:
            skreet.vy = -2
            #skreet.facing ="up"
        attempt_walk(skreet, m, ts)
        
        if distance(skreet,skreet.target) <= 200:
            skreet.mode = "attack"
            skreet.vx = 0
            skreet.vy = 0
        if distance(skreet,skreet.target) >= 1000:
            skreet.mode = "cheel"
            
            
    if skreet.mode =="attack":
        skreet.target.sanity-=0.01
        skreettung = Sprite(skreet.x, skreet.y, "skreettung",simple_img=world.image_db["skreettung"])
        #sprites.append(skreettung)
    
    
        tox = skreet.target.x
        toy = skreet.target.y
        if distance(skreet,skreet.target) >=500:
            
            skreet.mode = "chase"  
        if skreet.target.x > skreet.x:
            skreet.target.x -= 1
            skreet.target.facing ="left"
        if skreet.target.x < skreet.x:
            skreet.target.x += 1
            skreet.target.facing ="right"
        if skreet.target.y > skreet.y:
            skreet.target.y -= 1
            #skreet.facing ="down"
        if skreet.target.y < skreet.y:
            skreet.target.y += 1
        if not is_valid_spot(skreet.target, m, ts):
            skreet.target.x = tox
            skreet.target.y = toy
            
    if skreet.mode == "cheel":
        if distance(skreet,skreet.target) <=500:
            skreet.mode = "chase"
            
            
        if distance(skreet,skreet.target) >=200:
            skreet.mode = "chase"  
            


def tick_gloub(gloub, m, ts, sprites):
    if gloub.mode == "chase":
        if gloub.target.x > gloub.x:
            gloub.vx = 0.3
            gloub.facing ="right"
        if gloub.target.x < gloub.x:
            gloub.vx = -0.3
            gloub.facing ="left"
        if gloub.target.y > gloub.y:
            gloub.vy = 0.3
            gloub.facing ="down"
        if gloub.target.y < gloub.y:
            gloub.vy = -0.3
            gloub.facing ="up"
        attempt_walk(gloub, m, ts)
        
       
        if distance(gloub,gloub.target) >= 1000:
            gloub.mode = "cheel"
            
    if gloub.mode == "cheel":
        if distance(gloub,gloub.target) <=500:
            gloub.mode = "chase"            

def is_valid_spot(s, m, ts):

    hx = s.x + s.hitbox.x 
    hy = s.y + s.hitbox.y

    left = int(hx / world.TILE_WIDTH)
    right = int((hx + s.hitbox.width) / world.TILE_WIDTH)
    top = int(hy / world.TILE_WIDTH )
    bottom = int((hy + s.hitbox.height) / world.TILE_WIDTH )
    coords = [(left, top), (left, bottom), (right, top), (right, bottom)]

    collision = False
    for tx, ty in coords:
        if not walkable(tx, ty, m, ts):
            collision = True
    return not collision
        
def attempt_v_move(s, vx, vy,  m, ts):
    s.last_x = s.x
    s.last_y = s.y

    s.x += vx
    s.y += vy

    hx = s.x + s.hitbox.x 
    hy = s.y + s.hitbox.y

    left = int(hx / world.TILE_WIDTH)
    right = int((hx + s.hitbox.width) / world.TILE_WIDTH)
    top = int(hy / world.TILE_WIDTH )
    bottom = int((hy + s.hitbox.height) / world.TILE_WIDTH )
    coords = [(left, top), (left, bottom), (right, top), (right, bottom)]

    collision = False
    for tx, ty in coords:
        if not walkable(tx, ty, m, ts):
            collision = True  

    if collision:
        s.x = s.last_x
        s.y = s.last_y
        return
    

def attempt_walk(s, m, ts):
    attempt_v_move(s, s.vx, 0, m, ts)
    attempt_v_move(s, 0, s.vy, m, ts)
    

def make_shield():
    #swidth = player.get_rect().width + 100 #35
    #smiddle = int(swidth / 2)
    #shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    
    #shield = creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 
    #border_surf = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    #pygame.draw.rect(border_surf, (255,0,0), (0,0,32,32), 1)
    pass

def tick_shield():
    #shield.x = player.x - 65
    #shield.y = player.y - 65
    #player_sx, player_sy = #display.calc_screen_coords(coords, camrect)
    #shield.simple_img = display.render_shield(0, 0, mouse_x, mouse_y, swidth)
    pass
