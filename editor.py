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
            button = Button(x, y, 1, temp)
            self.buttons.append(button)
        self.buttons.append(Button(settings.screenWidth-200, settings.screenHeight-175, 2))#TileID
        self.buttons.append(Button(settings.screenWidth-400, settings.screenHeight-175, 3))#Layer

    def draw(self, frame):
        pygame.draw.rect(frame, (0, 0, 255),(0, settings.screenHeight-self.height, settings.screenWidth, self.height))
        for button in self.buttons:
            button.draw(frame)

    def onClick(self, x, y, clickType):#return index of button
        for index, button in enumerate(self.buttons):
            if (x > button.x) and (x < button.x+button.width):
                if (y > button.y) and (y < button.y+button.height):
                    print("Clicked a button! Index: " + str(index) + " ID: " + str(button.id))
                    if button.id == 1:
                        self.selectedImage = index
                    elif button.id == 2:
                        if clickType == 1:
                            self.selectedType += 1
                        elif clickType == 3:
                            self.selectedType -= 1
                        button.changeText("TileID: " + str(self.selectedType) + " ")
                    else:
                        if clickType == 1:
                            self.selectedLayer += 1
                        elif clickType == 3:
                            self.selectedLayer -= 1
                        button.changeText("Layer: " + str(self.selectedLayer) + " ")
                    break

    def createTile(self, level, x, y):
        for layerID, layer in level.tiles.items():
            for tile in layer.sprites():
                if layerID == self.selectedLayer:
                    if (tile.rect.x == x) and (tile.rect.y == y):
                        self.removeTile(level, x, y)
                        break
        tile = Tile(x, y, settings.tileSize, self.selectedType, self.selectedImage+1, self.selectedLayer)
        if level.tiles.get(self.selectedLayer) is None:
            level.tiles[self.selectedLayer] = pygame.sprite.Group()
        level.tiles[self.selectedLayer].add(tile)
        level.tiles = dict(sorted(level.tiles.items()))

    def removeTile(self, level, x, y):
        for layerID, layer in level.tiles.items():
            for tile in layer.sprites():
                if layerID == self.selectedLayer:
                    if (tile.rect.x == x) and (tile.rect.y == y):
                        tile.kill()
                        del tile
