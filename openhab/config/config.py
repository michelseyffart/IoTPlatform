import json
import logs.create_logger as logs
from openhab.config.paths import *

path_config_file = path_config_folder.joinpath("config.json")
path_params_file = path_config_folder.joinpath("params.json")

log = logs.get_logger(name="config", filename="config.log")


def get_config():
    try:
        with open(path_config_file, 'r') as f:
            config = json.load(f)
        return config
    except json.decoder.JSONDecodeError:
        log.warning(msg="Nothing in the config file.")
        return None


def get_from_config(key):
    try:
        with open(path_config_file, 'r') as f:
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
        with open(path_config_file, 'r') as f:
            config = json.load(f)
        config[key] = value
    except json.decoder.JSONDecodeError:
        config = {}
    with open(path_config_file, 'w') as f:
        json.dump(config, f, indent=4, sort_keys=True)
        log.info(f"Saved data:\t {key}:\t {value}")


def get_required_addons():
    try:
        with open("config/required_addons.json", 'r') as f:
            addons = json.load(f)
        return addons
    except KeyError:
        log.exception(KeyError)
        return None


def get_from_params(query_key):
    keys = query_key.split("/")
    try:
        with open(path_params_file, 'r') as f:
            params = json.load(f)
    except json.decoder.JSONDecodeError:
        log.warning(msg="Nothing in the params file.")
        return None
    try:
        data = params[keys[0]]
        for key in keys[1:]:
            data = data[key]
        return data
    except KeyError as e:
        log.exception(e)
        return None
