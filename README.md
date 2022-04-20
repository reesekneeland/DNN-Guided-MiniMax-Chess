# Guided-MiniMax-Chess
My chess algorithm uses an implementation of the MiniMax algorithm guided by a custom heuristic estimate to guide the agent’s decisions at each move, allowing it to play a competent game of chess against a user inside a Discord server environment.

![chess](https://user-images.githubusercontent.com/77468346/153057434-b374be29-a8b0-442e-a576-8701e2d05e08.gif)


## Graphical Interface
The script uses Discord and its custom emoji system as a graphical interface to represent the board so that we could test the bot in a collaborative environment. The program first generates an ASCII representation of the board in the terminal using the python-chess module, then uses a conversion function and a set of 26 custom emojis inside a Discord server to print out the entire board using those custom emojis. Players can then interact with the bot, and play the AI using the .chess command. 
### Command List
To begin a game you tell the program what gamemode you want to play:
-  ```.chess 1```: Starts a manual chess game, in which the moves for both sides are manual. Effective at playing other users in the discord server without any AI interference.
-  ```.chess 2``` Starts a chess game against the AI, in which the user plays white and the AI plays black.
-  ```.chess 3``` Starts a game where the AI plays both sides against itself, making moves until the game is completed or aborted.
All other commands are also preceded by the ```.chess``` command, which directs your next argument into the program. 
- ```undo```: undoes the last move and reverts the board to the previous position and the previous players turn
- ```reset```: resets the game board and restarts the program, taking the player back to gamemode selection
- ```exit``` or ```quit```: exits the program
- ```print```: prints the current state of the game board

You can tell the program what move to make by typing in one of the provided options it gives you for possible moves, this is case sensitive.


## MiniMax
My agent uses an implementation of the Minimax algorithm to make decisions about where to move and how to play out the game. To calculate the next move we populate the MiniMax tree with the values of the heuristic of each move and determining the best possible move for each turn. The AI and heuristic algorithm is built on top of the python-chess module, which is already equipped with all of the functionality needed to run a fully functional chess board inside of the code. 

https://python-chess.readthedocs.io/en/latest/

This allows the script to easily get a list of possible moves from any position on the board, and test different board positions inside of MiniMax through a standalone chess object. MiniMax is configured to take the current position and whose turn it is as inputs, it then generates the list of possible moves, and iterates through them calling itself recursively for every possible board position, pruning off unnecessary moves with the alpha-beta pruning method. In order to make the MiniMax algorithm more efficient and help it prune more branches, MiniMax also uses a move ordering method that checks if any of the possible moves check the opponent's king, or capture an enemy piece, as these are more likely to be good moves, so by having MiniMax test these possibilities first, we increase the number of branches MiniMax is able to prune on average, decreasing the runtime.

## Heuristic Calculations
The heuristic algorithms score of the board that MiniMax uses to choose moves is determined by three factors. The first factor the algorithm considers is the relative piece values. For example, in chess the Queen is worth 9 points, Rook’s are worth 5, Knights and Bishops 3, and Pawns 1. The heuristic algorithm will use these scores to add up the total material score for each side (out of 39), and the difference between those scores represents 80% of the heuristic weighting of a board position for the bot. The second factor considered was to observe where each piece was on the board. The algorithm will favor pieces that are more developed on the board and placed in a more advantageous position. For a pawn this means the closer it is to the opponent's end of the board, the better the score. For a Knight, we favored pieces placed closer to the center of the board, so they can reach more squares. Each piece has a respective piece map that can be found in the positionMap.py file of the code repository. These maps were custom made for our project but were inspired by the maps found in similar algorithms from the chessprogramming.com wiki.

https://www.chessprogramming.org/Simplified_Evaluation_Function#Piece-Square_Tables

The third factor the algorithm considers is whether a piece is under attack or not. This attack factor is defined by subtracting the number of opponent pieces attacking it from the number of friendly pieces defending it. If this attack factor is negative we know the piece is under attack and the 20% heuristic weight for that piece gets reduced by 90%. Additionally, all other attacks that the piece is creating get nullified if the piece is vulnerable, as it will likely be captured the next turn anyways before it has a chance to attack if defensive options aren’t taken. Comparing piece values is generally a pretty good way of seeing who is winning in a position, so that makes up the majority of our heuristic element, while seeing which pieces are better placed or under attack factor into the multiplier maps used to calculate the remaining 20%. MiniMax in its current state will look 3 moves ahead, which in the current implementation results in computation times ranging from 1-5 seconds to calculate a move depending on the complexity of the position. I did also develop and experiment with a version of MiniMax that multithreads the top layer of the calculation tree to all of the available CPU threads available in the machine its hosted on, which on my machine reduces computation times by about 90%, allowing for an additional layer and search to a depth of four. Unfortunately this multithreaded version of the MiniMax algorithm is unstable when used with the current Discord representation of the bot, and so only works with the terminal interface as of right now.

## Performance and Future Improvements
After much testing, a reasonable estimate for the rating of this agent is approimately 900 Elo. In general, the AI performed better against other AIs than players. This is probably due to players noticing the style and mistakes the AI made and taking advantage of weaknesses in the heuristic. The agent seemed to sometimes avoid checkmates as it was trying to take a piece instead of winning, as the only way it can end the game is if it can see a checkmate in the next 3 moves, leading to many situations where it could have won but instead tries to take pieces, causing it to draw or lose the game. This could be fixed if we more finetune the heuristic to favor common mating strategies. Another flaw is that the agent prefers to take pieces even if it means sacrificing less valued pieces, making it blind to forks and more advanced strategies used by advanced chess players. Future development and adjustments could address these issues, but there is no plans to advance the project at this time.
