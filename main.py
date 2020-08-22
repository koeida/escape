import pygame
import traceback
import display
from random import randint
import creatures

class Sprite:
    pass
     
    
def get_input(player, m):
    keys = pygame.key.get_pressed()
    speed = 1
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
    
    creatures.attempt_walk(player, dx, dy, m)

def main(screen):   
    clock = pygame.time.Clock()
    running = True
    
    ts = display.load_tileset("cavetiles_01.png", 32, 32)    
    
    player = Sprite()
    player.x = 400
    player.y = 400
    
    game_map = [[0 for x in range(100)] for y in range(100)]
    for x in range(1000):
        game_map[randint(0,99)][randint(0,99)] = randint(0,7)
    cam = display.Camera(player, 32*9, 32*9)
    
    while(running):
        clock.tick(60)
        
        screen.fill((0,0,0))        
       
        display.draw_camera(screen, cam, ts, game_map, 32, 32)
        screen.fill((255,0,0), (cam.width + 32, 0, 1, cam.height))
        
        get_input(player, game_map)
            
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
    
    