import pygame
from itertools import combinations
import particles as part
from random import randint
from sprites import Sprite
import gamemap
import world
import creatures
import dungeongen

pygame.mixer.init()
coindrop = pygame.mixer.Sound("coin-drop-4.wav")
keypickup = pygame.mixer.Sound("key_pickup.wav")
playerhurt = pygame.mixer.Sound("player-hurt.wav")
borghurt = pygame.mixer.Sound("borg-hurt.wav")
dooropen = pygame.mixer.Sound("door-open.wav")
dooropen.set_volume(0.3)
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
        num = m[ty][tx]
        if (num, s.kind) in tilecol:
            f = tilecol_db[(num, s.kind)]
            f(s, m)
    if collision:
        s.x = s.last_x
        s.y = s.last_y
        return
    

def attempt_move(s, m, ts):
    attempt_v_move2(s, s.vx, 0, m, ts)
    attempt_v_move2(s, 0, s.vy, m, ts)

def tick_null(p, m, ts, sprites):
  pass

def tick_blood(p, m, ts, sprites):
    pass

def tick_blood(p, m, ts, sprites):
    pass    

def tick_drop(coin, m, ts, sprites):
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
    
def make_item(x, y, image_name, kind, tick=tick_null):
    item = Sprite(x, y, kind, simple_img=world.image_db[image_name])
    item.target = None
    item.vy = randint(-3, 3)
    item.vx = randint(-3, 3)
    item.tick = tick
    item.alive = True
    return item

def keep_separated(s1, s2, sprites):
    s1.x = s1.last_x
    s1.y = s1.last_y
    s2.x = s2.last_x
    s2.y = s2.last_y    
    
def puke_hit(s1,s2, ss):
    blood = make_blood_splatter(s1.x + 15, s1.y + 25)
    s1.hitpoints -= 3
    s2.alive = False
    part.crazy_splatter(s2.x,s2.y,(180,0,0),randint(20,100))
    playerhurt.play()
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

            if randint(1,5) < 5:
                coin = make_item(s1.x+50, s1.y+32, "coin", "coin", tick_drop)
                coin.tick = creatures.tick_item
                ss.append(coin)
            if randint(1,4) == 2:
                fang = make_item(s1.x+50, s1.y+32, "borgalon_fang", "borg_fang", tick_drop)
                fang.tick = creatures.tick_item
                ss.append(fang)                
        borghurt.play()
        part.crazy_splatter(s2.x,s2.y,(0,125,0),randint(20,100))

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
    keypickup.play()
    sprites.remove(s2)
    
def get_item(s1, s2, sprites):
    s1.inventory.append(s2)
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

def climb_ladder(p1, p2, sprites):
    world.cur_world = "main"
    p1.x = p2.topx
    p1.y = p2.topy
    
def gointrap(s, m):
    dooropen.play()
    nm, cs, shield = dungeongen.trap_door_room(s)
    cs.insert(0, s)
    s.x = 40*32
    s.y = 40*32
    world.worlds["fwfwe"] = nm, cs
    world.cur_world = "fwfwe"
    print("Hey")
    return shield
    
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
        elif s2.item and s1.kind == "player" and hb1.colliderect(hb2):
            s1.inventory.append(s2)
            sprites.remove(s2)
            
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
                ("player", "borg_fang"): get_item,
                ("gloub", "puke"): wildbounce,
                ("gloub", "bloodyloodies"): wildbounce,
                ("player", "gloub"): beglobbed,
                ("player", "skreet"): beglobbed,
                ("shield", "borgalon"): deflect,
                ("skreet", "puke"): puke_borg_hit,
                ("skreet", "bloodyloodies"): puke_borg_hit,
                ("player", "wall"): keep_separated,
                ("player", "key"): get_key,
                ("player", "coin"): get_coin,
                ("player", "key"): get_key,
                ("player", "ladder"): climb_ladder}
                
tilecol_db = {(11, "player"): gointrap}
