from enum import Enum, auto
from os import path
import pygame


class Roles(Enum):

    Bubble = auto()
    Blocker = auto()
    Digger = auto()
    Exploder = auto()
    Pause = auto()
    FastFPS = auto()
    Mute = auto()
    SlowerFPS = auto()


class Colors:
    white = (255, 255, 255)
    blue1 = (152, 245, 255)
    blue2 = (0, 191, 255)
    yellow = (255, 236, 139)
    pink1 = (255, 105, 180)
    pink2 = (255, 20, 147)
    pink3 = (255, 181, 197)
    pink4 = (205, 145, 158)
    green = (102, 205, 0)
    black = (0, 0, 0)

# Paths

game_dir = path.dirname(__file__)
images_folder = path.join(game_dir, 'images')
sound_folder = path.join(game_dir, 'sound')

# Screen parameters

screen_width = 1000
screen_height = 600
title = 'Flamingo Game'
background_color = Colors.white
FPS = 30

# Flamingo settings

flamingoSize = 40
DefaultSize = flamingoSize
flamingo_start_x = 50
flamingo_start_y = 50

FlamingoMove = 5
flamingoButtonSize = 50
flamingoSize = 40

# button parameters
ButtonSize = 90
ButtonColor = Colors.pink1


# Default Settings

font = 'freesansbold.ttf'
defaultfontsize = 30
MainMenuMargin = 50
Coconut_size = 20
Coconut_freq = 300
Explosion_size = 70
DefaultImageSize_x = 50
DefaultImageSize_y = 50
IconSize = 70
Speed = 5

# Tiles parameters
TileSize = 50
Floors_list = []
Water_list = []


for i in range(0, screen_width+2*TileSize, TileSize):
    Floors_list.append((screen_width-TileSize-i, screen_height-4*TileSize))
    Water_list.append((screen_width-TileSize - i, screen_height-2.5*TileSize))
    Water_list.append((screen_width - TileSize - i, screen_height - 3 * TileSize))


GAME_IMAGES = { "water" : "watertop.png","ground": "DirtRock.png","rock": "ground.png","palm": "palma_1.png",
                "coconut": "coconut.png","coconut2": "coconut_1.png","escape": "Gold_0.png","exp1": "exp1.png",
                "exp2": "exp2.png","exp3": "exp3.png","exp4": "exp4.png","exp5": "exp5.png","exp6": "exp6.png",
                "fly1": "fly1.png","fly2": "fly2.png","fleming1": "fleming1.png","fleming2": "fleming2.png",
                "kursor": "kursor.png","bubble": "bubble.png","axe": "axe.png","bomb": "bomb.png","music": "music.png",
                "next": "next.png","previous": "previous.png","bubble_fly2": "bubble_fly2.png","bubble_fly1": "bubble_fly1.png",
                "bubble_walk_1": "bubble_walk_1.png","bubble_walk_2": "bubble_walk_2.png"}


icon_list = [(17, 510, "bubble.png", IconSize, IconSize),
             (110, 510, "axe.png", IconSize, IconSize),
             (210, 510, "stop.png", IconSize, IconSize),
             (310, 510, "bomb.png", IconSize, IconSize),
             (410, 510, "pause.png", IconSize, IconSize),
             (510, 510, "previous.png", IconSize, IconSize),
             (610, 510, "next.png", IconSize, IconSize),
             (710, 520, "music.png", IconSize, IconSize)]


# Global functions

# get_graphic function

__all_game_images = {}

def get_graphic(image_name, size_x=DefaultSize, size_y=DefaultSize):
    global __all_game_images
    image_path = path.join(images_folder, image_name)
    image = __all_game_images.get(image_path)
    if not image:
        image = pygame.image.load(path.join(images_folder, image_name)).convert_alpha()
        image = pygame.transform.scale(image, (size_x, size_y))
        __all_game_images[image_path] = image
    return image

# get sound function

_sound_files = {}

def play_sound(game,sound_name, volume = 1):
    global _sound_files
    sound_path = path.join(sound_folder, sound_name)
    sound = _sound_files.get(sound_path)
    if not sound:

        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(volume)
        _sound_files[sound_path] = sound
    if game.mute == False:
        sound.play()

