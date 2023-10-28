import pygame, settings


class Button:
    def __init__(self, x, y, id, image = None):
        self.x, self.y = x, y
        self.id = id
        if self.id == 1:#ImageID Button
            self.image = image
        elif self.id == 2:#TileID Button
            self.image = settings.font.render("TileID: 0 ", False, (0, 0, 0), (255, 255, 255))
        else:#Layer Button
            self.image = settings.font.render("Layer: 0 ", False, (0, 0, 0), (255, 255, 255))
        self.width, self.height = self.image.get_width(), self.image.get_height()

    def draw(self, frame):
        frame.blit(self.image, (self.x, self.y))

    def changeText(self, text):
        self.image = settings.font.render(text, False, (0, 0, 0), (255, 255, 255))
         
