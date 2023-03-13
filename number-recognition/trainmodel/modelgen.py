import tensorflow as tf
import numpy as np
import os
import cv2

###YOU NEED TO UNPACK trainingSet.zip

# Load the training data
data = []
labels = []
for i in range(10):
    path = './trainingSet/' + str(i)
    images = os.listdir(path)
    for image in images:
        img = cv2.imread(path + '/' + image, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28))
        data.append(img)
        labels.append(i)

data = np.array(data)
labels = np.array(labels)

# Normalize the data
data = data / 255.0

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2)

# Define data augmentation
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    shear_range=0.2,
    fill_mode='nearest')

# Define the CNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10)
])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model with data augmentation
history = model.fit(datagen.flow(train_data.reshape(-1, 28, 28, 1), train_labels, batch_size=32),
                    epochs=20,
                    validation_data=(test_data.reshape(-1, 28, 28, 1), test_labels))

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(test_data.reshape(-1, 28, 28, 1), test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

# Save the model
model.save('model.h5')
