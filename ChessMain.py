#main Driver for user input

import pygame as p
from CHESS import Engine,SmartMoves

width = height = 400
size = 8
square_size = height // size
FpsMax = 15
images = {}

#load images onto the board
def imageLoad():
    Units = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK' ]
    for Unit in Units:
        images[Unit] = p.transform.scale(p.image.load('images/' + Units + '.png')),(square_size, square_size)

#Main dirver: intake user input and update graphics to match
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.color('white'))
    gs = Engine.Ganestate()
    validMove = gs.getValidMoves()
    moveMade = False
    
    imageLoad()
    running = True
    square_select = () #keeps track of last selected click spot for unit
    P_Click = [] #tracks clicks from player
    playerOne = True
    playerTwo = False
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.even.get():
            if e.type == p.QUIT:
                running = False
           
            #handles mouseclicks
            elif e.type == p.MOUSEBUTTONDOWN:
                M_location = p.mouse.get_pos()
                col = M_location[0]//square_size
                row = M_location[1]//square_size
                if square_select == (row, col):
                    square_select = () #undo
                    P_Click =  [] #undo
                else:
                    square_select = (row, col)
                    P_Click.append(square_select)
                if len(P_Click) == 2:
                    move =  Engine.Move(P_Click[0], P_Click[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):    
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            gs.makeMove(move)
                            square_select = ()
                            P_Click = []
                    if not moveMade:
                        P_Click = [square_select]
            
            #handles keys
            elif e.type == p.KEYDOWN:
                if e.key == p.K_q: #press q to undo(hey that rhymes!)
                    gs.undoMove()
                    moveMade = True

        if not humanTurn:
            AIMove = SmartMoves.BestMove(gs, validMove)
            if AIMove is None:
                AIMove = SmartMoves.RandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(FpsMax)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawUnits(screen, gs.board)

#board squares
def drawBoard(screen):
    colours = [p.Color('white'), p.Color('gray')]
    for r in range(size):
        for c in range(size):
            colours = [((r+c)%2)]
            p.draw.rect(screen, colours, p.Rect(c*square_size, r*square_size, square_size, square_size))

#board units
def drawUnits(screen, board):
    for r in range(size):
        for c in range(size):
            Unit = board[r][c]
            if Unit != '--':
                screen.blit(images[Unit], p.Rect(c*square_size, r*square_size, square_size, square_size))

if __name__ == '__main__':
    main()
    
