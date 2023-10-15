import pygame
from vector import Vector2
from settings import pWidth, pHeight, pAnimationFrames

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animationFrames = {}
        for frame in pAnimationFrames:
            temp = pygame.image.load("./Assets/Sprites/" + frame + ".png").convert_alpha()
            temp = pygame.transform.scale(temp, (temp.get_width() * 4, temp.get_height() * 4))
            self.animationFrames[frame] = temp
        self.image = self.animationFrames["walking1"]#pygame.image.load("./Assets/Sprites/walking1.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        self.rect = pygame.Rect((x, y), (pWidth, pHeight))#self.image.get_rect(topleft = (x, y))#box collider with size of image

        self.velocity = Vector2(0, 0)
        self.onGround = False
        self.jumpStrength = 25
        self.speed = 13
        self.gravity = 1.7
        self.jumpFrames = 0
        self.checkpoint = None

        self.isFlipped = False

        self.animationTicks = 0
    def jump(self):
        if self.onGround or self.jumpFrames > 0:
            self.velocity.y = self.jumpStrength

    def getInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.velocity.x != -1 and self.isFlipped == False:
                self.swapImage()
            self.velocity.x = -1
        elif keys[pygame.K_d]:
            if self.velocity.x != 1 and self.isFlipped == True:
                self.swapImage()
            self.velocity.x = 1
        else:
            self.velocity.x = 0
        if keys[pygame.K_SPACE]:
            self.jump()

    def swapImage(self):
        self.isFlipped = not self.isFlipped
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.getInput()
        self.velocity.y -= self.gravity #Gravity of player
        self.jumpFrames = max(0, self.jumpFrames - 1)
        self.animationTick()

    def updateImage(self, image):
        self.image = self.animationFrames[image]
        if self.isFlipped == True:
            self.image = pygame.transform.flip(self.image, True, False)

    def animationTick(self):
        if self.onGround == True:
            if self.velocity.x == 0:
                #idle animation
                self.updateImage("walking1")
            else:
                #walking animation
                if self.animationTicks <= 10:
                    self.animationTicks += 1
                    self.updateImage("walking1")
                elif self.animationTicks <= 20:
                    self.animationTicks += 1
                    self.updateImage("walking2")
                elif self.animationTicks <= 30:
                    self.animationTicks += 1
                    self.updateImage("walking3")
                elif self.animationTicks <= 40:
                    self.animationTicks += 1
                    self.updateImage("walking4")
                else:
                    self.animationTicks = 0
                
        else:
            if self.velocity.y > 0:
                #flying upwards animation
                self.updateImage("flyingup")
            else:
                #flying downwards animation
                self.updateImage("flyingdown")