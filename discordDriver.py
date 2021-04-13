import discord
import os
import chess
import sys
from funcs import *
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

game = MiniMaxChess()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if '.chess' in msg.content.lower():
        text = msg.content
        args = text.split(' ')
        try:
            cmd1 = args[1]
        except:
            pass
        discChannel = msg.channel.id
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
                await msg.channel.send(game.resetBoard())
                game.gameState = 0
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
            elif(game.gameState == 3):
                while(game.gameOver() == False):
                    await msg.channel.send("MINIMAX AB : Wait AI is choosing\n")
                    await msg.channel.send(game.choose_action())
                    game.makeMove(game.choose_action_pure())

                    await msg.channel.send(game.evalBoard())
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
            else:
                game.gameState = -1
                await msg.channel.send("That is not a recognized gamemode! Please try again.")

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)