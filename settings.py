layout = ["                    ",
          " XP                 ",
          " XXX          C     ",
          "     XX       X     ",
          "       X          X ",
          "        X    XXX    ",
          "         X          ",
          "          X         ",
          "          XXXXXX    ",
          "              XXX   "]#X = block, P = player, C = checkpoint empty layer: "                    "
screenWidth = 1200
screenHeight = 800

tileSize = 128
deathHeight = len(layout) * tileSize

pWidth, pHeight = 50, 75

playerColor = (0, 0, 255)
white = (255, 255, 255)
groundColor = (255, 0, 0)
checkpointColor = (255, 255, 0)