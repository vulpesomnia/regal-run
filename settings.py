#X = block, P = player, C = checkpoint E = end empty layer: "                    "
levels = [["                    ",
          "                    ",
          "                    ",
          "            E       ",
          "           XX       ",
          "      XX            ",
          "           XX  C    ",
          "               X    ",
          "        P   XX X    ",
          "       XXXXXXX X    "], 
          ["                    ",
          "         E          ",
          "        XXX         ",
          "     X   C   X      ",
          "        XXX         ",
          "    XX   P   XX     ",
          "        XXX         ",
          "                    ",
          "                    ",
          "                    "]]
CONST_screenWidth = 1920
CONST_screenHeight = 1080


#ratio = ~1.78(1.777)
screenWidth = 1920#1200
screenHeight = 1080#675

tileSize = 128
deathHeight = len(levels[0]) * tileSize

pWidth, pHeight = 55, 75
pAnimationFrames = ["walking1", "walking2", "walking3", "walking4", "flyingup", "flyingdown"]

playerColor = (0, 0, 255)
white = (255, 255, 255)
groundColor = (255, 0, 0)
checkpointColor = (255, 255, 0)
endColor = (0, 255, 0)