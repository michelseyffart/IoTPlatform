import random
import uuid
from openhab.openhab_interface import openhab_request
from openhab.config.config import *
from openhab.config.paths import *
import logs.create_logger as logs

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
    rc = openhab_request(payload=item_soc, endpoint=f"/items/", method="PUT")
    log.info(f"Posted Items Soc {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/soc_tes_{building_id}/metadata/stateDescription",
                         method="PUT")
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/soc_bat_{building_id}/metadata/stateDescription",
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
    rc = openhab_request(payload="OFF",
                         endpoint=f"/items/active_switch_{building_id}/state", method="PUT", content_type="text/plain")
    log.info(f"Posted State OFF Active Switch {building_id}: {rc}")


def post_link_active_switch(building_id: str):
    # create a link between the MQTT binding and the Active Switch
    thing_start_stop_uid = get_from_config("thing_start_stop_uid")
    channel_uid = f"{thing_start_stop_uid}:Start_Stop"
    item_name = f"active_switch_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Active Switch: {rc}")


def post_rule_timer(building_id: str, pre_optimized):
    # create a Timer Rule that triggers an action every given interval
    with open(path_templates_folder/"rules"/"rule_timer.json") as f:
        template_rule_timer = f.read()
    rule_timer_uid = str(uuid.uuid4()).split("-")[0]
    param_time_for_step = get_from_params("time_for_step")
    param_random_start = get_from_params("range_for_random_start")
    param_recency = get_from_params("learning_bid/recency")
    param_experimental = get_from_params("learning_bid/experimental")
    scenario = get_from_params("scenario")
    random_start = random.randint(0, param_random_start)
    template_rule_timer = template_rule_timer.replace(
        "RULE_TIMER_UID", rule_timer_uid).replace(
        "BUILDING_ID", building_id).replace(
        "RANDOM_START", str(random_start)).replace(
        "LENGTH", str(param_time_for_step))
    bridge_uid = get_from_config(key="bridge_uid")
    if pre_optimized:
        with open(path_templates_folder / "scripts" / "script_grid_and_pre_optimized") as f:
            script_pre_optimized_template = f.read()
        script_pre_optimized = script_pre_optimized_template.replace(
            "BRIDGE_UID", bridge_uid).replace(
            "BUILDING_ID", building_id).replace(
            "SCENARIO", scenario).replace(
            "RECENCY", str(param_recency)).replace(
            "EXPERIMENTAL", str(param_experimental))
        rule_timer = json.loads(template_rule_timer)
        rule_timer["actions"][0]["configuration"]["script"] = script_pre_optimized
    else:
        with open(path_templates_folder / "scripts" / "script_grid_and_opti") as f:
            script_grid_and_opti_template = f.read()
        script_grid_and_opti = script_grid_and_opti_template.replace(
            "BRIDGE_UID", bridge_uid).replace(
            "BUILDING_ID", building_id).replace(
            "SCENARIO", scenario).replace(
            "RECENCY", str(param_recency)).replace(
            "EXPERIMENTAL", str(param_experimental))
        rule_timer = json.loads(template_rule_timer)
        rule_timer["actions"][0]["configuration"]["script"] = script_grid_and_opti
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

    channel_uid = f"{thing_building_uid}:soc_tes_{building_id}"
    item_name = f"soc_tes_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Soc Tes {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:soc_bat_{building_id}"
    item_name = f"soc_bat_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Soc Bat {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:n_opt_{building_id}"
    item_name = f"n_opt_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link n_opt {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:strategy_{building_id}"
    item_name = f"strategy_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Strategy {building_id}: {rc}")


