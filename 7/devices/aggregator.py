from flask import Flask, request
import threading
from statistics import mean
import json

from custom.cfg import Aggregator
from custom.parse import parse
from custom.customThread import customThread

import requests
from time import sleep
from datetime import datetime

customData = {}
def startAggregator(id, cfg, port):
    global customData
    customData[id] = []
    app = Flask(__name__)
    print(f"{cfg.title} started")
    @app.route('/collect', methods=['POST'])
    def collect():
        global customData
        received = json.loads(request.json)
        data = received['content']
        for line in data:
            customData[id].append(int(line['Temperature']))
        return 'OK'

    def interval(id):
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
                    print(f'Data sent [{cfg.title}]')
                else:
                    print('Error')
                customData[id] = []

    customThread(target=interval, cfgId=id, name='aggregatorNested', args=(id)).start()
    # Trzeba potem zamknąć ten wątek w pliku wyżej
    app.run(port=port)

