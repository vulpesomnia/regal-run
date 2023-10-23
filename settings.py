#X = block, P = player, C = checkpoint E = end empty layer: "                    "
CONST_screenWidth = 1920
CONST_screenHeight = 1080


#ratio = ~1.78(1.777)
screenWidth = 1920#1200
screenHeight = 1080#675

tileSize = 128
deathHeight = 16 * tileSize

pWidth, pHeight = 55, 75
pAnimationFrames = ["walking1", "walking2", "walking3", "walking4", "flyingup", "flyingdown"]
tileSpriteCount = 51

playerColor = (0, 0, 255)
white = (255, 255, 255)
groundColor = (255, 0, 0)
checkpointColor = (255, 255, 0)
endColor = (0, 255, 0)

gamemode = 0

def setGamemode(int):
    global gamemode
    gamemode = int

#x(int), y(int), type(int), sprite(string)