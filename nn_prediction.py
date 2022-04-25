import torch
import numpy as np
import nn_training
#import neuralnet.pth


import time
from collections import OrderedDict

import torch
import numpy as np
torch.manual_seed(42)

import subprocess
import sys

from logging import exception
import os
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, IterableDataset, random_split
import pytorch_lightning as pl
from random import randrange

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
    
    
    
    
    

def nn_prediction(fen_map): #input of legal move passed in an fen format. Prediction of advantage gain or lossed predicted and returned
                            #range for move prediction outputted is [-15, 15].
    config = [
           {"layer_count": 4, "batch_size": 512},
          #  {"layer_count": 6, "batch_size": 1024},
           ]
    model = EvaluationModel(layer_count = 4, batch_size = 512, learning_rate=1e-3)
    model = model.load_state_dict(torch.load('neuralnet.pth'))
    #model = torch.load('neuralnet.pth') #Determine how we can load in the neural network model.
    model.eval() # Set model to eval mode
    print(model)
    with torch.no_grad(): # Deactivate gradients for the following code
        
        split = fen_map.split(" ") #Split fen mapping
        mapping = split[0] #Retrieve mapping of pieces on chess board only
        mapping = mapping.encode('utf-8') #encode fen mapping of chess board only in utf-8
        bin = np.frombuffer(mapping, dtype=np.uint8)
        bin = np.unpackbits(bin, axis=0).astype(np.single) #unpack utf-8 format of fen mapping of chess board only
        array = np.zeros(808) #byte length of unpacked fen mapping of chessboard only will vary depending upon how many pieces are left
                              #in game. Fen mapping of chessboard will never exceed 808 bytes therefore we employ 808 bytes as our input
                              #to the neural network.

        for value in range(len(array)):
            try:
                array[value] = array[value] + bin[value]
            except:
                break
        
        preds = model(array)
        prediction = preds[0]

        print(prediction)
            
    return(prediction)
    
prediction = nn_prediction("rrrr/8/1ppppppp aw 1 0")