import logging

formatter = logging.Formatter('%(asctime)s:\t %(levelname)s: %(name)s:\t %(message)s',
                              datefmt="%H:%M:%S (%d.%m.%y)")


def get_logger(filename: str, name: str):
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

    return logger
