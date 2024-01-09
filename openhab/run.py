import logging
import time

import paho.mqtt.client as mqtt
from setup import *
import openhab.create_logger as logs
import coordinator.coordinator as coordinator

log = logs.get_logger(filename="run.log", name="run", consolelevel=logging.INFO)

mqttc = mqtt.Client()
mqttc.connect("137.226.248.250")

initial_values = {
    "n_opt": 0,
    "soc": 50,
    "strategy": "random_bid"
}

buildings = [str(x) for x in range(5)]


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
    coordinator.coordinator_loop(duration=duration)
    stop_buildings()
    time.sleep(2)
    clear()


if __name__ == "__main__":
    setup_run_and_clear(duration=30)
