'''
Contains global variables and settings for the game.
Also contains global functions.
'''

import pygame, math, os


CONST_screenWidth = 1920
CONST_screenHeight = 1080


#Ratio = ~1.78(1.777)
screenWidth = 1920#1200
screenHeight = 1080#675

tileSize = 96
deathHeight = 16 * tileSize

pWidth, pHeight = 40, 80
pAnimationFrames = ["walking1", "walking2", "walking3", "walking4", "flyingup", "flyingdown"]
tileSpriteCount = 72

playerColor = (0, 0, 255)
backgroundColor = (50, 161, 231)
groundColor = (255, 0, 0)
checkpointColor = (255, 255, 0)
endColor = (0, 255, 0)

gamemode = 0
tileSprites = []
font = None

levels = []


# Appends to the array above all level files.
for obj in os.scandir("Assets/Levels"):
    if obj.is_file():
        levels.insert(0, obj.name)
print("LEVELS: " + str(levels))

def setGamemode(int):
    global gamemode
    gamemode = int

def initializeFont():
    global font
    font = pygame.font.SysFont("arial", 30)

def dictLength(dict):
    length = 0
    for key, values in dict.items():
        length += len(values)
    return length

# - These are for tilesets not floating point world coordinates. - #
def worldToScreenSpace(x, y):
    x = screenWidth - x * tileSize
    y = screenHeight - y * tileSize
    return (x, y)
    
#x + camera offset for world coordinates - screenwidth for 0, 0 to be at player spawn point divided by tilesize and floored to get x of a tile
def screenToWorldSpace(level, x, y):
    x = math.floor((x+level.camera.x - screenWidth)/tileSize) * -1
    y = math.floor((y+level.camera.y - screenHeight)/tileSize) * -1
    return (x, y)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
