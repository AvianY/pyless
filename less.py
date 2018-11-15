import pygame, sys, os, copy
import random as rnd
import math as m
import itertools

from pygame.locals import *
from roundrects import round_rect # https://github.com/Mekire/rounded-rects-pygame/blob/master/example.py

white=(255,255,255)
grey=(220,220,220)
grey1=(248,248,248)
grey2=(190,190,190)
blue=(0,0,255)
khaki=(240,230,140)
brown=(160,82,45)
green=(173,255,47)

statusX = 100
gameSIDE = 900
dX = gameSIDE + statusX
dY = gameSIDE
bSIDE = m.ceil(gameSIDE/3)
bSEG = m.ceil(bSIDE/2)
piece_radius = int(bSEG/4)
wall_thickness = int(bSEG/5)

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

class Walls:
    def __init__(self, wall_list):
        self.walls = wall_list
        if sum([nwall[1] for nwall in self.walls] )<9:
            raise ValueError("Total number of availible wall configurations must be greater than total number of used blocks")


    def getRandWall(self):
        chosenWall = rnd.choice(self.walls)
        while chosenWall[1]==0:
            chosenWall = rnd.choice(self.walls)

        chosenWall[1] = chosenWall[1]-1
        return copy.deepcopy(chosenWall[0])

class Block:
    def __init__(self, DISPLAY, xpos, ypos, walls, w_thickness, rotation):
        self.DISPLAY = DISPLAY
        self.xpos = xpos
        self.ypos = ypos
        self.xcor = xpos * bSIDE
        self.ycor = ypos * bSIDE
        self.walls= walls
        self.w_thickness = w_thickness
        self.rotateBlock(rotation)

    def drawBlock(self):
        round_rect(self.DISPLAY, [self.xcor, self.ycor, bSIDE, bSIDE], grey, 0, 3, grey1)
        pygame.draw.line(self.DISPLAY, grey2, [self.xcor + bSEG, self.ycor], [self.xcor + bSEG, self.ycor + bSIDE], 3)
        pygame.draw.line(self.DISPLAY, grey2, [self.xcor, self.ycor + bSEG], [self.xcor + bSIDE, self.ycor + bSEG], 3)
        for segment in self.walls:
            vert = int((segment[0] + 1)/2)
            hor = 1 - vert
            prex  = self.xcor  + bSEG + (bSEG - self.w_thickness/2) * segment[1]* vert - self.w_thickness/2 * segment[2]*hor
            prey  = self.ycor  + bSEG + (bSEG - self.w_thickness/2) * segment[1]* hor - self.w_thickness/2 * segment[2]*vert
            postx = self.xcor  + bSEG + (bSEG - self.w_thickness/2) * segment[1 + hor]
            posty = self.ycor  + bSEG + (bSEG - self.w_thickness/2) * segment[1 + vert]
            pygame.draw.line(self.DISPLAY, blue, [prex, prey], [postx, posty], self.w_thickness)

    def rotateBlock(self, cw_rotation):
        for iter in range(0,cw_rotation):
            for segment in self.walls:
                segment[1] = segment[0]*segment[1]
                segment[2] = -segment[0]*segment[2]
                segment[0] = -segment[0] # spremenimo na koncu, ker ostala dva zavisita od njega v trenutnem stanju

    def pointOn(self, xcor, ycor):
        if self.xcor < xcor < self.xcor + bSIDE and self.ycor < ycor < self.ycor + bSIDE:
            return True
        else:
            return False

    def getPosition(self, xcor, ycor):
        if self.pointOn(xcor, ycor):
            xcor_in = xcor - self.xcor
            ycor_in = ycor - self.ycor
            return [ self.xpos, self.ypos, m.floor(xcor_in / bSEG), m.floor(ycor_in / bSEG) ]
        else:
            raise ValueError("Point outside of Block")

class Piece:
    def __init__(self, DISPLAY, startpos, color, radius):
        self.DISPLAY = DISPLAY
        self.pos = startpos # pos je sestavljen iz x,y koord. bloka ter x,y koord v bloku
        self.xcor = int(self.pos[0]*bSIDE + self.pos[2]*bSEG + bSEG/2)
        self.ycor = int(self.pos[1]*bSIDE + self.pos[3]*bSEG + bSEG/2)
        self.d_color = color
        self.color = color
        self.rad = radius
        self.selected = False

    def drawPiece(self):
        if self.selected:
            self.xcor = pygame.mouse.get_pos()[0]
            self.ycor = pygame.mouse.get_pos()[1]
        else:
            self.xcor = int(self.pos[0]*bSIDE + self.pos[2]*bSEG + bSEG/2)
            self.ycor = int(self.pos[1]*bSIDE + self.pos[3]*bSEG + bSEG/2)
        pygame.draw.circle(self.DISPLAY, self.color, (self.xcor,self.ycor), self.rad)

    def pointOn(self, xcor, ycor):
        return m.sqrt((xcor - self.xcor)**2+(ycor - self.ycor)**2) < self.rad

    def toggleSelected(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True

    def setSelected(self):
        self.selected = True

    def unsetSelected(self):
        self.selected = False

    def isSelected(self):
        return self.selected

    def changePosition(self, newpos):
        self.pos = newpos

    def getPosition(self):
        return self.pos

def flat(table):
    return list(itertools.chain.from_iterable(table))

def onObj(objs, xcor, ycor):
    for obj in flat(objs):
        if obj.pointOn(xcor,ycor):
            return True
    return False

def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((dX,dY))

    wall_configurations = [[bFullSide, 1],
                           [bHalfSide, 1],
                           [bZigZag, 2],
                           [bT_Block, 1],
                           [bTopLeft, 2],
                           [bTopRight, 2],
                           [bBottomRight,3]]

    walls = Walls(wall_configurations)
    field = [ [Block(DISPLAY, x, y,
                     walls.getRandWall(), wall_thickness, rnd.randrange(0,4))
               for x in range(3)] for y in range(3) ]

    wpieces = [[ Piece(DISPLAY, [0,0,x,y], khaki, piece_radius)
              for x in range(2)] for y in range(2)]
    bpieces = [[ Piece(DISPLAY, [2,2,x,y], brown, piece_radius)
              for x in range(2)] for y in range(2)]
    pieces = wpieces + bpieces

    while True:
        DISPLAY.fill(white)
        for block in flat(field):
            block.drawBlock()
        for piece in flat(pieces):
            piece.drawPiece()

        for event in pygame.event.get():

            pcs_pos = [ piece.getPosition() for piece in flat(pieces) ]
            # mp = pygame.mouse.get_pos()

            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()
            if event.type==MOUSEMOTION:
                mp = event.pos
            if event.type==MOUSEBUTTONDOWN:
                if onObj(field,mp[0],mp[1]):
                    for piece in flat(pieces):
                        if piece.pointOn(mp[0],mp[1]):
                            piece.setSelected()

            if event.type==MOUSEBUTTONUP:
                for piece in flat(pieces):
                    if piece.isSelected():
                        for block in flat(field):
                            if block.pointOn(mp[0],mp[1]):
                                bposition = block.getPosition(mp[0],mp[1])
                                if bposition not in pcs_pos:
                                    piece.changePosition(bposition)
                        piece.unsetSelected()

        pygame.display.flip()

main()
