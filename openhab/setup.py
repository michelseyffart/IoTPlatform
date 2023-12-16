import time

from elements.building import setup_building, clear_building
from elements.addons import install_all_addons
from elements.broker import setup_mqtt_structure, delete_mqtt_structure


def clear_everything(buildings: list):
    for building in buildings:
        clear_building(building)
    delete_mqtt_structure()


def setup_everything(buildings: list):
    setup_mqtt_structure()
    for building in buildings:
        setup_building(building)


def reset():
    clear_everything()
    time.sleep(2)
    setup_everything()


if __name__ == "__main__":
    clear_building("0")
