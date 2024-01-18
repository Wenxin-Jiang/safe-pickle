import torch

# Load the state dictionary from the .pth file
state_dict = torch.load('model_weights.pth')

# Print the keys and shapes of the weights in the state dictionary
for key, value in state_dict.items():
    print(key, value.shape)
