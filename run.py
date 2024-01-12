import logging

import paho.mqtt.client as mqtt
from openhab.setup import *
import logs.create_logger as logs
import market.coordinator as coordinator
import datetime
import openhab.config.config as config
import data_collection.collector as collector
import time

log = logs.get_logger(filename="run.log", name="run", consolelevel=logging.INFO)

mqttc = mqtt.Client()
mqttc.connect("137.226.248.250")

initial_values = {
    "n_opt": 0,
    "soc": 50,
    "strategy": "random_bid"
}

buildings = [str(x) for x in range(20)]


def set_initial_values():
    log.info("Setting initial values")
    for building in buildings:
        for key in initial_values.keys():
            mqttc.publish(topic=f"{building}/{key}", payload=f"{initial_values[key]}")
    time.sleep(1)
    log.info("Set initial values")
    return


def start_buildings():
    log.info("Starting buildings")
    mqttc.publish(topic="active", payload="start")
    log.info("Started buildings")


def stop_buildings():
    log.info("Stopping buildings")
    mqttc.publish(topic="active", payload="stop")
    log.info("Stopped buildings")


def setup():
    log.info("Setting up openHAB")
    setup_everything(buildings=buildings)
    log.info("Set up complete")


def clear():
    log.info("Clearing openHAB")
    clear_everything(buildings=buildings)
    log.info("Clearing complete")


def run_simulation(clearing_mechanism: str, duration: int = 180):
    c = coordinator.Coordinator()
    data_collector = collector.MQTTCollector()
    data_collector.start()
    log.info("Waiting to start")
    time.sleep(len(buildings))
    start_at_second = config.get_from_params("time_for_step")
    while not int(datetime.datetime.now().strftime("%S")) % 10 == start_at_second - 1:
        time.sleep(0.1)
    start_buildings()
    time.sleep(1)
    c.coordinator_loop(duration=duration, clearing_mechanism=clearing_mechanism)
    stop_buildings()
    time.sleep(2)
    data_collector.stop()


def setup_run_and_clear(clearing_mechanism: str, duration: int = 180):
    setup()
    time.sleep(5)
    set_initial_values()
    run_simulation(duration=duration, clearing_mechanism=clearing_mechanism)
    clear()


if __name__ == "__main__":
    run_simulation(duration=60, clearing_mechanism="c")
    #setup()
    #set_initial_values()
