import pygame
import sys

from level import Level
from settings import * 

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

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
    
    screen.fill(white)
    if level.reset == 0:#Wont reset
        level.tick()
    else:
        if level.reset == 2:#End of level else is just death without checkpoint
            levelCount += 1
        level = Level(levels[levelCount], screen)
        level.loadLevel()

    pygame.display.flip()### NOTE: Use this for double buffering later on. ###


    clock.tick(50)#Temporary workaround for no double buffering, should be 60fps but whatever


