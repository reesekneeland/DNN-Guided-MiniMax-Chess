import chess
import sys
from funcs import *


game = MiniMaxChess(0)
#main input loop
while(True):
    if(game.gameState == 0):
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
    if(game.setState == 1):
        game.setFen(raw_input)
        game.evalBoard()
        game.setState = 0
        continue
    if(game.gameState > 0):
        if(raw_input == "undo"):
            game.undoMove()
            continue
        if(raw_input == "get"):
            print(game.getFen())
            continue
        if(raw_input == "set"):
            print("Please enter your board string.")
            game.setState = 1
            continue
        if(raw_input == "print"):
            game.evalBoard()
            continue
        if(raw_input == "reset"):
            game.resetBoard()
            game.gameState = 0
            continue
        if(game.gameState == 1):
            if(game.makeMove(raw_input) == 1):
                game.evalBoard()
                print("MINIMAX AB : Wait AI is choosing\n")
                print(game.choose_action())
                pass
            else:
                continue
        elif(game.gameState == 2):
            if(game.makeMove(raw_input) == 1):
                game.evalBoard()
                print("MINIMAX AB : Wait AI is choosing\n")
                game.makeMove(game.choose_action())
                game.evalBoard()
                pass
            else:
                continue
        elif(game.gameState == 3):
            continue
    if(game.gameState <= 0):
        if(raw_input == "1"): 
            game.gameState = 1
            print("You have chosen singleplayer!")
            game.evalBoard()
            print("MINIMAX AB : Wait AI is choosing\n")
            print(game.choose_action())
        elif(raw_input == "2"): 
            game.gameState = 2
            print("You have chosen to play against an AI!")
            game.evalBoard()
        elif(raw_input == "3"): 
            game.gameState = 3
            print("You have chosen to watch the AI play itself!")
            game.evalBoard()
            while(game.gameOver() == False):
                print("MINIMAX AB : Wait AI is choosing\n")
                move = str(game.choose_action_pure())
                if(game.makeMove(move) == 1):
                    print(game.choose_action())
                    game.evalBoard()
                else:
                    print("move  failed")
                    continue
        else:
            game.gameState = -1
            print("That is not a recognized gamemode! Please try again.")
    if(raw_input == ""): continue


        