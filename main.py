import pygame
import sys
from pygame.locals import *

from level import Level
from settings import * 

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight), DOUBLEBUF)
clock = pygame.time.Clock()
renderingFrame = pygame.Surface((CONST_screenWidth, CONST_screenHeight))

levelCount = 0

pygame.display.set_caption("Platformer Game")
level = Level(levels[0], screen)
level.loadLevel()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    renderingFrame.fill(white)
    if level.reset == 0:#Wont reset
        level.tick(renderingFrame)
    else:
        if level.reset == 2:#End of level else is just death without checkpoint aka resets whole level
            levelCount += 1
        level = Level(levels[levelCount], screen)
        level.loadLevel()

    pygame.display.flip()### NOTE: Use this for double buffering later on. ###


    clock.tick(50)#Temporary workaround for no double buffering, should be 60fps but whatever


