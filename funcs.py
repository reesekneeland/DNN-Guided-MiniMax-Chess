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

def getBoardMap(board):
    whitePStr = str(board.pieces(chess.PAWN, chess.WHITE))
    whitePStr.replace(".", "0.0")
    whitePList = re.split(' |\n', whitePStr)
    whiteBStr = str(board.pieces(chess.BISHOP, chess.WHITE))
    whiteBStr.replace(".", "0.0")
    whiteBList = re.split(' |\n', whiteBStr)
    whiteKnStr = str(board.pieces(chess.KNIGHT, chess.WHITE))
    whiteKnStr.replace(".", "0.0")
    whiteKnList = re.split(' |\n', whiteKnStr)
    whiteRStr = str(board.pieces(chess.ROOK, chess.WHITE))
    whiteRStr.replace(".", "0.0")
    whiteRList = re.split(' |\n', whiteRStr)
    whiteQStr = str(board.pieces(chess.QUEEN, chess.WHITE))
    whiteQStr.replace(".", "0.0")
    whiteQList = re.split(' |\n', whiteQStr)
    blackPStr = str(board.pieces(chess.PAWN, chess.BLACK))
    blackPStr.replace(".", "0.0")
    blackPList = re.split(' |\n', blackPStr)
    blackBStr = str(board.pieces(chess.BISHOP, chess.BLACK))
    blackBStr.replace(".", "0.0")
    blackBList = re.split(' |\n', blackBStr)
    blackKnStr = str(board.pieces(chess.KNIGHT, chess.BLACK))
    blackKnStr.replace(".", "0.0")
    blackKnList = re.split(' |\n', blackKnStr)
    blackRStr = str(board.pieces(chess.ROOK, chess.BLACK))
    blackRStr.replace(".", "0.0")
    blackRList = re.split(' |\n', blackRStr)
    blackQStr = str(board.pieces(chess.QUEEN, chess.BLACK))
    blackQStr.replace(".", "0.0")
    blackQList = re.split(' |\n', blackQStr)
    pieceMap = []
    for i in range(0, 64):
        if(whitePList[i] == "1"):
            appendVal = 1.0 * getMultiplierMap(board, chess.PAWN, chess.WHITE)[i]
        elif(whiteBList[i] == "1"):
            appendVal = 3.0 * getMultiplierMap(board, chess.BISHOP, chess.WHITE)[i]
        elif(whiteKnList[i] == "1"):
            appendVal = 3.0 * getMultiplierMap(board, chess.KNIGHT, chess.WHITE)[i]
        elif(whiteQList[i] == "1"):
            appendVal = 9.0 * getMultiplierMap(board, chess.QUEEN, chess.WHITE)[i]
        elif(whiteRList[i] == "1"):
            appendVal = 5.0 * getMultiplierMap(board, chess.ROOK, chess.WHITE)[i]
        elif(blackPList[i] == "1"):
            appendVal = -1.0 * getMultiplierMap(board, chess.PAWN, chess.BLACK)[i]
        elif(blackBList[i] == "1"):
            appendVal = -3.0 * getMultiplierMap(board, chess.BISHOP, chess.BLACK)[i]
        elif(blackKnList[i] == "1"):
            appendVal = -3.0 * getMultiplierMap(board, chess.KNIGHT, chess.BLACK)[i]
        elif(blackQList[i] == "1"):
            appendVal = -9.0 * getMultiplierMap(board, chess.QUEEN, chess.BLACK)[i]
        elif(blackRList[i] == "1"):
            appendVal = -5.0 * getMultiplierMap(board, chess.ROOK, chess.BLACK)[i]
        else:
            appendVal = 0.0
        pieceMap.append(round(appendVal, 2))
    res_list = []
    for i in range(0, len(pieceMap)):
        if(pieceMap[i] > 0):
            if(getAttackers(board, i, chess.WHITE) >= 0):
                attackFactor = 1.0 + getAttackers(board, i, chess.WHITE)/3
            else:
                attackFactor = 0.1
        elif(pieceMap[i] < 0):
            if(getAttackers(board, i, chess.BLACK) >= 0):
                attackFactor = 1.0 + getAttackers(board, i, chess.BLACK)/3
            else:
                attackFactor = 0.1
        else:
            attackFactor = 1.0
        print(attackFactor)

        res_list.append(round(pieceMap[i] * attackFactor, 2))
    print(sum(res_list))
    return res_list
        

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
            attackFactor = 1.0 + getAttackers(board, i, color)/3
        else:
            attackFactor = 0.1
        res_list.append(boardList[i] * multiplierMap[i] * attackFactor)
    return res_list

def getAttackers(board, square, color):
    if(color == chess.WHITE):
        return len(board.attackers(chess.BLACK, square)) - len(board.attackers(chess.WHITE, square))
    elif(color == chess.BLACK):
        return len(board.attackers(chess.WHITE, square)) - len(board.attackers(chess.BLACK, square))

def getAttackerMap(board):
    attackList = []
    for i in range(0, 64):
        attackList.append(getAttackers(board, i, board.turn))
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
    print("Current Heuristic: " + str(heuristic(board)))
    
    if(board.is_checkmate()):
        print(getCurPlayer(board) + " has been checkmated! " + getNextPlayer(board) + " wins!")
    elif(board.is_check()):
        print(getCurPlayer(board) + " is in check! Possible moves are: " + str(getMoveList(board)))
    elif(board.is_stalemate()):
        print("Stalemate! The game ends in a draw")
    else:
        print("Possible moves for " + getCurPlayer(board) + ": " + str(getMoveList(board)))
        print(getBoardMap(board))
        # print(getAttackerMap(board))

def heuristic(board):
    if(str(board.result()) == "0-1"):
        return -100
    elif(str(board.result()) == "1-0"):
        return 100
    # if()
    pointDif = whiteValue(board) - blackValue(board)
    valueHeuristic = 83 * math.atan(pointDif/15)
    totalHeuristic = 1 * valueHeuristic
    return totalHeuristic
