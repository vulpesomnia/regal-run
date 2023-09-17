import pygame
from vector import Vector2
from settings import pHeight, pWidth, playerColor, tileSize

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((pWidth, pHeight))
        self.image.fill(playerColor)
        self.rect = self.image.get_rect(topleft = (x, y))

        self.velocity = Vector2(0, 0)
        self.onGround = False
        self.jumpStrength = tileSize*0.2#25
        self.speed = tileSize*0.12#15
        self.gravity = self.jumpStrength*0.08#2
        self.jumpFrames = 0
        self.checkpoint = None
    def jump(self):
        if self.onGround or self.jumpFrames > 0:
            self.velocity.y = self.jumpStrength

    def getInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity.x = -1
        elif keys[pygame.K_d]:
            self.velocity.x = 1
        else:
            self.velocity.x = 0
        if keys[pygame.K_SPACE]:
            self.jump()

    def update(self):
        self.getInput()
        self.velocity.y -= self.gravity #Gravity of player
        self.jumpFrames = max(0, self.jumpFrames - 1)