import pygame
from settings import groundColor, checkpointColor, endColor

tileColors = (groundColor, checkpointColor, endColor)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, type):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(tileColors[type])
        self.rect = self.image.get_rect(topleft = (x, y))
        self.type = type