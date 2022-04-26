import torch
import numpy as np
torch.manual_seed(42)

import subprocess
import sys

from pip._internal import main as pipmain

#!pip install peewee pytorch-lightning
#Download before running wget if you don't already have wget installed: https://eternallybored.org/misc/wget/
#Copy and paste wget.exe found in downloads to C:\Windows\System32 directory.
#!wget https://storage.googleapis.com/chesspic/datasets/2021-07-31-lichess-evaluations-37MM.db.gz
#Gzip can be downloader here: http://gnuwin32.sourceforge.net/packages/gzip.htm after installing navigate to C:\Program Files (x86)\GnuWin32\bin
#copy gzip.exe and place within C:\Windows\System32 directory.
#!gzip -d "2021-07-31-lichess-evaluations-37MM.db.gz"
#!rm "2021-07-31-lichess-evaluations-37MM.db.gz"

from peewee import *
import base64

db = SqliteDatabase('2021-07-31-lichess-evaluations-37MM.db')

class Evaluations(Model):
  id = IntegerField()
  fen = TextField()
  binary = BlobField()
  eval = FloatField()

  class Meta:
    database = db

  def binary_base64(self):
    return base64.b64encode(self.binary)
db.connect()

#connection = db.cursor()
#connection.execute("select * from evaluations")
#result = connection.fetchall()
#print(result)

#print(Evaluations.id)
LABEL_COUNT = 37164639
#print(LABEL_COUNT)
#print(str(Evaluations))
eval = Evaluations.get(Evaluations.id == 1)

split = eval.fen.split(" ")
mapping = split[0]
mapping = mapping.encode('utf-8')
mapping = np.frombuffer(mapping, dtype=np.uint8)
mapping = np.unpackbits(mapping, axis=0).astype(np.single)

print(eval.binary_base64())

from logging import exception
import os
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, IterableDataset, random_split
import pytorch_lightning as pl
from random import randrange

class EvaluationDataset(IterableDataset):
  def __init__(self, count):
    self.count = count
  def __iter__(self):
    return self
  def __next__(self):
    idx = randrange(self.count)
    return self[idx]
  def __len__(self):
    return self.count
  def __getitem__(self, idx):
    eval = Evaluations.get(Evaluations.id == idx+1)
    #print(eval)
    split = eval.fen.split(" ")
    mapping = split[0]
    mapping = mapping.encode('utf-8')
    bin = np.frombuffer(mapping, dtype=np.uint8)
    bin = np.unpackbits(bin, axis=0).astype(np.single)
    array = np.zeros(808)
    count = 0
    for value in range(len(array)):
        try:
          array[value] = array[value] + bin[value]
          count = count + 1
        except:
          break
    #print(array)
    #bin = np.frombuffer(eval.binary, dtype=np.uint8)
    #bin = np.unpackbits(bin, axis=0).astype(np.single)
    #print(len(array))
    eval.eval = max(eval.eval, -15)
    eval.eval = min(eval.eval, 15)
    ev = np.array([eval.eval]).astype(np.single)
    array = array.astype(np.single)
    return {'binary':array, 'eval':ev}    

dataset = EvaluationDataset(count=LABEL_COUNT)

# Start tensorboard.
#%load_ext tensorboard
#%tensorboard --logdir lightning_logs/

dataset = EvaluationDataset(count=LABEL_COUNT)
dataset.__getitem__(1)


import time
from collections import OrderedDict

class EvaluationModel(pl.LightningModule):
  def __init__(self,learning_rate=1e-3,batch_size=1024,layer_count=10):
    super().__init__()
    self.batch_size = batch_size
    self.learning_rate = learning_rate
    layers = []
    for i in range(layer_count-1):
      layers.append((f"linear-{i}", nn.Linear(808, 808)))
      layers.append((f"relu-{i}", nn.ReLU()))
    layers.append((f"linear-{layer_count-1}", nn.Linear(808, 1)))
    self.seq = nn.Sequential(OrderedDict(layers))

  def forward(self, x):
    return self.seq(x)

  def training_step(self, batch, batch_idx):
    x, y = batch['binary'], batch['eval']
    y_hat = self(x)
    loss = F.l1_loss(y_hat, y)
    self.log("train_loss", loss)
    return loss

  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

  def train_dataloader(self):
    dataset = EvaluationDataset(count=LABEL_COUNT)
    return DataLoader(dataset, batch_size=self.batch_size, num_workers=0, pin_memory=True)

