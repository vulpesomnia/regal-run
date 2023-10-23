import pygame
from settings import groundColor, checkpointColor, endColor

tileColors = (groundColor, checkpointColor, endColor)

class Tile(pygame.sprite.Sprite):#Tileids: 0 = no collision, 1 = collision block, 2 = death, 3 = checkpoint, 4 = end point
    def __init__(self, x, y, size, tileID, imageID):
        super().__init__()
        self.imageID = imageID
        self.tileID = tileID
        self.image = pygame.Surface((size, size))
        self.image.fill(tileColors[0])
        self.rect = self.image.get_rect(topleft = (x, y))