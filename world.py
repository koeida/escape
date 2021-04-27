import pygame
from collections import namedtuple


TILE_WIDTH = 32
TILE_HEIGHT = 32
total_ticks = 0 
FPS = 60
mode = "game"
dialogue_message = ""
diakey = ""
diaindex = 0
choice = ""  
partner = None
globs = {"tortoise_spawn": False}
cur_world = "main"
worlds = {}
image_db = ["BODY_male.png",
            "LEGS_robe_skirt.png",
            "boganim.png",
            "puke.png",
            "i_square.png",
            "i_square_select.png",
            "BLOOD.png",
            "VLATION.png",
            "bloodyloodies.png",
            "Gloub.png",
            "Skreets.png",
            "skreettung.png",
            "key.png",
            "borgalon_fang.png",
            "keyanimation.png",
            "cornershadow.png",
            "topshadow.png",
            "sideshadow.png",
            "portal.png",
            "coin.png",
            "dbtl.png",
            "dbt.png",
            "dbtr.png",
            "dbl.png",
            "dbr.png",
            "dbbl.png",
            "dbb.png",
            "dbbr.png",
            "stranger.png",
            "boss1.png",
            "Deathscreen.png",
            "darkscreen.png",
            "torches.png",
            "chest2.png",
            "chest.png",
            "tortoise2.png",
            "light.png",
            "tortoise_collector.png"]
            
def tile(walkable=True, floor_tile=False, matching_tile=None):
    results = TileInfo()
    results.walkable = walkable
    results.floor_tile = floor_tile
    results.matching_tile = matching_tile
    return results

class TileInfo:
    pass
    
Tileset = namedtuple("Tileset", "image tile_width tile_height tiles_per_line rows data")

def load_tileset(tileset_img, tile_width, tile_height):
    img_width = tileset_img.get_rect().width   
    img_height = tileset_img.get_rect().height    
    tiles_per_line = int(img_width / tile_width)
    rows = int(img_height / tile_height)   
    
    data = {0: tile(True, True),
            1: tile(False, matching_tile=6),
            3: tile(False),
            5: tile(False, matching_tile=9),
            6: tile(False),
            7: tile(False, matching_tile=8),
            8: tile(False),
            9: tile(False),
            10: tile(False),
            11: tile(True), 
            12: tile(False),
            13: tile(False),
            14: tile(True),
            15: tile(True, True),
            16: tile(True, True),
            17: tile(False),
            18: tile(False, matching_tile=19),
            19: tile(False),
            20: tile(True),
            21: tile(False, matching_tile=22),
            22: tile(False),
            23: tile(True, True),
            24: tile(False, matching_tile=25),
            25: tile(False),
            26: tile(True, True),
            27: tile(True, True),
            28: tile(False, matching_tile=29),
            29: tile(False),
            30: tile(False, matching_tile=31),
            31: tile(False),
            32: tile(True),
            33: tile(True, True)}
            
    return Tileset(tileset_img, tile_width, tile_height, tiles_per_line, rows, data)
    
def load_assets():
    global image_db
    assets_dir = "lpc_entry/png/walkcycle/" 

    result = {}
    for fname in image_db:
        noending = fname[:-4]
        try:
            result[noending] = pygame.image.load(assets_dir + fname)
        except:
            print(assets_dir + fname)
            exit()
    image_db = result

tsimg = pygame.image.load("tile sheet.png")
#tsimg.convert()
TILES = load_tileset(tsimg, 32, 32)        
