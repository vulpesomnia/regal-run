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
screenWidth = 1920#1200
screenHeight = 1080#800

tileSize = screenWidth/15#rabbithole of resolution and camera size aligning starts here pls help
deathHeight = len(levels[0]) * tileSize

pWidth, pHeight = tileSize/2.56, tileSize/1.7

playerColor = (0, 0, 255)
white = (255, 255, 255)
groundColor = (255, 0, 0)
checkpointColor = (255, 255, 0)
endColor = (0, 255, 0)