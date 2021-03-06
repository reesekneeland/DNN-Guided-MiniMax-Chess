import torch
import numpy as np
#import nn_training
#import neuralnet.pth

import time
from collections import OrderedDict

import numpy as np
torch.manual_seed(42)

import subprocess
import sys
import torchvision
from logging import exception
import os
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, IterableDataset, random_split
import pytorch_lightning as pl
from random import randrange


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        input_dim = 808; hidden_dim = 808; output_dim = 1
        self.linear1 = torch.nn.Linear(input_dim, hidden_dim)
        self.act_fn1 = torch.nn.ReLU() #may change - logisitc sigmoid for Xavier Initialization
        self.linear2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.act_fn2 = torch.nn.ReLU()
        self.linear3 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.act_fn3 = torch.nn.ReLU()
        self.linear4 = torch.nn.Linear(hidden_dim, output_dim)
        #self.act_fn_end = torch.nn.Sigmoid()


        # initialize here
        torch.nn.init.xavier_uniform_(self.linear1.weight)
        torch.nn.init.xavier_uniform_(self.linear2.weight)
        torch.nn.init.xavier_uniform_(self.linear3.weight)
        torch.nn.init.xavier_uniform_(self.linear4.weight)

    def forward(self, x):    
      #
        x = self.linear1(x)
        x = self.act_fn1(x)
        x = self.linear2(x)
        x = self.act_fn2(x)
        x = self.linear3(x)
        x = self.act_fn3(x)
        x = self.linear4(x)
      #x = self.act_fn_end(x)
        return x
    

    
    

def predict(model, fen_map): #input of legal move passed in an fen format. Prediction of advantage gain or lossed predicted and returned
                            #range for move prediction outputted is [-15, 15].
    with torch.no_grad(): # Deactivate gradients for the following code
        #model.load_state_dict(torch.load('chess_model.pth'))
        #model.eval()
        split = fen_map.split(" ") #Split fen mapping
        mapping = split[0] #Retrieve mapping of pieces on chess board only
        mapping = mapping.encode('utf-8') #encode fen mapping of chess board only in utf-8
        bin = np.frombuffer(mapping, dtype=np.uint8)
        bin = np.unpackbits(bin, axis=0).astype(np.single) #unpack utf-8 format of fen mapping of chess board only
                                #byte length of unpacked fen mapping of chessboard only will vary depending upon how many pieces are left
                              #in game. Fen mapping of chessboard will never exceed 808 bytes therefore we employ 808 bytes as our input
                              #to the neural network.
        bin.resize((808,))
        new_array = torch.from_numpy(bin)
        new_array = new_array.float()
        preds = model(new_array)
        prediction = preds[0]
    return(prediction.item())
    
#prediction = predict(Net(), "rnb1kbnr/ppp2ppp/8/3pp3/4P2P/2N5/PPPP1P1P/R1BQKBNR b KQkq - 0 4")
#print(prediction)