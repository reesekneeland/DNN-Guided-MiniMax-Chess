import chess
from funcs import *
import math
import numpy as np
import csv

games=[]
with open('data/2021_data.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        games.append(row)
total_heurarray=[]
count=0
for game in games:
    heurArray = generateGameHeuristics(game)
    count+=1
    total_heurarray.append(heurArray)

