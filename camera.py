# © 2023-2024 Tommy Kroon <tommy.m.kroon@gmail.com>

'''
This file contains the camera system for the game.

The camera follows the player each frame by interpolating to the player's location.
Then all rendered objects are offset by the camera's location. This creates the illusion that the screen
is following the player. In conclusion all objects are just dragged to the screen with the player in the middle.
'''

import settings

class Camera:

    def __init__(self, x, y, player):
        self.player = player
        self.yOffset = -15
        self.x, self.y = x - settings.CONST_screenWidth / 2, y - settings.CONST_screenHeight / 2 + self.yOffset

    def updatePosition(self):#Updates position of camera to player using linear interpolation aka just damping, how does it work? I forgot.
        player = self.player.sprite
        if (player.isDead == 0):
            newX = self.x * 0.75 + ((player.rect.x - settings.CONST_screenWidth / 2)) * 0.25
        
            newY = self.y * 0.75 + ((player.rect.y - settings.CONST_screenHeight / 2)) * 0.25 + self.yOffset



            if settings.gamemode == 0:
                self.x, self.y = newX, min(settings.deathHeight- settings.CONST_screenHeight, max(0, newY))
            else:
                editorYOffset = settings.currentLevel.editor.height
                self.x, self.y = newX, min(settings.deathHeight- settings.CONST_screenHeight + editorYOffset, max(0, newY))

    def getPosition(self):
        return (self.x - settings.CONST_screenWidth/2, self.y - settings.CONST_screenHeight/2 + self.yOffset)
