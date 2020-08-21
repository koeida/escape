import pygame
import traceback

def main(screen):   
    clock = pygame.time.Clock()
    running = True

    while(running):
        clock.tick(60)
        
        screen.fill((0,0,0))    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                
        pygame.display.flip()

        
pygame.init()
screen = pygame.display.set_mode((1024,768))
try:
    main(screen)
except Exception as e:
    pygame.display.quit()
    print(traceback.format_exc())        
    
    