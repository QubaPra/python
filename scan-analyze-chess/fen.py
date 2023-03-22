from PIL import Image
import cv2
import numpy as np
from tensorflow import keras

pieces = ["b","k","n", "p", "q", "r", "1","B","K", "N", "P", "Q", "R"]

# Load the trained model
model = keras.models.load_model('model.h5')

# Open the image
img = Image.open("./image.png")

# Get the size of the image
width, height = img.size

# Set the number of pieces to divide the image into
rows = cols = 8

# Calculate the size of each piece
piece_width = width // cols
piece_height = height // rows

fen=""

# Loop through the image and crop each piece
for i in range(rows):
    for j in range(cols):
        left = j * piece_width
        top = i * piece_height
        right = left + piece_width
        bottom = top + piece_height
        piece = img.crop((left, top, right, bottom))
                
        # load and convert the image to a numpy array
        piece = piece.resize((60, 60))            
        
        # normalize the image data
        piece = np.array(piece) / 255.0        

        # Make a prediction
        predictions = model.predict(np.expand_dims(piece, axis=0))
            
        # Get the predicted label
        predicted_label = np.argmax(predictions)
        
        p = pieces[predicted_label]
        if fen!="" and fen[-1].isdigit() and p.isdigit():
            
            p=str(int(p) + int(fen[-1]))
            fen=fen[:-1]        
        fen+=p     
    if i<7:
        fen+="/"

print(fen)