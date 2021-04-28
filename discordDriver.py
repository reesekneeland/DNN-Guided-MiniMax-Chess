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
AIip = 0
pid = -1
game = MiniMaxChess(0)
     
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    pid = -1

@client.event
async def on_message(msg):
    global pid
    if msg.author == client.user:
        return
    if '.chess' in msg.content.lower():
        discChannel = msg.channel.id
        # proc = multiprocessing.Process(target=gameMode3, args=([discChannel]))
        text = msg.content
        args = text.split(' ')
        try:
            cmd1 = args[1]
        except:
            pass
        if(game.gameState == 0):
            await msg.channel.send("Welcome to MiniMax Chess! Please enter the type of game you would like to play, 1 for singleplayer, 2 to play vs an AI, and 3 to have the AI play itself")
        if(cmd1 == "exit" or cmd1 == "quit"):
                game.resetBoard()
                game.setState == 0
                if(pid>0):
                    os.kill(pid, signal.SIGKILL)
                AIip == 0
        if(game.setState == 1):
            await msg.channel.send(game.setFen(cmd1))
            msg1, msg2, msg3, msg4 = game.evalDiscBoard()
            await msg.channel.send(msg1)
            await msg.channel.send(msg2)
            await msg.channel.send(msg3)
            await msg.channel.send(msg4)
            game.setState = 0
        if(game.gameState > 0):
            if(cmd1 == "undo"):
                await msg.channel.send(game.undoMove())
            elif(cmd1 == "get"):
                await msg.channel.send(game.getFen())
            elif(cmd1 == "set"):
                await msg.channel.send("Please enter your board string.")
                game.setState = 1
            elif(cmd1 == "alist"):
                await msg.channel.send(game.getBoardMap)
            elif(cmd1 == "print"):
                msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                await msg.channel.send(msg1)
                await msg.channel.send(msg2)
                await msg.channel.send(msg3)
                await msg.channel.send(msg4)
            elif(cmd1 == "reset"):
                if(pid>0):
                    os.kill(pid, signal.SIGKILL)
                AIip == 0
                game.gameState = 0
                await msg.channel.send(game.resetBoard())
            elif(game.gameState == 1):
                if(game.makeMove(cmd1) == 1):
                    msg1, msg2, msg3, msg4 = game.evalDiscBoard()
                    await msg.channel.send(msg1)
                    await msg.channel.send(msg2)
                    await msg.channel.send(msg3)
                    await msg.channel.send(msg4)
                    await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                    await msg.channel.send(game.choose_action())
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
                    await msg.channel.send(game.choose_action())
                    game.makeMove(game.choose_action_pure())
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
                await msg.channel.send(game.choose_action())
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
                    AIip == 1
                    if(pid > 0):
                        os.kill(pid, signal.SIGKILL)
                    # os.system('/home/shared/4511w/Guided-MiniMax-Chess/startDiscAI.sh {}' .format(str(discChannel)))
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