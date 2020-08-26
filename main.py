import pygame
import pygame.gfxdraw
import traceback
import display
from random import randint
import creatures
import timers
import world
import collisions
import math
    
def get_input(player, m, ts):
    keys = pygame.key.get_pressed()
    speed = 4
    dx = 0
    dy = 0
    
    w = keys[pygame.K_w]
    s = keys[pygame.K_s]
    d = keys[pygame.K_d]
    a = keys[pygame.K_a]
    
    if w:
        player.vy = -speed
    if s:
        player.vy = speed
    if d:
        player.vx = speed
    if a:
        player.vx = -speed
        
    if not s and not w:
        player.vy = 0
    if not a and not d:
        player.vx = 0    
    
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
    
    world.load_assets(world.image_db)
    ts = display.load_tileset(pygame.image.load("cavetiles_01.png"), 32, 32)    
    
    panim = {"walking": ("dude", 64, 64, range(1,9), 5)}
    player = creatures.Sprite(400, 400, "player", panim)
    enemy = creatures.Sprite(600, 600, "monk", panim)
    
    #swidth = player.get_rect().width + 35
    #smiddle = int(swidth / 2)
    #shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    #
    #shield = creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 
    #border_surf = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    #pygame.draw.rect(border_surf, (255,0,0), (0,0,32,32), 1)
    game_map = gen_test_map()
        
    sprites = [player, enemy]
    
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
                creatures.attempt_walk(s, game_map, ts)
            
        #shield.x = player.x - 17
        #shield.y = player.y - 10
        #player_sx, player_sy = display.calc_screen_coords(coords, camrect)
        #shield.simple_img = render_shield(player_sx, player_sy, mouse_x, mouse_y, swidth)
        
        collisions.check_collisions(sprites)
            
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
screen = pygame.display.set_mode((800, 600))
try:
    main(screen)
except Exception as e:
    pygame.display.quit()
    print(traceback.format_exc())        
    
    
