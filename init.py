import math as m
import pygame, sys, os
import itertools

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


bFullSide =    [ [ 1,-1,-1 ], [ 1,-1, 1 ] ]
bHalfSide =    [ [ 1,-1, 1 ] ]
bZigZag =      [ [ 1,-1,-1 ], [-1, 0, -1], [1, 0, 1] ]
bT_Block=      [ [ 1,-1,-1 ], [ 1,-1, 1 ], [-1, 0,-1] ]
bTopLeft =     [ [ 1,-1,-1 ], [-1, 0,-1 ] ]
bTopRight =    [ [ 1, 0,-1 ], [-1, 0, 1 ] ]
bBottomRight = [ [ 1, 0, 1 ], [-1, 1, 1 ] ]

wall_configurations = [bFullSide,
                       bHalfSide,
                       bZigZag,
                       bZigZag,
                       bT_Block,
                       bTopLeft,
                       bTopLeft,
                       bTopRight,
                       bTopRight,
                       bBottomRight,
                       bBottomRight,
                       bBottomRight]

