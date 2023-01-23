from custom.cfg import Configuration
from custom.timer import timer
from custom.csvToJson import csvToJson
from custom.parse import parse

import paho.mqtt.client as mqtt
import os
import requests

def publish(id, cfg):
    def on_publish(client, userdata, mid):
        print(f'Data sent [MQTT]')

    print('\n', cfg)

    scriptName = cfg.title
    client = mqtt.Client(scriptName)
    client.on_publish = on_publish

    live = 0
    while True:
        data = csvToJson(cfg.dataset).dataInJson

        if cfg.request.upper() == "MQTT":
            client.connect(cfg.address)
            client.publish(cfg.MQTT_topic, data)
            client.disconnect()

        elif cfg.request.upper() == "HTTP":
            if requests.post(cfg.address, data={'json': data}):
                print(f'Data sent [{cfg.title}]')
            else:
                print('Error')

        live += timer(live, cfg.send_frequency, 1)
