
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
        self.tiles = pygame.sprite.Group()
        levelFile = open("./Assets/Levels/" + self.name + ".level", "r")#Open file in reading mode
        tileData = []
        for rawData in levelFile:#loop through lines
            tileData = rawData.split("|")#split data {x, y, tileID, imageID}
            for index, data in enumerate(tileData):#cast as integers
                tileData[index] = int(data)
            x, y = Level.worldToScreenSpace(tileData[0], tileData[1])
            tile = Tile(x, y, settings.tileSize, tileData[2], tileData[3])
            self.tiles.add(tile)
        playerSprite = Player(settings.screenWidth + settings.tileSize/2 - settings.pWidth/2, settings.screenHeight)
        self.player.add(playerSprite)
        self.camera = Camera(settings.screenWidth, settings.screenHeight, self.player)

    def saveLevel(self):#NOTE: fun todo maybe create a squared saving system to save some space luls (sort col and rows in group -> check square regions of same type&image&layer -> save square regions with corners)
        levelFile = open("./Assets/Levels/" + self.name + ".level", "w")#Open file in writing mode (overrides text aka DO NOT CLOSE WHILE SAVING AAAAAAAAA[shouldnt be able to anyways since its fast])
        for tile in self.tiles:
            data = []
            data.append(str(int((tile.rect.x - settings.screenWidth) / settings.tileSize * -1)))# x coordinate i calculated this with basic algebra
            data.append(str(int((tile.rect.y - settings.screenHeight) / settings.tileSize * -1)))# y coordinate
            data.append(str(tile.tileID))# tileid
            data.append(str(tile.imageID))# imageid

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
        for tile in self.tiles.sprites():
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
            for tile in self.tiles.sprites():
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
            for tile in self.tiles.sprites():
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
            if player.onGround == True and onGround == False:
                player.jumpFrames = 3
            player.onGround = onGround
            if self.player.sprite.rect.y > settings.deathHeight:
                self.resetLevel()
        else: 
            if player.velocity.y != -player.gravity:
                player.rect.y -= player.velocity.y
            player.velocity.y = 0
            onGround = True

    def generalCollision(self, tile):
        if tile.tileID == 3:
            self.player.sprite.checkpoint = (tile.rect.x + tile.rect.width / 2 - self.player.sprite.rect.width / 2, tile.rect.y)
        elif tile.tileID == 4:
            self.reset = 2
        elif tile.tileID == 1:
            self.resetLevel()


    # - These are for tilesets not floating point world coordinates. - #
    def worldToScreenSpace(x, y):
        x = settings.screenWidth - x * settings.tileSize
        y = settings.screenHeight - y * settings.tileSize
        return (x, y)
    
    def screenToWorldSpace(level, x, y):#x + camera offset for world coordinates - screenwidth for 0, 0 to be at player spawn point divided by tilesize and floored to get x of a tile
        x = math.floor((x+level.camera.x - settings.screenWidth)/settings.tileSize) * -1
        y = math.floor((y+level.camera.y - settings.screenHeight)/settings.tileSize) * -1
        return (x, y)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#


        