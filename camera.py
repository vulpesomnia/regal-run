'''
This file contains the camera system for the game.

The camera follows the player each frame by interpolating to the player's location.
Then all rendered objects are offset by the camera's location. This creates the illusion that the screen
is following the player. In conclusion all objects are just dragged to the screen with the player in the middle.
'''

import settings

class Camera:

    def __init__(self, x, y, player):
        self.x, self.y = x, y
        self.player = player

    def updatePosition(self):#Updates position of camera to player using linear interpolation aka just damping, how does it work? I forgot.
        player = self.player.sprite
        newX = self.x * 0.75 + (player.rect.x - settings.CONST_screenWidth / 2) * 0.25
        
        #TODO: make sure this value is good! (the constant at the end of the equation, used for offsetting camera. lots of unused y-axis space)
        newY = self.y * 0.75 + (player.rect.y - settings.CONST_screenHeight / 2) * 0.25 - 12
        self.x, self.y = newX, newY

    def getPosition(self):
        return (self.x - settings.CONST_screenWidth/2, self.y - settings.CONST_screenHeight/2)