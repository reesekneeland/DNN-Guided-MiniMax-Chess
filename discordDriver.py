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
pid = -1
game = MiniMaxChess()

async def gameMode3(chan):
    channel = client.get_channel(chan)
    await channel.send("MINIMAX AB : Wait AI is choosing\n")
    await channel.send(game.choose_action())
    game.makeMove(game.choose_action_pure())
    await channel.send(game.evalBoard())
    while(game.gameOver() == False):
        await channel.send("MINIMAX AB : Wait AI is choosing\n")
        await channel.send(game.choose_action())
        game.makeMove(game.choose_action_pure())
        await channel.send(game.evalBoard())
            

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
        print("loop check")
        discChannel = msg.channel.id
        # proc = multiprocessing.Process(target=gameMode3, args=([discChannel]))
        text = msg.content
        args = text.split(' ')
        try:
            cmd1 = args[1]
        except:
            pass
        discAuthor = msg.author.id
        print(discChannel, discAuthor)
        if(game.gameState == 0):
            await msg.channel.send("Welcome to MiniMax Chess! Please enter the type of game you would like to play, 1 for singleplayer, 2 to play vs an AI, and 3 to have the AI play itself")
        if(cmd1 == "exit" or cmd1 == "quit"):
                game.resetBoard()
                game.setState == 0
        if(game.setState == 1):
            await msg.channel.send(game.setFen(cmd1))
            await msg.channel.send(game.evalBoard())
            game.setState = 0
        if(game.gameState > 0):
            if(cmd1 == "undo"):
                await msg.channel.send(game.undoMove())
            if(cmd1 == "get"):
                await msg.channel.send(game.getFen())
            if(cmd1 == "set"):
                await msg.channel.send("Please enter your board string.")
                game.setState = 1
            if(cmd1 == "print"):
                await msg.channel.send(game.evalBoard())
            if(cmd1 == "reset"):
                if(pid == os.getpid()):
                    print(pid)
                    os.kill(pid, 9)
                game.gameState = 0
                await msg.channel.send(game.resetBoard())
            if(game.gameState == 1):
                if(game.makeMove(cmd1) == 1):
                    await msg.channel.send(game.evalBoard())
                    await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                    await msg.channel.send(game.choose_action())
                else:
                    await msg.channel.send("Move " + str(cmd1) + " not legal, try again. The legal moves for " + game.getCurPlayer() + " are : " + str(game.getMoveList()))
            elif(game.gameState == 2):
                if(game.makeMove(cmd1) == 1):
                    await msg.channel.send(game.evalBoard())
                    await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                    await msg.channel.send(game.choose_action())
                    game.makeMove(game.choose_action_pure())
                    await msg.channel.send(game.evalBoard())
                else:
                    await msg.channel.send("Move " + str(cmd1) + " not legal, try again. The legal moves for " + game.getCurPlayer() + " are : " + str(game.getMoveList()))
        elif(game.gameState <= 0):
            if(cmd1 == "1"): 
                game.gameState = 1
                await msg.channel.send("You have chosen singleplayer!")
                await msg.channel.send(game.evalBoard())
                await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                await msg.channel.send(game.choose_action())
            elif(cmd1 == "2"): 
                game.gameState = 2
                await msg.channel.send("You have chosen to play against an AI!")
                await msg.channel.send(game.evalBoard())
            elif(cmd1 == "3"): 
                game.gameState = 3
                await msg.channel.send("You have chosen to watch the AI play itself!")
                await msg.channel.send(game.evalBoard())
                # if(pid > 0):
                #     os.kill(pid, 9)
                pid = os.fork()
                if(pid == 0):
                    print("I am the child, my pid is %d", os.getpid())
                    pid = os.getpid()
                    while(game.gameOver() == False):
                        # await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                        action = game.choose_action()
                        await msg.channel.send(action)
                        game.makeMove(game.choose_action_pure())
                        await msg.channel.send(game.evalBoard())
                else:
                    print("I am the parent, my pid is %d", os.getpid())
                print("Parent is proceeding")
            else:
                game.gameState = -1
                await msg.channel.send("That is not a recognized gamemode! Please try again.")

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)