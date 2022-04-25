import torch
import numpy as np

def nn_prediction(fen_map): #input of legal move passed in an fen format. Prediction of advantage gain or lossed predicted and returned
                            #range for move prediction outputted is [-15, 15].
    model = torch.load('entire_model.pth') #Determine how we can load in the neural network model.
    model.eval() # Set model to eval mode
    
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