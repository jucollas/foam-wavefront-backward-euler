import json
import os

def load_config(path='config/constants.json'):
    """
    Loads configuration parameters from a JSON file.

    This function reads a JSON file from the specified path and returns its contents
    as a Python dictionary. It is typically used to load simulation or model parameters.

    Args:
        path (str, optional): Path to the configuration JSON file. 
            Defaults to 'config/constants.json'.

    Returns:
        dict: Dictionary containing the configuration parameters.
    """
    with open(path, 'r') as file:
        return json.load(file)
