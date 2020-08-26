from gamemap import get_map_coords, onscreen, walkable
import world
import display
import pygame

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
        self.anim_timer = None if animations == None else animations[current_animation][4]
        self.last_x = self.x
        self.last_y = self.y
        self.vx = 0
        self.vy = 0
        self.simple_img = simple_img
    def get_rect(self):
        if self.simple_img != None:
            return self.simple_img.get_rect()
        else:
            aname, width, height, aframes, adelay = self.animations[self.current_animation]
            img = world.image_db[aname]
            ts = display.load_tileset(img, width, height)
            result = pygame.Rect(self.x, self.y, width, height)
            return result 
            

def tick_anim(s):
    if s.anim_timer == None:
        return
    s.cur_anim_timer += 1
    if s.cur_anim_timer > s.anim_timer:
        s.cur_anim_timer = 0
        s.current_frame = s.current_frame + 1 if s.current_frame < len(s.animations[s.current_animation][3]) - 1 else 0

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
    
