"""
This file contains all CONSTANTS of the game that are not considered to be changed
"""
import pygame

BLUE = (25, 180, 200)
BLACK = (30, 30, 30)
RED = (204, 0, 0)
PURPLE = (204, 0, 80)
WHITE = (204, 204, 204)

SPECIAL_CONTENT = ['river', 'exit', 'treasure', 'map', 'wormhole']
SOURCES = '../Sources/'
IMG_PLAYER = SOURCES + 'player.png'
IMG_ALIEN = SOURCES + 'alien.png'
IMG_HORN = SOURCES + 'horned_skull.png'
IMG_BEAR = SOURCES + 'bear_face.png'
IMG_HOLE = SOURCES + 'hole.png'
IMG_MAP = SOURCES + 'map.png'
IMG_TREASURE = SOURCES + 'treasure.png'
IMG_RIVER = SOURCES + 'river.png'
IMG_RIVER_START = SOURCES + 'river_start.png'
IMG_EXIT = SOURCES + 'exit.png'
TITLE = 'Dark Labyrinth'

KEY_MAP = {
    'right': [pygame.K_d, pygame.K_RIGHT],
    'left': [pygame.K_a, pygame.K_LEFT],
    'down': [pygame.K_s, pygame.K_DOWN],
    'up': [pygame.K_w, pygame.K_UP],
    'activate': [pygame.K_e],
    'skip': [pygame.K_p],
    'quit': [pygame.K_ESCAPE]
}
