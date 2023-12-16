import random
import uuid
from openhab.openhab_interface import openhab_request
from openhab.config.config import *
from openhab.config.paths import *
import openhab.create_logger as logs

log = logs.get_logger(filename="setup.log", name="building")


def post_group(building_id: str):
    with open(path_templates_folder / "items" / "item_group_building.json") as f:
        item_group_building_template = f.read()
    item_group_building_template = item_group_building_template.replace("BUILDING_ID", building_id)
    item_group_building = json.loads(item_group_building_template)
    rc = openhab_request(payload=item_group_building, endpoint=f"/items/building_{building_id}", method="PUT")
    log.info(f"Posted Item Group Building {building_id}: {rc}")


def post_item_demand(building_id: str):
    with open(path_templates_folder/"items"/"item_demand.json") as f:
        item_demand_template = f.read()
    item_demand_template = item_demand_template.replace("BUILDING_ID", building_id)
    item_demand = json.loads(item_demand_template)
    rc = openhab_request(payload=item_demand, endpoint=f"/items/demand_{building_id}", method="PUT")
    log.info(f"Posted Item Demand {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/demand_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Demand {building_id}: {rc}")


def post_item_surplus(building_id: str):
    with open(path_templates_folder/"items"/"item_surplus.json") as f:
        item_surplus_template = f.read()
    item_surplus_template = item_surplus_template.replace("BUILDING_ID", building_id)
    item_surplus = json.loads(item_surplus_template)
    rc = openhab_request(payload=item_surplus, endpoint=f"/items/surplus_{building_id}", method="PUT")
    log.info(f"Posted Item Surplus {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/surplus_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Surplus {building_id}: {rc}")


def post_item_soc(building_id: str):
    with open(path_templates_folder/"items"/"item_soc.json") as f:
        item_soc_template = f.read()
    item_soc_template = item_soc_template.replace("BUILDING_ID", building_id)
    item_soc = json.loads(item_soc_template)
    rc = openhab_request(payload=item_soc, endpoint=f"/items/soc_{building_id}", method="PUT")
    log.info(f"Posted Item Soc {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/soc_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Soc {building_id}: {rc}")


def post_item_n_opt(building_id: str):
    with open(path_templates_folder/"items"/"item_n_opt.json") as f:
        item_n_opt_template = f.read()
    item_n_opt_template = item_n_opt_template.replace("BUILDING_ID", building_id)
    item_n_opt = json.loads(item_n_opt_template)
    rc = openhab_request(payload=item_n_opt, endpoint=f"/items/n_opt_{building_id}", method="PUT")
    log.info(f"Posted Item n_opt {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_int.json") as f:
        metadata_int = json.load(f)
    rc = openhab_request(payload=metadata_int, endpoint=f"/items/n_opt_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata n_opt {building_id}: {rc}")


def post_item_active_switch(building_id: str):
    with open(path_templates_folder/"items"/"item_active_switch.json") as f:
        item_active_switch_template = f.read()
    item_active_switch_template = item_active_switch_template.replace("BUILDING_ID", building_id)
    item_active_switch = json.loads(item_active_switch_template)
    rc = openhab_request(payload=item_active_switch, endpoint=f"/items/active_switch_{building_id}", method="PUT")
    log.info(f"Posted Item Active Switch {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_string.json") as f:
        metadata_string = json.load(f)
    rc = openhab_request(payload=metadata_string,
                         endpoint=f"/items/active_switch_{building_id}/metadata/stateDescription", method="PUT")
    log.info(f"Posted Metadata Active Switch {building_id}: {rc}")


def post_link_active_switch(building_id: str):
    # create a link between the MQTT binding and the Active Switch
    thing_start_stop_uid = get_from_config("thing_start_stop_uid")
    channel_uid = f"{thing_start_stop_uid}:Start_Stop"
    item_name = f"active_switch_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Active Switch: {rc}")


