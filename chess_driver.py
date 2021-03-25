import chess
import sys
from funcs import *

board = chess.Board()
evalBoard(board)
#main input loop
while(True):
    raw_input = ""
    try:
        raw_input = input(">>> ")
    except KeyboardInterrupt:
        print("\nQuitting...")
        sys.exit()
    except:
        print("\nGracefully crashing...")
        raw_input = "exit"
    if(raw_input == ""): continue
    elif(raw_input == "undo"):
        undoMove(board)
    elif(raw_input == "exit" or raw_input == "quit"):
        sys.exit()
    else:
        if(makeMove(board, raw_input) == 1):
            pass
        else:
            continue
    evalBoard(board)
    
print("Exit")

        