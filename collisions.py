import pygame
from itertools import combinations
import particles as part
from random import randint
from sprites import Sprite
import gamemap
import world

pygame.mixer.init()
coindrop = pygame.mixer.Sound("coin-drop-4.wav")
keypickup = pygame.mixer.Sound("key_pickup.wav")
playerhurt = pygame.mixer.Sound("player-hurt.wav")
borghurt = pygame.mixer.Sound("borg-hurt.wav")
keypickup.set_volume(0.25)
playerhurt.set_volume(0.25)
        
def attempt_v_move2(s, vx, vy,  m, ts):
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
        if not gamemap.walkable(tx, ty, m, ts):
            collision = True  

    if collision:
        s.x = s.last_x
        s.y = s.last_y
        return
    

def attempt_move(s, m, ts):
    attempt_v_move2(s, s.vx, 0, m, ts)
    attempt_v_move2(s, 0, s.vy, m, ts)

def tick_blood(p, m, ts, sprites):
    pass    

def tick_coin(coin, m, ts, sprites):
    attempt_move(coin, m, ts)
    coin.vx = pull(coin.vx, 0.1)
    coin.vy = pull(coin.vy, 0.1)
    
def pull(x, amt):
    if x > 0:
        x = x-amt
        if x < 0:
            x = 0
    elif x < 0:
        x = x+amt
    else:
        x = 0
    return x
    

def make_blood_splatter(x, y):
    blood = Sprite(x, y, "BLOOD", simple_img=world.image_db["BLOOD"])
    blood.target = None
    blood.vy = 0
    blood.vx = 0
    blood.tick = tick_blood
    blood.alive = True
    return blood    
    
def make_coin(x, y):
    coin = Sprite(x, y, "coin", simple_img=world.image_db["coin"])
    coin.target = None
    coin.vy = randint(-3, 3)
    coin.vx = randint(-3, 3)
    coin.tick = tick_coin
    coin.alive = True
    return coin

def keep_separated(s1, s2, sprites):
    s1.x = s1.last_x
    s1.y = s1.last_y
    s2.x = s2.last_x
    s2.y = s2.last_y    
    
def puke_hit(s1,s2, ss):
    blood = make_blood_splatter(s1.x + 15, s1.y + 25)
    s1.hitpoints -= 1
    s2.alive = False
    part.crazy_splatter(s2.x,s2.y,(180,0,0),randint(20,100))
    playerhurt.play()
    ss.insert(0, blood)

def puke_borg_hit(s1,s2, ss):
    if s2.deflected_timer != 0:
        s2.alive = False
        s1.alive = False
        coin = make_coin(s1.x+50, s1.y+32)
        borghurt.play()
        ss.append(coin)
        part.crazy_splatter(s2.x,s2.y,(0,125,0),randint(20,100))

    
def deflect(s1, s2, sprites):
    if s2.deflected_timer == 0:
        s2.x = s2.last_x
        s2.y = s2.last_y    
        s2.vy *= -1.25
        s2.vx *= -1.25
        s2.deflected_timer = 20

def get_key(s1, s2, sprites):
    s1.inventory.append(s2)
    keypickup.play()
    sprites.remove(s2)
        
def get_coin(s1, s2, sprites):
    s1.money += 1
    coindrop.play()
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
                ("shield", "puke"): deflect,
                ("shield", "borgalon"): deflect,
                ("player", "wall"): keep_separated,
                ("player", "key"): get_key,
                ("player", "coin"): get_coin}
             