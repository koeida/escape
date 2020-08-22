import pygame
import traceback
import display
from random import randint
import creatures
import timers
    
def get_input(player, m, ts):
    keys = pygame.key.get_pressed()
    speed = 10
    dx = 0
    dy = 0
    
    if keys[pygame.K_d]:
        dx = speed
    if keys[pygame.K_w]:
        dy = -speed
    if keys[pygame.K_a]:
        dx = -speed
    if keys[pygame.K_s]:
        dy = speed
    
    creatures.attempt_walk(player, dx, dy, m, ts)

def main(screen):   
    clock = pygame.time.Clock()
    running = True
    
    ts = display.load_tileset("cavetiles_01.png", 32, 32)    
    
    player = creatures.Sprite()
    player.x = 400
    player.y = 200
    player.img = pygame.Surface((10,10))
    player.img.fill((255,0,0),(3,3,3,3))
    
    game_map = [[0 for x in range(100)] for y in range(100)]
    for x in range(1000):
        game_map[randint(0,99)][randint(0,99)] = randint(0,7)
    
    for x in range(100):
        game_map[10][x] = 16 * 6 + 2
        
    sprites = [player]

    timers.add_timer(3, lambda: player.img.fill((0,0,255), (3,3,3,3)))
    
    cam = display.Camera(player, 32*9, 32*9)
    
    while(running):
        clock.tick(60)
        timers.update_timers()
        
        screen.fill((0,0,0))        
       
        display.draw_camera(screen, cam, ts, game_map, 32, 32, sprites)
        screen.fill((255,0,0), (cam.width + 32, 0, 1, cam.height))
        
        get_input(player, game_map, ts)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                
                
        pygame.display.flip()

        
pygame.init()
screen = pygame.display.set_mode((800, 600))
try:
    main(screen)
except Exception as e:
    pygame.display.quit()
    print(traceback.format_exc())        
    
    