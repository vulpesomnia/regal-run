import settings
import pygame

class parallaxObject:
    def __init__(self, parallaxValue, image):
        self.startX = settings.screenWidth/2
        self.parallaxValue = parallaxValue
        self.image = image

    def update(self, frame, camera):
        cameraPos = camera.getPosition()
        cameraYOffset = -camera.y * 0.1 + settings.screenHeight * 0.05
       # travel = self.startX - cameraPos[0]

       # self.x = self.startX - travel * self.parallaxValue
       # red_box = pygame.Surface((50, 50))
        #red_box.fill((255, 0, 0))   
        travel = (cameraPos[0] + settings.screenWidth) - self.startX

        self.x = self.startX + travel * self.parallaxValue
        distance = abs((cameraPos[0] + settings.screenWidth) - self.x)
        #print("Anchor: " + str(self.startX) + " Normal x: " + str(self.x))
        #print(str(distance))
        #if self.parallaxValue == 0.2:
            #print(str(distance))
        if distance > settings.screenWidth:
           # print("RESET: " + str(distance))
            self.startX = cameraPos[0] + settings.screenWidth


        #The offsets are a bit weird but it works ig
        frame.blit(self.image, (self.x - settings.screenWidth - cameraPos[0], cameraYOffset))
        frame.blit(self.image, (self.x - cameraPos[0], cameraYOffset))
        frame.blit(self.image, (self.x - settings.screenWidth * 2 - cameraPos[0], cameraYOffset))
        #if self.parallaxValue == 0.2:
            #frame.blit(red_box, (self.startX - settings.screenWidth/2 - cameraPos[0], settings.screenHeight/2))
            #frame.blit(red_box, (self.startX - cameraPos[0], settings.screenHeight/2))
            #frame.blit(red_box, (self.startX + settings.screenWidth/2 - cameraPos[0], settings.screenHeight/2))


        #NOTE: origin + (travel * parallax)
        #camera coordinate in world coordinates: self.camera.getPosition()[0] + settings.screenWidth
        


