import pygame, sys, os, copy
import random as rnd

from pygame.locals import *
from roundrects import round_rect # https://github.com/Mekire/rounded-rects-pygame/blob/master/example.py
from math import ceil

white=(255,255,255)
grey=(220,220,220)
grey1=(190,190,190)
blue=(0,0,255)
khaki=(240,230,140)
brown=(165,41,41)

statusX = 100
gameSIDE = 900
dX = gameSIDE + statusX
dY = gameSIDE
bSIDE = ceil(gameSIDE/3)
bSEG = ceil(bSIDE/2)

# 1. usmerjenost (-1 = horizontalno, 1 = vertikalno)  
# 2. pozicija v mat. smislu (-1 = levo/dol, 0 = sredina, 1 = desno/gor)  
# 3. precizna pozicija v mat. smislu (-1 = gor/levo, 1 = dol/desno)  
# vogali so pozicionirani tako, da narišejo črko L

bFullSide =    [ [ 1,-1,-1 ], [ 1,-1, 1 ] ]
bHalfSide =    [ [ 1,-1, 1 ] ]
bZigZag =      [ [ 1,-1,-1 ], [-1, 0, -1], [1, 0, 1] ]
bT_Block=      [ [ 1,-1,-1 ], [ 1,-1, 1 ], [-1, 0,-1] ]
bTopLeft =     [ [ 1,-1,-1 ], [-1, 0,-1 ] ]
bTopRight =    [ [ 1, 0,-1 ], [-1, 0, 1 ] ]
bBottomRight = [ [ 1, 0, 1 ], [-1, 1, 1 ] ]

wall_configurations = ( bFullSide,
                       bHalfSide,
                       bZigZag,
                       bT_Block,
                       bTopLeft,
                       bTopRight,
                       bBottomRight)


class Block:
    def __init__(self, DISPLAY, xpos, ypos, walls, rotation):
        self.DISPLAY = DISPLAY
        self.xcor = xpos * bSIDE
        self.ycor = ypos * bSIDE
        self.walls= walls
        self.rotateBlock(rotation)

    def drawBlock(self):
        round_rect(self.DISPLAY, [self.xcor, self.ycor, bSIDE, bSIDE], grey, ceil(bSIDE/10), 3)
        pygame.draw.line(self.DISPLAY, grey1, [self.xcor + bSEG, self.ycor], [self.xcor + bSEG, self.ycor + bSIDE], 3)
        pygame.draw.line(self.DISPLAY, grey1, [self.xcor, self.ycor + bSEG], [self.xcor + bSIDE, self.ycor + bSEG], 3)
        for segment in self.walls:
            vert = int((segment[0] + 1)/2)
            hor = 1 - vert
            prex = self.xcor + bSEG * (1 + segment[1]*vert)
            prey = self.ycor + bSEG * (1 + segment[1]*hor)
            postx = self.xcor + bSEG * (1 + segment[1 + hor])
            posty = self.ycor + bSEG * (1 + segment[1 + vert])
            pygame.draw.line(self.DISPLAY, blue, [prex, prey], [postx, posty], 10)

    def rotateBlock(self, cw_rotation):
        for iter in range(0,cw_rotation):
            for segment in self.walls:
                segment[1] = segment[0]*segment[1]
                segment[2] = -segment[0]*segment[2]
                segment[0] = -segment[0] # spremenimo na koncu, ker ostala dva zavisita od njega v trenutnem stanju

def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((dX,dY))
    DISPLAY.fill(white)

    field = [ [Block(DISPLAY, x, y,
                     rnd.choice(wall_configurations), rnd.randrange(0,4))
               for x in range(3)] for y in range(3) ]
    for row in field:
        for block in row:
            block.drawBlock()

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main()
