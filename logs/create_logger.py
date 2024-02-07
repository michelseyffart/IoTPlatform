import logging
from openhab.config.paths import *

formatter = logging.Formatter('%(asctime)s:\t %(levelname)s: %(name)s:\t %(message)s',
                              datefmt="%H:%M:%S (%d.%m.%y)")


def get_logger(filename: str, name: str, consolelevel=logging.WARNING):
    handler = logging.FileHandler(path_logs_folder.joinpath(filename))
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(consolelevel)
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

    return logger
