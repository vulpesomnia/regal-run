
from tile import Tile
from playerScript import Player
from camera import Camera
import settings
from editor import Editor
import pygame, math

tileTypes = {"X" : 0, "C" : 1, "E" : 2}

class Level:

    def __init__(self, name, screen):
        self.name = name
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.reset = 0
        self.doRender = True
        self.editor = Editor(200)
        settings.setGamemode(0)

    def loadLevel(self):#TODO: create layer flag for different layers
        self.tiles = {0 : pygame.sprite.Group()}
        levelFile = open("./Assets/Levels/" + self.name + ".level", "r")#Open file in reading mode
        tileData = []
        for rawData in levelFile:#loop through lines
            tileData = rawData.split("|")#split data {x, y, tileID, imageID}
            for index, data in enumerate(tileData):#cast as integers
                tileData[index] = int(data)
            x, y = settings.worldToScreenSpace(tileData[0], tileData[1])
            tile = Tile(x, y, settings.tileSize, tileData[2], tileData[3], 0)
            layer = 0
            if len(tileData) >= 5:
                layer = tileData[4]
            if self.tiles.get(layer) is None:
                self.tiles[layer] = pygame.sprite.Group()
            self.tiles[layer].add(tile)
        self.tiles = dict(sorted(self.tiles.items()))

        playerSprite = Player(settings.screenWidth + settings.tileSize/2 - settings.pWidth/2, settings.screenHeight)
        self.player.add(playerSprite)
        self.camera = Camera(settings.screenWidth, settings.screenHeight, self.player)


    def loadLevel_squared(self):#TODO: create layer flag for different layers
        self.tiles = {0 : pygame.sprite.Group()}
        levelFile = open("./Assets/Levels/" + self.name + ".level", "r")#Open file in reading mode
        tileData = []
        for rawData in levelFile:#loop through lines
            if rawData == "\n":
                break
            tileData = rawData.split("|")#split data{x, y, tileID, imageID}

            for index, data in enumerate(tileData):#cast as integers
                if index != 0:
                    tileData[index] = int(data)

            boundaries = tileData[0].split(",")
            for index, data in enumerate(boundaries):#cast as integers
                boundaries[index] = int(data)
            for i in range(min(boundaries[1], boundaries[3]), max(boundaries[1], boundaries[3])+1):#y
                y = settings.worldToScreenSpace(0, i)[1]
                for j in range(boundaries[2], boundaries[0]+1):#x
                    x = settings.worldToScreenSpace(j, 0)[0]
                    tile = Tile(x, y, settings.tileSize, tileData[1], tileData[2], tileData[3])
                    layer = tileData[3]
                    if self.tiles.get(layer) is None:
                        self.tiles[layer] = pygame.sprite.Group()
                    self.tiles[layer].add(tile)

        self.tiles = dict(sorted(self.tiles.items()))

        playerSprite = Player(settings.screenWidth + settings.tileSize/2 - settings.pWidth/2, settings.screenHeight)
        self.player.add(playerSprite)
        self.camera = Camera(settings.screenWidth, settings.screenHeight, self.player)



    def saveLevel(self):#NOTE: fun todo maybe create a squared saving system to save some space luls (sort col and rows in group -> check square regions of same type&image&layer -> save square regions with corners)
        levelFile = open("./Assets/Levels/" + self.name + ".level", "w")#Open file in writing mode (overrides text aka DO NOT CLOSE WHILE SAVING AAAAAAAAA[shouldnt be able to anyways since its fast])
        for layerID, layer in self.tiles.items():
            for tile in layer.sprites():
                data = []
                data.append(str(int(tile.x)))# x coordinate
                data.append(str(int(tile.y)))# y coordinate
                data.append(str(tile.tileID))# tileid
                data.append(str(tile.imageID))# imageid
                data.append(str(tile.layer))# layer
                levelFile.write("|".join(data) + "\n")
        levelFile.close()
        print("[LEVEL SAVE] " + self.name + ".level has been successfully saved!")

    def saveLevel_squared(self):

        sortedTiles = {}#{Layer(INT) : {y-coordinate(INT) : [x-coordinates(INT)]}}, basically sorted as such: depth, col, row
        for layerID, layer in self.tiles.items():# (Sort tiles from highest y and highest x to lowest y and lowest x)
            if sortedTiles.get(layerID) == None:
                sortedTiles[layerID] = {}
            for tile in layer.sprites():
                if sortedTiles[layerID].get(tile.y) == None:
                    sortedTiles[layerID][tile.y] = [tile]
                else:
                    for index, sortedTile in enumerate(sortedTiles[layerID][tile.y]):
                        if tile.x > sortedTile.x:
                            sortedTiles[layerID][tile.y].insert(index, tile)
                            break
                        elif index == len(sortedTiles[layerID][tile.y])-1:
                            sortedTiles[layerID][tile.y].append(tile)
                            break

        keys = sortedTiles.keys()
        
        for key in keys:
            sortedTiles[key] = dict(sorted(sortedTiles[key].items(), reverse=True))

        squaredChunks = []#[(x,y), (x,y), tileid, imageid, layerid]


        for layer in sortedTiles.keys():
            while settings.dictLength(sortedTiles[layer]) != 0:#{x,y,x,y}|TileID|ImageID|LayerID
                tempSquare = [(0, 0), (0, 0), 0, 0, 0]
                tilesToRemove = []
                currentX = 0
                endX = 0
                endY = 0
                count = 0
                for yKey, tiles in sortedTiles[layer].items():#loop through y levels
                    for index, tile in enumerate(tiles):
                        count += 1
                        if count == 1:#Get first tile for chunk
                            tempSquare[0] = (tile.x, tile.y)
                            tempSquare[2] = tile.tileID
                            tempSquare[3] = tile.imageID
                            tempSquare[4] = layer
                            currentX = tile.x
                            endY = yKey
                            endX = tile.x
                        elif (tile.x == currentX-1) and ((tile.tileID == tempSquare[2]) and (tile.imageID == tempSquare[3])):#check if tile data matches chunk's data
                                currentX = tile.x
                                endY = yKey
                        else:#if tile doesnt match chunk data
                            if endY == yKey:#If we have atleast 1 tile in this y level then we can put the endX to the currentX
                                endX = currentX
                            break
                        endX = currentX#this should work maybe?
                    currentX = tempSquare[0][0]+1#Put currentx to x of starting tile, +1 is for the if statement to work
                    if endY != yKey:
                        break



                tempSquare[1] = (endX, endY)

                for yKey, tiles in sortedTiles[layer].items():#add tiles in chunk to be removed
                    for tile in tiles:
                        if (tile.x <= tempSquare[0][0]) and (tile.y <= tempSquare[0][1]):#if tile x is less than
                            if (tile.x >= tempSquare[1][0]) and (tile.y >= tempSquare[1][1]):
                                if (tile.layer == tempSquare[4]):
                                    tilesToRemove.append(tile)

                squaredChunks.append(tempSquare)#Add square to total squares

                yKeys = []
                for yKey in sortedTiles[layer].keys():
                    yKeys.append(yKey)
                for tileToRemove in tilesToRemove:
                    for yKey in yKeys:#remove looped tiles from sortedtiles list
                        if tileToRemove in sortedTiles[layer][yKey]:
                            sortedTiles[layer][yKey].remove(tileToRemove)
                    
                for yKey in yKeys:
                    if len(sortedTiles[layer][yKey]) == 0:
                        del sortedTiles[layer][yKey]
        levelFile = open("./Assets/Levels/" + self.name + ".level", "w")
        for chunk in squaredChunks:#{x,y,x,y}|TileID|ImageID|LayerID
            boundaries = []
            boundaries.append(str(chunk[0][0]))
            boundaries.append(str(chunk[0][1]))
            boundaries.append(str(chunk[1][0]))
            boundaries.append(str(chunk[1][1]))
            boundaries = ",".join(boundaries)

            data = []
            data.append(boundaries)
            data.append(str(chunk[2]))# tileid
            data.append(str(chunk[3]))# imageid
            data.append(str(chunk[4]))# layer
            levelFile.write("|".join(data) + "\n")
        levelFile.close()
        print("[LEVEL SAVE] " + self.name + ".level has been successfully saved!")
    

            

    
    def resetLevel(self):
        player = self.player.sprite
        if player.checkpoint != None:
            player.rect.x = player.checkpoint[0]
            player.rect.y = player.checkpoint[1]
        else:
            self.reset = 1
                
    def tick(self):
        self.player.update()
        self.horizontalMovementCollision()

    def toggleEditor(self):
        player = self.player.sprite
        if settings.gamemode == 0:
            settings.setGamemode(1)
            player.speed = 18
        else:
            settings.setGamemode(0)
            player.speed = 13

    def render(self, frame):
        frame.fill(settings.backgroundColor)
        self.camera.updatePosition()
        for layerID, layer in self.tiles.items():
            for tile in layer.sprites():
                camOffsetX = tile.rect.x - self.camera.x
                camOffsetY = tile.rect.y - self.camera.y
                frame.blit(tile.image, (camOffsetX, camOffsetY))
        player = self.player.sprite

        camOffsetX = player.rect.x - self.camera.x - player.image.get_width() / 2 + 25
        camOffsetY = player.rect.y - self.camera.y - player.image.get_height() / 2 + 12
        frame.blit(player.image, (camOffsetX-settings.pWidth/4, camOffsetY))
        if settings.gamemode == 1:
            self.editor.draw(frame)
        self.screen.blit(pygame.transform.scale(frame, (settings.screenWidth, settings.screenHeight)), (0, 0))
        self.doRender = True


    def horizontalMovementCollision(self):
        player = self.player.sprite
        player.rect.x += player.velocity.x * player.speed
        if settings.gamemode == 0:
            for layerID, layer in self.tiles.items():
                for tile in layer.sprites():
                    if tile.rect.colliderect(player.rect):
                        if tile.tileID == 0:
                            if player.velocity.x < 0:
                                player.rect.left = tile.rect.right
                            elif player.velocity.x > 0:
                                player.rect.right = tile.rect.left
                        else:
                            self.generalCollision(tile)
        self.verticalMovementCollision()
    def verticalMovementCollision(self):
        player = self.player.sprite
        if settings.gamemode == 0:
            player.rect.y -= player.velocity.y
            onGround = False
            for layerID, layer in self.tiles.items():
                for tile in layer.sprites():
                    if tile.rect.colliderect(player.rect):
                        if tile.tileID == 0:
                            if player.velocity.y < 0:
                                player.rect.bottom = tile.rect.top
                                player.velocity.y = 0
                                onGround = True
                            elif player.velocity.y > 0:
                                player.rect.top = tile.rect.bottom
                                player.velocity.y = 0
                        else:
                            self.generalCollision(tile)
            if onGround == True:
                player.jumpFrames = 4
            if self.player.sprite.rect.y > settings.deathHeight:
                self.resetLevel()
        else: 
            if player.velocity.y != -player.gravity:
                player.rect.y -= player.velocity.y
            player.velocity.y = 0
            onGround = True

    def generalCollision(self, tile):
        if tile.tileID == 2:
            self.player.sprite.checkpoint = (tile.rect.x + tile.rect.width / 2 - self.player.sprite.rect.width / 2, tile.rect.y)
        elif tile.tileID == 3:
            self.reset = 2
        elif tile.tileID == 1:
            self.resetLevel()




        