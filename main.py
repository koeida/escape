import pygame
import traceback
import display

def main(screen):   
    clock = pygame.time.Clock()
    running = True
    
    ts = display.load_tileset("cavetiles_01.png", 32, 32)    

    while(running):
        clock.tick(60)
        
        screen.fill((0,0,0))
        for x in range(16):
            display.draw_tile(screen, ts, x, x * 32, 10)
        
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
    
    