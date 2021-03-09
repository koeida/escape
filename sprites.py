import pygame
import display
import world

def null_tick(p, m, ts, sprites):
    pass

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
        self.tick = null_tick
        self.alive = True
        self.hitpoints = 5
        self.hitbox = self.get_rect()
        self.hitbox.x = 0
        self.hitbox.y = 0
        self.deflected_timer = 0
        self.inventory = []
        self.original_img = simple_img
        self.angle = None
        self.conversation = None
        self.can_act = True
        
    def set_can_act(self):
        self.can_act = True
        
    def get_rect(self):
        if self.simple_img != None:
            return self.simple_img.get_rect()
        else:
            aname, width, height, aframes, adelay = self.animations[self.current_animation][self.facing]
            img = world.image_db[aname]
            ts = world.load_tileset(img, width, height)
            result = pygame.Rect(self.x, self.y, width, height)
            return result 
    def get_img(self):
        if self.simple_img != None:
            return self.simple_img
        else:
            aname, width, height, aframes, adelay = self.animations[self.current_animation][self.facing]
            img = world.image_db[aname]
            return img 