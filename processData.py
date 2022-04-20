import chess
from funcs import *
import math
import numpy as np

testGame = ["e4", "Nf6", "Nc3", "e5", "Nf3", "Nc6", "Bb5", "Bb4", "d3", "d6", "Bd2", "O-O", "Ng5", "h6", "h4", "Nd4", "Bc4", "hxg5", "hxg5", "Ne8", "Qh5", "Bh3", "Rxh3", "Nf3+", "gxf3", "g6", "Qh7#"]

heurArray = generateGameHeuristics(testGame)
print(heurArray)