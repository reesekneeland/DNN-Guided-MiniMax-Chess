import torch
torch.manual_seed(42)

gpu_avail = torch.cuda.is_available()
print(f"Is the GPU available? {gpu_avail}")

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print("Device", device)

from peewee import *
import base64
import numpy as np

db = SqliteDatabase('2021-07-31-lichess-evaluations-37MM.db')

from peewee import *
import base64
import numpy as np

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
#Query database
#cursor = db.cursor()
#cursor.execute("select * from evaluations limit 7")
#row = cursor.fetchone()
#print(row[1])

LABEL_COUNT = 37164639
print(LABEL_COUNT)

eval = Evaluations.get(Evaluations.id == 1)
print(Evaluations)
print(eval.binary)
print(eval.fen)
split = eval.fen.split(" ")
mapping = split[0]
mapping = mapping.encode('utf-8')
mapping = np.frombuffer(mapping, dtype=np.uint8)
mapping = np.unpackbits(mapping, axis=0).astype(np.single)
print(len(mapping))
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
        except Exception as e:
          break
    #bin = np.frombuffer(eval.binary, dtype=np.uint8)
    #bin = np.unpackbits(bin, axis=0).astype(np.single)
    eval.eval = max(eval.eval, -15)
    eval.eval = min(eval.eval, 15)
    ev = np.array([eval.eval]).astype(np.single)
    return {'binary':array, 'eval':ev}    

dataset = EvaluationDataset(count=LABEL_COUNT)

train_dataloader = DataLoader(dataset, batch_size=524, drop_last=True)

import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter # TensorBoard support
from tqdm.notebook import tqdm
import time
import os
import math
import numpy as np 
import seaborn as sns
sns.set()
writer = SummaryWriter('runs/chess')
import torch
torch.manual_seed(42)

gpu_avail = torch.cuda.is_available()
print(f"Is the GPU available? {gpu_avail}")

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print("Device", device)


input_dim = 808; hidden_dim = 808; output_dim = 1

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        #print(len(cleaned_data))
        #print("Shape: ", {cleaned_data.shape})
        # layers here
        self.linear1 = torch.nn.Linear(input_dim, hidden_dim)
        self.act_fn1 = torch.nn.ReLU() #may change - logisitc sigmoid for Xavier Initialization
        self.linear2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.act_fn2 = torch.nn.ReLU()
        self.linear3 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.act_fn3 = torch.nn.ReLU()
        self.linear4 = torch.nn.Linear(hidden_dim, output_dim)
        self.act_fn_end = torch.nn.Sigmoid()


        # initialize here
        torch.nn.init.xavier_uniform_(self.linear1.weight)
        torch.nn.init.xavier_uniform_(self.linear2.weight)

    def forward(self, x):    
      #
      x = self.linear1(x)
      x = self.act_fn1(x)
      x = self.linear2(x)
      x = self.act_fn2(x)
      x = self.linear3(x)
      x = self.act_fn3(x)
      x = self.linear4(x)
      x = self.act_fn_end(x)
      return x

# STEP 2:
# instantiate your network and use a cross entropy loss and set up your optimizer.  Use ADAM with defaults
net = Net()
net.to(device)
loss_module = torch.nn.L1Loss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.001) #Default learning rate is 0.001
# STEP 3:
# train your model
def train_model(model, optimizer, train_dataloader, loss_module, num_epochs):
    # Set model to train mode
    model.train()
    model_plotted = False
    # Training loop
    for epoch in range(num_epochs):
        running_loss = 0.0
        count = 0
        for value in tqdm(train_dataloader):
            count = count + 1
            x1 = value['binary']
            y1 = value['eval']
            x1 = x1.float(); y1 = y1.float()
            x1 = x1.to(device)
            y1 = y1.to(device)

            #Tensor Hook
            if(epoch == 0):
                writer.add_graph(net, x1)
                

            ##Run the model on the input data
            preds = model(x1)
            #preds = preds.squeeze(dim=1) # Output is [Batch size, 1], but we want [Batch size]

            ## Step 3: Calculate the loss
            loss = loss_module(preds, y1)

            ## Step 4: Perform backpropagation
            # Before calculating the gradients, we need to ensure that they are all zero. 
            # The gradients would not be overwritten, but actually added to the existing ones.
            optimizer.zero_grad() 
            # Perform backpropagation
            loss.backward()
            
            ## Step 5: Update the parameters
            optimizer.step()

            #Tensorboard hook
            running_loss += loss.item()
            running_loss /= len(train_dataloader)
            writer.add_scalar('Training loss', running_loss/1000, count)
            
            

            
        print(model)
        torch.save(model.state_dict(), 'chess_model.pth')

train_model(net, optimizer, train_dataloader, loss_module, num_epochs = 1)

writer.flush()
writer.close()
#%tensorboard --logdir=runs/chess