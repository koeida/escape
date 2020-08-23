import pygame
import traceback
import display
from random import randint
import creatures
import timers
import world
import collisions
    
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
    
        
    
    
    

def main(screen):   
    clock = pygame.time.Clock()
    running = True
    
    world.load_assets(world.image_db)
    ts = display.load_tileset("cavetiles_01.png", 32, 32)    
    
    panim = {"walking": ("test_monk", [0], 40)}
    player = creatures.Sprite(400, 400, "player", panim)
    enemy = creatures.Sprite(600, 600, "monk", panim)
    
    game_map = [[0 for x in range(100)] for y in range(100)]
    for x in range(1000):
        game_map[randint(0,99)][randint(0,99)] = randint(0,7)
    
    for x in range(100):
        game_map[10][x] = 16 * 6 + 2
        
    sprites = [player, enemy]
    
    
    cam = display.Camera(player, 32*9, 32*9)
    
    # Timer Example
    timers.add_timer(5, lambda: cam.set_shake(5))
    timers.add_timer(10, lambda: cam.set_shake(0))
    
    while(running):
        clock.tick(60)
        timers.update_timers()
        
        
        get_input(player, game_map, ts)
        
        for s in sprites:
            creatures.attempt_walk(s, game_map, ts)
        
        collisions.check_collisions(sprites)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                
        screen.fill((0,0,0))        
       
        camx = 50
        camy = 50
        cam_surface = display.render_camera(cam, ts, game_map, sprites)
        screen.blit(cam_surface, (camx, camy))
        screen.fill((255,0,0), (cam.width + camx, camy, 1, cam.height))        
        screen.fill((255,0,0), (camx, camy, cam.width, 1))        
        screen.fill((255,0,0), (camx, camy + cam.height, cam.width, 1))        
        screen.fill((255,0,0), (camx, camy, 1, cam.height))            
        screen.fill((255,0,0), (camx + int(cam.width / 2), camy + int(cam.height / 2), 2, 2))    
        pygame.display.flip()

        
pygame.init()
screen = pygame.display.set_mode((800, 600))
try:
    main(screen)
except Exception as e:
    pygame.display.quit()
    print(traceback.format_exc())        
    
    