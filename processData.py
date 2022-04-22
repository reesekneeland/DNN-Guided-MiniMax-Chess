import chess
from funcs import *
import math
import numpy as np
import csv

def heuristics_for_game(fname='data/2021_data.csv'):
    games=[]
    with open(fname, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            games.append(row)
    total_heurarray=[]
    count=0
    for game in games:
        heurArray = generateGameHeuristics(game)
        count+=1
        total_heurarray.append(heurArray)
    return(total_heurarray)


