from gamemap import get_map_coords, onscreen, walkable
import world
import display
import pygame

from tools import distance,get_coords, clamp
from random import randint, uniform,choice

import collisions

class Animation: 
    def __init__(self, name, anim_db):
        self.name = name
        self.anim_db = anim_db

class Sprite:
    def __init__(self, x, y, kind, animations=None, current_animation="walking", simple_img=None):
        self.x = x
        self.y = y
        self.kind = kind
        self.animations = animations
        self.current_animation = current_animation
        self.current_frame = 0
        self.cur_anim_timer = 0
        self.facing = "down"
        self.anim_timer = None if animations == None else animations[current_animation][self.facing][4]
        self.last_x = self.x
        self.last_y = self.y
        self.vx = 0
        self.vy = 0
        self.simple_img = simple_img
        self.next_anim = None
        self.tick = generic_tick
        self.alive = True
        self.hitpoints = 100
        self.hitbox = self.get_rect()
        self.hitbox.x = 0
        self.hitbox.y = 0
        self.deflected_timer = 0

    def get_rect(self):
        if self.simple_img != None:
            return self.simple_img.get_rect()
        else:
            aname, width, height, aframes, adelay = self.animations[self.current_animation][self.facing]
            img = world.image_db[aname]
            ts = display.load_tileset(img, width, height)
            result = pygame.Rect(self.x, self.y, width, height)
            return result 
    def get_img(self):
        if self.simple_img != None:
            return self.simple_img
        else:
            aname, width, height, aframes, adelay = self.animations[self.current_animation][self.facing]
            img = world.image_db[aname]
            return img 

            
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
            
def randomspawn(s, m):
    spawnpoints = get_coords(m,0)
    spawn_x, spawn_y = choice(spawnpoints)
    s.x = spawn_x * 32
    s.y = spawn_y * 32
    
            
def generic_tick(p, m, ts, sprites):
    attempt_walk(p,m,ts)
    
def tick_puke(p, m, ts, sprites):
    if p.deflected_timer > 0:
        p.deflected_timer -= 1
    else:
        if p.target.x > p.x:
            p.vx += 0.1
        if p.target.x < p.x:
            p.vx -= 0.1
        if p.target.y > p.y:
            p.vy += 0.1
            #p.facing ="down"
        if p.target.y < p.y:
            p.vy -=0.1
            #p.facing ="up"
        max_vel = 4
        min_vel = -4
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
            puke.vy = 3
            puke.vx = uniform(-5, 5)
            puke.lifespan = randint(50,250)
            puke.tick = tick_puke
            sprites.append(puke)
        if distance(borgalon,borgalon.target) >=500:
            borgalon.mode = "chase"
        #borgalon.facing = "down"
    #if distance(borgalon,borgalon.target) < 300:
    #    borgalon.targeszt = borgalon.target.y - 100
        
    
        
            

def attempt_walk(s, m, ts):
    s.last_x = s.x
    s.last_y = s.y

    s.x += s.vx
    s.y += s.vy

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
