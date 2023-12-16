import logging

import paho.mqtt.client as mqtt
from setup import *
import openhab.create_logger as logs

log = logs.get_logger(filename="run.log", name="run", consolelevel=logging.INFO)

mqttc = mqtt.Client()
mqttc.connect("137.226.248.250")

initial_values = {
    "n_opt": 0,
    "soc": 50
}

buildings = ["0", "1", "2", "3"]


def set_initial_values():
    for building in buildings:
        for key in initial_values.keys():
            mqttc.publish(topic=f"{building}/{key}", payload=f"{initial_values[key]}")
    log.info("Set initial values")


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


if __name__ == "__main__":
    setup()
    time.sleep(1)
    set_initial_values()
    time.sleep(1)
    start_buildings()
    time.sleep(10)
    stop_buildings()
    time.sleep(1)
    clear()
    mqttc.disconnect()
