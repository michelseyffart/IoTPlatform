import json
import logs.create_logger as logs
from fiware.config.paths import path_config_file

log = logs.get_logger(name="config", filename="config.log")


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
