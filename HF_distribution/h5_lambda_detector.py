import json
import threading
from tqdm import tqdm

import transformers
from tensorflow.keras.layers import Lambda
from loguru import logger

# Define the function for counting layers with a time limit
def count_layers_in_model_helper(model_path):
    try:
        repo_path = '/'.join(model_path.split('/')[:-1])
        model = transformers.TFAutoModel.from_pretrained(repo_path)
    except Exception as e:
        logger.error(f"Error loading model: {model_path}")
        logger.error(e)
        return 0, 0

    lambda_count = 0
    custom_count = 0

    for layer in model.layers:
        if isinstance(layer, Lambda):
            lambda_count += 1
        # Add your custom layer check here

    return lambda_count, custom_count

def count_layers_in_model(model_path):
    result = [0, 0]
    thread = threading.Thread(target=lambda: result.__setitem__(slice(None), count_layers_in_model_helper(model_path)))
    thread.start()
    thread.join(timeout=60)  # Timeout of 60 seconds

    if thread.is_alive():
        logger.warning(f"Processing of model {model_path} took too long and was skipped.")
        thread.join()  # Ensure thread is cleaned up
        return 0, 0
    else:
        return result

# Load the list of model files
with open('h5_models.json', 'r') as f:
    h5_models = json.load(f)

model_files = h5_models
total_lambda_count = 0

# Process each model file
with open('model_layer_counts.txt', 'w') as file:
    for model_file in tqdm(model_files):
        try:
            logger.debug(f"Processing model: {model_file}")
            lambda_count, custom_count = count_layers_in_model(model_file)
            
            result_str = f'Model: {model_file}, Lambda Layers: {lambda_count}, Custom Layers: {custom_count}\n'
            if lambda_count > 0:
                total_lambda_count += 1

            print(result_str.strip())
            file.write(result_str)
        except Exception as e:
            error_str = f"Error processing {model_file}: {e}\n"
            print(error_str)
            file.write(error_str)
    
    file.write(f"\n\nTotal models with Lambda layers: {total_lambda_count}\n")
