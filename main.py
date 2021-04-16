from gamemap import gen_test_map
from input import get_input
from random import randint, uniform, choice
from tools import get_coords, distance, filter_dict, first
import collisions
import creatures
import display
import math
import pygame
import pygame.gfxdraw
import timers
import traceback
import world
import dungeongen
import particles as part
from pygame.locals import *

pygame.mixer.init()
dooropen = pygame.mixer.Sound("door-open.wav")
dooropen.set_volume(0.3)

import dialobjects

def get_input(player, m, ts, cs):
    keys = pygame.key.get_pressed()
    speed = 4
    dx = 0
    dy = 0
    
    w = keys[pygame.K_w]
    s = keys[pygame.K_s]
    d = keys[pygame.K_d]
    a = keys[pygame.K_a]
    o = keys[pygame.K_o]
    q = keys[pygame.K_q]  
    oldfacing = player.facing
    
    ks = list(filter(lambda i: i.kind == "key", player.inventory))
    
    if keys[pygame.K_t]:
        matched = False
        for y in range(len(m)):
            if matched == True:
                break
            for x in range(len(m[0])):
                if m[y][x] == 16:
                    player.x = x*32
                    player.y = y*32
                    matched = True
                    break
    if w:   
        player.vy = -speed
        player.facing = "up"
    if s:
        player.vy = speed
        player.facing = "down"
    if d:
        player.vx = speed
        player.facing = "right"
    if a:
        player.vx = -speed
        player.facing = "left"

    if o and ks != []:
        x = int((player.x + 32) / 32)
        y = int((player.y + 32)/ 32)
        adjacenttiles = ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y - 1, x - 1), (y + 1, x - 1), (y - 1, x + 1))
        doors = list(filter(lambda t: m[t[0]][t[1]] == 12, adjacenttiles))
        if doors != []:
            dy, dx = doors[0]
            m[dy][dx] = 13
            ks[0].hitpoints -= 1
            dooropen.play()
            if ks[0].hitpoints == 0:
                player.inventory.remove(ks[0])
    if q and player.can_act:
        player.can_act = False
        timers.add_timer(0.1, lambda: player.set_can_act())
        for c in cs:
            if distance(player, c) < 50 and c.conversation != None:
                world.mode = "dialogue"
                world.dialogue_message = ""
                world.diakey = c.conversation
                world.partner = c
                player.sanity +=2
            elif distance(player, c) < 50 and c.kind == "chest":
                cs.remove(c)

        r = player.get_rect()
        y = int((player.y + r.height/2)/32)
        x = int((player.x + r.width/2)/32)
        if m[y][x] == 20:
            m[y][x] = 11  
    if not s and not w:
        player.vy = 0
    if not a and not d:
        player.vx = 0    
    
    if player.vx == 0 and player.vy == 0:
        creatures.switch_anim(player,"standing")
    else:
        creatures.switch_anim(player,"walking")

    if player.facing != oldfacing:
        player.current_frame = 0

def tortoise_spawn(z, sprites):
    for t in range(5):
        room = choice(z.rooms)
        turtle = creatures.Sprite(randint(room.x + 4, room.x + room.w - 5)*32, randint(room.y + 4, room.y + room.h - 5)*32, "tortoise", simple_img=world.image_db["tortoise2"])
        turtle.item = True
        turtle.tick = creatures.tick_item
        sprites.append(turtle)
        
def gen_test_map():
    game_map = [[0 for x in range(100)] for y in range(100)]
    for x in range(1000):
        game_map[randint(0,99)][randint(0,99)] = randint(0,7)
    
    for x in range(100):
        game_map[0][x] = 16 * 6 + 2
        game_map[len(game_map[0]) - 1][x] = 16 * 6 + 2
    
    
    for y in range(100):
        game_map[y][0] = 16 * 6 + 2
        game_map[y][len(game_map) - 1] = 16 * 6 + 2
        
    
    return game_map
