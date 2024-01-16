import time
import json

from openhab.elements.building import setup_building, clear_building
from openhab.elements.addons import install_all_addons
from openhab.elements.broker import setup_mqtt_structure, delete_mqtt_structure
from openhab.openhab_interface import openhab_request
import logs.create_logger as logs

log = logs.get_logger(filename="setup.log", name="setup")


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


def hard_clear():
    concepts_with_key = [("rules", "uid"), ("items", "name"), ("things", "UID")]
    for concept_with_key in concepts_with_key:
        concept = concept_with_key[0]
        key = concept_with_key[1]
        instances = openhab_request(endpoint=f"/{concept}", method="GET", return_response_text=True)
        instance_names = [instance[key] for instance in json.loads(instances)]
        for instance_name in instance_names:
            rc = openhab_request(endpoint=f"/{concept}/{instance_name}", method="DELETE")
            log.info(f"Deleted {concept} {instance_name}: {rc}")
    rc = openhab_request(endpoint=f"/links/purge", method="POST")
    log.info(f"Deleted links: {rc}")


if __name__ == "__main__":
    clear_everything(["0"])
