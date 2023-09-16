from settings import screenHeight,screenWidth
class Camera:

    def __init__(self, x, y, player):
        self.x, self.y = x, y
        self.player = player

    def updatePosition(self):
        player = self.player.sprite
        newX = self.x * 0.75 + (player.rect.x - screenWidth / 2) * 0.25
        newY = self.y * 0.75 + (player.rect.y - screenHeight / 2) * 0.25
        self.x, self.y = newX, newY

