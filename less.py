from init import *
from objects import *
import math as m
import pygame, sys, os
from pygame.locals import *
import itertools
from roundrects import round_rect # https://github.com/Mekire/rounded-rects-pygame/blob/master/example.py


# 1. usmerjenost (-1 = horizontalno, 1 = vertikalno)  
# 2. pozicija v mat. smislu (-1 = levo/dol, 0 = sredina, 1 = desno/gor)  
# 3. precizna pozicija v mat. smislu (-1 = gor/levo, 1 = dol/desno)  
# vogali so pozicionirani tako, da narišejo črko L

def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((dX,dY))

    # if sum([nwall[1] for nwall in self.walls] )<9:
    #     raise ValueError("Total number of availible wall configurations must be greater than total number of used blocks")

    field = [ [Block(DISPLAY, x, y, wall_configurations, rnd.randrange(0,4))
               for x in range(3)] for y in range(3) ]

    wpieces = flat([[ Piece(DISPLAY, [0,0,x,y], khaki, piece_radius)
              for x in range(2)] for y in range(2)])
    bpieces = flat([[ Piece(DISPLAY, [2,2,x,y], brown, piece_radius)
              for x in range(2)] for y in range(2)])
    pieces = [wpieces , bpieces]

    while True:
        DISPLAY.fill(white)
        for block in flat(field):
            block.drawBlock()
        for piece in flat(pieces):
            piece.drawPiece()

        for event in pygame.event.get():

            pcs_pos = [ piece.getPos() for piece in flat(pieces) ]
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
                selectPiece(mp, pieces, field)

            if event.type==MOUSEBUTTONUP:
                putPiece(mp, pieces, field, pcs_pos)

        pygame.display.flip()

main()
