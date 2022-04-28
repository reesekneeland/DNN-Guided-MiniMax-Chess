import chess
import time
from positionMap import *
import math
import re
import sys
import random
import numpy as np
import multiprocessing
from itertools import starmap
import itertools
# import nn_prediction


class MiniMaxChess:

    def __init__(self, fen):
        self.board = chess.Board()
        try:
            self.board.set_fen(fen)
        except:
            self.board.set_fen(chess.STARTING_BOARD_FEN)
        self.board.castling_rights |= chess.BB_A8
        self.board.castling_rights |= chess.BB_A1
        self.board.castling_rights |= chess.BB_H1
        self.board.castling_rights |= chess.BB_H8
        self.positionMap = np.array([wPawnMap, wKnightMap, wBishopMap, wRookMap,wQueenMap, bPawnMap, bKnightMap, bBishopMap, bRookMap, bQueenMap])
        self.hash = [[[random.randint(1,2**64 - 1) for i in range(12)]for j in range(8)]for k in range(8)]
        self.hasBlackCastled = False
        self.hasWhiteCastled = False
        self.maxTime = 5
        self.maxDepth = 3
        self.hashMap = {}
        self.gameState = 0
        self.initialzed = 0
        self.aiRecState = 0 #set to 2 to enable AI assist messages in singleplayer, 1 to disable, 0 to not use
        self.AIstate = 0
        self.pid = -1
        self.msg_text_1 = ""
        self.msg_text_2 = ""
        self.msg1 = None
        self.msg2 = None

    def makeMoveHeur(self, sanStr):
        moveStr = str(self.board.parse_san(sanStr))
        if(self.makeMove(sanStr)):
            return self.heuristic()
        else:
            print("Move " + moveStr + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
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

    def makeMoveCastle(self, sanStr):
        try:
            moveStr = str(self.board.parse_san(sanStr))
            move = chess.Move.from_uci(moveStr)
        except:
            return 0
        if(move in self.board .legal_moves):
            print("MOVE: ", move, self.board.is_castling(move))
            if(self.board.is_castling(move)):
                print("IS CASTLING")
                if(self.board.turn == chess.WHITE):
                    self.hasWhiteCastled = True
                else:
                    self.hasBlackCastled = True
            print("WHITE", self.hasWhiteCastled)
            print("BLACK", self.hasBlackCastled)
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
        return fen

    def getBoardMap(self):
        color = chess.WHITE
        whiteAttackValMap = np.zeros(64)
        blackAttackValMap = np.zeros(64)
        posList = np.zeros((10, 64)).astype(int)
        for i in range(len(posList)):
            piece = i%5+1
            if(i==5):
                color = chess.BLACK
            if(i<5):
                posList[i] = np.array((self.board.pieces(piece, color).mirror().tolist())).astype(int)
                whiteAttackValMap += self.getAttackValue(piece) * posList[i].astype(int)
            else:
                posList[i] = -np.array((self.board.pieces(piece, color).mirror().tolist())).astype(int)
                blackAttackValMap += self.getAttackValue(piece) * posList[i].astype(int)
            posList[i] = self.getPieceValue(piece) * posList[i]
            posList[i] = np.add(posList[i], self.positionMap[i], where=(posList[i]>0))
        
        pieceMap = np.sum(posList, axis=0)
        return pieceMap, whiteAttackValMap, blackAttackValMap

    def getPieceMap(self):
        boardList = str(self.board)
        # print(boardList)
        pieceMap = np.zeros(64).astype(int)
        attackMap = np.zeros(64).astype(int)
        attackHash = {}
        attackTracker = np.zeros((12,64)).astype(int)
            #0 indicates how many white pieces are attacking the square
            #11 indicates how many black pieces are attacking the squares
            #1 indicates white pawns
            #2 indicates white knights
            #3 indicates white bishops
            #4 indicates white rooks
            #5 indicates white queens
            #6 indicates black pawns
            #7 indicates black knights
            #8 indicates black bishops
            #9 indicates black rooks
            #10 indicates black queens
            
            #8
        i=0
        #[wPawnMap, wKnightMap, wBishopMap, wRookMap,wQueenMap, bPawnMap, bKnightMap, bBishopMap, bRookMap, bQueenMap])
        for x in boardList:
            if x == ".":
                pieceMap[i] = 0
            elif x == "r":
                pieceMap[i] = -500 - self.positionMap[8][i]
                #DO THIS FOR ALL IF STATEMENTS
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap -= self.getAttackValue(chess.ROOK) * map
                attackTracker[11] += map
                attackTracker[9] += map
            elif x == "n":
                pieceMap[i] = -320 - self.positionMap[6][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap -= self.getAttackValue(chess.KNIGHT)* map
                attackTracker[11] += map
                attackTracker[7] += map
            elif x == "p":
                pieceMap[i] = -100 - self.positionMap[5][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap -= self.getAttackValue(chess.PAWN)* map
                attackTracker[11] += map
                attackTracker[6] += map
            elif x == "b":
                pieceMap[i] = -330 - self.positionMap[7][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap -= self.getAttackValue(chess.BISHOP)* map
                attackTracker[11] += map
                attackTracker[8] += map
            elif x == "q":
                pieceMap[i] = -900 - self.positionMap[9][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap -= self.getAttackValue(chess.QUEEN)* map
                attackTracker[11] += map
                attackTracker[10] += map
            elif x == "k":
                pieceMap[i] = 0
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap -= self.getAttackValue(chess.KING)* map
                attackTracker[11] += map
            elif x == "R":
                pieceMap[i] = 500 + self.positionMap[3][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap += self.getAttackValue(chess.ROOK)* map
                attackTracker[0] += map
                attackTracker[4] += map
            elif x == "N":
                pieceMap[i] = 320 + self.positionMap[1][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap += self.getAttackValue(chess.KNIGHT)* map
                attackTracker[0] += map
                attackTracker[2] += map
            elif x == "P":
                pieceMap[i] = 100 + self.positionMap[0][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap += self.getAttackValue(chess.PAWN)* map
                attackTracker[0] += map
                attackTracker[1] += map
            elif x == "B":
                pieceMap[i] = 330 + self.positionMap[2][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap += self.getAttackValue(chess.BISHOP)* map
                attackTracker[0] += map
                attackTracker[3] += map
            elif x == "Q":
                pieceMap[i] = 900 + self.positionMap[4][i]
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap += self.getAttackValue(chess.QUEEN)* map
                attackTracker[0] += map
                attackTracker[5] += map
            elif x == "K":
                pieceMap[i] = 0
                map = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                attackMap += self.getAttackValue(chess.KING)* map
                attackTracker[0] += map
            else:
                i-=1
            i+=1
        # print(self.makeReadable(pieceMap))
        # print(self.makeReadable(attackMap))
        # print(attackTracker)
        return pieceMap, attackMap, attackTracker

    def getAttackerMap(self, pieceMap, attackMap, attackTracker):
        retMap = pieceMap
        # print("piece\n", self.makeReadable(pieceMap))
        for i, square in enumerate(pieceMap):
            if(square != 0):
                #check for attacks from weaker pieces
                pieceType = self.board.piece_type_at(self.convertCoordinates(i))
                curPiece=pieceType-1
                while(curPiece>0):
                    # print("attacktracker[curPiece]",curPiece, self.makeReadable(attackTracker[curPiece]))
                    if(self.board.turn == chess.WHITE):
                        # print("WHITE TURN, SQUARE: COLOR", self.convertCoordinates(i), self.board.color_at(self.convertCoordinates(i)))
                        if(not self.board.color_at(self.convertCoordinates(i))): #square is black
                            if(attackTracker[curPiece][i]>0):
                                # print("MOD ACTIVATED", attackMap[i])
                                attackMap[i] = 10000
                                # print(attackMap[i])
                    else:                                                   
                        # print("BLACK TURN, SQUARE: COLOR", self.convertCoordinates(i), self.board.color_at(self.convertCoordinates(i)))     
                        if(self.board.color_at(self.convertCoordinates(i))):
                            if(attackTracker[curPiece+5][i]>0):
                                # print("MOD ACTIVATED", attackMap[i])
                                attackMap[i] = -10000
                                # print(attackMap[i])
                    curPiece -=1
                #check if both players are attacking a square to give defender advantage
                if(attackTracker[11][i]>0 and attackTracker[0][i]>0):
                    if(not self.board.color_at(self.convertCoordinates(i))):
                        attackMap[i] -= self.getAttackValue(pieceType) 
                    else:
                        attackMap[i] += self.getAttackValue(pieceType)
        #kamikaze prevention
        curPiece=5
        while(curPiece>0):
            for i, square in enumerate(pieceMap):
                attackVal = attackMap[i]
                pieceType = self.board.piece_type_at(self.convertCoordinates(i))
                if(pieceType==curPiece):
                    if(attackVal!=0):
                        if(self.board.turn == chess.BLACK):
                            if(square > 0 and attackVal<0): 
                                subMap = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                                attackMap-= self.getAttackValue(pieceType) * subMap
                        else:
                            if(square < 0 and attackVal>0): 
                                subMap = np.array((self.board.attacks(self.convertCoordinates(i)).mirror().tolist())).astype(int)
                                attackMap+=(self.getAttackValue(pieceType) * subMap)
            curPiece-=1
        #devalue insecure pieces
        for i, square in enumerate(pieceMap):
            if(square != 0):
                attackVal = attackMap[i]
                if(attackVal!=0):
                    if(square > 0):
                        if(attackVal<0):
                            retMap[i] = square/2
                    elif(square < 0):
                        if(attackVal>0):
                            retMap[i] = square/2

        # print("attackMap\n",self.makeReadable(attackMap))
        # print("retMap\n",self.makeReadable(retMap))
        return retMap

    def getIndex(self, piece):
    # mapping each piece to a particular number
        if (piece=='P'):
            return 0
        if (piece=='N'):
            return 1
        if (piece=='B'):
            return 2
        if (piece=='R'):
            return 3
        if (piece=='Q'):
            return 4
        if (piece=='K'):
            return 5
        if (piece=='p'):
            return 6
        if (piece=='n'):
            return 7
        if (piece=='b'):
            return 8
        if (piece=='r'):
            return 9
        if (piece=='q'):
            return 10
        if (piece=='k'):
            return 11
        else:
            return -1

    def computeHash(self, board):
        h = 0
        boardList = np.array(re.split(' |\n', str(board)))
        boardList = boardList.reshape((-1,8))
        for i in range(8):
            for j in range(8):
            # print board[i][j]
                if boardList[i][j] != '-':
                    piece = self.getIndex(boardList[i][j])
                    h ^= self.hash[i][j][piece]
        return h

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
            difference.append(int(list1_i)+int(list2_i))
        return difference

    def listMerge(self, list1, list2):
        difference = []
        zip_object = zip(list1, list2)
        for list1_i, list2_i in zip_object:
            if(list1_i == "1" or list2_i=="1"):
                difference.append("1")
            else:
                difference.append(".")
        return difference

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
            return 100
        elif(piece == chess.KNIGHT):
            return 320
        elif(piece == chess.BISHOP):
            return 330
        elif(piece == chess.ROOK):
            return 500
        elif(piece == chess.QUEEN):
            return 900

    def getAttackValue(self, piece):
        if(piece == chess.PAWN):
            return 900
        elif(piece == chess.KNIGHT):
            return 600
        elif(piece == chess.BISHOP):
            return 500
        elif(piece == chess.ROOK):
            return 200
        elif(piece == chess.QUEEN):
            return 100
        elif(piece == chess.KING):
            return 100

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

    def resetBoard(self):
        self.board.reset()
        print("Board has been reset")

    def gameOver(self):
        return self.board.is_game_over()
    
    def castleEval(self):
        val = 0
        if(self.board.has_castling_rights(chess.WHITE)==True):
            val+=3
        if(self.board.has_castling_rights(chess.BLACK)==True):
            val-=3
        if(self.hasWhiteCastled==True):
            val+=10
        if(self.hasBlackCastled==True):
            val-=10
        return val

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

        eStr += ("\n:black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:")
        return eStr

    def evalDiscBoardHeur(self, headerMsg):
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

    def evalDiscBoard(self, headerMsg):
        returnStr = headerMsg
        returnStr += self.emojiConvert()
        print(str(self.board))
        returnStr2 = ""
        
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

    def heuristic(self, move=""):
        if(str(self.board.result()) == "0-1"):
            return -100
        elif(str(self.board.result()) == "1-0"):
            return 100
        p, a, t = self.getPieceMap()
        attackMap = self.getAttackerMap(p, a, t)
        totalHeuristic = 83 * math.atan(sum(attackMap)/1500)
        totalHeuristic += self.castleEval()
        # print("castle eval", self.castleEval())
        # if(self.board.is_check()):
        #     if(self.board.turn ==chess.WHITE):
        #         totalHeuristic -=3
        #     else:
        #         totalHeuristic +=3 
        # self.hashMap[self.computeHash(self.board)] = round(totalHeuristic, 2)
        return round(totalHeuristic, 2)

    def choose_action(self, mode=0, init=False, prevMove=""): 
        #mode 0 for only AI predictions, 
        #mode 1 for player UI, 
        #mode 2 for player UI with AI input
        #init true if first move, false if not
        
        start_time = time.time()
        if(mode==0):
            if(self.getCurPlayer() == "white"):
                eval_score, action = self.minimax(self, self.getFen(),0,True,float('-inf'),float('inf'), start_time)
            else:
                eval_score, action = self.minimax(self, self.getFen(),0,False,float('-inf'),float('inf'), start_time)
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
            if(self.getCurPlayer() == "white"):
                eval_score, action = self.minimax(self, self.getFen(),0,True,float('-inf'),float('inf'), start_time)
            else:
                eval_score, action = self.minimax(self, self.getFen(),0,False,float('-inf'),float('inf'), start_time)
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
                if(self.getCurPlayer() == "white"):
                    eval_score, action = self.minimax(self, self.getFen(),0,True,float('-inf'),float('inf'), start_time)
                else:
                    eval_score, action = self.minimax(self, self.getFen(),0,False,float('-inf'),float('inf'), start_time)
                returnStr = ("MINIMAX : Previous move = %s\n" % prevMove)
                returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                returnStr += ("MINIMAX : Chosen move: %s\n" % action)
            else:
                if(init):
                    returnStr = ("MINIMAX : Chosen move: %s\n" % action)
                    returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
                    returnStr += ("MINIMAX : Waiting...\n")
                else:
                    if(self.getCurPlayer() == "white"):
                        eval_score, action = self.minimax(self, self.getFen(),0,True,float('-inf'),float('inf'), start_time)
                    else:
                        eval_score, action = self.minimax(self, self.getFen(),0,False,float('-inf'),float('inf'), start_time)
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
    def minimax(self, fen, current_depth, is_max_turn, alpha, beta, startTime):
        
        chessObj = MiniMaxChess(fen)
        possible_actions = chessObj.orderMoves(chessObj.getMoveList())
        best_value = float('-inf') if is_max_turn else float('inf')
        action = ""
        move_evals = []
        #move_evals_nn = []
        for move_key in possible_actions:
            ret = chessObj.makeMove(str(move_key))
            boardHash = self.computeHash(chessObj.board)
            if(boardHash in self.hashMap):
                heur = self.hashMap[boardHash]
            else:
                heur = chessObj.heuristic()
                self.hashMap[self.computeHash(chessObj.board)] = heur
            move_evals.append([move_key, heur])
            
            #Pass in Fen representation of possible move
            #neural_network_input = chessObj.board.fen()
            
            #Prediction of how much move will help or hinder player, currently prediction is within range [-15, 15]
            #prediction = nn_prediction(neural_network_input)
            #move_evals_nn = ([move_key, prediction])
            chessObj.board.pop()
        if(is_max_turn): 
            move_evals = sorted(move_evals, key=lambda x: -x[1])
        else:
            move_evals = sorted(move_evals, key=lambda x: x[1])
        for move_key, eval in move_evals:
            if(time.time()- startTime > self.maxTime):
                return best_value, str(action)
            ret = chessObj.makeMove(str(move_key))
            eval_child = MiniMaxChess.minimaxHelper(self, chessObj,current_depth+1,not is_max_turn, alpha, beta, str(move_key), eval, startTime)
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
            
        if(time.time()- startTime < self.maxTime):
            print(time.time()- startTime)
            self.maxDepth +=1
            print("DEEPENING SEARCH TO DEPTH: ", self.maxDepth)
            self.minimax(self, fen, current_depth, is_max_turn, alpha, beta, startTime)
        self.maxDepth = 3
        return best_value, str(action)

    def minimaxHelper(self, chessObj, current_depth, is_max_turn, alpha, beta, lastMove, heur, startTime):
        if (current_depth == self.maxDepth or chessObj.board.is_game_over() or time.time()- startTime > self.maxTime):
                return float(heur)
        possible_actions = chessObj.orderMoves(chessObj.getMoveList())
        best_value = float('-inf') if is_max_turn else float('inf')
        action = ""
        move_evals = []
        #move_evals_nn = [] #Uncomment when  we employ neural network
        for move_key in possible_actions:
            ret = chessObj.makeMove(str(move_key))
            boardHash = self.computeHash(chessObj.board)
            if(boardHash in self.hashMap):
                heur = self.hashMap[boardHash]
            else:
                heur = chessObj.heuristic()
                self.hashMap[self.computeHash(chessObj.board)] = heur
            move_evals.append([move_key, heur])
            #prediction = nn_prediction(chessObj.board) #Uncomment when we employ neural network
            #move_evals.append([move_key, prediction]) #Uncomment when we employ neural network
            chessObj.board.pop()
        # if(is_max_turn): 
        #     move_evals = np.array(sorted(move_evals, key=lambda x: -x[1]))
        #     if(float(min(move_evals[:,1])) < 0 < float(max(move_evals[:,1]))):
        #         idx = len(move_evals)
        #         sign_detector = move_evals[:,1].astype(float)
        #         valOne = sign_detector[0]
        #         for i in range(len(sign_detector)-1):
        #             if(valOne * sign_detector[i+1] < 0):
        #                 idx = i+1
        #                 break
        #             elif(sign_detector[i] != 0):
        #                 valOne = sign_detector[i]
        #         move_evals = move_evals[0:idx]
        # else:
        #     move_evals = np.array(sorted(move_evals, key=lambda x: x[1]))
        #     if(float(min(move_evals[:,1])) < 0 < float(max(move_evals[:,1]))):
        #         idx = len(move_evals)
        #         sign_detector = move_evals[:,1].astype(float)
        #         valOne = sign_detector[0]
        #         for i in range(len(sign_detector)-1):
        #             if(valOne * sign_detector[i+1] < 0):
        #                 idx = i+1
        #                 break
        #             elif(sign_detector[i] != 0):
        #                 valOne = sign_detector[i]
        #         move_evals = move_evals[0:idx]
        
        for move_key, eval in move_evals:
            if(time.time()- startTime > self.maxTime):
                return best_value
            ret = chessObj.makeMove(str(move_key))
            eval_child = MiniMaxChess.minimaxHelper(self, chessObj,current_depth+1,not is_max_turn, alpha, beta, str(move_key), eval, startTime)
            chessObj.board.pop()
            # print(eval_child)
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
        return best_value

    #MULTITHREADED MINIMAX, CURRENTLY NOT WORKING
    # @staticmethod
    # def minimaxMulti(fen, current_depth, is_max_turn, alpha, beta, is_fertile = True):

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
    #         ret = chessObj.makeMove(str(move_key))
    #         # print(chessObj.board.fen())
    #         # chessObj.evalBoard()

    #         eval_child, action_child = MiniMaxChess.minimaxMulti(str(chessObj.board.fen()),current_depth+1,not is_max_turn, alpha, beta, False)
            
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

def generateGameHeuristics(moveList):
    evalGame = MiniMaxChess(0)
    heurMoveList = []
    moveTuple = []
    for i, move in enumerate(moveList):
        moveTuple.append(move)
        heur = evalGame.makeMoveHeur(move)
        if(i%2 == 1):
            moveTuple.append(heur)
            heurMoveList.append(moveTuple)
            moveTuple = []
        elif(i==len(moveList)-1):
            moveTuple.append(heur)
            heurMoveList.append(moveTuple)

    return heurMoveList