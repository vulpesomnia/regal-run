import pygame, settings, math
from button import Button

colCount = 28
buttonSize = 64 #Cubic

class Editor:

    def __init__(self, height):
        self.selectedButton = 0
        self.height = height
        self.buttons = []
        #self.rect = pygame.rect(0, settings.screenHeight-self.height, settings.screenWidth, self.height)
        for i in range(1, settings.tileSpriteCount+1):
            x = i * buttonSize - math.floor(i/colCount) * (colCount-1) * buttonSize
            y = settings.screenHeight-self.height + math.floor(1 + i/colCount) * buttonSize
            temp = pygame.image.load("./Assets/Sprites/Tiles/tile" + str(i) + ".png").convert_alpha()
            temp = pygame.transform.scale(temp, (temp.get_width() * 4, temp.get_height() * 4))
            button = Button(x, y, temp)
            self.buttons.append(button)

    def draw(self, frame):
        pygame.draw.rect(frame, (0, 0, 255),(0, settings.screenHeight-self.height, settings.screenWidth, self.height))
        for button in self.buttons:
            button.draw(frame)

    def onClick(self, x, y):#return index of button
        for index, button in enumerate(self.buttons):
            if (x > button.x-buttonSize) and (x < button.x+buttonSize):
                if (y > button.y-buttonSize) and (y < button.y+buttonSize):
                    print(str(index))
                    self.selectedButton = index
                    break
