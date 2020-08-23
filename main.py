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
    speed = 10
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
    ts = display.load_tileset("cavetiles_01.png", 32, 32)    
    
    panim = {"walking": ("test_monk", [0], 40)}
    player = creatures.Sprite(400, 400, "player", panim)
    enemy = creatures.Sprite(600, 600, "monk", panim)
    
    swidth = player.get_rect().width + 35
    smiddle = int(swidth / 2)
    shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
    
    shield= creatures.Sprite(400, 400, "shield", simple_img=shield_surface) 
    
    game_map = gen_test_map()
        
    sprites = [player, enemy, shield]
    
    
    cam = display.Camera(player, 32*9, 32*9)
    
    # Timer Example
    timers.add_timer(5, lambda: cam.set_shake(5))
    timers.add_timer(10, lambda: cam.set_shake(0))
    
    while(running):
        clock.tick(60)
        timers.update_timers()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        get_input(player, game_map, ts)       
        
        
        for s in sprites:
            creatures.attempt_walk(s, game_map, ts)
            
        shield.x = player.x - 17
        shield.y = player.y - 10
        cam_size = 32*9
        cam_pos = 50
        rel_x, rel_y = mouse_x - cam_pos - cam_size, mouse_y - cam_pos - cam_size
        #angle = math.atan2(rel_y, rel_x)
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        shield_surface = pygame.Surface((swidth, swidth), pygame.SRCALPHA)
        sangle = 90 / 2
        pygame.gfxdraw.arc(shield_surface, smiddle, smiddle, 45, 
                           int(angle - sangle), int(angle + sangle),
                           (255, 255, 255))  
        shield.simple_img = shield_surface
        
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
    
    