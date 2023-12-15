'''
This file contains the code for the player.

Movement, input, animations and rendering are handled here.
Collision is in level.py.
'''

import pygame, settings
from vector import Vector2


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

        self.isHidden = False
        self.isDead = 0

        self.velocity = Vector2(0, 0)
        


        self.jumpStrength = 25
        self.speed = 13
        self.gravity = 1.7
        self.jumpFrames = 0
        self.jumpFrameMax = 8
        self.checkpoint = None
        self.jumpSound = pygame.mixer.Sound("./Assets/Sounds/jump.wav")
        self.explosionSound = pygame.mixer.Sound("./Assets/Sounds/explosion.wav")

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
            #self.velocity.x = 0
            if self.jumpFrames > 0:
                self.velocity.x = 0
            else:
                if self.isFlipped == True:
                    if self.velocity.x > -0.1:
                        self.velocity.x = 0
                else:
                    if self.velocity.x < 0.1:
                        self.velocity.x = 0
                self.velocity.x *= 0.8
        if keys[pygame.K_SPACE]:
            self.jump(1)
        elif keys[pygame.K_LSHIFT] and settings.gamemode == 1:
            self.jump(-1)

    def swapImage(self):
        self.isFlipped = not self.isFlipped
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.isDead == 0:
            self.getInput()
            self.velocity.y -= self.gravity #Gravity of player
            if settings.gamemode == 1:
                self.jumpFrames = self.jumpFrameMax
            else:
                self.jumpFrames = max(0, self.jumpFrames - 1)
        self.animationTick()

    def updateImage(self, image):
        self.image = self.animationFrames[image]
        if self.isFlipped == True:
            self.image = pygame.transform.flip(self.image, True, False)

    def render(self, frame, camera):
        camOffsetX = self.rect.x - camera.x - self.image.get_width() / 2 + 25
        camOffsetY = self.rect.y - camera.y - self.image.get_height() / 2 + 12
        frame.blit(self.image, (camOffsetX-settings.pWidth/4, camOffsetY))
        

    def animationTick(self):
        if self.isDead == 0:
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

        elif self.isDead == 1:
            if self.animationTicks >= 16:
                self.isDead = 2
                settings.currentLevel.fadeIn()
            else:
                self.updateImage("death" + str(min(self.animationTicks+1, 12)))
            self.animationTicks += 1