configs = [
           {"layer_count": 4, "batch_size": 512},
          #  {"layer_count": 6, "batch_size": 1024},
           ]
for config in configs:
  version_name = f'{int(time.time())}-batch_size-{config["batch_size"]}-layer_count-{config["layer_count"]}'
  logger = pl.loggers.TensorBoardLogger("lightning_logs", name="chessml", version=version_name)
  trainer = pl.Trainer(precision=16,max_epochs=1,auto_lr_find=True,logger=logger) #first argument "gpus=1" removed
  model = EvaluationModel(layer_count=config["layer_count"],batch_size=config["batch_size"],learning_rate=1e-3)
  # trainer.tune(model)
  # lr_finder = trainer.tuner.lr_find(model, min_lr=1e-6, max_lr=1e-3, num_training=25)
  # fig = lr_finder.plot(suggest=True)
  # fig.show()
  trainer.fit(model)
  break
  
from IPython.display import display, SVG
from random import randrange

SVG_BASE_URL = "https://us-central1-spearsx.cloudfunctions.net/chesspic-fen-image/" 

def svg_url(fen):
  fen_board = fen.split()[0]
  return SVG_BASE_URL + fen_board

def show_index(idx):
  eval = Evaluations.select().where(Evaluations.id == idx+1).get()
  batch = dataset[idx]
  x, y = torch.tensor(batch['binary']), torch.tensor(batch['eval'])
  y_hat = model(x)
  loss = F.l1_loss(y_hat, y)
  print(f'Idx {idx} Eval {y.data[0]:.2f} Prediction {y_hat.data[0]:.2f} Loss {loss:.2f}')
  print(f'FEN {eval.fen}')
  display(SVG(url=svg_url(eval.fen)))

for i in range(5):
  idx = randrange(LABEL_COUNT)
  show_index(idx)

# need to do better on "tactics" like 700756

import chess

MATERIAL_LOOKUP = {chess.KING:0,chess.QUEEN:9,chess.ROOK:5,chess.BISHOP:3,chess.KNIGHT:3,chess.PAWN:1}

def avg(lst):
    return sum(lst) / len(lst)

def material_for_board(board):
  eval = 0.0
  for sq, piece in board.piece_map().items():
    mat = MATERIAL_LOOKUP[piece.piece_type] 
    if piece.color == chess.BLACK:
      mat = mat * -1
    eval += mat
  return eval
  
def guess_zero_loss(idx):
  eval = Evaluations.select().where(Evaluations.id == idx+1).get()
  y = torch.tensor(eval.eval)
  y_hat = torch.zeros_like(y)
  loss = F.l1_loss(y_hat, y)
  return loss

def guess_material_loss(idx):
  eval = Evaluations.select().where(Evaluations.id == idx+1).get()
  board = chess.Board(eval.fen)
  y = torch.tensor(eval.eval)
  y_hat = torch.tensor(material_for_board(board))
  loss = F.l1_loss(y_hat, y)
  return loss

def guess_model_loss(idx):
  eval = Evaluations.select().where(Evaluations.id == idx+1).get()
  batch = dataset[idx]
  x, y = torch.tensor(batch['binary']), torch.tensor(batch['eval'])
  y_hat = model(x)
  loss = F.l1_loss(y_hat, y)
  return loss

zero_losses = []
mat_losses = []
model_losses = []
for i in range(100):
  idx = randrange(LABEL_COUNT)
  zero_losses.append(guess_zero_loss(idx))
  mat_losses.append(guess_material_loss(idx))
  model_losses.append(guess_model_loss(idx))
print(f'Guess Zero Avg Loss {avg(zero_losses)}')
print(f'Guess Material Avg Loss {avg(mat_losses)}')
print(f'Guess Model Avg Loss {avg(model_losses)}')
print(model.get_parameter)

torch.save(model, 'chess_model.pth')