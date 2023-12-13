import uuid
from openhab_interface import openhab_request, bridge_uid
from openhab.config.config import *
import openhab.create_logger as logs

log = logs.get_logger(filename="logs/setup.log", name="setup")

def post_thing_start_stop():
    with open("templates/things/start_stop.json") as f:
        template_thing_start_stop = f.read()
    uid = str(uuid.uuid4()).split("-")[0]
    bridge_uid_short = get_from_config(key="bridge_uid_short")
    thing_uid = f"mqtt:topic:{bridge_uid_short}:{uid}"
    template_thing_start_stop = template_thing_start_stop.replace(
        "BRIDGE_UID", bridge_uid).replace(
        "THING_UID", thing_uid)
    thing_start_stop = json.loads(template_thing_start_stop)
    save_to_config(key="thing_start_stop_uid", value=thing_uid)
    rc = openhab_request(payload=thing_start_stop, endpoint="/things", method="POST")
    log.info(f"Posted Thing Start Stop: {rc}")


def post_rule_timer():
    with open("templates/rules/rule_timer.json") as f:
        template_rule_timer = f.read()
    with open("templates/scripts/script_timer") as f:
        script_timer = f.read()
    rule_timer_uid = str(uuid.uuid4()).split("-")[0]
    template_rule_timer = template_rule_timer.replace(
        "RULE_TIMER_UID", rule_timer_uid)
    rule_timer = json.loads(template_rule_timer)
    rule_timer["actions"][0]["configuration"]["script"] = script_timer
    save_to_config(key="rule_timer_uid", value=rule_timer_uid)
    rc = openhab_request(payload=rule_timer, endpoint="/rules", method="POST")
    log.info(f"Posted Rule Timer: {rc}")


def post_item_active_switch():
    with open("templates/items/item_active_switch") as f:
        item_active_switch = json.load(f)
    rc = openhab_request(payload=item_active_switch, endpoint="/items/Active_Switch", method="PUT")
    log.info(f"Posted Item Active Switch: {rc}")


def post_link_activate_switch():
    thing_start_stop_uid = get_from_config("thing_start_stop_uid")
    channel_uid = f"{thing_start_stop_uid}:Start_Stop"
    item_name = "Active_Switch"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Active Switch: {rc}")


def setup_timer():
    post_item_active_switch()
    post_thing_start_stop()
    post_link_activate_switch()
    post_rule_timer()


def clear_timer():
    # delete Item Active Switch
    rc = openhab_request(endpoint=f"/items/Active_Switch", method="DELETE")
    log.info(f"Deleted Item Active Switch: {rc}")

    # delete Thing Start Stop
    thing_start_stop_uid = get_from_config(key="thing_start_stop_uid")
    rc = openhab_request(endpoint=f"/things/{thing_start_stop_uid}", method="DELETE")
    log.info(f"Deleted Thing Start Stop: {rc}")

    # delete Rule Timer
    rule_timer_uid = get_from_config(key="rule_timer_uid")
    rc = openhab_request(endpoint=f"/rules/{rule_timer_uid}", method="DELETE")
    log.info(f"Deleted Rule Timer: {rc}")


if __name__ == "__main__":
    clear_timer()
    setup_timer()
