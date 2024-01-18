import torch
import torch.nn as nn

import json


# Define the model architecture (this must match the architecture used when the state_dict was saved)
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.linear1 = nn.Linear(2, 10)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(10, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        x = self.sigmoid(x)
        return x

model = MyModel()

model_architecture = str(model)

# Save the architecture as a text file
with open('model_architecture.txt', 'w') as f:
    f.write(model_architecture)

torch.save(model.state_dict(), 'model_weights.pth')