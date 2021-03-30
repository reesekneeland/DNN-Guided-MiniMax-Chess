import chess
from minimax import *
from positionMap import *
import math
import re

def makeMove(board, sanStr):
    try:
        moveStr = str(board.parse_san(sanStr))
        move = chess.Move.from_uci(moveStr)
    except:
        print("Move not legal, try again. The legal moves for " + getCurPlayer(board) + " are : " + str(getMoveList(board)))
        return 0
    if(move in board.legal_moves):
        board.push(move)
        print("Black value is: " + str(blackValue(board)))
        print("White value is: " + str(whiteValue(board)))
        return 1
    else:
        print("Move not legal, try again. The legal moves for " + getCurPlayer(board) + " are : " + str(getMoveList(board)))
        return 0

def getMoveList(board):
    moveStrList = str(board.legal_moves)
    moveStrList = moveStrList[39:-2]
    moveList = moveStrList.split(", ")
    return moveList

def getMultiplierMap(board, piece, color):
    if(color == chess.BLACK):
        if(piece == chess.PAWN):
            return blackPawnMap
        elif(piece == chess.KNIGHT):
            return blackKnightMap
        elif(piece == chess.BISHOP):
            return blackBishopMap
        elif(piece == chess.ROOK):
            return blackRookMap
        elif(piece == chess.QUEEN):
            return blackQueenMap
    if(color == chess.WHITE):
        if(piece == chess.PAWN):
            return whitePawnMap
        elif(piece == chess.KNIGHT):
            return whiteKnightMap
        elif(piece == chess.BISHOP):
            return whiteBishopMap
        elif(piece == chess.ROOK):
            return whiteRookMap
        elif(piece == chess.QUEEN):
            return whiteQueenMap

def getPieceMap(board, piece, color):
    multiplierMap = getMultiplierMap(board, piece, color)
    boardStr = str(board.pieces(piece, color))
    boardStr.replace(".", "0.0")
    boardList = re.split(' |\n', boardStr)
    for x, value in enumerate(boardList):
        if(value == "."):
            boardList[x] = 0.0
        if(value == "1"):
            boardList[x] = 1.0 * getPieceValue(piece)

    res_list = []
    print("len of boardlist: " + str(len(boardList)))
    for i in range(0, len(boardList)):
        if(getAttackers(board, i, color) >= 0):
            res_list.append(boardList[i] * multiplierMap[i])
        else:
            attackFactor = -1/(getAttackers(board, i, color) - 1)
            print(str(i) + ":" + str(attackFactor))
            res_list.append(boardList[i] * multiplierMap[i] * attackFactor)
    return res_list

def getAttackers(board, square, color):
    if(color == chess.WHITE):
        return len(board.attackers(chess.WHITE, square)) - len(board.attackers(chess.BLACK, square))
    elif(color == chess.BLACK):
        return len(board.attackers(chess.BLACK, square)) - len(board.attackers(chess.WHITE, square))

def getAttackerMap(board):
    attackList = []
    for i in range(0, 63):
        attackList.append(getAttackers(board, i))
    return attackList

def getPieceValue(piece):
    if(piece == chess.PAWN):
        return 1.0
    elif(piece == chess.KNIGHT):
        return 3.0
    elif(piece == chess.BISHOP):
        return 3.0
    elif(piece == chess.ROOK):
        return 4.0
    elif(piece == chess.QUEEN):
        return 9.0

def getCurPlayer(board):
    if(board.turn == chess.WHITE):
        return "white"
    else:
        return "black"

def getNextPlayer(board):
    if(board.turn == chess.WHITE):
        return "black"
    else:
        return "white"

def undoMove(board):
    board.pop()
    print("Move undone")
    evalBoard(board)

def resetBoard(board):
    board.reset()
    print("Board has been reset")


def whiteValue(board):
    pawnv = len(board.pieces(chess.PAWN, chess.WHITE))
    knightv = 3 * len(board.pieces(chess.KNIGHT, chess.WHITE))
    bishopv = 3 * len(board.pieces(chess.BISHOP, chess.WHITE))
    rookv = 5 * len(board.pieces(chess.ROOK, chess.WHITE))
    queenv = 9 * len(board.pieces(chess.QUEEN, chess.WHITE))
    return pawnv + knightv + bishopv + rookv + queenv

def blackValue(board):
    pawnv = len(board.pieces(chess.PAWN, chess.BLACK))
    knightv = 3 * len(board.pieces(chess.KNIGHT, chess.BLACK))
    bishopv = 3 * len(board.pieces(chess.BISHOP, chess.BLACK))
    rookv = 5 * len(board.pieces(chess.ROOK, chess.BLACK))
    queenv = 9 * len(board.pieces(chess.QUEEN, chess.BLACK))
    return pawnv + knightv + bishopv + rookv + queenv

def evalBoard(board):
    print("\nblack\n---------------")
    print(board)
    print("---------------\nwhite\n")
    print("White value: " + str(whiteValue(board)))
    print("Current Heuristic: " + str(heuristic(board)))
    
    if(board.is_checkmate()):
        print(getCurPlayer(board) + " has been checkmated! " + getNextPlayer(board) + " wins!")
    elif(board.is_check()):
        print(getCurPlayer(board) + " is in check! Possible moves are: " + str(getMoveList(board)))
    elif(board.is_stalemate()):
        print("Stalemate! The game ends in a draw")
    else:
        print("Possible moves for " + getCurPlayer(board) + ": " + str(getMoveList(board)))
        # print(getPieceMap(board, chess.KNIGHT, chess.WHITE))
        # print(getAttackerMap(board))

def heuristic(board):
    if(str(board.result()) == "0-1"):
        return -100
    elif(str(board.result()) == "1-0"):
        return 100
    pointDif = whiteValue(board) - blackValue(board)
    valueHeuristic = 83 * math.atan(pointDif/15)
    totalHeuristic = 1 * valueHeuristic
    return totalHeuristic
