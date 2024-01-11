import paho.mqtt.client as mqtt
import time
import pickle
import datetime
from pathlib import Path
import logs.create_logger as logs
import logging


class Collector:
    def __init__(self):
        self.log = logs.get_logger(filename="run.log", name="collector", consolelevel=logging.INFO)
        folder = Path(__file__).parent.joinpath("rawdata").resolve()
        time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.file_name = folder.joinpath(f"{time_now}.p")
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.connect("137.226.248.250")
        self.mqttc.subscribe("data/#")
        self.log.info("Created data collector")

    def start(self):
        self.mqttc.loop_start()
        self.log.info("Data collector started")

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        data_to_save = [topic, payload]
        with open(self.file_name, "ab") as f:
            pickle.dump(data_to_save, file=f)

    def stop(self):
        self.mqttc.loop_stop()
        self.log.info("Data collector stopped")


if __name__ == "__main__":
    c = Collector()
    c.start()
    time.sleep(30)
    c.stop()
