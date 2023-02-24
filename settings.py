import pygame as pg

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# Game settings
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY
FONT = "PixeloidMono-VGj6x.ttf"
DEFAULT_TIME = 6
TILESIZE = 32
EXIT_IMG = "exit.png"
LIGHT_IMG = "light.png"
MAPS = ['debugmap.tmx', 'map1.tmx', 'map2.tmx', 'map3.tmx', 'map4.tmx']

# Player settings
PLAYER_SPEED = 30
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)
PLAYER_IMG = "spritesheet_player.png"

# Mob settings
MOB_SPEED = 2
MOB_HIT_RECT = pg.Rect(0, 0, 32, 32)
MOB_IMG = "enemy.png"

# Audio and music
MAIN_MENU_MUSIC = 'Menu_music.mp3'
GAME_MUSIC = 'Game_music.mp3'
EFFECT_SOUNDS = {'level_start': 'Game_start.wav',
                'death': 'Death_sound_effect.wav',
                'win': 'Win_sound_effect.wav'}