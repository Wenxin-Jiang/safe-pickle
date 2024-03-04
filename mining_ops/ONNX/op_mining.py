import onnx
from collections import Counter

def count_custom_layers(model_path):
    # Load the model
    model = onnx.load(model_path)

    # Counter for layer types
    layer_counter = Counter()

    # Iterate over all nodes in the model
    for node in model.graph.node:
        # Assuming custom layers have a specific pattern or identifiable characteristic
        # Update this condition based on your definition of a custom layer
        if 'Custom' in node.op_type:
            layer_counter[node.op_type] += 1

    return layer_counter

# List of your ONNX model file paths
model_paths = ['path_to_model1.onnx', 'path_to_model2.onnx', ...]

# Dictionary to hold the frequency of custom layers across all models
overall_custom_layers_frequency = Counter()

# Process each model
for path in model_paths:
    custom_layers_in_model = count_custom_layers(path)
    overall_custom_layers_frequency.update(custom_layers_in_model)

# Print the frequencies
print("Custom Layers Frequency Across All Models:")
for layer, count in overall_custom_layers_frequency.items():
    print(f"{layer}: {count}")
