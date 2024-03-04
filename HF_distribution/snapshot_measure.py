import os
import json

def find_model_paths(root_folder):
    h5_models = []
    onnx_models = []

    # Walk through the directory
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # Check the file extension and add it to the respective list
            if file.endswith('.h5'):
                h5_models.append(os.path.join(root, file))
            elif file.endswith('.onnx'):
                onnx_models.append(os.path.join(root, file))

    return h5_models, onnx_models

def save_paths_to_json(paths, filename):
    # Serialize list to JSON and write to a file
    with open(filename, 'w') as f:
        json.dump(paths, f, indent=4)

# Specify the root folder path
root_folder = '/scratch/gilbreth/jiang784/peatmoss_fortress/huggingface_data'

# Find model paths
h5_models, onnx_models = find_model_paths(root_folder)

# Save the paths to JSON files
save_paths_to_json(h5_models, 'h5_models.json')
save_paths_to_json(onnx_models, 'onnx_models.json')

print(f"Saved {len(h5_models)} h5 model paths to h5_models.json")
print(f"Saved {len(onnx_models)} ONNX model paths to onnx_models.json")