import chess

def makeMove(board, moveStr):
    move = chess.Move.from_uci(moveStr)
    if(move in board.legal_moves):
        board.push(move)
        return 1
    else:
        print("Move not legal, try again. The legal moves are: " + str(board.legal_moves))
        return 0


def undoMove(board):
    board.pop()
    print("Move undone")

def evalBoard(board):
    print("\nblack\n---------------")
    print(board)
    print("---------------\nwhite\n")
    if(board.turn == chess.WHITE):
        curPlayer = "white"
        nextPlayer = "black"
    else:
        curPlayer = "black"
        nextPlayer = "white"
    
    if(board.is_checkmate()):
        print(curPlayer + " has been checkmated! " + nextPlayer + " wins!")
    elif(board.is_check()):
        print(curPlayer + " is in check! Possible moves are: " + str(board.legal_moves))
    else:
        print("Possible moves for " + curPlayer + ": " + str(board.legal_moves))