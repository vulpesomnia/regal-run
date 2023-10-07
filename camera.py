from settings import CONST_screenHeight,CONST_screenWidth
class Camera:

    def __init__(self, x, y, player):
        self.x, self.y = x, y
        self.player = player

    def updatePosition(self):#Updates position of camera to player using linear interpolation aka just damping, how does it work? I forgot.
        player = self.player.sprite
        newX = self.x * 0.75 + (player.rect.x - CONST_screenWidth / 2) * 0.25
        newY = self.y * 0.75 + (player.rect.y - CONST_screenHeight / 2) * 0.25
        self.x, self.y = newX, newY

