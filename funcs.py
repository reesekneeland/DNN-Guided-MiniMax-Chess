import chess
import time
import random
from positionMap import *
import math
import re

class MiniMaxChess:

    board = chess.Board()
    gameState = 0
    setState = 0

    def init(self):
        self.board = chess.Board()
        self.gameState = 0
        self.setState = 0

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
        return("Your board string is: %s" % self.board.fen())

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
            return 4.0
        elif(piece == chess.QUEEN):
            return 9.0

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
            returnStr += ("Stalemate! The game ends in a draw")
        else:
            returnStr += ("Possible moves for " + self.getCurPlayer() + ": " + str(self.getMoveList()))
        print(returnStr)
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

        eval_score, action = self.minimax(0,True,float('-inf'),float('inf'))
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

        eval_score, action = self.minimax(0,True,float('-inf'),float('inf'))
        return action

    def minimax(self, current_depth, is_max_turn, alpha, beta):

        if current_depth == 3 or self.gameOver():
            return self.heuristic(), ""

        possible_actions = self.getMoveList()

        # random.shuffle(possible_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for move_key in possible_actions:
            self.makeMoveHeur(str(move_key))

            eval_child, action_child = self.minimax(current_depth+1,not is_max_turn, alpha, beta)
            self.board.pop()
            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = move_key
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = move_key
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
        return best_value, action_target 