def dialogue_mode():
    # if there is no current dialogue message, grab it from the dialogue database with diakey
    cur_dialogue = dialobjects.conversation[world.diakey][world.diaindex]
    # if the type of cur_dialogue is a message
    if type(cur_dialogue) == dialobjects.C_Text:
        if world.dialogue_message == "":
            world.dialogue_message = cur_dialogue.message
    if type(cur_dialogue) == dialobjects.C_Switch:
        world.partner.conversation = cur_dialogue.new_conv
        world.mode = "game"
        world.diakey = ""
        world.diaindex = 0
        world.dialogue_message = ""
        world.choice = ""
    if type(cur_dialogue) == dialobjects.C_Give:
        world.diaindex += 1
        # world.mode = "game"
        # world.diakey = c.target
        # world.diaindex = 0
        # world.dialogue_message = ""
        # world.choice = ""
    # if the type is a switch, then change the current conversation partner's conv to the switch
    # if the type is a give, then return to game mode for now
    if type(cur_dialogue) == dialobjects.C_Global:
        world.globs[cur_dialogue.key] = cur_dialogue.value
        world.diaindex += 1
        world.dialogue_message = ""
        world.choice = ""
        print(world.globs["tortoise_spawn"])
    for event in pygame.event.get():
        if world.choice != "":
            if event.type == pygame.KEYDOWN:
                for c in cur_dialogue.choices:
                    if event.key == c.key:
                        world.diakey = c.target
                        world.diaindex = 0
                        world.dialogue_message = ""
                        world.choice = ""# loop over possible valid button presses
                # if they've pressed the button, quit out of dialogue
        else:
            if event.type == pygame.QUIT:
                world.mode = "game"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    world.mode = "game"
                if event.key == pygame.K_q:
                    lpb = 56
                    boxes = display.text_lines(lpb, world.dialogue_message)
                    start = len(boxes[0])
                    if len(boxes) > 1:
                        world.dialogue_message = world.dialogue_message[start:]  
                    else:
                        # if there is a choice associated with this conversation thread
                        if cur_dialogue.choices != None:
                            world.choice = "    ".join(list(map(lambda v:v.text ,cur_dialogue.choices)))
                        elif len(dialobjects.conversation[world.diakey]) > world.diaindex + 1:
                            world.diaindex += 1
                            world.choice = ""
                            world.dialogue_message = ""
                            # reset all those global variables other than diaindex and diakey
                        else:# switch into choice mode(?) and display choices
                            world.mode = "game"
                        
def game_mode(timers, player, game_map, ts, sprites, shield, swidth, running):   
    
    timers.update_timers()
    world.total_ticks += 1
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
      
    get_input(player, game_map, ts, sprites)       
    
    for s in sprites:
        creatures.tick_anim(s)
        if s.kind != "wall":
            if s.tick != None:
                s.tick(s, game_map, ts, sprites)
                #creaures.attempt_walk(s, game_map, ts)
    for p in part.particles:
        part.tick_particle(p)
        if p.lifespan <= 0:
            part.particles.remove(p)
        
    shield.x = player.x - 17
    shield.y = player.y - 10
    
    #player_sx, player_sy = display.calc_screen_coords(coords, camrect)
    shield.simple_img = display.render_shield(mouse_x, mouse_y, swidth, shield)       
    
    
    if player.hitpoints <= 0:
        player.alive = False
        shield.alive = False
    
    nearby_sprites = list(filter(lambda s: distance(s,player) < 250, sprites))
    collisions.check_collisions(nearby_sprites, sprites)

    sprites = list(filter(lambda s: s.alive, sprites))
                    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            part.crazy_splatter(player.x + 50, player.y + 50, (255,0,0))
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
        
    return(sprites, running)
    
def addtorch(m,sprites,anim):
    for y in range(len(m)):
        for x in range(len(m[0])):
            tnum = m[y][x] 
            torches = creatures.Sprite(x*32, y*32, "torches", anim)
            if tnum in (1,5,6,7,8,9,17,18,19,20,21,23,24,27,28):
               if randint(1,10) ==1:
                    sprites.append(torches)
            

