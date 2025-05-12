import json
import os

def load_config(path='config/constants.json'):
  with open(path, 'r') as file:
    return json.load(file)
