import discord
import os
import chess
import sys
import signal
from funcs import *
from dotenv import load_dotenv
import multiprocessing

load_dotenv()
client = discord.Client()
AIip_dict = {}
pid_dict = {}
game_dict = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    pid = -1

@client.event
async def on_message(msg):
    global pid_dict
    global game_dict
    global AIip_dict
    if msg.author == client.user:
        return
    if msg.content.lower().startswith(".chess"):
        discChannel = msg.channel.id

        if not (discChannel in game_dict):
            game_dict[discChannel] = MiniMaxChess(0)
            pid_dict[discChannel] = -1
            AIip_dict[discChannel] = 0

        AIip = AIip_dict[discChannel]
        pid = pid_dict[discChannel]
        game = game_dict[discChannel]

        text = msg.content
        cmd1 = text[7:]
        if(cmd1 == "help"):
            await msg.channel.send("Welcome to Guided MiniMax Chess! Here is a list of the available commands:\nTo begin a game from the gamemode selection screen, input the command```.chess <1, 2, or 3>```1 is for singleplayer, where you control both sides of the board (boring, this is mostly used for development), 2 is to play a singleplayer game against the AI opponent, and 3 is to watch the AI play itself! In this gamemode the AI will loop until it finishes the game unless you interrupt it with a quit command. In this state it will not respond to most of the other commands (yet)```.chess quit```Resets the game and exit back to the gamemode selection screen```.chess undo```Undoes the most recent move, in gamemode 2, it will undo both your move and the AI's move.```.chess get```Gets the current representation of the board in a string.```.chess set <board string here>``` sets the current board position to whatever string you give it.```.chess print``` prints the current board, useful if the bot messed up sending the message for the board and you need it reprinted.```.chess reset``` Resets the board back to the gamemode selection screen.\n\nTo actually interact with the board during play, use the command ```.chess <move>``` where the move is one of the strings of text given to you in the \"possible moves\" list it prints out every turn.\n\nIts worth noting that as of right now only one instance of the chess bot can be running at a time, so please interact with it one at a time to not disrupt each others games. If you have any more questions or a suggestion, shoot my developer, Reese Kneeland, a message!")
        else:
            if(game.gameState == 0):
                await msg.channel.send("Welcome to Guided MiniMax Chess! Please enter the type of game you would like to play, 1 for singleplayer, 2 to play vs an AI, and 3 to have the AI play itself")
            if(game.gameState > 0):
                if(cmd1 == "exit" or cmd1 == "quit" or cmd1 == "kill"):
                    game.resetBoard()
                    game.gameState == 0
                    if(pid>0):
                        os.kill(pid, signal.SIGKILL)
                    await msg.channel.send("Game has been stopped")
                    AIip == 0
                elif(cmd1 == "undo"):
                    if(game.gameState == 1):
                        await msg.channel.send(game.undoMove())
                    elif(game.gameState == 2):
                        game.undoMove()
                        await msg.channel.send(game.undoMove())
                    else:
                        await msg.channel.send("Error, you are not in a gamemode that permits undoing moves")
                elif(cmd1 == "get"):
                    await msg.channel.send(game.getFen())
                elif("set " in cmd1):
                    await msg.channel.send(game.setFen(text[11:]))
                    msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                    await msg.channel.send(msg1)
                    await msg.channel.send(msg2)
                    await msg.channel.send(msg3)
                    await msg.channel.send(msg4)
                elif(cmd1 == "piecemap"):
                    await msg.channel.send(game.makeReadable(game.getBoardMap()))
                elif(cmd1 == "alist"):
                    await msg.channel.send(game.makeReadable(game.getAttackerMap()))
                elif(cmd1 == "attacks"):
                    await msg.channel.send(game.getAttacks(26))
                elif(cmd1 == "print"):
                    msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                    await msg.channel.send(msg1)
                    await msg.channel.send(msg2)
                    await msg.channel.send(msg3)
                    await msg.channel.send(msg4)
                elif(cmd1 == "reset"):
                    if(pid>0):
                        os.kill(pid, signal.SIGKILL)
                    AIip = 0
                    game.gameState = 0
                    game.resetBoard()
                    await msg.channel.send("Game has been reset")
                elif(game.gameState == 1):
                    if(game.makeMove(cmd1) == 1):
                        msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                        await msg.channel.send(msg1)
                        await msg.channel.send(msg2)
                        await msg.channel.send(msg3)
                        await msg.channel.send(msg4)
                        await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                        action, minimaxmsg = game.choose_action()
                        await msg.channel.send(minimaxmsg)
                    else:
                        await msg.channel.send("Move " + str(cmd1) + " not legal, try again. The legal moves for " + game.getCurPlayer() + " are : " + str(game.getMoveList()))
                elif(game.gameState == 2):
                    if(game.makeMove(cmd1) == 1):
                        msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                        await msg.channel.send(msg1)
                        await msg.channel.send(msg2)
                        await msg.channel.send(msg3)
                        await msg.channel.send(msg4)
                        await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                        action, minimaxmsg = game.choose_action()
                        await msg.channel.send(minimaxmsg)
                        game.makeMove(action)
                        msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                        await msg.channel.send(msg1)
                        await msg.channel.send(msg2)
                        await msg.channel.send(msg3)
                        await msg.channel.send(msg4)
                    else:
                        await msg.channel.send("Move " + str(cmd1) + " not legal, try again. The legal moves for " + game.getCurPlayer() + " are : " + str(game.getMoveList()))
            elif(game.gameState <= 0):
                if(cmd1 == "1"): 
                    game.gameState = 1
                    await msg.channel.send("You have chosen singleplayer!")
                    msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                    await msg.channel.send(msg1)
                    await msg.channel.send(msg2)
                    await msg.channel.send(msg3)
                    await msg.channel.send(msg4)
                    await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                    action, minimaxmsg = game.choose_action()
                    await msg.channel.send(minimaxmsg)
                elif(cmd1 == "2"): 
                    game.gameState = 2
                    await msg.channel.send("You have chosen to play against an AI!")
                    msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                    await msg.channel.send(msg1)
                    await msg.channel.send(msg2)
                    await msg.channel.send(msg3)
                    await msg.channel.send(msg4)
                elif(cmd1 == "3"): 
                    game.gameState = 3
                    await msg.channel.send("You have chosen to watch the AI play itself!")
                    if(AIip == 0):
                        AIip = 1
                        if(pid > 0):
                            os.kill(pid, signal.SIGKILL)
                        pid = os.fork()
                        discChannelStr = str(discChannel)
                        if(pid == 0):
                            os.execvp("python3", ["python3", "discAI.py", str(discChannel)])
                        else:
                            pass
                else:
                    game.gameState = -1
                    await msg.channel.send("That is not a recognized gamemode! Please try again.")

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)