def post_rule_bid(building_id: str):
    with open(path_templates_folder/"rules"/"rule_bid.json") as f:
        template_rule_bid = f.read()
    with open(path_templates_folder/"scripts"/"script_bid") as f:
        script_bid_template = f.read()
    with open(path_templates_folder/"scripts"/"script_bid_WT") as f:
        script_bid_wt_template = f.read()
    rule_bid_uid = str(uuid.uuid4()).split("-")[0]
    template_rule_bid = template_rule_bid.replace(
        "RULE_BID_UID", rule_bid_uid).replace(
        "BUILDING_ID", building_id)
    bridge_uid = get_from_config(key="bridge_uid")
    rule_bid = json.loads(template_rule_bid)
    if building_id == "WT":
        rule_bid["actions"][0]["configuration"]["script"] = script_bid_wt_template
    else:
        script_bid = script_bid_template.replace("BUILDING_ID", building_id)
        rule_bid["actions"][0]["configuration"]["script"] = script_bid
    save_to_config(key=f"rule_bid_{building_id}_uid", value=rule_bid_uid)
    rc = openhab_request(payload=rule_bid, endpoint="/rules", method="POST")
    log.info(f"Posted Rule Bid {building_id}: {rc}")


def post_items_bid(building_id:str):
    with open(path_templates_folder/"items"/"items_bid.json") as f:
        items_bid_template = f.read()
    items_bid_template = items_bid_template.replace("BUILDING_ID", building_id)
    items_bid = json.loads(items_bid_template)
    rc = openhab_request(payload=items_bid, endpoint=f"/items/", method="PUT")
    log.info(f"Posted Items Bid {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/quant_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Quant {building_id}: {rc}")
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/price_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Price {building_id}: {rc}")
    rc = openhab_request(payload=metadata_float,
                         endpoint=f"/items/adjusted_price_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Adjusted Price {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_string.json") as f:
        metadata_string = json.load(f)
    rc = openhab_request(payload=metadata_string, endpoint=f"/items/buying_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Buying {building_id}: {rc}")
    rc = openhab_request(payload=metadata_string, endpoint=f"/items/strategy_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Strategy {building_id}: {rc}")


def post_items_grid(building_id:str):
    with open(path_templates_folder/"items"/"items_grid.json") as f:
        items_grid_template = f.read()
    items_grid_template = items_grid_template.replace("BUILDING_ID", building_id)
    items_grid = json.loads(items_grid_template)
    rc = openhab_request(payload=items_grid, endpoint=f"/items/", method="PUT")
    log.info(f"Posted Items Grid {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/to_grid_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata To Grid {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/from_grid_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata From Grid {building_id}: {rc}")


def post_items_transaction(building_id:str):
    with open(path_templates_folder/"items"/"items_transaction.json") as f:
        items_transaction_template = f.read()
    items_transaction_template = items_transaction_template.replace("BUILDING_ID", building_id)
    items_transaction = json.loads(items_transaction_template)
    rc = openhab_request(payload=items_transaction, endpoint=f"/items/", method="PUT")
    log.info(f"Posted Items Transaction {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/trans_quant_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Transaction Quant {building_id}: {rc}")
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/trans_price_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Transaction Price {building_id}: {rc}")
    rc = openhab_request(payload=metadata_float,
                         endpoint=f"/items/total_trans_price_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Total Transaction Price {building_id}: {rc}")
    rc = openhab_request(payload=metadata_float,
                         endpoint=f"/items/total_trans_quant_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Total Transaction Price {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_string.json") as f:
        metadata_string = json.load(f)
    rc = openhab_request(payload=metadata_string, endpoint=f"/items/trans_buying_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Transaction Buying {building_id}: {rc}")


def post_links_transaction(building_id: str):
    # create links
    thing_building_uid = get_from_config(key=f"thing_building_{building_id}_uid")

    channel_uid = f"{thing_building_uid}:trans_buying_{building_id}"
    item_name = f"trans_buying_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Transaction Buying {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:trans_price_{building_id}"
    item_name = f"trans_price_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Transaction Price {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:trans_quant_{building_id}"
    item_name = f"trans_quant_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Transaction Quantity {building_id}: {rc}")

    #channel_uid = f"{thing_building_uid}:total_trans_quant_{building_id}"
    #item_name = f"total_trans_quant_{building_id}"
    #payload = {"itemName": item_name, "channelUID": channel_uid}
    #rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    #log.info(f"Posted Link Total Transaction Quantity {building_id}: {rc}")

    #channel_uid = f"{thing_building_uid}:total_trans_price_{building_id}"
    #item_name = f"total_trans_price_{building_id}"
    #payload = {"itemName": item_name, "channelUID": channel_uid}
    #rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    #log.info(f"Posted Link Total Transaction Price {building_id}: {rc}")


