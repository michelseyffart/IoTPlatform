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
mqttc.connect(url_mosquitto, keepalive=3600)


initial_values = {
    "n_opt": 4344,
    "soc_bat": 0,
    "soc_tes": 0,
    "strategy": "learning",
    "total_trans_quant": 0,
    "total_trans_price": 0,
    "learning_bid_prop": 0.01
}

scenario_options = {
    "scenario": "40_2",
    "month": 7
}

buildings = [str(x) for x in range(40)]
buildings.append("WT")


def set_initial_values(buildings_: list):
    log.info("Setting initial values")
    for building in buildings_:
        for key in initial_values.keys():
            mqttc.publish(topic=f"{building}/{key}", payload=f"{initial_values[key]}")
        time.sleep(1)
    time.sleep(1)
    log.info("Set initial values")
    return


def set_scenario_options():
    log.info("Setting scenario options")
    for key, value in scenario_options.items():
        mqttc.publish(topic=key, payload=value)
    time.sleep(1)
    log.info(f"Set scenario options to {scenario_options}.")
    return


def set_gateways(value):
    log.info(f"Setting gateways to {value}.")
    mqttc.publish(topic="gateway", payload=value)


def send_dummy_transactions(buildings_: list):
    log.info(f"Sending dummy transactions.")
    dummy_bid = {
        "buying": False,
        "price": 0.15,
        "quant": 100
    }
    for building in buildings_:
        mqttc.publish(topic=f"transactions/Transaction:{building}", payload=json.dumps(dummy_bid))
    log.info(f"Sent dummy transactions.")


def send_dummy_public_info():
    log.info(f"Sending dummy public info to trigger bid adjustment.")
    dummy_public_info = {
        "equilibrium_price": 0.3,
        "equilibrium_quantity": 200
    }
    mqttc.publish(topic=f"public_info", payload=json.dumps(dummy_public_info))


def start_buildings():
    log.info("Starting buildings")
    mqttc.publish(topic="active", payload="start")
    time.sleep(1)
    log.info("Started buildings")


def stop_buildings():
    log.info("Stopping buildings")
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
    set_scenario_options()
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
    clear()
    set_up_sequence(pre_optimized=True)
