import pygame
import creatures

def get_input(player, m, ts):
    keys = pygame.key.get_pressed()
    speed = 4
    dx = 0
    dy = 0
    
    w = keys[pygame.K_w]
    s = keys[pygame.K_s]
    d = keys[pygame.K_d]
    a = keys[pygame.K_a]

    oldfacing = player.facing
    
    if w:
        player.vy = -speed
        player.facing = "up"
    if s:
        player.vy = speed
        player.facing = "down"
    if d:
        player.vx = speed
        player.facing = "right"
    if a:
        player.vx = -speed
        player.facing = "left"
    if not s and not w:
        player.vy = 0
    if not a and not d:
        player.vx = 0    

    if player.vx == 0 and player.vy == 0:
        creatures.switch_anim(player,"standing")
    else:
        creatures.switch_anim(player,"walking")

    if player.facing != oldfacing:
        player.current_frame = 0
