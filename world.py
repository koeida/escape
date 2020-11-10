import pygame

TILE_WIDTH = 32
TILE_HEIGHT = 32
FPS = 60

image_db = ["BODY_male.png",
            "LEGS_robe_skirt.png",
            "boganim.png",
            "puke.png",
            "BLOOD.png",
            "key.png"]
def load_assets():
    global image_db
    assets_dir = "lpc_entry/png/walkcycle/" 

    result = {}
    for fname in image_db:
        noending = fname[:-4]
        result[noending] = pygame.image.load(assets_dir + fname)
    image_db = result
