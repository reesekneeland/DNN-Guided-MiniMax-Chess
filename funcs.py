import chess

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
    
    if(board.is_checkmate()):
        print(getCurPlayer(board) + " has been checkmated! " + getNextPlayer(board) + " wins!")
    elif(board.is_check()):
        print(getCurPlayer(board) + " is in check! Possible moves are: " + str(getMoveList(board)))
    elif(board.is_stalemate()):
        print("Stalemate! The game ends in a draw")
    else:
        print("Possible moves for " + getCurPlayer(board) + ": " + str(getMoveList(board)))