def post_rule_transaction(building_id: str):
    with open(path_templates_folder / "rules" / "rule_transaction.json") as f:
        template_rule_transaction = f.read()
    with open(path_templates_folder / "scripts" / "script_transaction") as f:
        script_transaction_template = f.read()
    rule_uid = str(uuid.uuid4()).split("-")[0]
    template_rule_transaction = template_rule_transaction.replace(
        "RULE_UID", rule_uid).replace(
        "BUILDING_ID", building_id)
    script_transaction = script_transaction_template.replace(
        "BUILDING_ID", building_id)
    rule_transaction = json.loads(template_rule_transaction)
    rule_transaction["actions"][0]["configuration"]["script"] = script_transaction
    save_to_config(key=f"rule_transaction_{building_id}_uid", value=rule_uid)
    rc = openhab_request(payload=rule_transaction, endpoint="/rules", method="POST")
    log.info(f"Posted Rule Transaction {building_id}: {rc}")


def post_rule_bid_to_fiware(building_id: str):
    with open(path_templates_folder / "rules" / "rule_bid_to_fiware.json") as f:
        template_rule_bid_to_fiware = f.read()
    with open(path_templates_folder / "scripts" / "script_bid_to_fiware") as f:
        script_bid_to_fiware_template = f.read()
    rule_uid = str(uuid.uuid4()).split("-")[0]
    template_rule_bid_to_fiware = template_rule_bid_to_fiware.replace(
        "RULE_UID", rule_uid).replace(
        "BUILDING_ID", building_id)
    bridge_uid = get_from_config(key="bridge_uid")
    script_bid_to_fiware = script_bid_to_fiware_template.replace(
        "BUILDING_ID", building_id).replace(
        "BRIDGE_UID", bridge_uid)
    rule_bid_to_fiware = json.loads(template_rule_bid_to_fiware)
    rule_bid_to_fiware["actions"][0]["configuration"]["script"] = script_bid_to_fiware
    save_to_config(key=f"rule_bid_to_fiware_{building_id}_uid", value=rule_uid)
    rc = openhab_request(payload=rule_bid_to_fiware, endpoint="/rules", method="POST")
    log.info(f"Posted Rule Bid to Fiware {building_id}: {rc}")


def post_rule_adjusted_bid_to_fiware(building_id: str):
    with open(path_templates_folder / "rules" / "rule_adjusted_bid_to_fiware.json") as f:
        template_rule_adjusted_bid_to_fiware = f.read()
    with open(path_templates_folder / "scripts" / "script_adjusted_bid_to_fiware") as f:
        script_adjusted_bid_to_fiware_template = f.read()
    rule_uid = str(uuid.uuid4()).split("-")[0]
    template_rule_adjusted_bid_to_fiware = template_rule_adjusted_bid_to_fiware.replace(
        "RULE_UID", rule_uid).replace(
        "BUILDING_ID", building_id)
    bridge_uid = get_from_config(key="bridge_uid")
    script_adjusted_bid_to_fiware = script_adjusted_bid_to_fiware_template.replace(
        "BUILDING_ID", building_id).replace(
        "BRIDGE_UID", bridge_uid)
    rule_adjusted_bid_to_fiware = json.loads(template_rule_adjusted_bid_to_fiware)
    rule_adjusted_bid_to_fiware["actions"][0]["configuration"]["script"] = script_adjusted_bid_to_fiware
    save_to_config(key=f"rule_adjusted_bid_to_fiware_{building_id}_uid", value=rule_uid)
    rc = openhab_request(payload=rule_adjusted_bid_to_fiware, endpoint="/rules", method="POST")
    log.info(f"Posted Rule Bid to Fiware {building_id}: {rc}")


