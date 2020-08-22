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
        if cpair in collision_db and s1.get_rect().colliderect(s2.get_rect()):
            collision_db[cpair](s1, s2)
        
    

collision_db = {("player", "monk"): keep_separated}
