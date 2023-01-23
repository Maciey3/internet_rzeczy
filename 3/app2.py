from custom.getCfg import Configuration
from custom.timer import timer
from custom.csvToJson import csvToJson

import paho.mqtt.client as mqtt
import os
import requests


def publish():
    def on_publish(client, userdata, mid):
        print("Data published")


    cfg = Configuration()
    datasetName = cfg.getFirstUnworkingDataset()
    if not datasetName:
        print("Not available datasets")
        return False

    data = csvToJson(datasetName).dataInJson

    if cfg.request.upper() == "MQTT":
        scriptName = os.path.basename(__file__)
        client = mqtt.Client(scriptName)
        client.on_publish = on_publish

        live = 0
        while True:
            live += timer(live, cfg.send_frequency, 1)
            client.connect(cfg.address)
            client.publish(cfg.MQTT_topic, data)
            client.disconnect()

            if live >= cfg.live_time:
                cfg.unmarkDataset(datasetName)
                return True

    elif cfg.request.upper() == "HTTP":

        live = 0
        while True:
            live += timer(live, cfg.send_frequency, 1)
            if requests.post(cfg.address, data={'json': data}):
                print('Data sent')
            else:
                print('Error')

            if live >= cfg.live_time:
                # cfg.unmarkDataset(datasetName)
                return True

publish()