def main(screen):   
    global player
    clock = pygame.time.Clock()
    running = True
    key_timer = 0
    
    world.load_assets()

    stacked_dude = display.stack_spritesheets(["BODY_male", "LEGS_robe_skirt"])
    world.image_db["dude"] = stacked_dude
    

    game_map, keys, start, end, zones = dungeongen.make_dungeon(140)
    
    
    tsimg = pygame.image.load("tile sheet.png")
    tsimg.convert()
    ts = world.load_tileset(tsimg, 32, 32)        
    panim = {
             "standing": {"up": ("dude", 64, 64, [0], 5),
                         "left": ("dude", 64, 64, [9], 5),
                         "down": ("dude", 64, 64, [18], 5),
                         "right": ("dude", 64, 64, [29], 5)},
             "walking": {"up": ("dude", 64, 64, range(1,9), 2),
                        "left": ("dude", 64, 64, range(10, 18), 2),
                        "down": ("dude", 64, 64, range(19, 27), 2),
                        "right": ("dude", 64, 64, range(28, 36), 2)}}

    
                        
    banim = { "walking": {"left": ("boganim", 105, 80, [0,1,2], 7),
                          "right": ("boganim", 105, 80, [3,4,5], 7),
                          #"up": ("boganim", 105, 80, [5], 7),
                          "down": ("boganim", 105, 80, [5], 7)
                         }}
                         
    vlanim = { "walking": {"left": ("VLATION", 64, 59, [0,1], 7), 
                          "right": ("VLATION", 64, 59, [0,1], 7),
                          "up": ("VLATION", 64, 59, [0,1], 7),
                          "down": ("VLATION", 64, 59, [0,1], 7)
            }}
            
    glanim = { "walking": {"left": ("Gloub", 61, 45, [0,1,2,3,4,5], 7), 
                          "right": ("Gloub", 61, 45, [0,1,2,3,4,5], 7),
                          "up": ("Gloub", 61, 45, [0,1,2,3,4,5], 7),
                          "down": ("Gloub", 61, 45, [0,1,2,3,4,5], 7)
            }}
            
    skanim = { "walking": {"left": ("Skreets", 73, 91, [0,1,2,3], 5), 
                          "right": ("Skreets", 73, 91, [0,1,2,3], 5),
                          "up":("Skreets", 73, 91, [0,1,2,3], 5),
                          "down": ("Skreets", 73, 91, [0,1,2,3], 5)
            }}
            
    boss1anim = { "walking": {"left": ("boss1", 150, 276, [0,1], 5), 
                          "right": ("boss1", 150, 276, [0,1], 5),
                          "up":("boss1", 150, 276, [0,1], 5),
                          "down": ("boss1", 150, 276, [0,1], 5)
            }}
    
    
    puke_anim = { "walking": {"down": ("puke", 20, 20, [0], 7)}}
    torch_anim = { "walking": {"down": ("torches", 20, 30, [0,1,2,1], 3)}}

    room = dungeongen.shrink_room(choice(start.rooms))
    py = randint(room.y + 1, room.y + room.h - 3)
    px = randint(room.x + 1, room.x + room.w - 3)
    player = creatures.Sprite(px * 32, py * 32, "player", panim)
    player.light = True

    loogie_anim = { "walking": {"down": ("bloodyloodies", 20, 20, [0], 7)}}
    player.tick = creatures.tick_player
    #player.x = 1000
    #player.y = 1000
    player.hitbox = pygame.Rect(24, 43, 18, 18)
    player.hitpoints = 100
    player.sanity=200
    
    
    enemy = creatures.Sprite(600, 600, "monk", panim)
    assert(start.rooms != end.rooms)
    room2 = dungeongen.shrink_room(choice(end.rooms))
    portaly = randint(room2.y + 1, room2.y + room2.h - 2)
    portalx = randint(room2.x + 1, room2.x + room2.w - 2)
    portal = creatures.Sprite(portalx * 32, portaly * 32, "portal", simple_img=world.image_db["portal"])
    portal.tick = creatures.portal_tick
    portal.original_img = portal.simple_img
    portal.angle = 0
    
    
    
    swidth = player.get_rect().width + 35
    smiddle = int(swidth / 2)
    shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    
    shield = creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 

        

    sprites = [player, shield] + keys
    
    sprites.append(portal)
    boss1 = creatures.Sprite(portalx*32,(portaly*32 - 300), "boss1", boss1anim)
    boss1.hitpoints = 50
    boss1.facing = "left"
    boss1.mode = "cheel"
    boss1.target = player
    boss1.tick = None
    sprites.append(boss1)
    
    for x in range(1):
        addtorch(game_map,sprites,torch_anim)
     
    #dungeongen.add_shadow(game_map, sprites)
    
    spawnpoints = get_coords(game_map, filter_dict(lambda x: x.floor_tile, world.TILES.data))
    for x in range(100):
        borgalon = creatures.Sprite(500,500, "borgalon", banim)
        creatures.randomspawn(borgalon,game_map, spawnpoints)
        borgalon.hitpoints = 5
        borgalon.vx = 1
        borgalon.vy = 0
        borgalon.light = True

        borgalon.hitpoints = 5
        borgalon.facing = "left"
        borgalon.mode = "cheel"
        borgalon.target = player
        borgalon.tick = creatures.tick_borgalon
        sprites.append(borgalon)
        
    for x in range(20):
        chests = creatures.Sprite(32,32, "chest", simple_img=world.image_db["chest"])
        creatures.randomspawn(chests,game_map, spawnpoints)
        sprites.insert(0,chests)
    
    room = dungeongen.shrink_room(choice(start.rooms))
    ty = randint(room.y + 1, room.y + room.h - 3)
    tx = randint(room.x + 1, room.x + room.w - 3)
    tortoise_merch = creatures.Sprite(tx*32, ty*32, "tortoise_collector", simple_img=world.image_db["tortoise_collector"])
    tortoise_merch.conversation = "tortoise"
    sprites.append(tortoise_merch)
    
    room = dungeongen.shrink_room(choice(start.rooms))
    ty = randint(room.y + 1, room.y + room.h - 3)
    tx = randint(room.x + 1, room.x + room.w - 3)
    stranger = creatures.Sprite(tx*32, ty*32, "stranger", simple_img=world.image_db["stranger"])
    stranger.conversation = "stranger"
    sprites.append(stranger)
    
    puke = creatures.Sprite(350, 350, "puke", puke_anim)
    
    for x in range(50):
        vlation = creatures.Sprite(500,500, "vlation", vlanim)
        creatures.randomspawn(vlation,game_map, spawnpoints)
        vlation.vx = 1
        vlation.vy = 0
        vlation.hitpoints = 10
        vlation.facing = "left"
        vlation.mode = "cheel"
        vlation.target = player
        vlation.tick = creatures.tick_vlation
        sprites.append(vlation)
    loogies = creatures.Sprite(350, 350, "bloodyloodies", loogie_anim)
    
    for x in range(50):
        skreet = creatures.Sprite(500,500, "skreet", skanim)
        creatures.randomspawn(skreet,game_map, spawnpoints)
        skreet.vx = 1
        skreet.vy = 0
        skreet.hitpoints = 10
        skreet.facing = "left"
        skreet.mode = "cheel"
        skreet.target = player
        skreet.tick = creatures.tick_skreet
        sprites.append(skreet)
        tung = creatures.Sprite(32, 32, "skreettung", simple_img=world.image_db["skreettung"])
    
    
    for x in range(50):
        gloub = creatures.Sprite(500,500, "gloub", glanim)
        creatures.randomspawn(gloub,game_map, spawnpoints)
        gloub.vx = 1
        gloub.vy = 0
        gloub.hitpoints = 18
        gloub.facing = "left"
        gloub.mode = "cheel"
        gloub.target = player
        gloub.tick = creatures.tick_gloub
        sprites.append(gloub)
    

    
    shield = creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 
    border_surf = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    pygame.draw.rect(border_surf, (255,0,0), (0,0,32,32), 1)
    
    sprites.append(shield)
    
    cam_size = 32 * 15 
    cam = display.Camera(player, 32, 32, cam_size, cam_size)
    
    
    shield.width = 90
    shield.maxwidth = 90
    
    while(running):
        clock.tick(60)
        if shield.width <= shield.maxwidth:
            shield.width+= 0.025
        key_timer += 1
        if world.globs["tortoise_spawn"] == True:
            tortoise_spawn(creatures.cur_zone(player, zones), sprites)
            world.globs["tortoise_spawn"] = False
        if world.mode == "game":
            sprites, running = game_mode(timers, player, game_map, ts, sprites, shield, swidth, running)
        elif world.mode == "dialogue":
            dialogue_mode()
        else:
            assert(False)
        
        nearby_sprites = list(filter(lambda s: distance(s,player) < 250, sprites))
        collisions.check_collisions(nearby_sprites, sprites)

        sprites = list(filter(lambda s: s.alive, sprites))
            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                part.crazy_splatter(player.x + 50, player.y + 50, (255,0,0))
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                
        screen.fill((0,0,0))        
        if player.alive:
            display.draw_interface(screen, cam, ts, game_map, sprites)
    
        if player.hitpoints <= 0:
            player.alive = False
            shield.alive = False
            screen.blit(world.image_db["Deathscreen"],(0,0))
    
        pygame.display.flip()

        
pygame.init()
flags = DOUBLEBUF
screen = pygame.display.set_mode((800, 600), flags)
try:
    main(screen)
except Exception as e:
    pygame.display.quit()
    print(traceback.format_exc())        
    
    
