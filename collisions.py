import pygame
from itertools import combinations
import particles as part
from random import randint
from sprites import Sprite
import world


def tick_blood(p, m, ts, sprites):
    pass

def make_blood_splatter(x, y):
    blood_anim = { "walking": {"down": ("BLOOD", 32, 32, [0], 3)}}
    blood = Sprite(x, y, "BLOOD", simple_img=world.image_db["BLOOD"])
    blood.target = None
    blood.vy = 0
    blood.vx = 0
    blood.tick = tick_blood
    blood.alive = True
    return blood

def keep_separated(s1, s2, sprites):
    s1.x = s1.last_x
    s1.y = s1.last_y
    s2.x = s2.last_x
    s2.y = s2.last_y    
    
def puke_hit(s1,s2, ss):
    blood = make_blood_splatter(s1.x + 15, s1.y + 25)
    s1.hitpoints -= 1
    s2.alive = False
    part.crazy_splatter(s2.x,s2.y,(140,0,0),randint(20,100))
    ss.insert(0, blood)
    
def wildbounce(s1,s2,sprites):
    if s2.is_wild == False:
        s2.x = s2.last_x
        s2.y = s2.last_y   
        s2.vy *= randint(-20,20)
        s2.vx *= randint(-20,20)
        s2.is_wild = True
        s1.hitpoints -= 1
        
    
def beglobbed(s1,s2,sprites):
    s1.hitpoints-=1
    

def puke_borg_hit(s1,s2, ss):
    if s2.deflected_timer != 0:
        s2.alive = False
        s1.hitpoints -= 1
        if s1.hitpoints == 0:
            s1.alive = False
        part.crazy_splatter(s2.x,s2.y,(127,127,0),randint(20,100))



def deflect(s1, s2, sprites):
    s2.x = s2.last_x
    s2.y = s2.last_y    
    s2.vy *= -20
    s2.vx *= -20
    s2.deflected_timer = 100
    if s1.width > 0:
        s1.width -=1
        if s1.width < 0:
            s1.width =0
    

def get_key(s1, s2, sprites):
    s1.inventory.append(s2)
    sprites.remove(s2)

    
def shrinkyrect(r, percent):
    shrunkwidth = (r.width/100) * percent
    shrunkheight = (r.width/100) * percent
    widthmod = shrunkwidth/2
    heightmod = shrunkheight/2 
    newx = r.x +  widthmod
    newwidth = r.width - widthmod
    newy = r.y +  heightmod
    newheight = r.height - heightmod
    return pygame.Rect(newx, newy, newwidth, newheight)

def check_collisions(nearby, sprites):
    scombs = combinations(nearby, 2)
    for s1, s2 in scombs:
        cpair = (s1.kind, s2.kind)

        # adjust hitbox x and y 
        hb1 = pygame.Rect(s1.x + s1.hitbox.x, s1.y + s1.hitbox.y, s1.hitbox.width, s1.hitbox.height)
        hb2 = pygame.Rect(s2.x + s2.hitbox.x, s2.y + s2.hitbox.y, s2.hitbox.width, s2.hitbox.height)
        if s1.kind == "shield":
            #hb1.x += 25
            #hb1.y += 20
            offset = hb2[0] - hb1[0], hb2[1] - hb1[1]
            shield_mask = pygame.mask.from_surface(s1.simple_img)
            s2mask = pygame.mask.from_surface(s2.get_img())
            overlap = shield_mask.overlap(s2mask, offset)
            if cpair in collision_db and overlap != None:
                collision_db[cpair](s1, s2, sprites)
        else:
            if cpair in collision_db and hb1.colliderect(hb2):
                collision_db[cpair](s1, s2, sprites)
        
collision_db = {("player", "monk"): keep_separated,
                ("player", "puke"): puke_hit,
                ("borgalon", "puke"): puke_borg_hit,
                ("player", "bloodyloodies"): puke_hit,
                ("vlation", "bloodyloodies"): puke_borg_hit,
                ("vlation", "puke"): puke_borg_hit,
                ("borgalon", "bloodyloodies"): puke_borg_hit,
                ("shield", "bloodyloodies"): deflect,
                ("shield", "puke"): deflect,
                ("gloub", "puke"): wildbounce,
                ("gloub", "bloodyloodies"): wildbounce,
                ("player", "gloub"): beglobbed,
                ("player", "skreet"): beglobbed,
                ("shield", "borgalon"): deflect,
                ("skreet", "puke"): puke_borg_hit,
                ("skreet", "bloodyloodies"): puke_borg_hit,
                ("player", "wall"): keep_separated,
                ("player", "key"): get_key}
