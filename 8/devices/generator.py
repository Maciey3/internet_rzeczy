from custom.cfg import Configuration
from custom.timer import timer
from custom.csvToJson import csvToJson
from custom.customThread import customThread
from datetime import datetime
import paho.mqtt.client as mqtt
import requests
import json
from flask import Flask, request
import threading
import colorama
colorama.init(autoreset=True)

def startGenerator(id, cfg, port):
    app = Flask(__name__)

    @app.route('/history', methods=['GET'])
    def sendHistory():
        return json.dumps(cfg.history)


    def interval(id, cfg):
        def on_publish(client, userdata, mid):
            print(f'Data sent [MQTT]')

        scriptName = cfg.title
        client = mqtt.Client(scriptName)
        client.on_publish = on_publish

        live = 0
        while True:
            data = json.loads(csvToJson(cfg.dataset).dataInJson)
            message = {
                'content': data,
                'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                'from': cfg.title
            }

            if cfg.request.upper() == "MQTT":
                client.connect(cfg.address)
                client.publish(cfg.MQTT_topic, message)
                client.disconnect()

            elif cfg.request.upper() == "HTTP":
                if requests.post(cfg.address, json=json.dumps(message), timeout=10):
                    cfg.addElementToHistory(message['content'])
                    print(f"{colorama.Fore.LIGHTGREEN_EX}({message['date']}) Data sent [{cfg.title}]")
                else:
                    print(f"{colorama.Fore.LIGHTRED_EX}({message['date']}) Error")

            live += timer(live, cfg.send_frequency, 1)

    customThread(target=interval, cfgId=id, name='generatorNested', args=(id, cfg)).start()
    print(f'{colorama.Fore.CYAN}Nested thread started [{cfg.title}]')
    app.run(port=port)
