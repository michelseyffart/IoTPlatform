import time

from elements.building import setup_building, clear_building
from elements.addons import install_all_addons
from elements.broker import setup_mqtt_structure, delete_mqtt_structure


def clear_everything():
    clear_building("0")
    delete_mqtt_structure()


def setup_everything():
    setup_mqtt_structure()
    setup_building("1")


def reset():
    clear_everything()
    time.sleep(2)
    setup_everything()


if __name__ == "__main__":
    setup_building("1")