def post_rule_timer(building_id: str):
    # create a Timer Rule that triggers an action every given interval
    with open(path_templates_folder/"rules"/"rule_timer.json") as f:
        template_rule_timer = f.read()
    with open(path_templates_folder/"scripts"/"script_timer") as f:
        script_timer_template = f.read()
    rule_timer_uid = str(uuid.uuid4()).split("-")[0]
    param_time_for_step = get_from_params("time_for_step")
    param_random_start = get_from_params("range_for_random_start")
    random_start = random.randint(0, param_random_start)
    template_rule_timer = template_rule_timer.replace(
        "RULE_TIMER_UID", rule_timer_uid).replace(
        "BUILDING_ID", building_id).replace(
        "RANDOM_START", str(random_start)).replace(
        "LENGTH", str(param_time_for_step))
    bridge_uid = get_from_config(key="bridge_uid")
    script_timer = script_timer_template.replace(
        "BRIDGE_UID", bridge_uid).replace(
        "BUILDING_ID", building_id)
    rule_timer = json.loads(template_rule_timer)
    rule_timer["actions"][0]["configuration"]["script"] = script_timer
    save_to_config(key=f"rule_timer_{building_id}_uid", value=rule_timer_uid)
    rc = openhab_request(payload=rule_timer, endpoint="/rules", method="POST")
    log.info(f"Posted Rule Timer {building_id}: {rc}")


def post_thing_building_topic(building_id: str):
    # create a thing that receives mqtt messages sent to building
    with open(path_templates_folder / "things" / "thing_building_topic.json") as f:
        template_thing_building = f.read()
    uid = str(uuid.uuid4()).split("-")[0]
    bridge_uid = get_from_config(key="bridge_uid")
    bridge_uid_short = get_from_config(key="bridge_uid_short")
    thing_uid = f"mqtt:topic:{bridge_uid_short}:{uid}"
    template_thing_building = template_thing_building.replace(
        "BRIDGE_UID", bridge_uid).replace(
        "THING_UID", thing_uid).replace(
        "BUILDING_ID", building_id)
    thing_building = json.loads(template_thing_building)
    save_to_config(key=f"thing_building_{building_id}_uid", value=thing_uid)
    rc = openhab_request(payload=thing_building, endpoint="/things", method="POST")
    log.info(f"Posted Thing Start Stop: {rc}")


def post_links_building_values(building_id: str):
    # create a links
    thing_building_uid = get_from_config(key=f"thing_building_{building_id}_uid")

    channel_uid = f"{thing_building_uid}:soc_{building_id}"
    item_name = f"soc_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Soc {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:n_opt_{building_id}"
    item_name = f"n_opt_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link n_opt {building_id}: {rc}")


def setup_building(building_id: str):
    post_group(building_id)
    post_item_demand(building_id)
    post_item_surplus(building_id)
    post_item_soc(building_id)
    post_item_n_opt(building_id)
    post_item_active_switch(building_id)
    post_link_active_switch(building_id)
    post_rule_timer(building_id)
    post_thing_building_topic(building_id)
    post_links_building_values(building_id)


def clear_building(building_id: str):
    rc = openhab_request(endpoint=f"/items/demand_{building_id}", method="DELETE")
    log.info(f"Deleted Item Demand {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/surplus_{building_id}", method="DELETE")
    log.info(f"Deleted Item Surplus {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/soc_{building_id}", method="DELETE")
    log.info(f"Deleted Item Soc {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/n_opt_{building_id}", method="DELETE")
    log.info(f"Deleted Item n_opt {building_id}: {rc}")
    thing_start_stop_uid = get_from_config("thing_start_stop_uid")
    channel_uid = f"{thing_start_stop_uid}:Start_Stop"
    rc = openhab_request(endpoint=f"/links/active_switch_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Item Active Switch: {rc}")
    rule_timer_uid = get_from_config(key=f"rule_timer_{building_id}_uid")
    rc = openhab_request(endpoint=f"/rules/{rule_timer_uid}", method="DELETE")
    log.info(f"Deleted Rule Timer {building_id}: {rc}")
    # delete Item Active Switch
    rc = openhab_request(endpoint=f"/items/active_switch_{building_id}", method="DELETE")
    log.info(f"Deleted Item Active Switch {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/building_{building_id}", method="DELETE")
    log.info(f"Deleted Group Building {building_id}: {rc}")

    thing_building_uid = get_from_config(f"thing_building_{building_id}_uid")
    channel_uid = f"{thing_building_uid}:soc_{building_id}"
    rc = openhab_request(endpoint=f"/links/soc_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Soc {building_id}: {rc}")
    channel_uid = f"{thing_building_uid}:n_opt_{building_id}"
    rc = openhab_request(endpoint=f"/links/n_opt_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for n_opt {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/things/{thing_building_uid}", method="DELETE")
    log.info(f"Deleted Thing Building {building_id}: {rc}")


if __name__ == "__main__":
    clear_building("0")
