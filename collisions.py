import pygame
from itertools import combinations

def keep_separated(s1, s2):
    s1.x = s1.last_x
    s1.y = s1.last_y
    s2.x = s2.last_x
    s2.y = s2.last_y
    
def check_collisions(sprites):
    scombs = combinations(sprites, 2)
    for s1, s2 in scombs:
        cpair = (s1.kind, s2.kind)
        # adjust hitbox x and y 
        hb1 = pygame.Rect(s1.x + s1.hitbox.x, s1.y + s1.hitbox.y, s1.hitbox.width, s1.hitbox.height)
        hb2 = pygame.Rect(s2.x + s2.hitbox.x, s2.y + s2.hitbox.y, s2.hitbox.width, s2.hitbox.height)
        if cpair in collision_db and hb1.colliderect(hb2):
            collision_db[cpair](s1, s2)
        
collision_db = {("player", "monk"): keep_separated,
                ("player", "wall"): keep_separated}
