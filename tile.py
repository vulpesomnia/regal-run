'''
Tile class is contained in this file.

TileIDs:
 0 : Collision
 1 : Death
 2 : Checkpoint
 3 : Endpoint
 4 : No Collision
'''

import pygame, settings

class Tile(pygame.sprite.Sprite):
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
        if self.imageID == 72:
            self.collider = pygame.Rect((x, y + settings.tileSize * 0.69), (settings.tileSize, settings.tileSize * 0.31))
        else:
            self.collider = self.image.get_rect(topleft = (x, y))
