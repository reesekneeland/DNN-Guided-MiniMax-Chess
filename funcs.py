import chess
import time
import random
from positionMap import *
import math
import re
import multiprocessing
from itertools import starmap
import itertools


class MiniMaxChess:

    def __init__(self, fen):
        self.board = chess.Board()
        try:
            self.board.set_fen(fen)
        except:
            self.board.set_fen(chess.STARTING_BOARD_FEN)
        self.gameState = 0
        self.initialzed = 0
        self.aiRecState = 0 #set to 2 to enable AI assist messages in singleplayer, 1 to disable, 0 to not use
        self.AIstate = 0
        self.pid = -1
        self.msg_text_1 = ""
        self.msg_text_2 = ""
        self.msg1 = None
        self.msg2 = None

    def makeMovePure(self, sanStr):
        try:
            moveStr = str(self.board.parse_san(sanStr))
            move = chess.Move.from_uci(moveStr)
            if(move in self.board.legal_moves):
                self.board .push(move)
            else:
                print("Move " + move + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
        except:
            print("Move " + sanStr + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))


    def makeMoveHeur(self, sanStr):
        try:
            moveStr = str(self.board.parse_san(sanStr))
            move = chess.Move.from_uci(moveStr)
            if(move in self.board.legal_moves):
                self.board .push(move)
                heur = self.heuristic()
                return heur
            else:
                print("Move " + move + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
                return -10000
        except:
            print("Move " + sanStr + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
            return -10000
        

    def makeMove(self, sanStr):
        try:
            moveStr = str(self.board.parse_san(sanStr))
            move = chess.Move.from_uci(moveStr)
        except:
            return 0
        if(move in self.board .legal_moves):
            self.board.push(move)
            return 1
        else:
            return 0

    def getMoveList(self):
        moveStrList = str(self.board.legal_moves)
        moveStrList = moveStrList[39:-2]
        moveList = moveStrList.split(", ")
        return moveList

    def convertCoordinates(self, i):
        notationMap = [
            56, 57, 58, 59, 60, 61, 62, 63,
            48, 49, 50, 51, 52, 53, 54, 55,
            40, 41, 42, 43, 44, 45, 46, 47,
            32, 33, 34, 35, 36, 37, 38 ,39,
            24, 25, 26, 27, 28, 29, 30, 31,
            16, 17, 18, 19, 20, 21, 22, 23,
            8, 9, 10, 11, 12, 13, 14, 15,
            0, 1, 2, 3, 4, 5, 6, 7
        ]
        return notationMap[i]

    def getFen(self):
        return(self.board.fen())

    def setFen(self, fen):
        self.board.set_fen(fen)
        return("Board has been set to: " + fen)

    def getMultiplierMap(self, piece, color):
        if(color == chess.BLACK):
            if(piece == chess.PAWN):
                return blackPawnMap
            elif(piece == chess.KNIGHT):
                return blackKnightMap
            elif(piece == chess.BISHOP):
                return blackBishopMap
            elif(piece == chess.ROOK):
                return blackRookMap
            elif(piece == chess.QUEEN):
                return blackQueenMap
        if(color == chess.WHITE):
            if(piece == chess.PAWN):
                return whitePawnMap
            elif(piece == chess.KNIGHT):
                return whiteKnightMap
            elif(piece == chess.BISHOP):
                return whiteBishopMap
            elif(piece == chess.ROOK):
                return whiteRookMap
            elif(piece == chess.QUEEN):
                return whiteQueenMap

    def getBoardMap(self):
        whitePStr = str(self.board.pieces(chess.PAWN, chess.WHITE))
        whitePStr.replace(".", "0.0")
        whitePList = re.split(' |\n', whitePStr)
        whiteBStr = str(self.board.pieces(chess.BISHOP, chess.WHITE))
        whiteBStr.replace(".", "0.0")
        whiteBList = re.split(' |\n', whiteBStr)
        whiteKnStr = str(self.board.pieces(chess.KNIGHT, chess.WHITE))
        whiteKnStr.replace(".", "0.0")
        whiteKnList = re.split(' |\n', whiteKnStr)
        whiteRStr = str(self.board.pieces(chess.ROOK, chess.WHITE))
        whiteRStr.replace(".", "0.0")
        whiteRList = re.split(' |\n', whiteRStr)
        whiteQStr = str(self.board.pieces(chess.QUEEN, chess.WHITE))
        whiteQStr.replace(".", "0.0")
        whiteQList = re.split(' |\n', whiteQStr)
        blackPStr = str(self.board.pieces(chess.PAWN, chess.BLACK))
        blackPStr.replace(".", "0.0")
        blackPList = re.split(' |\n', blackPStr)
        blackBStr = str(self.board.pieces(chess.BISHOP, chess.BLACK))
        blackBStr.replace(".", "0.0")
        blackBList = re.split(' |\n', blackBStr)
        blackKnStr = str(self.board.pieces(chess.KNIGHT, chess.BLACK))
        blackKnStr.replace(".", "0.0")
        blackKnList = re.split(' |\n', blackKnStr)
        blackRStr = str(self.board.pieces(chess.ROOK, chess.BLACK))
        blackRStr.replace(".", "0.0")
        blackRList = re.split(' |\n', blackRStr)
        blackQStr = str(self.board.pieces(chess.QUEEN, chess.BLACK))
        blackQStr.replace(".", "0.0")
        blackQList = re.split(' |\n', blackQStr)
        pieceMap = []
        for i in range(0, 64):
            if(whitePList[i] == "1"):
                appendVal = 1.0 * self.getMultiplierMap(chess.PAWN, chess.WHITE)[i]
            elif(whiteBList[i] == "1"):
                appendVal = 3.0 * self.getMultiplierMap(chess.BISHOP, chess.WHITE)[i]
            elif(whiteKnList[i] == "1"):
                appendVal = 3.0 * self.getMultiplierMap(chess.KNIGHT, chess.WHITE)[i]
            elif(whiteQList[i] == "1"):
                appendVal = 9.0 * self.getMultiplierMap(chess.QUEEN, chess.WHITE)[i]
            elif(whiteRList[i] == "1"):
                appendVal = 5.0 * self.getMultiplierMap(chess.ROOK, chess.WHITE)[i]
            elif(blackPList[i] == "1"):
                appendVal = -1.0 * self.getMultiplierMap(chess.PAWN, chess.BLACK)[i]
            elif(blackBList[i] == "1"):
                appendVal = -3.0 * self.getMultiplierMap(chess.BISHOP, chess.BLACK)[i]
            elif(blackKnList[i] == "1"):
                appendVal = -3.0 * self.getMultiplierMap(chess.KNIGHT, chess.BLACK)[i]
            elif(blackQList[i] == "1"):
                appendVal = -9.0 * self.getMultiplierMap(chess.QUEEN, chess.BLACK)[i]
            elif(blackRList[i] == "1"):
                appendVal = -5.0 * self.getMultiplierMap(chess.ROOK, chess.BLACK)[i]
            else:
                appendVal = 0.0
            pieceMap.append(round(appendVal, 2))
        res_list = []
        attackMap = self.getAttackerMap()
        for i in range(0, len(pieceMap)):
            if(pieceMap[i] > 0 and attackMap[i] < 0):
                attacks = self.getAttacks(self.convertCoordinates(i))
                attackMap = self.listSub(attackMap, attacks)
            if(pieceMap[i] < 0 and attackMap[i] > 0):
                attacks = self.getAttacks(self.convertCoordinates(i))
                attackMap = self.listAdd(attackMap, attacks)
        for i in range(0, len(pieceMap)):
            if(pieceMap[i] > 0):
                if(attackMap[i] >= 0):
                    attackFactor = 1.0 + attackMap[i]/5
                else:
                    attackFactor = 0.1
            elif(pieceMap[i] < 0):
                if(attackMap[i] <= 0):
                    attackFactor = 1.0 + attackMap[i]/-5
                else:
                    attackFactor = 0.1
            else:
                attackFactor = 1.0

            res_list.append(round(pieceMap[i] * attackFactor, 2))
        return res_list
            
    def listSub(self, list1, list2):
        difference = []
        zip_object = zip(list1, list2)
        for list1_i, list2_i in zip_object:
            difference.append(list1_i-list2_i)
        return difference

    def listAdd(self, list1, list2):
        difference = []
        zip_object = zip(list1, list2)
        for list1_i, list2_i in zip_object:
            difference.append(list1_i+list2_i)
        return difference

    def getPieceMap(self, piece, color):
        multiplierMap = self.getMultiplierMap(piece, color)
        boardStr = str(self.board.pieces(piece, color))
        boardStr.replace(".", "0.0")
        boardList = re.split(' |\n', boardStr)
        for x, value in enumerate(boardList):
            if(value == "."):
                boardList[x] = 0.0
            if(value == "1"):
                boardList[x] = 1.0 * self.getPieceValue(piece)

        res_list = []
        for i in range(0, len(boardList)):
            if(self.getAttackers(i, color) >= 0):
                attackFactor = 1.0 + self.getAttackers(i, color)/3
            else:
                attackFactor = 0.1
            res_list.append(boardList[i] * multiplierMap[i] * attackFactor)
        return res_list

    def getAttackers(self, square, color):
        if(color == chess.WHITE):
            return len(self.board.attackers(chess.BLACK, square)) - len(self.board.attackers(chess.WHITE, square))
        elif(color == chess.BLACK):
            return len(self.board.attackers(chess.WHITE, square)) - len(self.board.attackers(chess.BLACK, square))

    def getAttacks(self, square):
        boardStr = str(self.board.attacks(square))
        boardStr.replace(".", "0")
        boardList = re.split(' |\n', boardStr)
        for x, value in enumerate(boardList):
            if(value == "."):
                boardList[x] = 0
            if(value == "1"):
                boardList[x] = 1
        return boardList

    def getAttackerMap(self):
        attackList = []
        for x in range(0, 64):
            attackList.append(-1000)
        for i in range(0, 64):
            attackList[self.convertCoordinates(i)] = self.getAttackers(i, chess.BLACK)
        return attackList

    def makeReadable(self, llist):
        returnStr = ""
        x=0
        for i in llist:   
            if(x%8 == 0):
                returnStr += " \n"
            returnStr += " " + str(i)
            x+=1
        return returnStr

    def getPieceValue(self, piece):
        if(piece == chess.PAWN):
            return 1.0
        elif(piece == chess.KNIGHT):
            return 3.0
        elif(piece == chess.BISHOP):
            return 3.0
        elif(piece == chess.ROOK):
            return 5.0
        elif(piece == chess.QUEEN):
            return 9.0
    def getBoard(self):
        return self.board

    def getCurPlayer(self):
        if(self.board.turn == chess.WHITE):
            return "white"
        else:
            return "black"

    def getNextPlayer(self):
        if(self.board.turn == chess.WHITE):
            return "black"
        else:
            return "white"

    def undoMove(self):
        self.board.pop()
        print("Move undone")
        return self.evalBoard()

    def resetBoard(self):
        self.board.reset()
        print("Board has been reset")


    def whiteValue(self):
        pawnv = len(self.board.pieces(chess.PAWN, chess.WHITE))
        knightv = 3 * len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bishopv = 3 * len(self.board.pieces(chess.BISHOP, chess.WHITE))
        rookv = 5 * len(self.board.pieces(chess.ROOK, chess.WHITE))
        queenv = 9 * len(self.board.pieces(chess.QUEEN, chess.WHITE))
        return pawnv + knightv + bishopv + rookv + queenv

    def blackValue(self):
        pawnv = len(self.board.pieces(chess.PAWN, chess.BLACK))
        knightv = 3 * len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        bishopv = 3 * len(self.board.pieces(chess.BISHOP, chess.BLACK))
        rookv = 5 * len(self.board.pieces(chess.ROOK, chess.BLACK))
        queenv = 9 * len(self.board.pieces(chess.QUEEN, chess.BLACK))
        return pawnv + knightv + bishopv + rookv + queenv

    def gameOver(self):
        return self.board.is_game_over()

    def emojiConvert(self):
        boardStr = str(self.board)
        eStr = ""
        count = 0
        for x in boardStr:
            count += 1
            if(count == 1):
                eStr += ":eight:"
            if(count == 10):
                eStr += ":seven:"
            if(count == 19):
                eStr += ":six:"
            if(count == 28):
                eStr += ":five:"
            if(count == 37):
                eStr += ":four:"
            if(count == 46):
                eStr += ":three:"
            if(count == 55):
                eStr += ":two:"
            if(count == 64):
                eStr += ":one:"
            if x == "\n":
                eStr += ("\n")
            elif x == ".":
                if (count % 2) == 0:
                    eStr += ("<:ds:835909517304660009>")
                else:
                    eStr += ("<:ls:835909517572177970>")
            elif x == "r":
                if (count % 2) == 0:
                    eStr += ("<:bdr:835909517656457257>")
                else:
                    eStr += ("<:blr:835909517644267530>")
            elif x == "n":
                if (count % 2) == 0:
                    eStr += ("<:bdn:835909517665501234>")
                else:
                    eStr += ("<:bln:835909517710852136>")
            elif x == "p":
                if (count % 2) == 0:
                    eStr += ("<:bd:835909517652787273>")
                else:
                    eStr += ("<:bl:835909517781762098>")
            elif x == "b":
                if (count % 2) == 0:
                    eStr += ("<:bdb:835909517530890322>")
                else:
                    eStr += ("<:blb:835909517178699861>")
            elif x == "q":
                if (count % 2) == 0:
                    eStr += ("<:bdq:835909517404536844>")
                else:
                    eStr += ("<:blq:835909517744930876>")
            elif x == "k":
                if (count % 2) == 0:
                    eStr += ("<:bdk:835909517543211029>")
                else:
                    eStr += ("<:blk:835910672054222868>")
            elif x == "R":
                if (count % 2) == 0:
                    eStr += ("<:wdr:835909517564444733>")
                else:
                    eStr += ("<:wlr:835909517786087444>")
            elif x == "N":
                if (count % 2) == 0:
                    eStr += ("<:wdn:835909517896187945>")
                else:
                    eStr += ("<:wln:835909517451067423>")
            elif x == "P":
                if (count % 2) == 0:
                    eStr += ("<:wd:835909517769179198>")
                else:
                    eStr += ("<:wl:835909517883342879>")
            elif x == "B":
                if (count % 2) == 0:
                    eStr += ("<:wdb:835909517635223633>")
                else:
                    eStr += ("<:wlb:835909517882687508>")
            elif x == "Q":
                if (count % 2) == 0:
                    eStr += ("<:wdq:835909517911785523>")
                else:
                    eStr += ("<:wlq:835909517806927912>")
            elif x == "K":
                if (count % 2) == 0:
                    eStr += ("<:wdk:835909517500874804>")
                else:
                    eStr += ("<:wlk:835909517635485757>")
            else:
                count -= 1
            
            # if(count == 27):
            #     eStr2 = eStr
            #     eStr = ""
            # if(count == 54):
            #     eStr3 = eStr
            #     eStr = ""
        eStr += ("\n:black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:")
        # return eStr2, eStr3, eStr
        return eStr

    def evalDiscBoard(self, headerMsg):
        returnStr = headerMsg
        returnStr += self.emojiConvert()
        print(str(self.board))
        returnStr2 = ("\nCurrent Heuristic: " + str(self.heuristic()) + "\n")
        
        if(self.board.is_checkmate()):
            returnStr2 += ("\n" + self.getCurPlayer() + " has been checkmated! " + self.getNextPlayer() + " wins!")
        elif(self.board.is_check()):
            returnStr2 += ("\n" + self.getCurPlayer() + " is in check! Possible moves are: " + str(self.getMoveList()))
        elif(self.board.is_stalemate()):
            returnStr2 += ("\nStalemate! The game ends in a draw")
        else:
            returnStr2 += ("\nPossible moves for " + self.getCurPlayer() + ": " + str(self.getMoveList()))
        self.msg_text_1 = returnStr
        self.msg_text_2 = returnStr2

    def evalBoard(self):
        returnStr = "\nblack\n"
        returnStr += ("```" + str(self.board) + "```")
        returnStr += ("white\n")
        returnStr += ("Current Heuristic: " + str(self.heuristic()) + "\n")
        
        if(self.board.is_checkmate()):
            returnStr += (self.getCurPlayer() + " has been checkmated! " + self.getNextPlayer() + " wins!")
        elif(self.board.is_check()):
            returnStr += (self.getCurPlayer() + " is in check! Possible moves are: " + str(self.getMoveList()))
        elif(self.board.is_stalemate()):
            returnStr += ("Stalemate! The game en        print(attackMap)ds in a draw")
        else:
            returnStr += ("Possible moves for " + self.getCurPlayer() + ": " + str(self.getMoveList()))
        print(returnStr)
        # print(self.emojiConvert())
        return returnStr

    def heuristic(self):
        if(str(self.board.result()) == "0-1"):
            return -100
        elif(str(self.board.result()) == "1-0"):
            return 100
        positionDif = sum(self.getBoardMap())
        pointDif = self.whiteValue() - self.blackValue()
        positionHeuristic = 83 * math.atan(positionDif/15)
        valueHeuristic = 83 * math.atan(pointDif/15)
        totalHeuristic = 0.8 * valueHeuristic + 0.2 * positionHeuristic
        return round(totalHeuristic, 2)

    def choose_action(self, mode=0, init=False, prevMove=""): 
        #mode 0 for only AI predictions, 
        #mode 1 for player UI, 
        #mode 2 for player UI with AI input
        #init true if first move, false if not
        
        start_time = time.time()
        if(self.getCurPlayer() == "white"):
            eval_score, action = self.minimax2(self.getFen(),0,True,float('-inf'),float('inf'))
        else:
            eval_score, action = self.minimax2(self.getFen(),0,False,float('-inf'),float('inf'))
        if(mode==0):
            returnStr = ("MINIMAX : Done, chosen move = %s\n" % action)
            returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
            returnStr += ("PLAYER : Your turn!\n")
        elif(mode==1):
            if(self.getCurPlayer() == "black"):
                returnStr = ("PLAYER1 : Done, chosen move = %s\n" % prevMove)
                returnStr += ("------------------\n")
                returnStr += ("PLAYER2 : Your turn!\n")
            else:
                if(init):
                    returnStr = ("PLAYER1 : Your turn!\n")
                    returnStr += ("------------------\n")
                    returnStr += ("PLAYER2 : Waiting...\n")
                else:
                    returnStr = ("PLAYER1 : Your turn!\n")
                    returnStr += ("------------------\n")
                    returnStr += ("PLAYER2 : Done, chosen move = %s\n" % prevMove)
        elif(mode==2):
            if(self.getCurPlayer() == "black"):
                returnStr = ("PLAYER1 : Done, chosen move = %s\n" % prevMove)
                returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                returnStr += ("PLAYER2 : Your turn! AI recommended move: %s\n" % action)
            else:
                if(init):
                    returnStr = ("PLAYER1 : Your turn! AI recommended move: %s\n" % action)
                    returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                    returnStr += ("PLAYER2 : Waiting...\n")
                else:
                    returnStr = ("PLAYER1 : Your turn! AI recommended move: %s\n" % action)
                    returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                    returnStr += ("PLAYER2 : Done, chosen move = %s\n" % prevMove)
        elif(mode==3):
            if(self.getCurPlayer() == "black"):
                returnStr = ("MINIMAX : Previous move = %s\n" % prevMove)
                returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                returnStr += ("MINIMAX : Chosen move: %s\n" % action)
            else:
                if(init):
                    returnStr = ("MINIMAX : Chosen move: %s\n" % action)
                    returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                    returnStr += ("MINIMAX : Waiting...\n")
                else:
                    returnStr = ("MINIMAX : Chosen move: %s\n" % action)
                    returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                    returnStr += ("MINIMAX : Previous move = %s\n" % prevMove)
        return action, returnStr

    def orderMoves(self, moveList):
        optimalList = []
        regularList = []
        for move in moveList:
            if "+" in move:
                optimalList.append(move)
            elif "x" in move:
                optimalList.append(move)
            elif "#" in move:
                optimalList.append(move)
            else:
                regularList.append(move)
        optimalList += regularList
        return optimalList

    @staticmethod
    def minimax2(fen, current_depth, is_max_turn, alpha, beta):
        chessObj = MiniMaxChess(fen)
        if (current_depth == 3 or chessObj.board.is_game_over()):
            return chessObj.heuristic(), ""
        possible_actions = chessObj.orderMoves(chessObj.getMoveList())
        best_value = float('-inf') if is_max_turn else float('inf')
        action = ""
        for move_key in possible_actions:
            chessObj.makeMovePure(str(move_key))
            eval_child, action_child = MiniMaxChess.minimax2(str(chessObj.board.fen()),current_depth+1,not is_max_turn, alpha, beta)

            chessObj.board.pop()
            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action = move_key
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action = move_key
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
        return best_value, str(action)

    # @staticmethod
    # def minimax(fen, current_depth, is_max_turn, alpha, beta, is_fertile = True):

    #     MAX_PROCESSES = 32

    #     chessObj = MiniMaxChess(fen)
    #     if (current_depth == 4 or chessObj.board.is_game_over()):
    #         return chessObj.heuristic(), ""

    #     possible_actions = chessObj.getMoveList()
    #     # print(possible_actions)
    #     random.shuffle(possible_actions) #randomness
    #     best_value = float('-inf') if is_max_turn else float('inf')
    #     action = ""

    #     args = []

    #     if not is_fertile:
    #         args = [(fen, current_depth, is_max_turn, alpha, beta, possible_actions, chessObj)]
    #     else:
    #         x = 0
    #         if len(possible_actions) < MAX_PROCESSES:
    #             MAX_PROCESSES = len(possible_actions)
    #         while x < len(possible_actions):
    #             args = args + [(fen, current_depth, is_max_turn, alpha, beta, possible_actions[x:x + int(len(possible_actions)/MAX_PROCESSES)], chessObj)] if x + len(possible_actions)/MAX_PROCESSES < len(possible_actions) else args + [(fen, current_depth, is_max_turn, alpha, beta, possible_actions[x:], chessObj)]
    #             x += int(len(possible_actions) / MAX_PROCESSES)

    #     ret_obj_l = []
    #     if is_fertile:
    #         with multiprocessing.Pool(MAX_PROCESSES) as pool:
    #             ret_obj_l = pool.starmap(MiniMaxChess.minimax_helper, args)
    #     else:
    #         ret_obj_l2 = itertools.starmap(MiniMaxChess.minimax_helper, args)
    #         for x in ret_obj_l2:
    #             ret_obj_l += x
    #         return ret_obj_l[0], ret_obj_l[1]
    #     for ret_obj in ret_obj_l:
    #         if(is_max_turn):
    #             if ret_obj[0] > best_value:
    #                 action = ret_obj[1]
    #                 best_value = ret_obj[0]
    #         else:
    #             if ret_obj[0] < best_value:
    #                 action = ret_obj[1]
    #                 best_value = ret_obj[0]
    #     # print("Depth: " + str(current_depth) + " My chosen action is: " + str(action) + " with score: " + str(best_value)) #debugging line
    #     return best_value, str(action)

    # @staticmethod
    # def minimax_helper(fen, current_depth, is_max_turn, alpha, beta, possible_actions, chessObj):
    #     best_value = float('-inf') if is_max_turn else float('inf')
    #     action = ""
    #     for move_key in possible_actions:
    #         chessObj.makeMovePure(str(move_key))
    #         # print(chessObj.board.fen())
    #         # chessObj.evalBoard()

    #         eval_child, action_child = MiniMaxChess.minimax(str(chessObj.board.fen()),current_depth+1,not is_max_turn, alpha, beta, False)
            
    #         chessObj.board.pop()
    #         if is_max_turn and best_value < eval_child:
    #             best_value = eval_child
    #             action = move_key
    #             alpha = max(alpha, best_value)
    #             if beta <= alpha:
    #                 break

    #         elif (not is_max_turn) and best_value > eval_child:
    #             best_value = eval_child
    #             action = move_key
    #             beta = min(beta, best_value)
    #             if beta <= alpha:
    #                 break
    #     return best_value, action