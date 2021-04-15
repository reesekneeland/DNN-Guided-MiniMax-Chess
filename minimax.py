import chess
import sys
from funcs import MiniMaxChess

def minimax(board, current_depth, is_max_turn, alpha, beta):
    chessObj = MiniMaxChess()
    if current_depth == 3 or chessObj.gameOver():
        return chessObj.heuristic(), ""

    possible_actions = chessObj.getMoveList()

    # random.shuffle(possible_actions) #randomness
    best_value = float('-inf') if is_max_turn else float('inf')
    action = ""
    for move_key in possible_actions:
        chessObj.makeMoveHeur(str(move_key))

        eval_child, action_child = minimax(chessObj,current_depth+1,not is_max_turn, alpha, beta)
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
