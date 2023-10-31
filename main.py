import pygame
import sys
import math
from pygame.locals import *

from level import Level
import settings

pygame.init()
settings.initializeFont()

screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
clock = pygame.time.Clock()
renderingFrame = pygame.Surface((settings.CONST_screenWidth, settings.CONST_screenHeight))

levelCount = 0

pygame.display.set_caption("Platformer Game")

for i in range(1, settings.tileSpriteCount+1):
    temp = pygame.image.load("./Assets/Sprites/Tiles/tile" + str(i) + ".png").convert_alpha()
    settings.tileSprites.append(temp)

level = Level("test", screen)
level.loadLevel_squared()

fixedTimeStep = 1.0 / 45.0 #60fps timestep
accumulatedTime = 0
currentTime = pygame.time.get_ticks()



# Main game loop
while True:
    #Get difference of time between last frame and current frame
    newTime = pygame.time.get_ticks()
    frameTime = (newTime - currentTime) / 1000.0  
    currentTime = newTime
    accumulatedTime += frameTime# Accumulate it into a variable

    for event in pygame.event.get():
        if event.type == pygame.QUIT:#disables pygame and system libraries on program exit
            pygame.quit()
            sys.exit()
        elif settings.gamemode == 1:#Check if clicked and if gamemode is editing mode
            if event.type == pygame.MOUSEBUTTONUP:

                #Get second coordinate and stop showing preview
                selCords = level.editor.selectionCoordinates

                pos = pygame.mouse.get_pos()
                x, y = settings.screenToWorldSpace(level, pos[0], pos[1])#get world coordinate of tile at clicked coordinate
                if pos[1] > settings.screenHeight-200:
                    level.editor.onClick(pos[0], pos[1], event.button)
                elif event.button == 1:
                    level.editor.createTile(level, (selCords[0], selCords[1]), (x, y))
                elif event.button == 3:
                    level.editor.removeTile(level, (selCords[0], selCords[1]), (x, y))
                level.editor.selectionCoordinates = None
            elif event.type == pygame.MOUSEBUTTONDOWN:


                #Get first coordinate and ##also if statement to render preview##
                pos = pygame.mouse.get_pos()
                x, y = settings.screenToWorldSpace(level, pos[0], pos[1])#get world coordinate of tile at clicked coordinate

                level.editor.selectionCoordinates = (x, y)
        


        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    level.toggleEditor()
                elif event.key == pygame.K_v:    
                    level.saveLevel_squared()
            


    #Gameplay
    if accumulatedTime >= fixedTimeStep:#If accumulated time is say twice the amount of the fixed time step then run gameplay twice so it catches up (spiral of death factor can occur perhaps? dunno)
        #print("Accumulated Time:" + str(accumulatedTime))
        if level.reset == 0:#Wont reset
            level.tick()
        else:
            if level.reset == 2:#End of level else is just death without checkpoint aka resets whole level
                levelCount += 1
            level = Level("test", screen)
            level.loadLevel_squared()
        accumulatedTime -= fixedTimeStep


    #Double buffered rendering (kinda wonk with only pygame, maybe needs opengl support)
    if level.doRender == True:
        pygame.display.flip()
        level.doRender = False
        level.render(renderingFrame)
    clock.tick(45)


