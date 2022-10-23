from shutil import move
from turtle import Turtle


class CurrentState():

    def _init_(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.WhiteMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.StaleMate = False
        self.enpassantPossible = () #possible enpassant coord
        self.currentCastling = Castling(True, True, True, True)
        self.castlingLog = [Castling(self.currentCastling.wks, self.currentCastling.bks, self.currentCastling, self.currentCastling.bqs)]

        


    # executes moves(exceptions en passant, castle, promotion etc.)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #history of moves for undo function
        self.whiteToMove = not self.whiteToMove
        
        #king location update
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #promotion of pawn
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #pawn capture
        
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()

        self.updateCastling(move)
        self.castlingLog.append([Castling(self.currentCastling.wks, self.currentCastling.bks, self.currentCastling, self.currentCastling.bqs)])

        #actual Castle Move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'



    def updateCastling(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastling.wks = False
            self.currentCastling.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastling.bks = False
            self.currentCastling.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastling.wqs = False
                elif move.startCol == 7:
                    self.currentCastling.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastling.bqs = False
                elif move.startCol == 7:
                    self.currentCastling.bks = False



    #undo previous move
    def undoMove(self):
        moveLog = []
        if len(self.moveLog) != 0:
            move = moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endRow] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
                
            
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            
            #undo 2 square adv
            if move.pieceMoved[1] == 'p' and abs(move.startRow- move.endRow) == 2:
                self.enpassantPossible = ()
            #undocastling right
            self.castlingLog.pop()
            self.currentCastling = self.castlingLog[-1]

            #undo castling
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol +1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol +1] = '--'




    
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastling = Castling(self.currentCastling.wks, self.currentCastling.bks, self.currentCastling.wqs, self.currentCastling.bqs)
        # all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1])
        #make the move
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])

        #see if king is under attack for all of opponents moves
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck(0):
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastling = tempCastling
        return moves

    def Check(self): #is the king in check?
        if self.whiteToMove:
            return self.SquareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.SquareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def SquareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponenets turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                self.whiteToMove = not self.whiteToMove
                return True
        


    
    def GetAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    Unit = self.board[r][c][1]
                    if Unit == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif Unit == 'R':
                        self.getRookMoves(r,c,moves)
                    elif Unit == 'N':
                        self.getKnightMoves(r,c,moves)
                    elif Unit == 'B':
                        self.getBishopMoves(r,c,moves)
                    elif Unit == 'Q':
                        self.getQueenMoves(r, c, moves)
                    else:
                        self.getKingMoves(r,c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: 
            if self.board[r-1][c] == '--': #1 square white pawn advance
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 square white pawn advance
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))

            if c +1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))

        else: #black to move
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c), (r+1, c), self.board))
                if r ==1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r +2, c), self.board))
            
            #for captured peice
            if c-1 >= 0: #right capture
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c + 1 <= 7: #left capture
                if self.board[r+1][c+1][0] == 'w':
                 moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0, -1), (1, 0), (0, 1))
        oppColour = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if  0 <=  endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append((r,c), (endRow, endCol), self.board)
                    elif endPiece[0] == oppColour:
                        moves.append(Move(r, c), (endRow, endCol), self.board)
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves =  ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColour = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r +m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColour:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1,1), (1, -1), (1, 1))
        oppColour = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] *i
                endCol = r + d[1] *i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == oppColour:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1,-1), (1, 0), (1, 1))
        allyColour = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0<= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece == self.board[endRow][endCol]:
                    if endPiece[0] != allyColour:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
        self.getCastkeMoves(r, c,moves, allyColour)

    def getCastleMoves(self, r, c, moves, allyColour):
        if self.SquareUnderAttack(r, c):
            return #not able to castle in check
        if self.whiteToMove and self.currentCastling.wks or (not self.whiteToMove and self.currentCastling.bks):
            self.getKingsideCastleMoves(r,c, moves, allyColour)
        if self.whiteToMove and self.currentCastling.wqs or (not self.whiteToMove and self.currentCastling.bqs):
            self.getKingsideCastleMoves(r,c, moves, allyColour)

    def getKingsideCastleMoves(self, r, c, moves, allyColour):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.SquareUnderAttack(r, c+1) and not self.SquareUnderAttack(r, c +2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))


    
    def getQueensideCastleMoves(self, r, c, moves, allyColour):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3]:
            if not self.SquareUnderAttack(r, c-1) and not self.SquareUnderAttack(r, c -2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))

        

class Castling():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


                    



class Move():

    ranksToRows = {'1': 7, '2': 6, '3': 5,  '4':4,
                   '5': 3, '6':2, '7': 1, '8': 0}
    ranksToRanks = {v: k  for k, v in ranksToRows.items()}
    filesToCols = {'a':0, 'b':1, 'c': 2, 'd':3, 
                   'e':4, 'f':5, 'g':6, 'h':7}
    ColsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.peiceMoved == 'bp' and self.endRow ==7):
            self.isPawnPromotion

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        
        #castle move
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow *1000 + self.startCol *100 + self.endRow *10 + self.endCol
        
        
        
    
    def __eq__(self, other):
        if isinstance(other, move):
            return self.moveID == other.moveID
        return False
        


    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
