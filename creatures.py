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
    
    new_x = s.x + s.vx
    new_y = s.y + s.vy
    
    sw = s.get_rect().width
    sh = s.get_rect().height
    
    xtl, ytl = get_map_coords(new_x, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    xtr, ytr = get_map_coords(new_x + sw, new_y, world.TILE_WIDTH, world.TILE_HEIGHT)
    xbl, ybl = get_map_coords(new_x, new_y + sh, world.TILE_WIDTH, world.TILE_HEIGHT)
    xbr, ybr = get_map_coords(new_x + sw, new_y + sh, world.TILE_WIDTH, world.TILE_HEIGHT)
    if not (walkable(xtl, xtl, m, ts) and walkable(xbl, ybl, m, ts) and walkable(xtr, ytr, m, ts) and walkable(xbr, ybr, m, ts)):
        dummy_sprite = Sprite(0,0,"wall", None)
        cfunc = collisions.collision_db[(s.kind, "wall")]
        cfunc(s,dummy_sprite)
    else:
        s.x = new_x
        s.y = new_y

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
