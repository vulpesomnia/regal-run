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

    #disables pygame and system libraries on program exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif (event.type == pygame.MOUSEBUTTONUP) and (settings.gamemode == 1):#Check if clicked and if gamemode is editing mode
            pos = pygame.mouse.get_pos()
            x = math.floor((pos[0]+level.camera.x - settings.screenWidth)/settings.tileSize)#Click.x + camera offset for world coordinates - screenwidth for 0, 0 to be at player spawn point divided by tilesize and floored to get x of a tile
            y = math.floor((pos[1]+level.camera.y - settings.screenHeight)/settings.tileSize)#same thing just y coordinate
            print(str(x) + ", " + str(y))#Coordinate of the tile you just clicked on
            if pos[1] > settings.screenHeight-200:
                level.editor.onClick(pos[0], pos[1])
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    level.enableEditor()
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
            level = Level(settings.levels[levelCount], screen)
            level.loadLevel()
        accumulatedTime -= fixedTimeStep


    #Double buffered rendering (kinda wonk with only pygame, maybe needs opengl support)
    if level.doRender == True:
        pygame.display.flip()
        level.doRender = False
        level.render(renderingFrame)
    clock.tick(45)


