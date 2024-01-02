import logging
import time

import paho.mqtt.client as mqtt
from setup import *
import openhab.create_logger as logs
from coordinator.coordinator import coordinator_loop

log = logs.get_logger(filename="run.log", name="run", consolelevel=logging.INFO)

mqttc = mqtt.Client()
mqttc.connect("137.226.248.250")

initial_values = {
    "n_opt": 0,
    "soc": 50,
    "strategy": "bid"
}

buildings = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
#buildings = ["0", "1"]


def set_initial_values():
    for building in buildings:
        for key in initial_values.keys():
            mqttc.publish(topic=f"{building}/{key}", payload=f"{initial_values[key]}")
    time.sleep(1)
    log.info("Set initial values")
    return


def start_buildings():
    mqttc.publish(topic="active", payload="start")
    log.info("Started buildings")


def stop_buildings():
    mqttc.publish(topic="active", payload="stop")
    log.info("Stopped buildings")


def setup():
    setup_everything(buildings=buildings)
    log.info("Set up complete")


def clear():
    clear_everything(buildings=buildings)
    log.info("Clearing complete")


def setup_run_and_clear(duration: int = 180):
    setup()
    time.sleep(5)
    set_initial_values()
    time.sleep(5)
    start_buildings()
    coordinator_loop()
    time.sleep(duration)
    stop_buildings()
    time.sleep(2)
    clear()


if __name__ == "__main__":
    setup_run_and_clear(duration=30)
