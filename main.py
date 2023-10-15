import pygame
import sys
from pygame.locals import *

from level import Level
from settings import * 

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
renderingFrame = pygame.Surface((CONST_screenWidth, CONST_screenHeight))

levelCount = 0

pygame.display.set_caption("Platformer Game")
level = Level(levels[0], screen)
level.loadLevel()

fixedTimeStep = 1.0 / 60.0 #60fps timestep
accumulatedTime = 0
currentTime = pygame.time.get_ticks()

# Main game loop
while True:

    #Get difference of time between last frame and current frame
    newTime = pygame.time.get_ticks()
    frameTime = (newTime - currentTime) / 1000.0  
    currentTime = newTime
    accumulatedTime += frameTime# Accumulate it into a variable

    #disable pygame and system libraries on program exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    #Gameplay
    while accumulatedTime >= fixedTimeStep:#If accumulated time is say twice the amount of the fixed time step then run gameplay twice so it catches up (spiral of death factor can occur perhaps? dunno)
        if level.reset == 0:#Wont reset
            level.tick(renderingFrame)
        else:
            if level.reset == 2:#End of level else is just death without checkpoint aka resets whole level
                levelCount += 1
            level = Level(levels[levelCount], screen)
            level.loadLevel()
        accumulatedTime -= fixedTimeStep

    #Double buffered rendering
    if level.doRender == True:
        pygame.display.flip()### NOTE: Use this for double buffering later on. ###
        level.doRender = False
        level.render(renderingFrame)
    clock.tick(30)


