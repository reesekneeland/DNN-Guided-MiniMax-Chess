#!/usr/bin/env python3
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
game = MiniMaxChess(0)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(int(sys.argv[1]))
    
    msg1, msg2, msg3, msg4 = game.evalDiscBoard()
    await channel.send(msg1)
    await channel.send(msg2)
    await channel.send(msg3)
    await channel.send(msg4)
    while(game.gameOver() == False):
        await channel.send("MINIMAX AB : Wait AI is choosing\n")
        action = game.choose_action()
        await channel.send(action)
        game.makeMove(game.choose_action_pure())
        msg1, msg2, msg3, msg4 = game.evalDiscBoard()
        await channel.send(msg1)
        await channel.send(msg2)
        await channel.send(msg3)
        await channel.send(msg4)
    sys.exit()
    

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)