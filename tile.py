import pygame
import settings

#tileColors = (groundColor, checkpointColor, endColor)

class Tile(pygame.sprite.Sprite):#Tileids: 0 = collision tile, 1 = no collision, 2 = death, 3 = checkpoint, 4 = end point
    def __init__(self, x, y, size, tileID, imageID, layer):
        super().__init__()
        self.x = int((x - settings.screenWidth) / settings.tileSize * -1)
        self.y = int((y - settings.screenHeight) / settings.tileSize * -1)
        self.imageID = imageID
        self.tileID = tileID
        self.layer = layer
        self.image = pygame.Surface((size, size))
        if self.imageID != 0:
            self.image = settings.tileSprites[self.imageID-1]
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (settings.tileSize/self.image.get_width()), self.image.get_height() * (settings.tileSize/self.image.get_height())))
        else:
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = (x, y))