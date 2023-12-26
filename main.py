# © 2023 Tommy Kroon <somnic.vulpes@gmail.com>


'''
Contains game loop, fps handling, rendering and level to level loading.
Running this file starts the game.

NOTE: Most important files are level.py, settings.py and this file.
'''

import pygame, sys, settings
from pygame.locals import *

from level import Level

pygame.init()
settings.initializeFont()

screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight), pygame.DOUBLEBUF)
clock = pygame.time.Clock()
renderingFrame = pygame.Surface((settings.CONST_screenWidth, settings.CONST_screenHeight))

levelCount = 0

pygame.display.set_caption("Python Platformer")

for i in range(1, settings.tileSpriteCount+1):
    temp = pygame.image.load("./Assets/Sprites/Tiles/tile" + str(i) + ".png").convert_alpha()
    settings.tileSprites.append(temp)


level = Level(settings.levels[levelCount], screen)

#Time Variables

physicsFps = 45
RenderingFps = 30

fixedTimeStep = 1.0 / physicsFps
accumulatedTime = 0
lastTime = pygame.time.get_ticks()



# Main game loop
while True:
    for event in pygame.event.get():
        #disables pygame and system libraries on program exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Check if clicked and if gamemode is editing mode
        elif settings.gamemode == 1:
            if event.type == pygame.MOUSEBUTTONUP:

                #Get second coordinate and stop showing preview
                selCords = level.editor.selectionCoordinates

                pos = pygame.mouse.get_pos()

                #get world coordinate of tile at clicked coordinate
                x, y = settings.screenToWorldSpace(level, pos[0], pos[1])

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

                #Get world coordinate of tile at clicked coordinate
                x, y = settings.screenToWorldSpace(level, pos[0], pos[1])

                level.editor.selectionCoordinates = (x, y)
        


        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    level.toggleEditor()
                elif event.key == pygame.K_v:    
                    level.saveLevel_squared()
            
    #Get difference of time between last frame and current frame
    currentTime = pygame.time.get_ticks()
    elapsedTime = (currentTime - lastTime) / 1000.0  

    accumulatedTime += elapsedTime# Accumulate it into a variable

    #Gameplay

    #This should be a while loop but it causes jittering i will have to look into that.
    while accumulatedTime >= fixedTimeStep:
        level.tick(1)
        accumulatedTime -= fixedTimeStep
        if level.reset == True:
            if level.alphaIncrement == 0:
                levelCount += 1
                if levelCount == len(settings.levels):
                    levelCount = 0
                level = Level(settings.levels[levelCount], screen)

    if accumulatedTime > 0:#Extrapolate next frame if theres a remainder
        level.tick(accumulatedTime / fixedTimeStep)
        accumulatedTime = 0
        

                


    pygame.display.flip()
    level.render(renderingFrame)
    lastTime = currentTime
    clock.tick(RenderingFps)


