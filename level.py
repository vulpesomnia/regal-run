
from tile import Tile
from playerScript import Player
from camera import Camera
from settings import * 
import pygame

class Level:

    def __init__(self, layout, screen):
        self.screen = screen
        self.layout = layout
        self.player = pygame.sprite.GroupSingle()
        self.reset = False



    def loadLevel(self):
        self.tiles = pygame.sprite.Group()
        for rowIndex, row in enumerate(self.layout):
            for colIndex, col in enumerate(row):
                x = colIndex * tileSize#Tilesize multiplication is so that the grid system works fine
                y = rowIndex * tileSize
                if col == "X":
                    tile = Tile(x, y, tileSize, 0)
                    self.tiles.add(tile)
                elif col == "C":
                    tile = Tile(x, y, tileSize, 1)
                    self.tiles.add(tile)
                elif col == "P":
                    playerSprite = Player(x, y)
                    self.player.add(playerSprite)
                    self.camera = Camera(x, y, self.player)
    def resetLevel(self):
        player = self.player.sprite
        if player.checkpoint != None:
            player.rect.x = player.checkpoint[0]
            player.rect.y = player.checkpoint[1]
        else:
            self.reset = True
                
    def tick(self):
        self.player.update()
        self.horizontalMovementCollision()
        self.render()


    def render(self):
        self.camera.updatePosition()
        for tile in self.tiles.sprites():
            camOffsetX = tile.rect.x - self.camera.x
            camOffsetY = tile.rect.y - self.camera.y
            self.screen.blit(tile.image, (camOffsetX, camOffsetY))
        player = self.player.sprite

        camOffsetX = player.rect.x - self.camera.x
        camOffsetY = player.rect.y - self.camera.y
        self.screen.blit(player.image, (camOffsetX, camOffsetY))

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
            player.jumpFrames = 4
        player.onGround = onGround
        if self.player.sprite.rect.y > deathHeight:
            self.resetLevel()

    def generalCollision(self, tile):
        if tile.type == 1:
            self.player.sprite.checkpoint = (tile.rect.x, tile.rect.y)

        