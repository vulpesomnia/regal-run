'''
Parallax system that uses 3 reoccuring images stacked next to eachother.
If you go to the middle of any of the 2 side images it will readjust it
so that the middle image is at your location. This creates a smooth parallax effect.
'''

import settings

class parallaxObject:
    def __init__(self, parallaxValue, image):
        self.startX = settings.screenWidth/2
        self.parallaxValue = parallaxValue
        self.image = image

    def update(self, frame, camera):
        cameraPos = camera.getPosition()
        cameraYOffset = -cameraPos[1] * 0.1 - 150
        parallaxOffset = self.image.get_width()


        travel = (cameraPos[0] + settings.screenWidth) - self.startX

        self.x = self.startX + travel * self.parallaxValue
        distance = abs((cameraPos[0] + settings.screenWidth) - self.x)
        if distance > parallaxOffset:
            self.startX = cameraPos[0] + settings.screenWidth

        #For some reason the 2nd blit's position is to the left of the player and not at the player, might be cause were not using camera's world coordinates.
        frame.blit(self.image, (self.x - parallaxOffset - cameraPos[0], cameraYOffset))
        frame.blit(self.image, (self.x - cameraPos[0], cameraYOffset))
        frame.blit(self.image, (self.x - parallaxOffset * 2 - cameraPos[0], cameraYOffset))

        #NOTE: Camera coordinate in world coordinates: (self.camera.getPosition()[0] + settings.screenWidth) same thing with y just opposite axis
        


