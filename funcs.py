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
        self.setState = 0
        self.pid = -1

    def makeMovePure(self, sanStr):
        try:
            moveStr = str(self.board.parse_san(sanStr))
            move = chess.Move.from_uci(moveStr)
        except:
            print("Move " + sanStr + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
        if(move in self.board.legal_moves):
            self.board .push(move)
        else:
            print("Move " + move + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))

    def makeMoveHeur(self, sanStr):
        try:
            moveStr = str(self.board.parse_san(sanStr))
            move = chess.Move.from_uci(moveStr)
        except:
            print("Move " + sanStr + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
            return -10000
        if(move in self.board.legal_moves):
            self.board .push(move)
            heur = self.heuristic()
            return heur
        else:
            print("Move " + move + " not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
            return -10000

    def makeMove(self, sanStr):
        try:
            moveStr = str(self.board.parse_san(sanStr))
            move = chess.Move.from_uci(moveStr)
        except:
            print("Move not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
            return 0
        if(move in self.board .legal_moves):
            self.board.push(move)
            return 1
        else:
            print("Move not legal, try again. The legal moves for " + self.getCurPlayer() + " are : " + str(self.getMoveList()))
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
        for i in range(0, len(pieceMap)):
            if(pieceMap[i] > 0):
                if(self.getAttackers(self.convertCoordinates(i), chess.BLACK) >= 0):
                    attackFactor = 1.0 + self.getAttackers(self.convertCoordinates(i), chess.BLACK)/5
                else:
                    attackFactor = 0.1
            elif(pieceMap[i] < 0):
                if(self.getAttackers(self.convertCoordinates(i), chess.WHITE) >= 0):
                    attackFactor = 1.0 + self.getAttackers(self.convertCoordinates(i), chess.WHITE)/5
                else:
                    attackFactor = 0.1
            else:
                attackFactor = 1.0

            res_list.append(round(pieceMap[i] * attackFactor, 2))
        return res_list
            

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

    def getAttackerMap(self):
        attackList = []
        for i in range(0, 64):
            attackList.append(self.getAttackers(i, self.board.turn))
        return attackList

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
        return ("Board has been reset. Welcome to MiniMax Chess! Please enter the type of game you would like to play, 1 for singleplayer, 2 to play vs an AI, and 3 to have the AI play itself")


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
                    eStr += ("<:dark_square:835909517304660009>")
                else:
                    eStr += ("<:light_square:835909517572177970>")
            elif x == "r":
                if (count % 2) == 0:
                    eStr += ("<:b_d_rook:835909517656457257>")
                else:
                    eStr += ("<:b_l_rook:835909517644267530>")
            elif x == "n":
                if (count % 2) == 0:
                    eStr += ("<:b_d_knight:835909517665501234>")
                else:
                    eStr += ("<:b_l_knight:835909517710852136>")
            elif x == "p":
                if (count % 2) == 0:
                    eStr += ("<:b_d_pawn:835909517652787273>")
                else:
                    eStr += ("<:b_l_pawn:835909517781762098>")
            elif x == "b":
                if (count % 2) == 0:
                    eStr += ("<:b_d_bishop:835909517530890322>")
                else:
                    eStr += ("<:b_l_bishop:835909517178699861>")
            elif x == "q":
                if (count % 2) == 0:
                    eStr += ("<:b_d_queen:835909517404536844>")
                else:
                    eStr += ("<:b_l_queen:835909517744930876>")
            elif x == "k":
                if (count % 2) == 0:
                    eStr += ("<:b_d_king:835909517543211029>")
                else:
                    eStr += ("<:b_l_king:835910672054222868>")
            elif x == "R":
                if (count % 2) == 0:
                    eStr += ("<:w_d_rook:835909517564444733>")
                else:
                    eStr += ("<:w_l_rook:835909517786087444>")
            elif x == "N":
                if (count % 2) == 0:
                    eStr += ("<:w_d_knight:835909517896187945>")
                else:
                    eStr += ("<:w_l_knight:835909517451067423>")
            elif x == "P":
                if (count % 2) == 0:
                    eStr += ("<:w_d_pawn:835909517769179198>")
                else:
                    eStr += ("<:w_l_pawn:835909517883342879>")
            elif x == "B":
                if (count % 2) == 0:
                    eStr += ("<:w_d_bishop:835909517635223633>")
                else:
                    eStr += ("<:w_l_bishop:835909517882687508>")
            elif x == "Q":
                if (count % 2) == 0:
                    eStr += ("<:w_d_queen:835909517911785523>")
                else:
                    eStr += ("<:w_l_queen:835909517806927912>")
            elif x == "K":
                if (count % 2) == 0:
                    eStr += ("<:w_d_king:835909517500874804>")
                else:
                    eStr += ("<:w_l_king:835909517635485757>")
            else:
                count -= 1
            
            if(count == 27):
                eStr2 = eStr
                eStr = ""
            if(count == 54):
                eStr3 = eStr
                eStr = ""
        eStr += ("\n:black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:")
        return eStr2, eStr3, eStr

    def evalDiscBoard(self):
        returnStr, returnStr2, returnStr3 = self.emojiConvert()
        print("calculating msg4")
        returnStr4 = ("\nCurrent Heuristic: " + str(self.heuristic()) + "\n")
        
        if(self.board.is_checkmate()):
            returnStr4 += ("\n" + self.getCurPlayer() + " has been checkmated! " + self.getNextPlayer() + " wins!")
        elif(self.board.is_check()):
            returnStr4 += ("\n" + self.getCurPlayer() + " is in check! Possible moves are: " + str(self.getMoveList()))
        elif(self.board.is_stalemate()):
            returnStr4 += ("\nStalemate! The game ends in a draw")
        else:
            returnStr4 += ("\nPossible moves for " + self.getCurPlayer() + ": " + str(self.getMoveList()))
        print(returnStr + returnStr2 + returnStr3 + returnStr4)
        return returnStr, returnStr2, returnStr3, returnStr4

    def evalBoard(self):
        returnStr = "\nblack\n"
        returnStr += ("```" + str(self.board) + "```")
        returnStr += ("white\n")
        # returnStr += ("Current Heuristic: " + str(self.heuristic()) + "\n")
        
        if(self.board.is_checkmate()):
            returnStr += (self.getCurPlayer() + " has been checkmated! " + self.getNextPlayer() + " wins!")
        elif(self.board.is_check()):
            returnStr += (self.getCurPlayer() + " is in check! Possible moves are: " + str(self.getMoveList()))
        elif(self.board.is_stalemate()):
            returnStr += ("Stalemate! The game ends in a draw")
        else:
            returnStr += ("Possible moves for " + self.getCurPlayer() + ": " + str(self.getMoveList()))
        print(returnStr)
        print(self.emojiConvert())
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

    def choose_action(self):
        # """
        # Predict the move using minimax algorithm
        # Parameters
        # ----------
        # board : board
        # Returns
        # -------
        # float, str:
        #     The evaluation or utility and the action key name
        # """

        start_time = time.time()

        eval_score, action = self.minimax(self.getFen(),0,True,float('-inf'),float('inf'))
        returnStr = ("MINIMAX : Done, eval = %d\n" % (eval_score))
        returnStr += ("--- %s seconds ---\n" % str(round((time.time() - start_time), 3)))
        returnStr += ("MINIMAX : Chosen move: %s" % action)
        return returnStr

    def choose_action_pure(self):
        # """
        # Predict the move using minimax algorithm
        # Parameters
        # ----------
        # board : board
        # Returns
        # -------
        # float, str:
        #     The evaluation or utility and the action key name
        # """

        eval_score, action = self.minimax(self.getFen(), 0,True,float('-inf'),float('inf'))
        return action

    @staticmethod
    def minimax(fen, current_depth, is_max_turn, alpha, beta, is_fertile = True):

        MAX_PROCESSES = 32

        chessObj = MiniMaxChess(fen)
        if (current_depth == 4 or chessObj.board.is_game_over()):
            return chessObj.heuristic(), ""

        possible_actions = chessObj.getMoveList()
        # print(possible_actions)
        random.shuffle(possible_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action = ""

        args = []

        if not is_fertile:
            args = [(fen, current_depth, is_max_turn, alpha, beta, possible_actions, chessObj)]
        else:
            x = 0
            if len(possible_actions) < MAX_PROCESSES:
                MAX_PROCESSES = len(possible_actions)
            while x < len(possible_actions):
                args = args + [(fen, current_depth, is_max_turn, alpha, beta, possible_actions[x:x + int(len(possible_actions)/MAX_PROCESSES)], chessObj)] if x + len(possible_actions)/MAX_PROCESSES < len(possible_actions) else args + [(fen, current_depth, is_max_turn, alpha, beta, possible_actions[x:], chessObj)]
                x += int(len(possible_actions) / MAX_PROCESSES)

        ret_obj_l = []
        if is_fertile:
            with multiprocessing.Pool(MAX_PROCESSES) as pool:
                ret_obj_l = pool.starmap(MiniMaxChess.minimax_helper, args)
        else:
            ret_obj_l2 = itertools.starmap(MiniMaxChess.minimax_helper, args)
            for x in ret_obj_l2:
                ret_obj_l += x
            return ret_obj_l[0], ret_obj_l[1]
        for ret_obj in ret_obj_l:
            if ret_obj[0] > best_value:
                action = ret_obj[1]
                best_value = ret_obj[0]

        # print("Depth: " + str(current_depth) + " My chosen action is: " + str(action) + " with score: " + str(best_value)) #debugging line
        return best_value, str(action)

    @staticmethod
    def minimax_helper(fen, current_depth, is_max_turn, alpha, beta, possible_actions, chessObj):
        best_value = float('-inf') if is_max_turn else float('inf')
        action = ""
        for move_key in possible_actions:
            chessObj.makeMovePure(str(move_key))
            # print(chessObj.board.fen())
            # chessObj.evalBoard()

            eval_child, action_child = MiniMaxChess.minimax(str(chessObj.board.fen()),current_depth+1,not is_max_turn, alpha, beta, False)
            
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
        return best_value, action