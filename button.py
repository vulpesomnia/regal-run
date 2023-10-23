import pygame

class Button:

    def __init__(self, x, y, image):
        self.x, self.y = x, y
        self.image = image

    def draw(self, frame):
         frame.blit(self.image, (self.x, self.y))
         
