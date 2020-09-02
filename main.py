from gamemap import gen_test_map
from input import get_input
from random import randint
import collisions
import creatures
import display
import math
import pygame
import pygame.gfxdraw
import timers
import traceback
import world

def main(screen):   
    clock = pygame.time.Clock()
    running = True
    
    world.load_assets()

    stacked_dude = display.stack_spritesheets(["BODY_male", "LEGS_robe_skirt"])
    world.image_db["dude"] = stacked_dude

    ts = display.load_tileset(pygame.image.load("cavetiles_01.png"), 32, 32)    
    
    panim = {
             "standing": {"up": ("dude", 64, 64, [0], 5),
                         "left": ("dude", 64, 64, [9], 5),
                         "down": ("dude", 64, 64, [18], 5),
                         "right": ("dude", 64, 64, [29], 5)},
             "walking": {"up": ("dude", 64, 64, range(1,9), 5),
                        "left": ("dude", 64, 64, range(10, 18), 5),
                        "down": ("dude", 64, 64, range(19, 27), 5),
                        "right": ("dude", 64, 64, range(28, 36), 5)}}

    player = creatures.Sprite(400, 400, "player", panim)
    enemy = creatures.Sprite(600, 600, "monk", panim) 

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
            creatures.attempt_walk(s, game_map, ts)
        
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
    
    
