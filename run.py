import logging

import paho.mqtt.client as mqtt
import openhab.setup as setup
import logs.create_logger as logs
import market.coordinator as coordinator
import datetime
import openhab.config.config as config
import data_collection.collector as collector
import time
import json
import fiware.config.config as fiware_config

log = logs.get_logger(filename="run.log", name="run", consolelevel=logging.INFO)

url_mosquitto = fiware_config.get_from_config("url_mosquitto")
mqttc = mqtt.Client()
mqttc.connect(url_mosquitto)


initial_values = {
    "n_opt": 0,
    "soc_bat": 0,
    "soc_tes": 0,
    "demand": 0,
    "surplus": 0,
    "price": 0,
    "quant": 0,
    "strategy": "learning",
    "total_trans_quant": 0,
    "total_trans_price": 0,
    "learning_bid_prop": 0.01
}

scenario_options = {
    "scenario": "40_1",
    "month": 1
}

starting_step_for_month = {
    1: 0,
    4: 2160,
    7: 4344
}

buildings = [str(x) for x in range(40)]
buildings.append("WT")


def set_initial_values(buildings_: list, month_: int = None, scenario_: str = None):
    log.info("Setting initial values")
    if month_:
        scenario_options["month"] = month_
        initial_values["n_opt"] = starting_step_for_month[month_]
    if scenario_:
        scenario_options["scenario"] = scenario_
    if not mqttc.is_connected():
        mqttc.reconnect()
    set_gateways("OFF")
    for building in buildings_:
        for key in initial_values.keys():
            mqttc.publish(topic=f"init_value/{building}/{key}", payload=f"{initial_values[key]}")
        time.sleep(1)
    for key, value in scenario_options.items():
        mqttc.publish(topic=key, payload=value)
    time.sleep(1)
    set_gateways("ON")
    time.sleep(1)
    log.info("Set initial values")
    return


def set_gateways(value):
    if not mqttc.is_connected():
        mqttc.reconnect()
    mqttc.publish(topic="gateway", payload=value)
    log.info(f"Set gateways to {value}.")


def send_dummy_transactions(buildings_: list):
    log.info(f"Sending dummy transactions.")
    dummy_bid = {
        "buying": False,
        "price": 0.15,
        "quant": 100
    }
    if not mqttc.is_connected():
        mqttc.reconnect()
    for building in buildings_:
        mqttc.publish(topic=f"transactions/Transaction:{building}", payload=json.dumps(dummy_bid))
    log.info(f"Sent dummy transactions.")


def send_dummy_public_info():
    log.info(f"Sending dummy public info to trigger bid adjustment.")
    dummy_public_info = {
        "equilibrium_price": 0.3,
        "equilibrium_quantity": 200
    }
    if not mqttc.is_connected():
        mqttc.reconnect()
    mqttc.publish(topic=f"public_info", payload=json.dumps(dummy_public_info))


def start_buildings():
    log.info("Starting buildings")
    if not mqttc.is_connected():
        mqttc.reconnect()
    mqttc.publish(topic="active", payload="start")
    time.sleep(1)
    log.info("Started buildings")


def stop_buildings():
    log.info("Stopping buildings")
    if not mqttc.is_connected():
        mqttc.reconnect()
    mqttc.publish(topic="active", payload="stop")
    time.sleep(1)
    log.info("Stopped buildings")


def complete_setup(buildings_: list, pre_optimized: bool = False):
    log.info(f"Setting up openHAB")
    setup.setup_everything(buildings=buildings_, pre_optimized=pre_optimized)
    log.info("Set up complete")


def clear():
    log.info("Clearing openHAB")
    setup.hard_clear()
    log.info("Clearing complete")


def run_simulation(clearing_mechanism: str, duration: int = 180):
    c = coordinator.Coordinator()
    data_collector = collector.MQTTCollector()
    data_collector.start()
    log.info("Waiting to start")
    time.sleep(len(buildings)/2)
    start_at_second = config.get_from_params("time_for_step")
    while not int(datetime.datetime.now().strftime("%S")) % start_at_second == start_at_second - 5:
        time.sleep(0.1)
    set_gateways("ON")
    start_buildings()
    time.sleep(5)
    c.coordinator_loop(duration=duration, clearing_mechanism=clearing_mechanism)
    time.sleep(5)
    stop_buildings()
    time.sleep(2)
    data_collector.stop()


def setup_run_and_clear(clearing_mechanism: str, duration: int = 180):
    complete_setup(buildings_=buildings)
    time.sleep(5)
    set_initial_values(buildings_=buildings)
    run_simulation(duration=duration, clearing_mechanism=clearing_mechanism)
    clear()


def set_up_sequence(pre_optimized):
    log.info("Starting Set Up Sequence")
    complete_setup(buildings_=buildings, pre_optimized=pre_optimized)
    time.sleep(60)
    set_gateways("OFF")
    time.sleep(30)
    set_initial_values(buildings_=buildings)
    time.sleep(30)
    start_buildings()
    time.sleep(180)
    stop_buildings()
    time.sleep(60)
    start_buildings()
    set_gateways("ON")
    time.sleep(180)
    stop_buildings()
    set_gateways("OFF")
    time.sleep(60)
    send_dummy_transactions(buildings_=buildings)
    time.sleep(180)
    send_dummy_public_info()
    time.sleep(180)
    set_gateways("ON")
    send_dummy_public_info()
    time.sleep(180)

    log.info(f"Setup complete")


if __name__ == "__main__":
    #clear()
    #complete_setup(buildings_=buildings, pre_optimized=True)
    #set_up_sequence(pre_optimized=True)
    for auction_type in ["d"]:
        for scenario in ["40_1", "40_2"]:
            for month in [1, 4, 7]:
                log.info(f"Starting: auction_type: {auction_type}, scenario: {scenario}, month: {month}")
                set_initial_values(buildings_=buildings, scenario_=scenario, month_=month)
                run_simulation(clearing_mechanism=auction_type, duration=30)
                log.info(f"Finished: auction_type: {auction_type}, scenario: {scenario}, month: {month}")
                time.sleep(10)
    mqttc.disconnect()
