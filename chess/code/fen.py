import subprocess
from PIL import ImageGrab
import numpy as np
import webbrowser
from tensorflow import keras
import time

pieces = ["b","k","n", "p", "q", "r", "1","B","K", "N", "P", "Q", "R"]

# Load the trained model
model = keras.models.load_model('model.h5')

img = ImageGrab.grabclipboard()

while img is None:
    # Get the image from the clipboard
    print("Make screenshot with chessboard...",end="\r")
    img = ImageGrab.grabclipboard()    
    time.sleep(1)

img = img.convert("RGB")

# Get the size of the image
width, height = img.size

size = min(width, height)
left = (width - size) // 2
top = (height - size) // 2
right = left + size
bottom = top + size
img = img.crop((left, top, right, bottom))
img = img.resize((480,480))

fen=""

# Loop through the image and crop each piece
for i in range(8):
    for j in range(8):
        left = j * 60
        top = i * 60
        right = left + 60
        bottom = top + 60
        piece = img.crop((left, top, right, bottom))                                   
        #piece.save(f"test{i}_{j}.png")
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

color = input("White move (w) or Black move (b)")
url = f"https://lichess.org/analysis/{fen}"
if "w" in color.lower():
    url+=" w"
    webbrowser.open(url)
elif "b" in color.lower():
    url+=" b"
    webbrowser.open(url)
else:
    print(fen)
    subprocess.call(["python", "main.py", str(fen)])

