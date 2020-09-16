from gamemap import get_map_coords, onscreen, walkable
import world
import display
import pygame
from tools import distance
from random import randint, uniform

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
    def get_rect(self):
        if self.simple_img != None:
            return self.simple_img.get_rect()
        else:
            aname, width, height, aframes, adelay = self.animations[self.current_animation][self.facing]
            img = world.image_db[aname]
            ts = display.load_tileset(img, width, height)
            result = pygame.Rect(self.x, self.y, width, height)
            return result 
            
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
from tools import distance  

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
            
def generic_tick(p, m, ts, sprites):
    attempt_walk(p,m,ts)
    
def tick_puke(p, m, ts, sprites):
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
        if borgalon.target.y > borgalon.y+200:
            borgalon.vy = 1
            #borgalon.facing ="down"
        if borgalon.target.y < borgalon.y+200:
            borgalon.vy = -1
            #borgalon.facing ="up"
        attempt_walk(borgalon, m, ts)
        
        if borgalon.x == borgalon.target.x and borgalon.y+200 == borgalon.target.y:
            borgalon.mode = "attack"
            borgalon.vx = 0
            borgalon.vy = 0
        
    if borgalon.mode == "attack":
        if randint(1,5) == 1:
            puke_anim = { "walking": {"down": ("puke", 20, 20, [0, 1], 3)}}
            puke = Sprite(borgalon.x, borgalon.y, "puke", puke_anim)
            puke.target = borgalon.target
            puke.vy = 3
            puke.vx = uniform(-3, 3)
            puke.lifespan = randint(50,250)
            puke.tick = tick_puke
            sprites.append(puke)
        #borgalon.facing = "down"
    #if distance(borgalon,borgalon.target) < 300:
    #    borgalon.targeszt = borgalon.target.y - 100
        
    
        
            

def attempt_walk(s, m, ts):
    s.last_x = s.x
    s.last_y = s.y
    
    new_x = s.x + s.vx
    new_y = s.y + s.vy
    
    sw = s.get_rect().width
    sh = s.get_rect().height
    
    xtl, ytl = get_map_coords(new_x, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    xtr, ytr = get_map_coords(new_x + sw, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    xbl, ybl = get_map_coords(new_x, new_y + sh, world.TILE_WIDTH, world.TILE_HEIGHT)
    xbr, ybr = get_map_coords(new_x + sw, new_y + sh, world.TILE_WIDTH, world.TILE_HEIGHT)
    if (walkable(xtl, xtl, m, ts) and walkable(xbl, ybl, m, ts) and 
        walkable(xtr, ytr, m, ts) and walkable(xbr, ybr, m, ts)):
        s.x = new_x
        s.y = new_y
    
