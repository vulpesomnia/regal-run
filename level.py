
from tile import Tile
from playerScript import Player
from camera import Camera
from settings import * 
import pygame

tileTypes = {"X" : 0, "C" : 1, "E" : 2}

class Level:

    def __init__(self, layout, screen):
        self.screen = screen
        self.layout = layout
        self.player = pygame.sprite.GroupSingle()
        self.reset = 0
        self.doRender = True



    def loadLevel(self):
        self.tiles = pygame.sprite.Group()
        for rowIndex, row in enumerate(self.layout):
            for colIndex, col in enumerate(row):
                x = colIndex * tileSize#Tilesize multiplication is so that the grid system works fine
                y = rowIndex * tileSize
                if col == "P":
                    playerSprite = Player(x + tileSize/2 - pWidth/2, y)
                    self.player.add(playerSprite)
                    self.camera = Camera(x, y, self.player)
                elif col != " ":
                    tile = Tile(x, y, tileSize, tileTypes.get(col))
                    self.tiles.add(tile)
    def resetLevel(self):
        player = self.player.sprite
        if player.checkpoint != None:
            player.rect.x = player.checkpoint[0]
            player.rect.y = player.checkpoint[1]
        else:
            self.reset = 1
                
    def tick(self, frame):
        self.player.update()
        self.horizontalMovementCollision()
        #self.render(frame)


    def render(self, frame):#rendering function NOTE: Make object resizing dependent on resolution here and not in the other files.
        frame.fill(white)
        self.camera.updatePosition()
        for tile in self.tiles.sprites():
            camOffsetX = tile.rect.x - self.camera.x
            camOffsetY = tile.rect.y - self.camera.y
            frame.blit(tile.image, (camOffsetX, camOffsetY))
        player = self.player.sprite

        camOffsetX = player.rect.x - self.camera.x - player.image.get_width() / 2 + 25
        camOffsetY = player.rect.y - self.camera.y - player.image.get_height() / 2 + 12
        frame.blit(player.image, (camOffsetX, camOffsetY))
        self.screen.blit(pygame.transform.scale(frame, (screenWidth, screenHeight)), (0, 0))
        self.doRender = True


    def horizontalMovementCollision(self):
        player = self.player.sprite
        player.rect.x += player.velocity.x * player.speed
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if tile.type == 0:
                    if player.velocity.x < 0:
                        player.rect.left = tile.rect.right
                    elif player.velocity.x > 0:
                        player.rect.right = tile.rect.left
                else:
                    self.generalCollision(tile)
        self.verticalMovementCollision()
    def verticalMovementCollision(self):
        player = self.player.sprite
        player.rect.y -= player.velocity.y
        onGround = False
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if tile.type == 0:
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
        if self.player.sprite.rect.y > deathHeight:
            self.resetLevel()

    def generalCollision(self, tile):
        if tile.type == 1:
            self.player.sprite.checkpoint = (tile.rect.x + tile.rect.width / 2 - self.player.sprite.rect.width / 2, tile.rect.y)
        elif tile.type == 2:
            self.reset = 2



        