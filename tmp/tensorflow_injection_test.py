import numpy as np
from tensorflow import keras

model = keras.models.load_model("model_malicious")
data = np.random.random((1, 5))

# print the architecture of the model
model.summary()

