import pygame
from vector import Vector2
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animationFrames = {}
        for frame in settings.pAnimationFrames:
            temp = pygame.image.load("./Assets/Sprites/" + frame + ".png").convert_alpha()
            temp = pygame.transform.scale(temp, (temp.get_width() * 4.25, temp.get_height() * 4.25))
            self.animationFrames[frame] = temp
        self.image = self.animationFrames["walking1"]
        self.rect = pygame.Rect((x, y), (settings.pWidth, settings.pHeight))

        self.velocity = Vector2(0, 0)
        #self.onGround = False
        self.jumpStrength = 23
        self.speed = 13
        self.gravity = 1.7
        self.jumpFrames = 0
        self.checkpoint = None
        self.jumpSound = pygame.mixer.Sound("./Assets/Sounds/jump.wav")

        self.isFlipped = False

        self.animationTicks = 0
    def jump(self, direction):
        if self.jumpFrames > 0:
            self.velocity.y = self.jumpStrength * direction
            if (settings.gamemode == 0):
                    self.jumpFrames = 0
                    pygame.mixer.Sound.play(self.jumpSound)

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
            self.jump(1)
        elif keys[pygame.K_LSHIFT] and settings.gamemode == 1:
            self.jump(-1)

    def swapImage(self):
        self.isFlipped = not self.isFlipped
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.getInput()
        self.velocity.y -= self.gravity #Gravity of player
        if settings.gamemode == 1:
            self.jumpFrames = 4
        else:
            self.jumpFrames = max(0, self.jumpFrames - 1)
        self.animationTick()

    def updateImage(self, image):
        self.image = self.animationFrames[image]
        if self.isFlipped == True:
            self.image = pygame.transform.flip(self.image, True, False)

    def animationTick(self):
        if self.jumpFrames > 0:
            if self.velocity.x == 0:
                #idle animation
                self.updateImage("walking1")
            else:
                #walking animation
                if self.animationTicks <= 7:
                    self.animationTicks += 1
                    self.updateImage("walking1")
                elif self.animationTicks <= 15:
                    self.animationTicks += 1
                    self.updateImage("walking2")
                elif self.animationTicks <= 22:
                    self.animationTicks += 1
                    self.updateImage("walking3")
                elif self.animationTicks <= 30:
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