import uuid
from openhab.openhab_interface import openhab_request
from openhab.config.config import *
import logs.create_logger as logs
from openhab.config.paths import *

log = logs.get_logger(filename="setup.log", name="setup")


def post_broker():
    with open(path_templates_folder / "things" / "broker.json") as f:
        template_thing_mqtt_broker = f.read()
    uid = str(uuid.uuid4()).split("-")[0]
    bridge_uid = f"mqtt:broker:{uid}"
    template_thing_mqtt_broker = template_thing_mqtt_broker.replace("THING_MQTT_BROKER_UID", bridge_uid)
    thing_mqtt_broker = json.loads(template_thing_mqtt_broker)
    save_to_config(key="bridge_uid", value=bridge_uid)
    save_to_config(key="bridge_uid_short", value=uid)
    rc = openhab_request(payload=thing_mqtt_broker, endpoint="/things", method="POST")
    log.info(f"Posted Thing MQTT Broker: {rc}")


def post_thing_start_stop():
    # create a MQTT binding that allows toggling the Active Switch and therefore starting and stopping the Timer Rule
    with open(path_templates_folder/"things"/"start_stop.json") as f:
        template_thing_start_stop = f.read()
    uid = str(uuid.uuid4()).split("-")[0]
    bridge_uid = get_from_config(key="bridge_uid")
    bridge_uid_short = get_from_config(key="bridge_uid_short")
    thing_uid = f"mqtt:topic:{bridge_uid_short}:{uid}"
    template_thing_start_stop = template_thing_start_stop.replace(
        "BRIDGE_UID", bridge_uid).replace(
        "THING_UID", thing_uid)
    thing_start_stop = json.loads(template_thing_start_stop)
    save_to_config(key="thing_start_stop_uid", value=thing_uid)
    rc = openhab_request(payload=thing_start_stop, endpoint="/things", method="POST")
    log.info(f"Posted Thing Start Stop: {rc}")


def post_links_public_info():
    thing_start_stop_uid = get_from_config(key=f"thing_start_stop_uid")

    channel_uid = f"{thing_start_stop_uid}:equilibrium_price"
    item_name = f"equilibrium_price"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Equilibrium Price: {rc}")

    channel_uid = f"{thing_start_stop_uid}:equilibrium_quant"
    item_name = f"equilibrium_quant"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Equilibrium Quantity: {rc}")


def post_items_public_info():
    with open(path_templates_folder/"items"/"items_public_info.json") as f:
        items_public_info = json.load(f)
    rc = openhab_request(payload=items_public_info, endpoint=f"/items/", method="PUT")
    log.info(f"Posted Items Public Info: {rc}")

    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/equilibrium_price/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Equilibrium Price: {rc}")
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/equilibrium_quant/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Equilibrium Price: {rc}")


def delete_items_public_info():
    thing_start_stop_uid = get_from_config(key=f"thing_start_stop_uid")

    channel_uid = f"{thing_start_stop_uid}:equilibrium_price"
    item_name = f"equilibrium_price"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Link Equilibrium Price: {rc}")

    channel_uid = f"{thing_start_stop_uid}:equilibrium_quant"
    item_name = f"equilibrium_quant"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Link Equilibrium Quantity: {rc}")

    rc = openhab_request(endpoint=f"/items/equilibrium_quant", method="DELETE")
    log.info(f"Deleted Item Equilibrium Quantity: {rc}")
    rc = openhab_request(endpoint=f"/items/equilibrium_price", method="DELETE")
    log.info(f"Deleted Item Equilibrium Price: {rc}")


def delete_broker():
    thing_broker_uid = get_from_config(key="bridge_uid")
    rc = openhab_request(endpoint=f"/things/{thing_broker_uid}", method="DELETE")
    log.info(f"Deleted Thing MQTT Broker: {rc}")
    delete_items_public_info()


def delete_thing_start_stop():
    # delete Thing Start Stop
    thing_start_stop_uid = get_from_config(key="thing_start_stop_uid")
    rc = openhab_request(endpoint=f"/things/{thing_start_stop_uid}", method="DELETE")
    log.info(f"Deleted Thing Start Stop: {rc}")


def setup_mqtt_structure():
    post_broker()
    post_thing_start_stop()
    post_items_public_info()
    post_links_public_info()


def delete_mqtt_structure():
    delete_thing_start_stop()
    delete_broker()

if __name__ == "__main__":
    delete_mqtt_structure()
