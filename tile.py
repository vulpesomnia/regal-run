import pygame
import settings

#tileColors = (groundColor, checkpointColor, endColor)

class Tile(pygame.sprite.Sprite):#Tileids: 0 = collision tile, 1 = no collision, 2 = death, 3 = checkpoint, 4 = end point
    def __init__(self, x, y, size, tileID, imageID):
        super().__init__()
        self.imageID = imageID
        self.tileID = tileID
        self.image = pygame.Surface((size, size))
        if self.imageID != 0:
            self.image = settings.tileSprites[self.imageID-1]
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (settings.tileSize/self.image.get_width()), self.image.get_height() * (settings.tileSize/self.image.get_height())))
        else:
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = (x, y))