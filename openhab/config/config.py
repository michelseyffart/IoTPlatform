import json
import openhab.create_logger as logs

path = "config/config.json"

log = logs.get_logger(name="config", filename="logs/config.log")


def get_config():
    try:
        with open(path, 'r') as f:
            config = json.load(f)
        return config
    except json.decoder.JSONDecodeError:
        log.warning(msg="Nothing in the config file.")
        return None


def get_from_config(key):
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except json.decoder.JSONDecodeError:
        log.warning(msg="Nothing in the config file.")
        return None
    try:
        return config[key]
    except KeyError:
        log.exception(KeyError)
        return None


def save_to_config(key, value):
    try:
        with open(path, 'r') as f:
            config = json.load(f)
        config[key] = value
    except json.decoder.JSONDecodeError:
        config = {}
    with open(path, 'w') as f:
        json.dump(config, f, indent=4, sort_keys=True)
        log.info(f"Saved data:\t {key}:\t {value}")
