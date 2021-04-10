import chess
import sys
from funcs import *


board = chess.Board()
gameState = 0
setState = 0
#main input loop
while(True):
    if(gameState == 0):
        print("Welcome to MiniMax Chess! Please enter the type of game you would like to play, 1 for singleplayer, 2 to play vs an AI, and 3 to have the AI play itself")
    raw_input = ""
    try:
        raw_input = input(">>> ")
    except KeyboardInterrupt:
        print("\nQuitting...")
        sys.exit()
    except:
        print("\nGracefully crashing...")
        raw_input = "exit"
    if(raw_input == "exit" or raw_input == "quit"):
            sys.exit()
    if(setState == 1):
        setFen(raw_input, board)
        evalBoard(board)
        setState = 0
        continue
    if(gameState > 0):
        if(raw_input == "undo"):
            undoMove(board)
            continue
        if(raw_input == "get"):
            getFen(board)
            continue
        if(raw_input == "set"):
            print("Please enter your board string.")
            setState = 1
            continue
        if(raw_input == "print"):
            evalBoard(board)
            continue
        if(raw_input == "reset"):
            resetBoard(board)
            gameState = 0
            continue
        if(gameState == 1):
            if(makeMove(board, raw_input) == 1):
                evalBoard(board)
                print(choose_action(board))
                pass
            else:
                continue
        elif(gameState == 2):
            if(makeMove(board, raw_input) == 1):
                evalBoard(board)
                makeMove(board, choose_action(board))
                evalBoard(board)
                pass
            else:
                continue
        elif(gameState == 3):
            while(gameOver(board) == False):
                makeMove(board, choose_action(board))
                evalBoard(board)
    if(gameState <= 0):
        if(raw_input == "1"): 
            gameState = 1
            print("You have chosen singleplayer!")
            evalBoard(board)
            print(choose_action(board))
        elif(raw_input == "2"): 
            gameState = 2
            print("You have chosen to play against an AI!")
            evalBoard(board)
        elif(raw_input == "3"): 
            gameState = 3
            print("You have chosen to watch the AI play itself!")
            evalBoard(board)
        else:
            gameState = -1
            print("That is not a recognized gamemode! Please try again.")
    if(raw_input == ""): continue
    
print("Exit")

        