def post_items_auction_iteration(building_id: str):
    with open(path_templates_folder/"items"/"items_auction_iteration.json") as f:
        items_auction_iteration_template = f.read()
    items_auction_iteration_template = items_auction_iteration_template.replace("BUILDING_ID", building_id)
    items_auction_iteration = json.loads(items_auction_iteration_template)
    rc = openhab_request(payload=items_auction_iteration, endpoint=f"/items/", method="PUT")
    log.info(f"Posted Items Auction Iteration {building_id}: {rc}")
    with open(path_templates_folder/"metadata"/"metadata_float.json") as f:
        metadata_float = json.load(f)
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/auction_iter_quant_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Auction Iteration Quant {building_id}: {rc}")
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/auction_iter_price_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Auction Iteration Price {building_id}: {rc}")
    rc = openhab_request(payload=metadata_float, endpoint=f"/items/auction_iter_step_{building_id}/metadata/stateDescription",
                         method="PUT")
    log.info(f"Posted Metadata Auction Iteration Step {building_id}: {rc}")


def post_links_auction_iteration(building_id: str):
    # create links
    thing_building_uid = get_from_config(key=f"thing_building_{building_id}_uid")

    channel_uid = f"{thing_building_uid}:auction_iter_step_{building_id}"
    item_name = f"auction_iter_step_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Auction Iteration Step {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:auction_iter_price_{building_id}"
    item_name = f"auction_iter_price_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Auction Iteration Price {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:auction_iter_quant_{building_id}"
    item_name = f"auction_iter_quant_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Auction Iteration Quantity {building_id}: {rc}")


def post_item_gateway(building_id: str):
    with open(path_templates_folder / "items" / "item_gateway.json") as f:
        item_gateway_template = f.read()
    item_gateway_template = item_gateway_template.replace("BUILDING_ID", building_id)
    item_gateway = json.loads(item_gateway_template)
    rc = openhab_request(payload=item_gateway, endpoint=f"/items/gateway_{building_id}", method="PUT")
    log.info(f"Posted Item Gateway {building_id}: {rc}")
    with open(path_templates_folder / "metadata" / "metadata_string.json") as f:
        metadata_string = json.load(f)
    rc = openhab_request(payload=metadata_string,
                         endpoint=f"/items/gateway_{building_id}/metadata/stateDescription", method="PUT")
    log.info(f"Posted Metadata Gateway {building_id}: {rc}")


def post_link_gateway(building_id: str):
    # create a link between the MQTT binding and the Gateway
    thing_start_stop_uid = get_from_config("thing_start_stop_uid")
    channel_uid = f"{thing_start_stop_uid}:gateway"
    item_name = f"gateway_{building_id}"
    payload = {"itemName": item_name, "channelUID": channel_uid}
    rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
    log.info(f"Posted Link Gateway: {rc}")


def post_items_learning_bid(building_id: str):
    with open(path_templates_folder / "items" / "item_group_learning_bid.json") as f:
        item_group_learning_bid_template = f.read()
    item_group_learning_bid_template = item_group_learning_bid_template.replace("BUILDING_ID", building_id)
    item_group_learning_bid = json.loads(item_group_learning_bid_template)
    rc = openhab_request(payload=item_group_learning_bid, endpoint=f"/items/learning_bid_{building_id}",
                         method="PUT")
    log.info(f"Posted Item Group Learning Bid {building_id}: {rc}")

    thing_building_uid = get_from_config(key=f"thing_building_{building_id}_uid")
    min_price = get_from_params("learning_bid/min_price")
    max_price = get_from_params("learning_bid/max_price")
    step_width = get_from_params("learning_bid/step_width")
    for price in range(min_price, max_price+step_width, step_width):
        price = str(price)
        for bid_type in ["buying", "selling"]:
            with open(path_templates_folder / "items" / "item_learning_bid_prop.json") as f:
                item_learning_bid_prop_template = f.read()
            item_learning_bid_prop_template = item_learning_bid_prop_template.replace(
                "BUILDING_ID", building_id).replace(
                "PRICE", price).replace(
                "BUYING/SELLING", bid_type)
            item_learning_bid_prop = json.loads(item_learning_bid_prop_template)
            rc = openhab_request(payload=item_learning_bid_prop,
                                 endpoint=f"/items/{bid_type}_prop_{price}_{building_id}",
                                 method="PUT")
            log.info(f"Posted Item {bid_type} prop {price} {building_id}: {rc}")
            with open(path_templates_folder / "metadata" / "metadata_float.json") as f:
                metadata_float = json.load(f)
            rc = openhab_request(payload=metadata_float,
                                 endpoint=f"/items/{bid_type}_prop_{price}_{building_id}/metadata/stateDescription",
                                 method="PUT")
            log.info(f"Posted Metadata {bid_type} prop {price} {building_id}: {rc}")
            channel_uid = f"{thing_building_uid}:learning_bid_prop_{building_id}"
            item_name = f"{bid_type}_prop_{price}_{building_id}"
            payload = {"itemName": item_name, "channelUID": channel_uid}
            rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
            log.info(f"Posted Link {bid_type} Prop {price} {building_id}: {rc}")


