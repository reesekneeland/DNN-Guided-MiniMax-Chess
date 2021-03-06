import discord
import os
import time
import signal
from funcs import *
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
AIip_dict = {}
pid_dict = {}
game_dict = {}
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
    global pid_dict
    global game_dict
    global AIip_dict
    if msg.author == client.user:
        return
    if msg.content.lower().startswith(".chess"):
        discChannel = msg.channel.id

        #set the variables to data for this channel
        if not (discChannel in game_dict):
            game_dict[discChannel] = MiniMaxChess(0)
            pid_dict[discChannel] = -1
            AIip_dict[discChannel] = 0
        AIip = AIip_dict[discChannel]
        pid = pid_dict[discChannel]
        game = game_dict[discChannel]

        prevMove = ""
        text = msg.content
        cmd1 = text[7:]       
        if(cmd1 == "help"):
            await msg.channel.send("Welcome to Guided MiniMax Chess! Here is a list of the available commands:\nTo begin a game from the gamemode selection screen, input the command```.chess <1, 2, or 3>```1 is for manual mode, where both sides of the board are controlled manually by one player (for testing), or by two players, who play each other. If you type ```.chess 1 AI```, it will enter the same singleplayer mode, but with AI assisted predictions at each move, gamemode 2 is to play a singleplayer game as white against the AI opponent who plays black, and gamemode 3 is to watch the AI play itself! In this gamemode the AI will loop until it finishes the game unless you interrupt it with a quit command. ```.chess quit``` Resets the game and exit back to the gamemode selection screen```.chess undo```Undoes the most recent move, in gamemode 2, it will undo both your move and the AI's move.```.chess get```Gets the current representation of the board in a string.```.chess set <board string here>``` sets the current board position to whatever string you give it.```.chess print``` reprints the current board, useful if the bot messed up sending the message for the board and you need it reprinted.```.chess reset``` Resets the board back to the gamemode selection screen.\n\nTo actually interact with the board during play, use the command ```.chess <move>``` where the move is one of the strings of text given to you in the \"possible moves\" list it prints out every turn.\n\nIts worth noting that as of right now only one instance of the chess bot can be running at a time, so please interact with it one at a time to not disrupt each others games. If you have any more questions or a suggestion, shoot one of my developers, Reese Kneeland, a message!")
        else:
            if(game.initialzed == 0):
                introMsg = ("Welcome to Guided MiniMax Chess!")
                if(len(cmd1) == 0):
                    introMsg += " Please enter the type of game you would like to play, 1 for singleplayer, 2 to play vs an AI, and 3 to have the AI play itself"
                introMsg += "\n"
                await msg.channel.send(introMsg)
                game.initialzed = 1
            else:
                try:
                    await msg.delete()
                except discord.errors.Forbidden:
                    print("Could not delete valid command message, invalid permissions!")
                    
            if(game.gameState > 0):
                if(cmd1 == "exit" or cmd1 == "quit" or cmd1 == "kill"):
                    # game.AIstate = 0
                    game.resetBoard()
                    game.gameState = 0
                    # if(pid > 0):
                    #     os.kill(pid, signal.SIGKILL)
                    await msg.channel.send("Game has been stopped")
                    AIip = 0
                elif(cmd1 == "undo"):
                    if(game.gameState == 1):
                        game.undoMove()
                        headerStr = ("Move undone!\n------------------\nPLAYER: Your Turn\n")
                        game.evalDiscBoardHeur(headerStr)
                        await game.msg1.edit(content=game.msg_text_1)
                        await game.msg2.edit(content=game.msg_text_2)
                    elif(game.gameState == 2):
                        game.undoMove()
                        headerStr = ("MINIMAX: Move undone!\n------------------\nPLAYER: Your Turn\n")
                        game.evalDiscBoardHeur(headerStr)
                        await game.msg1.edit(content=game.msg_text_1)
                        await game.msg2.edit(content=game.msg_text_2)
                    else:
                        await msg.channel.send("Error, you are not in a gamemode that permits undoing moves")
                elif(cmd1 == "get"):
                    await msg.channel.send(game.getFen())
                elif("set " in cmd1):
                    await msg.channel.send(game.setFen(text[11:]))
                    headerStr = ("Game Loaded!\n------------------\nYour turn!\n")
                    game.evalDiscBoardHeur(headerStr)
                    await game.msg1.edit(content=game.msg_text_1)
                    await game.msg2.edit(content=game.msg_text_2)
                elif(cmd1 == "piecemap"):
                    await msg.channel.send(game.makeReadable(game.getBoardMap()))
                elif(cmd1 == "alist"):
                    await msg.channel.send(game.makeReadable(game.getAttackerMap()))
                elif(cmd1 == "attacks"):
                    await msg.channel.send(game.getAttacks(26))
                elif(cmd1 == "print"):
                    game.evalDiscBoardHeur()
                    await game.msg1.edit(content=game.msg_text_1)
                    await game.msg2.edit(content=game.msg_text_2)
                elif(cmd1 == "reset"):
                    if(pid > 0):
                        os.kill(pid, signal.SIGKILL)
                    AIip = 0
                    game.gameState = 0
                    game.resetBoard()
                    await msg.channel.send("Game has been reset")
                elif(game.gameState == 1):
                    if(game.makeMoveCastle(cmd1) == 1):
                        prevMove = cmd1
                        print(game.aiRecState)
                        action, headerStr = game.choose_action(mode=game.aiRecState, prevMove=prevMove)
                        if("AI" in cmd1): 
                            game.evalDiscBoardHeur(headerStr)
                        else:
                            game.evalDiscBoard(headerStr)
                        await game.msg1.edit(content=game.msg_text_1)
                        await game.msg2.edit(content=game.msg_text_2)
                    else:
                        await game.msg2.edit(content=(game.msg_text_2 + "\n\n**MOVE " + str(cmd1) + " NOT LEGAL, TRY AGAIN.**"))
                elif(game.gameState == 2):
                    if(game.makeMoveCastle(cmd1) == 1):
                        prevMove = cmd1
                        headerStr = ("MINIMAX AB: Wait, AI is choosing!\n------------------\nPLAYER: Chosen move: %s\n" % cmd1)
                        game.evalDiscBoardHeur(headerStr)
                        await game.msg1.edit(content=game.msg_text_1)
                        await game.msg2.edit(content=game.msg_text_2)
                        action, headerStr = game.choose_action(mode=0)
                        game.makeMoveCastle(action)
                        game.evalDiscBoardHeur(headerStr)
                        await game.msg1.edit(content=game.msg_text_1)
                        await game.msg2.edit(content=game.msg_text_2)
                    else:
                        await game.msg2.edit(content=(game.msg_text_2 + "\n\n**MOVE " + str(cmd1) + " NOT LEGAL, TRY AGAIN.**"))
            elif(game.gameState <= 0):
                if("1" in cmd1): 
                    game.gameState = 1
                    if("AI" in cmd1): 
                        game.aiRecState = 2
                        await msg.channel.send("You have chosen AI assisted manual mode!")
                        action, headerStr = game.choose_action(mode=2, init=True)
                    else:
                        game.aiRecState = 1
                        await msg.channel.send("You have chosen manual mode!")
                        action, headerStr = game.choose_action(mode=1, init=True)
                    game.evalDiscBoardHeur(headerStr)
                    game.msg1 = await msg.channel.send(game.msg_text_1)
                    game.msg2 = await msg.channel.send(game.msg_text_2)
                elif("2" in cmd1): 
                    game.gameState = 2
                    await msg.channel.send("You have chosen to play against an AI!")
                    headerStr = ("MINIMAX AB: Waiting...\n------------------\nPLAYER: Your turn!\n")
                    game.evalDiscBoardHeur(headerStr)
                    game.msg1 = await msg.channel.send(game.msg_text_1)
                    game.msg2 = await msg.channel.send(game.msg_text_2)
                elif("3" in cmd1): 
                    game.gameState = 3
                    await msg.channel.send("You have chosen to watch the AI play itself!")
                    headerStr = ("MINIMAX : Waiting...\n")
                    headerStr += ("------------------\n")
                    headerStr += ("MINIMAX : Waiting...\n")
                    game.evalDiscBoardHeur(headerStr)
                    game.msg1 = await msg.channel.send(game.msg_text_1)
                    game.msg2 = await msg.channel.send(game.msg_text_2)
                    prevMove = ""
                    while(game.gameOver() == False and game.gameState == 3):
                        action, headerStr = game.choose_action(mode=3, prevMove=prevMove)
                        print("Heuristic: ", game.heuristic)
                        game.makeMoveCastle(action)
                        game.evalDiscBoardHeur(headerStr)
                        await game.msg1.edit(content=game.msg_text_1)
                        await game.msg2.edit(content=game.msg_text_2)
                        prevMove = action
                        
                else:
                    game.gameState = -1
                    await msg.channel.send("That is not a recognized gamemode! Please try again.")

        #save everything to the dictionaries again (im not 100% sure this is needed)
        AIip_dict[discChannel] = AIip
        pid = pid_dict[discChannel]
        game = game_dict[discChannel]

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)