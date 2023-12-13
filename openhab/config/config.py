import json
import logging

path = "config/config.json"


def get_config():
    with open(path, 'r') as f:
        config = json.load(f)
    return config


def get_from_config(key):
    with open(path, 'r') as f:
        config = json.load(f)
    try:
        return config[key]
    except KeyError:
        logging.exception(KeyError)
        return None


def save_to_config(key, value):
    with open(path, 'r') as f:
        config = json.load(f)
    config[key] = value
    with open(path, 'w') as f:
        json.dump(config, f)
