import pygame
import sys

def draw_text(screen, s, x, y):
    font = pygame.font.SysFont(None, 24)
    img = font.render(s, True, (255,255,255))
    screen.blit(img, (x, y))


pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True

path = sys.argv[1]
tile_width = int(sys.argv[2])
img = pygame.image.load(path)
img_width = int(img.get_rect().width / tile_width)
img_height = int(img.get_rect().height / tile_width)

while(running):
    screen.fill((0,0,0))        

    screen.blit(img,(0,0))
    for y in range(img_height):
        for x in range(img_width):
            draw_text(screen, str(y * img_width + x), x * tile_width, y * tile_width)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
    
    pygame.display.flip()