def post_rule_bid_adjustment(building_id: str):
    with open(path_templates_folder / "rules" / "rule_bid_adjustment.json") as f:
        template_rule_bid_adjustment = f.read()
    with open(path_templates_folder / "scripts" / "script_bid_adjustment") as f:
        script_bid_adjustment_template = f.read()
    rule_uid = str(uuid.uuid4()).split("-")[0]
    template_rule_bid_adjustment = template_rule_bid_adjustment.replace(
        "RULE_UID", rule_uid).replace(
        "BUILDING_ID", building_id)
    script_bid_adjustment = script_bid_adjustment_template.replace(
        "BUILDING_ID", building_id)
    rule_bid_adjustment = json.loads(template_rule_bid_adjustment)
    rule_bid_adjustment["actions"][0]["configuration"]["script"] = script_bid_adjustment
    save_to_config(key=f"rule_bid_adjustment_{building_id}_uid", value=rule_uid)
    rc = openhab_request(payload=rule_bid_adjustment, endpoint="/rules", method="POST")
    log.info(f"Posted Rule bid_adjustment {building_id}: {rc}")


def post_links_init_values(building_id: str):
    thing_building_uid = get_from_config(key=f"thing_building_{building_id}_uid")

    for item in ["demand", "surplus", "soc_tes", "soc_bat", "n_opt", "strategy", "total_trans_price",
                 "total_trans_quant", "quant", "price"]:
        item_name = f"{item}_{building_id}"
        channel_uid = f"{thing_building_uid}:{item_name}"
        payload = {"itemName": item_name, "channelUID": channel_uid}
        rc = openhab_request(payload=payload, endpoint=f"/links/{item_name}/{channel_uid}", method="PUT")
        log.info(f"Posted Link {item} {building_id}: {rc}")


