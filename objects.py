import random as rnd
from init import *
import copy
import math as m
import pygame, sys, os
import itertools
from roundrects import round_rect # https://github.com/Mekire/rounded-rects-pygame/blob/master/example.py

class Block:
    def __init__(self, DISPLAY, xpos, ypos, walls, rotation):
        self.DISPLAY = DISPLAY
        self.xpos = xpos
        self.ypos = ypos
        self.xcor = xpos * bSIDE
        self.ycor = ypos * bSIDE
        self.walls = walls.pop(rnd.randint(0, len(walls)-1 ))
        self.rotateBlock(rotation)

    def drawBlock(self):
        round_rect(self.DISPLAY, [self.xcor, self.ycor, bSIDE, bSIDE], grey, 0, 3, grey1)
        pygame.draw.line(self.DISPLAY, grey2, [self.xcor + bSEG, self.ycor], [self.xcor + bSEG, self.ycor + bSIDE], 3)
        pygame.draw.line(self.DISPLAY, grey2, [self.xcor, self.ycor + bSEG], [self.xcor + bSIDE, self.ycor + bSEG], 3)
        for segment in self.walls:
            vert = int((segment[0] + 1)/2)
            hor = 1 - vert
            prex  = self.xcor  + bSEG + (bSEG - wall_thickness/2) * segment[1]* vert - wall_thickness/2 * segment[2]*hor
            prey  = self.ycor  + bSEG + (bSEG - wall_thickness/2) * segment[1]* hor - wall_thickness/2 * segment[2]*vert
            postx = self.xcor  + bSEG + (bSEG - wall_thickness/2) * segment[1 + hor]
            posty = self.ycor  + bSEG + (bSEG - wall_thickness/2) * segment[1 + vert]
            pygame.draw.line(self.DISPLAY, blue, [prex, prey], [postx, posty], wall_thickness)

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

    def getPos(self, xcor, ycor):
        if self.pointOn(xcor, ycor):
            xcor_in = xcor - self.xcor
            ycor_in = ycor - self.ycor
            return [ self.xpos, self.ypos, m.floor(xcor_in / bSEG), m.floor(ycor_in / bSEG) ]
        else:
            raise ValueError("Point outside of Block")

    def getCoords(self):
        return [self.xcor, self.ycor]

class Piece:
    def __init__(self, DISPLAY, startpos, color, radius):
        self.DISPLAY = DISPLAY

        self.pos = startpos # pos je sestavljen iz x,y koord. bloka ter x,y koord v bloku

        self.xcor = int(self.pos[0]*bSIDE + self.pos[2]*bSEG + bSEG/2)
        self.ycor = int(self.pos[1]*bSIDE + self.pos[3]*bSEG + bSEG/2)
        self.coords = [self.xcor, self.ycor]

        self.d_color = color # default color
        self.color = color # active color

        self.rad = radius # radius of the piece
        self.selected = False

    def drawPiece(self):
        if self.selected:
            mp = pygame.mouse.get_pos()
            self.xcor = mp[0]
            self.ycor = mp[1]
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

    def getPos(self):
        return self.pos

    def getCoords(self):
        return self.coords

def flat(table):
    return list(itertools.chain.from_iterable(table))

def onObj(objs, xcor, ycor):
    for obj in flat(objs):
        if obj.pointOn(xcor,ycor):
            return True
    return False

def selectPiece(mp, pieces, field):
        if onObj(field,mp[0],mp[1]):
                for piece in flat(pieces):
                        if piece.pointOn(mp[0],mp[1]):
                                piece.setSelected()
                                return
def selectedPiece(pieces):
    for piece in flat(pieces):
        if piece.isSelected():
            return piece.getPos()
    else:
        raise ValueError("No piece is selected")

def isOrthogonal(Bpos1, Bpos2):
    if Bpos1[0] == Bpos2[0] and Bpos1[2] == Bpos2[2]:
            return True
    elif Bpos1[1] == Bpos2[1] and Bpos1[3] == Bpos2[3]:
            return True
    else:
        return False

def Bdistance( Bpos1, Bpos2 ):
    return abs(( Bpos1[0]*2 + Bpos1[2] ) - ( Bpos2[0]*2 + Bpos2[2] )) + abs(( Bpos1[1]*2 + Bpos1[3] ) - ( Bpos2[1]*2 + Bpos2[3] ))

# def pathWalls(field, Bpos1, Bpos2):
#     dd = [ ( Bpos1[0]*2 + Bpos1[2] ) - ( Bpos2[0]*2 + Bpos2[2] ),  ( Bpos1[1]*2 + Bpos1[3] ) - ( Bpos2[1]*2 + Bpos2[3] ) ]
#     if dd[0] > 0 or dd[1] > 0: dd = 1
#     elif dd[0] < 0 or dd[1] < 0: dd = 0
#     else: raise ValueError("Positions are the same")

# def validPosition(Bpos, PCSpos, pieces, field):
#     prepos = selectedPiece(pieces).getPos()
#     if isOrthogonal(Bpos, prepos):
#         if Bdistance( prepos, Bpos) == 1:
#             path_walls = pathWalls(field, prepos, Bpos)


def putPiece(mp, pieces, field, pcs_pos):
    for piece in flat(pieces):
        if piece.isSelected():
            for block in flat(field):
                if block.pointOn(mp[0],mp[1]):
                    bposition = block.getPos(mp[0],mp[1])
                    # if validPosition(bposition,pcs_pos,field):
                    if bposition not in pcs_pos:
                        piece.changePosition(bposition)
            piece.unsetSelected()
            return
