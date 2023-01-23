from flask import Flask, request
from statistics import mean
from custom.cfg import Aggregator
from custom.customThread import customThread
from time import sleep
from datetime import datetime
import json
import requests
import threading
import colorama
colorama.init(autoreset=True)

customData = {}
def startAggregator(id, cfg, port):
    global customData
    customData[id] = []
    app = Flask(__name__)
    @app.route('/receive', methods=['POST'])
    def collect():
        global customData
        received = json.loads(request.json)
        data = received['content']
        for line in data:
            customData[id].append(int(line['Temperature']))
        return 'OK'

    @app.route('/history', methods=['GET'])
    def sendHistory():
        return json.dumps(cfg.history)

    def interval(id, cfg):
        global customData
        customData[id] = []
        result = 0
        while True:
            sleep(int(cfg.send_frequency))
            if len(customData[id]):
                if cfg.destination_form == 'avg':
                    result = mean(customData[id])
                elif cfg.destination_form == 'sum':
                    result = sum(customData[id])
                # if requests.post(cfg.address, data={'customData': result}, timeout=10):
                #     print(f'Data sent [{cfg.title}]')
                message = {
                    'content': result,
                    'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    'from': cfg.title
                }
                if requests.post(cfg.address, json=json.dumps(message), timeout=10):
                    cfg.addElementToHistory(message['content'])
                    print(f"{colorama.Fore.LIGHTGREEN_EX}({message['date']}) Data sent [{cfg.title}]")
                else:
                    print(f"{colorama.Fore.LIGHTRED_EX}({message['date']}) Error")
                customData[id] = []

    customThread(target=interval, cfgId=id, name='aggregatorNested', args=(id, cfg)).start()
    print(f'{colorama.Fore.CYAN}Nested thread started [{cfg.title}]')
    app.run(port=port)

