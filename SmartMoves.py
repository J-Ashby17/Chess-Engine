from logging.config import valid_ident
import random
from tabnanny import check

pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p':1 }
checkmate = 1000
stalemate = 0
DEPTH= 4

def RandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

#best move (material based)

def BestMoveNoRecursion():
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = checkmate
    BestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        random.shuffle(validMoves)
        opponentMaxScore = -checkmate
        if gs.stalemate:
            opponentMaxScore = stalemate
        elif gs.checkmate:
            opponentMaxScore = -checkmate
        else:
            opponentMaxScore = -checkmate
            for opponentsMove in opponentsMoves:
                gs.makeMoves(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = checkmate
                elif gs.stalemate:
                    score = stalemate
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
            if opponentMaxScore < opponentMinMaxScore:
                opponentMinMaxScore = opponentMaxScore
                BestMove = playerMove
            gs.undoMove()
    return BestMove


def bestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    MoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -checkmate, checkmate 1 if gs.whiteToMove else -1)
    return nextMove


def MoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return MaterialScore(gs.board)
    
    if whiteToMove:
        maxScore = -checkmate
        for move in validMoves:
            gs.makeMove()
            nextMoves = gs.getValidMoves()
            score = MoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = checkmate
        for move in validMoves:
            gs.makeMove()
            nextMoves = gs.getValidMoves()
            score = MoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undomove()
        return minScore



def MoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -checkmate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -MoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def MoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    

    
    maxScore = -checkmate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -MoveNegaMaxAlphaBeta(gs, nextMoves, depth-1,-beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning time!
            alpha = maxScore
        if alpha>= beta:
            break
    return maxScore



#positive good for white and negative is good for black

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -checkmate #black winner
        else:
            return checkmate #white winner
    elif gs.stalemate:
        return stalemate
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score +=pieceScore[square[1]]
            elif square[0] == 'b':
                score-=pieceScore[square[1]]
    return score



#material score
def MaterialScore(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score +=pieceScore[square[1]]
            elif square[0] == 'b':
                score-=pieceScore[square[1]]
    return score