def setup_building(building_id: str, pre_optimized: bool = False):
    post_group(building_id)
    post_item_demand(building_id)
    post_item_surplus(building_id)
    post_item_soc(building_id)
    post_item_n_opt(building_id)
    post_item_active_switch(building_id)
    post_link_active_switch(building_id)
    post_rule_timer(building_id, pre_optimized=pre_optimized)
    post_rule_bid(building_id)
    #post_rule_bid_to_fiware(building_id)
    post_rule_adjusted_bid_to_fiware(building_id)
    post_rule_transaction(building_id)
    post_items_bid(building_id)
    post_items_transaction(building_id)
    post_items_grid(building_id)
    post_item_gateway(building_id)
    post_thing_building_topic(building_id)
    #post_links_building_values(building_id)
    post_links_transaction(building_id)
    post_link_gateway(building_id)
    post_items_learning_bid(building_id)
    post_rule_bid_adjustment(building_id)
    post_links_init_values(building_id)


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
    channel_uid = f"{thing_building_uid}:strategy_{building_id}"
    rc = openhab_request(endpoint=f"/links/strategy_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Strategy {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:trans_quant_{building_id}"
    rc = openhab_request(endpoint=f"/links/trans_quant_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Transaction Quantity {building_id}: {rc}")
    channel_uid = f"{thing_building_uid}:trans_price_{building_id}"
    rc = openhab_request(endpoint=f"/links/trans_price_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Transaction Price {building_id}: {rc}")
    channel_uid = f"{thing_building_uid}:trans_buying_{building_id}"
    rc = openhab_request(endpoint=f"/links/trans_buying_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Transaction Buying {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:total_trans_price_{building_id}"
    rc = openhab_request(endpoint=f"/links/total_trans_price_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Total Transaction Quantity {building_id}: {rc}")
    channel_uid = f"{thing_building_uid}:total_trans_quant_{building_id}"
    rc = openhab_request(endpoint=f"/links/total_trans_quant_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Total Transaction Price {building_id}: {rc}")

    channel_uid = f"{thing_building_uid}:auction_iter_quant_{building_id}"
    rc = openhab_request(endpoint=f"/links/auction_iter_quant_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Auction Iteration Quantity {building_id}: {rc}")
    channel_uid = f"{thing_building_uid}:auction_iter_price_{building_id}"
    rc = openhab_request(endpoint=f"/links/auction_iter_price_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Auction Iteration Price {building_id}: {rc}")
    channel_uid = f"{thing_building_uid}:auction_iter_step_{building_id}"
    rc = openhab_request(endpoint=f"/links/auction_iter_step_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Auction Iteration Step {building_id}: {rc}")

    channel_uid = f"{thing_start_stop_uid}:gateway"
    rc = openhab_request(endpoint=f"/links/gateway_{building_id}/{channel_uid}", method="DELETE")
    log.info(f"Deleted Links for Gateway {building_id}: {rc}")

    rc = openhab_request(endpoint=f"/things/{thing_building_uid}", method="DELETE")
    log.info(f"Deleted Thing Building {building_id}: {rc}")
    rule_bid_uid = get_from_config(key=f"rule_bid_{building_id}_uid")
    rc = openhab_request(endpoint=f"/rules/{rule_bid_uid}", method="DELETE")
    log.info(f"Deleted Rule Bid {building_id}: {rc}")
    rule_bid_to_fiware_uid = get_from_config(key=f"rule_bid_to_fiware_{building_id}_uid")
    rc = openhab_request(endpoint=f"/rules/{rule_bid_to_fiware_uid}", method="DELETE")
    log.info(f"Deleted Rule Bid to Fiware {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/quant_{building_id}", method="DELETE")
    log.info(f"Deleted Item Quant {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/price_{building_id}", method="DELETE")
    log.info(f"Deleted Item Quant {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/buying_{building_id}", method="DELETE")
    log.info(f"Deleted Item Price {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/strategy_{building_id}", method="DELETE")
    log.info(f"Deleted Item Price {building_id}: {rc}")

    rc = openhab_request(endpoint=f"/items/trans_quant_{building_id}", method="DELETE")
    log.info(f"Deleted Item Trans Quant {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/trans_price_{building_id}", method="DELETE")
    log.info(f"Deleted Item Trans Price {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/trans_buying_{building_id}", method="DELETE")
    log.info(f"Deleted Item Trans Buying {building_id}: {rc}")

    rc = openhab_request(endpoint=f"/items/auction_iter_quant_{building_id}", method="DELETE")
    log.info(f"Deleted Item Trans Quant {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/auction_iter_price_{building_id}", method="DELETE")
    log.info(f"Deleted Item Trans Price {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/auction_iter_step_{building_id}", method="DELETE")
    log.info(f"Deleted Item Trans Buying {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/gateway_{building_id}", method="DELETE")
    log.info(f"Deleted Item Gateway {building_id}: {rc}")

    rc = openhab_request(endpoint=f"/items/from_grid_{building_id}", method="DELETE")
    log.info(f"Deleted Item From grid {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/to_grid_{building_id}", method="DELETE")
    log.info(f"Deleted Item To grid {building_id}: {rc}")

    rc = openhab_request(endpoint=f"/items/total_trans_price_{building_id}", method="DELETE")
    log.info(f"Deleted Item Total Transaction Price {building_id}: {rc}")
    rc = openhab_request(endpoint=f"/items/total_trans_quant_{building_id}", method="DELETE")
    log.info(f"Deleted Item Total Transaction Quantity {building_id}: {rc}")

    rule_transaction_uid = get_from_config(key=f"rule_transaction_{building_id}_uid")
    rc = openhab_request(endpoint=f"/rules/{rule_transaction_uid}", method="DELETE")
    log.info(f"Deleted Rule Transaction {building_id}: {rc}")


if __name__ == "__main__":
    print()
