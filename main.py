from gamemap import gen_test_map
from input import get_input
from random import randint, uniform, choice
from tools import get_coords, distance, filter_dict
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

def get_input(player, m, ts, cs):
    keys = pygame.key.get_pressed()
    speed = 8
    dx = 0
    dy = 0
    
    w = keys[pygame.K_w]
    s = keys[pygame.K_s]
    d = keys[pygame.K_d]
    a = keys[pygame.K_a]
    o = keys[pygame.K_o]
    
    oldfacing = player.facing
    
    ks = list(filter(lambda i: i.kind == "key", player.inventory))
    
    if keys[pygame.K_t]:
        key = list(filter(lambda x: x.kind == "portal", cs))[0]
        player.x = key.x + 5
        player.y = key.y + 5
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
   

def main(screen):   
    clock = pygame.time.Clock()
    running = True
    
    world.load_assets()

    stacked_dude = display.stack_spritesheets(["BODY_male", "LEGS_robe_skirt"])
    world.image_db["dude"] = stacked_dude
    
    game_map, keys, start, end = dungeongen.make_dungeon(140)
    
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
                         }
            }
    
    
    puke_anim = { "walking": {"down": ("puke", 20, 20, [0], 7)}}
    room = dungeongen.shrink_room(choice(start.rooms))
    py = randint(room.y + 1, room.y + room.h - 1)
    px = randint(room.x + 1, room.x + room.w - 1)
    player = creatures.Sprite(px * 32, py * 32, "player", panim)
    player.tick = creatures.tick_player
    #player.x = 1000
    #player.y = 1000
    player.hitbox = pygame.Rect(24, 43, 18, 18)
    player.hitpoints = 100
    enemy = creatures.Sprite(600, 600, "monk", panim)
    assert(start.rooms != end.rooms)
    room2 = dungeongen.shrink_room(choice(end.rooms))
    portaly = randint(room2.y + 1, room2.y + room2.h - 1)
    portalx = randint(room2.x + 1, room2.x + room2.w - 1)
    portal = creatures.Sprite(portalx * 32, portaly * 32, "portal", simple_img=world.image_db["portal"])
    portal.tick = creatures.portal_tick
    portal.original_img = portal.simple_img
    portal.angle = 0

    
    
    
    
    swidth = player.get_rect().width + 35
    smiddle = int(swidth / 2)
    shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    
    shield = creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 
    border_surf = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    pygame.draw.rect(border_surf, (255,0,0), (0,0,32,32), 1)
    

        

    sprites = [player, shield] + keys
    
    sprites.append(portal)
     
    dungeongen.add_shadow(game_map, sprites)
    
    spawnpoints = get_coords(game_map, filter_dict(lambda x: x.floor_tile, world.TILES.data))
    for x in range(200):
        borgalon = creatures.Sprite(500,500, "borgalon", banim)
        creatures.randomspawn(borgalon,game_map, spawnpoints)
        borgalon.hitpoints = 5
        borgalon.vx = 1
        borgalon.vy = 0
        borgalon.facing = "right"
        borgalon.mode = "cheel"
        borgalon.target = player
        borgalon.tick = creatures.tick_borgalon
        sprites.append(borgalon)
    puke = creatures.Sprite(350, 350, "puke", puke_anim)

    
    shield = creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 
    border_surf = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    pygame.draw.rect(border_surf, (255,0,0), (0,0,32,32), 1)
    
    sprites.append(shield)
    
    cam_size = 32 * 15 
    cam = display.Camera(player, 32, 32, cam_size, cam_size)
        
    while(running):
        clock.tick(60)
        timers.update_timers()
        
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
        shield.simple_img = display.render_shield(mouse_x, mouse_y, swidth)       
        
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
                
        screen.fill((0,0,0))    
        if player.alive:
            display.draw_interface(screen, cam, ts, game_map, sprites)
        
        pygame.display.flip()

        
pygame.init()
flags = DOUBLEBUF
screen = pygame.display.set_mode((800, 600), flags)
try:
    main(screen)
except Exception as e:
    pygame.display.quit()
    print(traceback.format_exc())        
    
    
