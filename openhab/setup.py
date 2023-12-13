import uuid
from openhab_interface import openhab_request, bridge_uid
from openhab.config.config import *


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
    openhab_request(payload=thing_start_stop, endpoint="/things", method="POST")


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
    openhab_request(payload=rule_timer, endpoint="/rules", method="POST")


def post_item_active_switch():
    with open("templates/items/item_active_switch") as f:
        item_active_switch = json.load(f)
    openhab_request(payload=item_active_switch, endpoint="/items/Active_Switch", method="PUT")


def post_link_activate_switch():
    thing_start_stop_uid = get_from_config("thing_start_stop_uid")
    channel_uid = f"{thing_start_stop_uid}:Start_Stop"
    item_name = "Active_Switch"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")


def setup_timer():
    post_item_active_switch()
    post_thing_start_stop()
    post_link_activate_switch()
    post_rule_timer()


if __name__ == "__main__":
    setup_timer()
