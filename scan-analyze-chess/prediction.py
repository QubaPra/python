import os
import cv2
import numpy as np
from tensorflow import keras

pieces = ["black_bishop","black_king","black_knight", "black_pawn", "black_queen", "black_rook", None,"white_bishop","white_king", "white_knight", "white_pawn", "white_queen", "white_rook"]

# Load the trained model
model = keras.models.load_model('model.h5')


for file_name in os.listdir('./'):
    if file_name.endswith(".png"):
        # load and convert the image to a numpy array
        img = cv2.imread(f'./{file_name}')        
        img = cv2.resize(img, (60, 60))

        # normalize the image data
        img_array = np.array(img) / 255.0        

        # Make a prediction
        predictions = model.predict(np.expand_dims(img_array, axis=0))
            
        # Get the predicted label
        predicted_label = np.argmax(predictions)
            

        print(f"Image: {file_name} Predicted label:", pieces[predicted_label])

    
