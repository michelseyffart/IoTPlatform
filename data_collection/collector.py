import paho.mqtt.client as mqtt
import time
import pickle
import datetime
import logs.create_logger as logs
import logging
import fiware.config.config as fiware_config
from openhab.config.paths import path_secondary_disk, path_rawdata_MQTT_folder, path_rawdata_python_folder
import shutil


class MQTTCollector:
    def __init__(self, month: int, scenario: str, auction_type: str):
        self.log = logs.get_logger(filename="run.log", name="MQTTCollector", consolelevel=logging.INFO)
        folder = path_rawdata_MQTT_folder
        time_now = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
        simulation_id = f"{scenario}-{month}-{auction_type}"
        self.file_name = folder.joinpath(f"{simulation_id}-{time_now}.p")
        url_mosquitto = fiware_config.get_from_config("url_mosquitto")
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.connect(url_mosquitto)
        self.mqttc.subscribe("data/#")
        self.mqttc.subscribe("json/#")
        self.mqttc.subscribe("transaction/#")
        self.mqttc.subscribe("public_info/#")
        self.log.info("Created MQTT data collector")

    def start(self):
        self.mqttc.loop_start()
        self.log.info("Data collector started")

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        time_now = datetime.datetime.now()
        data_to_save = [topic, payload, time_now]
        with open(self.file_name, "ab") as f:
            pickle.dump(data_to_save, file=f,)

    def stop(self):
        self.mqttc.loop_stop()
        self.log.info("Data collector stopped")


class PythonCollector:
    def __init__(self):
        self.log = logs.get_logger(filename="run.log", name="PythonCollector", consolelevel=logging.INFO)
        folder = path_rawdata_python_folder
        time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.file_name = folder.joinpath(f"{time_now}.p")
        self.log.info("Created Python data collector")

    def save_data(self, data):
        time_now = datetime.datetime.now()
        data_to_save = [data, time_now]
        with open(self.file_name, "ab") as f:
            pickle.dump(data_to_save, file=f)


def save_data_to_secondary_disk():
    try:
        shutil.copytree(path_rawdata_MQTT_folder, path_secondary_disk.joinpath("rawdata_MQTT"), dirs_exist_ok=True)
        shutil.copytree(path_rawdata_python_folder, path_secondary_disk.joinpath("rawdata_python"), dirs_exist_ok=True)
    except shutil.Error as e:
        logging.error(f"Couldn't save data to secondary disk: {e}.")


if __name__ == "__main__":
    c = MQTTCollector()
    c.start()
    time.sleep(30)
    c.stop()
