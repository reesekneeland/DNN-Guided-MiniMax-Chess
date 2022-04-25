def nn_prediction(fen_map): #Assumption is input will be board representation in "bitmap" format of post all possible moves. Example: 9 legal moves
                              #Therefore array of 9 values passed in. Each value being a bitmap of he board after possible move is taken.
    model = torch.load('entire_model.pth') #Determine how we can load in the neural network model.
    model.eval() # Set model to eval mode
    
    with torch.no_grad(): # Deactivate gradients for the following code
        
        split = fen_map.split(" ")
        mapping = split[0]
        mapping = mapping.encode('utf-8')
        bin = np.frombuffer(mapping, dtype=np.uint8)
        bin = np.unpackbits(bin, axis=0).astype(np.single)
        array = np.zeros(808)

        for value in range(len(array)):
            try:
                array[value] = array[value] + bin[value]
            except:
                break
        
        #cleaned_data, data_labels = cleaned_data.to(device), data_labels.to(device)
        preds = model(array)
        prediction = preds[0]

        print(prediction)
            
    return(prediction)