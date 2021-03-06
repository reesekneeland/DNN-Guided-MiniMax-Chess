import numpy as np
KnightMap = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5,  5, 15, 15,  5,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-35,-30,-30,-30,-30,-35,-50,
]
wKnightMap = KnightMap
bKnightMap = KnightMap[::-1]


PawnMap = [
0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 35, 35, 20, 10, 10,
 5,  5, 10, 30, 30, 10,  5,  5,
 0,  0,  0, 25, 25,  0,  0,  0,
 5,  5,-10,  0,  0,-10,  5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0
]

wPawnMap = PawnMap
bPawnMap = PawnMap[::-1]

BishopMap = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20,
]
wBishopMap = BishopMap
bBishopMap = BishopMap[::-1]

RookMap = [
  0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  -5,  0,  5,  5,  0,  -5,  0
  ]

wRookMap = RookMap
bRookMap = RookMap[::-1]

QueenMap = [
-20,-10,-10,  5,  5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10,  0,  0,-10,-10,-20
]

wQueenMap = QueenMap
bQueenMap = QueenMap[::-1]

