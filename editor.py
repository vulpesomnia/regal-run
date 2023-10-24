import pygame, settings, math
from button import Button
from tile import Tile

colCount = 28
buttonSize = 64 #Cubic

class Editor:

    def __init__(self, height):
        self.selectedImage = 0
        self.selectedType = 0
        self.selectedLayer = 0#array of sprite groups? for loop in render function then or hashmap {layerid : spritegroup} for negative "index" support
        self.height = height
        self.buttons = []
        #self.rect = pygame.rect(0, settings.screenHeight-self.height, settings.screenWidth, self.height)
        for i in range(settings.tileSpriteCount):
            x = i * buttonSize - math.floor(i/colCount) * (colCount-1) * buttonSize
            y = settings.screenHeight-self.height + math.floor(1 + i/colCount) * buttonSize
            temp = settings.tileSprites[i]
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
                    self.selectedImage = index
                    break

    def createTile(self, level, x, y):
        x = settings.screenWidth - x * settings.tileSize
        y = settings.screenHeight - y * settings.tileSize
        for tile in level.tiles:
            if (tile.rect.x == x) and (tile.rect.y == y):
                Editor.removeTile(level, tile)
                break
        tile = Tile(x, y, settings.tileSize, 0, self.selectedImage+1)
        level.tiles.add(tile)

    def removeTile(level, tile):
        #level.tiles.remove(tile)
        tile.kill()
        del tile
