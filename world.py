import pygame

TILE_WIDTH = 32
TILE_HEIGHT = 32
FPS = 60

image_db = {"dude": "BODY_male.png",
            "monk": "robe.png"}
    
def load_assets(db):
    for key in image_db.keys():
        image_db[key] = pygame.image.load(image_db[key])
