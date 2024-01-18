import torch
import re

from loguru import logger

# Function to create a layer from a string
def create_layer(layer_str):
    if "Linear" in layer_str:
        # Extracting in_features and out_features
        nums = [int(s) for s in re.findall(r'\d+', layer_str)]
        return torch.nn.Linear(nums[0], nums[1])
    elif "ReLU" in layer_str:
        return torch.nn.ReLU()
    elif "Sigmoid" in layer_str:
        return torch.nn.Sigmoid()
    else:
        logger.debug(f"Unknown layer type in architecture: {layer_str}")
        raise ValueError("Unknown layer type in architecture")

# Initialize an empty Sequential model
model = torch.nn.Sequential()

# Load the model architecture from the saved file
with open('model_architecture.txt', 'r') as f:
    for line in f:
        layer = create_layer(line.strip())
        model.add_module(line.strip(), layer)

# Load the model weights
model.load_state_dict(torch.load('model_weights.pth'))

# Set the model to evaluation mode
model.eval()

# Now your model is ready to use
