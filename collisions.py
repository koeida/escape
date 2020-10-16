import pygame
from itertools import combinations
import particles as part
from random import randint

def keep_separated(s1, s2):
    s1.x = s1.last_x
    s1.y = s1.last_y
    s2.x = s2.last_x
    s2.y = s2.last_y    
    
def puke_hit(s1,s2):
    s1.hitpoints -= 1
    s2.alive = False
    part.crazy_splatter(s2.x,s2.y,(111,127,0),randint(20,100))
    
def deflect(s1, s2):
    if s2.deflected_timer == 0:
        s2.x = s2.last_x
        s2.y = s2.last_y    
        s2.vy *= -1.25
        s2.vx *= -1.25
    
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

def check_collisions(sprites):
    scombs = combinations(sprites, 2)
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
            if overlap != None:
                collision_db[cpair](s1, s2)
        else:
            if cpair in collision_db and hb1.colliderect(hb2):
                collision_db[cpair](s1, s2)
        
collision_db = {("player", "monk"): keep_separated,
                ("player", "puke"): puke_hit,
                ("shield", "puke"): deflect,
                ("shield", "borgalon"): deflect,
                ("player", "wall"): keep_separated}
