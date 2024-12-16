# © 2023-2024 Tommy Kroon <tommy.m.kroon@gmail.com>

'''
Contains most of the logic for the game.
Handles the level saving and loading, player collision, rendering, and level logic.

Main game loop is in main.py.
'''

from tile import Tile
from playerScript import Player
from camera import Camera
from editor import Editor
import pygame, parallax, settings, math

class Level:

    def __init__(self, name, screen):
        self.name = name
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.reset = False
        self.editor = Editor(200)
        self.blackFade = pygame.Surface((settings.screenWidth, settings.screenHeight), pygame.SRCALPHA)
        self.blackFade.fill((0, 0, 0))
        self.blackFade.set_alpha(255)

        settings.currentLevel = self

        self.alphaIncrement = 0

        settings.setGamemode(0)

        self.parallaxObjects = []

        parallaxImages = {"sky": 0.9, "mountains": 0.8, "trees": 0.4}
        for name, parallaxValue in parallaxImages.items():
            temp = pygame.image.load("./Assets/Sprites/parallax-" + name + ".png").convert_alpha()
            temp = pygame.transform.scale(temp, (settings.screenWidth * 1.25, settings.screenHeight * 1.25))
            self.parallaxObjects.append(parallax.parallaxObject(parallaxValue, temp))

        self.loadLevel_squared()
        self.fadeOut()

    def loadLevel_squared(self):#TODO: create layer flag for different layers
        self.tiles = {0 : pygame.sprite.Group()}
        levelFile = open("./Assets/Levels/" + self.name, "r")#Open file in reading mode
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

        player = self.player.sprite#made camera's 0-point at player
        player.checkpoint = (player.rect.x, player.rect.y + settings.checkpointOffset)
        self.camera = Camera(player.rect.x, player.rect.y, self.player)

    def saveLevel_squared(self):

        sortedTiles = {}#{Layer(INT) : {y-coordinate(INT) : [x-coordinates(INT)]}}, basically sorted as such: depth, col, row

        # (Sort tiles from highest y and highest x to lowest y and lowest x)
        for layerID, layer in self.tiles.items():
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

        #Goes through all tiles in the specified layer and organizes them into chunks.
        for layer in sortedTiles.keys():#For each layer
            while settings.dictLength(sortedTiles[layer]) != 0:#While there are still tiles to be organized.
                tempSquare = [(0, 0), (0, 0), 0, 0, 0]
                tilesToRemove = []
                currentX = 0
                endX = 0
                endY = 0
                count = 0
                first_yKey = 0
                for yKey, tiles in sortedTiles[layer].items():#Goes through each y-level
                    #print(str(yKey))
                    #print([str(tile.y) for tile in tiles])
                    if count == 0:
                        first_yKey = yKey
                    else:
                        if (abs(yKey-endY) != 1):
                            break
                    for index, tile in enumerate(tiles):#Goes through all tiles.
                        count += 1
                        if count == 1:#Get first tile for chunk
                            tempSquare[0] = (tile.x, tile.y)
                            tempSquare[2] = tile.tileID
                            tempSquare[3] = tile.imageID
                            tempSquare[4] = layer
                            currentX = tile.x
                            endY = yKey
                            endX = tile.x
                        elif yKey == first_yKey:#Figure out max x with first y-layer
                            if (tile.x == endX-1) and ((tile.tileID == tempSquare[2]) and (tile.imageID == tempSquare[3])):#check if tile data matches chunk's data
                                endX = tile.x
                                endY = yKey
                        elif ((tile.x == currentX-1) and (tile.x >= endX)) and ((tile.tileID == tempSquare[2]) and (tile.imageID == tempSquare[3])):#check if tile data matches chunk's data
                            currentX = tile.x
                            endY = yKey

                    if (currentX != endX) and ((endY == yKey) and (first_yKey != yKey)):#If we werent able to fulfill the x requirement go back to last layer.
                        endY += 1
                        break
                    currentX = tempSquare[0][0]+1#Put currentx to x of starting tile (+1 is so that the check which goes 1 forward(-1 is forward for some reason) is checking under start pos)




                tempSquare[1] = (endX, endY)

                #Remove all tiles that have been used to make this chunk from the list that we are looping through. (Prevents conflicts)
                for yKey, tiles in sortedTiles[layer].items():
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



        levelFile = open("./Assets/Levels/" + self.name, "w")
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
    

            

    
    def playerDeath(self):

        player = self.player.sprite
        player.isDead = 1
        pygame.mixer.Sound.play(player.explosionSound)
        player.animationTicks = 0
        player.velocity.x, player.velocity.y = 0, -10
                
    def tick(self, frameTime):
        self.player.update()
        if self.player.sprite.isDead == 0:
            self.verticalMovementCollision(frameTime)
        self.fadeTick()

    def toggleEditor(self):
        player = self.player.sprite
        if settings.gamemode == 0:
            settings.setGamemode(1)
            pygame.mouse.set_visible(True)
            player.speed += 5
        else:
            settings.setGamemode(0)
            pygame.mouse.set_visible(False)
            player.speed -= 5

    def render(self, frame):#Frametime is an extrapolation factor for rendering
        frame.fill(settings.backgroundColor)
        self.camera.updatePosition()
        player = self.player.sprite
        
        for object in self.parallaxObjects:
            object.update(frame, self.camera)


        renderPlayer = True
        for layerID, layer in self.tiles.items():
            if (layerID == 1) and (settings.gamemode == 0):
                player.render(frame, self.camera)
                renderPlayer = False
            for tile in layer.sprites():
                camOffsetX = tile.rect.x - self.camera.x
                camOffsetY = tile.rect.y - self.camera.y
                tileImage = tile.image
                if abs(tile.rect.x + settings.tileSize/2 - self.camera.getPosition()[0]) > (settings.screenWidth/2 - settings.tileSize/2):#rendering culling
                    if (tile.layer > 0) and (tile.tileID == 5):
                        if player.isHidden == True:
                            distance = math.dist((tile.rect.x, tile.rect.y), (player.rect.x, player.rect.y))
                            if distance < 256:
                                tileImage.set_alpha(distance)
                            else:
                                tileImage.set_alpha(255)
                        elif settings.gamemode == 1:
                            tileImage.set_alpha(128)
                        else:
                            tileImage.set_alpha(255)

                    frame.blit(tileImage, (camOffsetX, camOffsetY))
        if renderPlayer == True:
            player.render(frame, self.camera)

        
        if settings.gamemode == 1:#Draw editor if in editor mode
            self.editor.draw(frame)
            
        frame.blit(self.blackFade, (0, 0))

        self.screen.blit(pygame.transform.scale(frame, (settings.screenWidth, settings.screenHeight)), (0, 0))


    def horizontalMovementCollision(self, frameTime):
        player = self.player.sprite
        player.isHidden = False
        player.rect.x += player.velocity.x * player.speed * frameTime
        if settings.gamemode == 0:
            for layer in self.tiles.values():
                for tile in layer.sprites():
                    if tile.collider.colliderect(player.rect):
                        if tile.tileID == 0:
                            if player.velocity.x < 0:
                                player.rect.left = tile.collider.right
                            elif player.velocity.x > 0:
                                player.rect.right = tile.collider.left
                        else:
                            self.generalCollision(tile)
    def verticalMovementCollision(self, frameTime):
        player = self.player.sprite
        if settings.gamemode == 0:
            player.rect.y -= player.velocity.y * frameTime
            onGround = False
            for layer in self.tiles.values():
                for tile in layer.sprites():
                    if abs(tile.rect.x - player.rect.x) < settings.tileSize * 2:#collision check culling
                        if tile.collider.colliderect(player.rect):
                            if tile.tileID == 0:
                                if player.velocity.y < 0:
                                    player.rect.bottom = tile.collider.top
                                    player.velocity.y = 0
                                    onGround = True
                                elif player.velocity.y > 0:
                                    player.rect.top = tile.collider.bottom
                                    player.velocity.y = 0
                            else:
                                self.generalCollision(tile)
            if onGround == True:
                player.jumpFrames = player.jumpFrameMax
            if player.rect.y > settings.deathHeight:
                self.playerDeath()
        else: 
            if player.velocity.y != -player.gravity:
                player.rect.y -= player.velocity.y
            player.velocity.y = 0
            onGround = True
        self.horizontalMovementCollision(frameTime)

    def generalCollision(self, tile):
        player = self.player.sprite
        if tile.tileID == 2:#Set checkpoint
            player.checkpoint = (tile.rect.x + tile.rect.width / 2 - player.rect.width / 2, tile.rect.y + settings.checkpointOffset)
        elif tile.tileID == 3 and self.reset == False:#next level
            self.fadeIn()
            self.reset = True
            pygame.mixer.Sound.play(player.explosionSound)
        elif tile.tileID == 1:#Death
            self.playerDeath()
        elif (tile.tileID == 5) and (tile.layer > 0):#Behind bush, opacity increase
            player.isHidden = True

    
    def fadeIn(self):
        self.alphaIncrement = 15
    
    def fadeOut(self):
        self.alphaIncrement = -15

    def fadeTick(self):
        player = self.player.sprite
        if self.alphaIncrement != 0:
            alpha = self.blackFade.get_alpha()
            alpha += self.alphaIncrement
            self.blackFade.set_alpha(alpha)
            if (alpha >= 255) or (alpha <= 0):
                self.alphaIncrement = 0
                if player.isDead == 2:
                    player.rect.x = player.checkpoint[0]
                    player.rect.y = player.checkpoint[1]
                    self.camera.x, self.camera.y = player.rect.x - settings.CONST_screenWidth/2, player.rect.y - settings.CONST_screenHeight/2 - 15
                    player.isDead = 3
                    self.fadeOut()
                elif player.isDead == 3:
                    player.isDead = 0




    
    
        




        
