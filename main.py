import pygame
import traceback
import display
from random import randint

class Sprite:
    pass

def main(screen):   
    clock = pygame.time.Clock()
    running = True
    
    ts = display.load_tileset("cavetiles_01.png", 32, 32)    
    
    player = Sprite()
    player.x = 400
    player.y = 400
    
    test_world = [[0 for x in range(100)] for y in range(100)]
    for x in range(1000):
        test_world[randint(0,99)][randint(0,99)] = randint(0,7)
    cam = display.Camera(player, 32*9, 32*9)
    
    while(running):
        clock.tick(60)
        
        screen.fill((0,0,0))        
       
        display.draw_camera(screen, cam, ts, test_world, 32, 32)
        screen.fill((255,0,0), (cam.width + 32, 0, 1, cam.height))
        
        keys = pygame.key.get_pressed()
        speed = 2
        if keys[pygame.K_d]:
            player.x += speed
        if keys[pygame.K_w]:
            player.y -= speed
        if keys[pygame.K_a]:
            player.x -= speed
        if keys[pygame.K_s]:
            player.y += speed
            
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
    
    