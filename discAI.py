#!/usr/bin/env python3
import discord
import os
import chess
import sys
import signal
from funcs import *
from dotenv import load_dotenv
import multiprocessing
import concurrent
import asyncio
import logging
import traceback

logging.basicConfig(level=logging.INFO)
load_dotenv()
client = discord.Client()
game = MiniMaxChess(0)
has_started = False

@client.event
async def on_error(event, *args, **kwargs):
    #message = args[0] #Gets the message object
    print(traceback.format_exc()) #logs the error
    await client.get_channel(int(sys.argv[1])).send("The bot encountered an error")

@client.event
async def on_ready():
    global has_started
    if(has_started):
        return
    has_started = True
    try:
        print('We have logged in as {0.user}'.format(client))
        channel = client.get_channel(int(sys.argv[1]))
        
        msg1, msg2, msg3, msg4 = game.evalDiscBoard()
        await channel.send(msg1)
        await channel.send(msg2)
        await channel.send(msg3)
        await channel.send(msg4)
        while(game.gameOver() == False):
            await channel.send("MINIMAX AB : Wait AI is choosing\n")
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            loop = asyncio.get_event_loop()
            action, minimaxmsg = await loop.run_in_executor(executor, game.choose_action)
            await channel.send(minimaxmsg)
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, game.makeMove, action)
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            loop = asyncio.get_event_loop()
            msg1, msg2, msg3, msg4 = await loop.run_in_executor(executor, game.evalDiscBoard)
            await channel.send(msg1)
            await channel.send(msg2)
            await channel.send(msg3)
            await channel.send(msg4)
        print("loop exited")
        time.sleep(10)
        sys.exit()
    except Exception as exn:
        print(exn)
        print("Exit by exn")
        exit(0)

@client.event
async def on_disconnect():
    print("DISCONNECTED")

@client.event
async def on_message(message):
    print("msg")

TOKEN = os.getenv('DISCORD_TOKEN')

loop = asyncio.get_event_loop()
while(True):
    loop.run_until_complete(client.start(TOKEN))
    print("Died, restarting")
    time.sleep(20)
print("Exit")