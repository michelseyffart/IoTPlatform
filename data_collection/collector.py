import paho.mqtt.client as mqtt
import time
import pickle
import datetime

mqttc = mqtt.Client()
mqttc.connect("137.226.248.250")


class Collector:
    def __init__(self):
        time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.file_name = f"rawdata/{time_now}.p"
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.connect("137.226.248.250")
        self.mqttc.subscribe("data/#")

    def start(self):
        self.mqttc.loop_start()

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        data_to_save = [topic, payload]
        with open(self.file_name, "ab") as f:
            pickle.dump(data_to_save, file=f)
        print("Saved message")

    def stop(self):
        self.mqttc.loop_stop()


if __name__ == "__main__":
    c = Collector()
    c.start()
    time.sleep(30)
    c.stop()
