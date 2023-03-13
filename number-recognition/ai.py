import numpy as np
from PIL import Image
import os
from tensorflow import keras

# load the model from a file
model = keras.models.load_model('model.h5')

for file_name in os.listdir('img'):
    if file_name.endswith(".png"):
        # load and convert the image to a numpy array
        img = Image.open(f'img/{file_name}').convert('L')
        img = img.resize((28, 28))
        img = np.array(img)

        # normalize the image data
        img = img / 255.0

        # reshape the image to a shape accepted by the model
        img = img.reshape((-1, 28, 28, 1))

        # make a prediction on the image
        pred = model.predict(img)
        digit = np.argmax(pred)

        print(f"Recognized digit for file {file_name} is: {digit}")
input("Press Enter to end...")
