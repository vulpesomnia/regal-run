import pygame
import sys
import math
from pygame.locals import *

from level import Level
import settings

pygame.init()

screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
clock = pygame.time.Clock()
renderingFrame = pygame.Surface((settings.CONST_screenWidth, settings.CONST_screenHeight))

levelCount = 0

pygame.display.set_caption("Platformer Game")

for i in range(1, settings.tileSpriteCount+1):
    temp = pygame.image.load("./Assets/Sprites/Tiles/tile" + str(i) + ".png").convert_alpha()
    settings.tileSprites.append(temp)

level = Level("test", screen)
level.loadLevel()

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
                pos = pygame.mouse.get_pos()
                x, y = Level.screenToWorldSpace(level, pos[0], pos[1])
                if pos[1] > settings.screenHeight-200:
                    level.editor.onClick(pos[0], pos[1])
                elif event.button == 1:
                    level.editor.createTile(level, x, y)
                elif event.button == 3:
                    x, y = Level.worldToScreenSpace(x, y)
                    for tile in level.tiles:
                        if (tile.rect.x == x) and (tile.rect.y == y):
                            level.editor.removeTile(tile)
                            break
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    level.toggleEditor()
                elif event.key == pygame.K_v:    
                    level.saveLevel()
            


    #Gameplay
    if accumulatedTime >= fixedTimeStep:#If accumulated time is say twice the amount of the fixed time step then run gameplay twice so it catches up (spiral of death factor can occur perhaps? dunno)
        #print("Accumulated Time:" + str(accumulatedTime))
        if level.reset == 0:#Wont reset
            level.tick()
        else:
            if level.reset == 2:#End of level else is just death without checkpoint aka resets whole level
                levelCount += 1
            level = Level("test", screen)
            level.loadLevel()
        accumulatedTime -= fixedTimeStep


    #Double buffered rendering (kinda wonk with only pygame, maybe needs opengl support)
    if level.doRender == True:
        pygame.display.flip()
        level.doRender = False
        level.render(renderingFrame)
    clock.tick(45)


