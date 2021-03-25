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

def evalBoard(board):
    print("\nblack\n---------------")
    print(board)
    print("---------------\nwhite\n")
    
    if(board.is_checkmate()):
        print(curPlayer + " has been checkmated! " + getNextPlayer(board) + " wins!")
    elif(board.is_check()):
        print(curPlayer + " is in check! Possible moves are: " + str(getMoveList(board)))
    else:
        print("Possible moves for " + getCurPlayer(board) + ": " + str(getMoveList(board)))