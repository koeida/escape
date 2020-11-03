from gamemap import gen_test_map
from input import get_input
from random import randint
from tools import get_coords, distance
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
from pygame.locals import *
    
def get_input(player, m, ts):
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
    if o:
        x = int((player.x + 32) / 32)
        y = int((player.y + 32)/ 32)
        adjacenttiles = ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y - 1, x - 1), (y + 1, x - 1), (y - 1, x + 1))
        doors = list(filter(lambda t: m[t[0]][t[1]] == 12, adjacenttiles))
        if doors != []:
            dy, dx = doors[0]
            m[dy][dx] = 13
            
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
    
    game_map = dungeongen.make_dungeon(140)
    
    tsimg = pygame.image.load("tile sheet.png")
    tsimg.convert()
    ts = display.load_tileset(tsimg, 32, 32)        
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

    player = creatures.Sprite(400, 400, "player", panim)
    player.tick = creatures.tick_player
    player = creatures.Sprite(400, 400, "player", panim)
    creatures.randomspawn(player,game_map)
    player.hitbox = pygame.Rect(24, 43, 18, 18)
    enemy = creatures.Sprite(600, 600, "monk", panim)
    
    sprites = [player]
    
    for x in range(20):
        borgalon = creatures.Sprite(500,500, "borgalon", banim)
        creatures.randomspawn(borgalon,game_map)
        borgalon.vx = 1
        borgalon.vy = 0
        borgalon.facing = "right"
        borgalon.mode = "chase"
        borgalon.target = player
        borgalon.tick = creatures.tick_borgalon
        sprites.append(borgalon)
    puke = creatures.Sprite(350, 350, "puke", puke_anim)

    swidth = player.get_rect().width + 35
    smiddle = int(swidth / 2)
    shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    
    shield = creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 
    border_surf = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    pygame.draw.rect(border_surf, (255,0,0), (0,0,32,32), 1)
    


        

    sprites = [player, borgalon, shield]
    
    cam_size = 32 * 15 
    cam = display.Camera(player, 32, 32, cam_size, cam_size)
    
    # Timer Example
    timers.add_timer(5, lambda: cam.set_shake(5))
    timers.add_timer(10, lambda: cam.set_shake(0))
    
    while(running):
        clock.tick(60)
        timers.update_timers()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        get_input(player, game_map, ts)       
        
        for s in sprites:
            creatures.tick_anim(s)
            if s.kind != "wall":
                if s.tick != None:
                    s.tick(s, game_map, ts, sprites)
                #creatures.attempt_walk(s, game_map, ts)
            
        shield.x = player.x - 17
        shield.y = player.y - 10
        #player_sx, player_sy = display.calc_screen_coords(coords, camrect)
        shield.simple_img = display.render_shield(mouse_x, mouse_y, swidth)       
        nearby = list(filter(lambda s: distance(s, player) <= 250, sprites))
        collisions.check_collisions(nearby)
        sprites = list(filter(lambda s: s.alive, sprites))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                
        screen.fill((0,0,0))        
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
    
    
