'''
Contains editor class.

Contains button input, editor rendering, editor instantiation and tile modification.
'''

import pygame, settings, math
from button import Button
from tile import Tile

colCount = 28
#Corresponds to width and height of button.
buttonSize = 48

class Editor:

    def __init__(self, height):
        self.selectionCoordinates = None

        self.selectedImage = 0
        self.selectedType = 0
        self.selectedLayer = 0

        self.height = height
        self.buttons = []

        for i in range(settings.tileSpriteCount):
            x = i * buttonSize - math.floor(i/colCount) * (colCount) * buttonSize + 15
            y = settings.screenHeight-self.height + math.floor(1 + i/colCount) * buttonSize - 10
            temp = settings.tileSprites[i]
            temp = pygame.transform.scale(temp, (temp.get_width() * 3, temp.get_height() * 3))
            button = Button(x, y, 1, temp)
            self.buttons.append(button)
        self.buttons.append(Button(settings.screenWidth-200, settings.screenHeight-190, 2))#TileID
        self.buttons.append(Button(settings.screenWidth-400, settings.screenHeight-190, 3))#Layer

    def draw(self, frame):
        pygame.draw.rect(frame, (0, 0, 0),(0, settings.screenHeight-self.height, settings.screenWidth, self.height))
        for button in self.buttons:
            button.draw(frame)

    def onClick(self, x, y, clickType):#return index of button
        for index, button in enumerate(self.buttons):
            if (x > button.x) and (x < button.x+button.width):
                if (y > button.y) and (y < button.y+button.height):
                    #print("Clicked a button! Index: " + str(index) + " ID: " + str(button.id))
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

    def createTile(self, level, start, end):
        for x in range(min(start[0], end[0]), max(start[0], end[0])+1):#x
            for y in range(min(start[1], end[1]), max(start[1], end[1])+1):#y
                x2, y2 = settings.worldToScreenSpace(x, y)
                for layerID, layer in level.tiles.items():
                    for tile in layer.sprites():
                        if layerID == self.selectedLayer:
                            if (tile.rect.x == x2) and (tile.rect.y == y2):
                                self.removeTile(level, (x, y), (x, y))
                                break
                tile = Tile(x2, y2, settings.tileSize, self.selectedType, self.selectedImage+1, self.selectedLayer)
                if level.tiles.get(self.selectedLayer) is None:
                    level.tiles[self.selectedLayer] = pygame.sprite.Group()
                level.tiles[self.selectedLayer].add(tile)
                level.tiles = dict(sorted(level.tiles.items()))

    def removeTile(self, level, start, end):
        for x in range(min(start[0], end[0]), max(start[0], end[0])+1):#x
            for y in range(min(start[1], end[1]), max(start[1], end[1])+1):#y
                x2, y2 = settings.worldToScreenSpace(x, y)
                for layerID, layer in level.tiles.items():
                    for tile in layer.sprites():
                        if layerID == self.selectedLayer:
                            if (tile.rect.x == x2) and (tile.rect.y == y2):
                               # print("LayerID: " + str(layerID) + " selectedLayer: " + str(self.selectedLayer))
                                tile.kill()
                                del tile
