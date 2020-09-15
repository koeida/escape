from gamemap import get_map_coords, onscreen, walkable
import world
import display
import pygame
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
        self.hitbox = self.get_rect()
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
            print("ow: (%d, %d)" % (tx, ty)) 
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
