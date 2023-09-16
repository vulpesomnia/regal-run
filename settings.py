#X = block, P = player, C = checkpoint empty layer: "                    "
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
screenWidth = 1200
screenHeight = 800

tileSize = 128
deathHeight = len(levels[0]) * tileSize

pWidth, pHeight = 50, 75

playerColor = (0, 0, 255)
white = (255, 255, 255)
groundColor = (255, 0, 0)
checkpointColor = (255, 255, 0)
endColor = (0, 255, 0)