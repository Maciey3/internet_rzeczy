from flask import Flask, request
import threading
from statistics import mean
import json

from custom.cfg import Aggregator
from custom.parse import parse
from custom.customThread import customThread

import requests
from time import sleep

customData = {}
def startAggregator(id, cfg, port):
    global customData
    customData[id] = []
    app = Flask(__name__)
    @app.route('/collect', methods=['POST'])
    def collect():
        global customData
        recieved = json.loads(request.json)
        for line in recieved:
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
                if requests.post(cfg.address, data={'customData': result}, timeout=10):
                    print(f'Data sent [{cfg.title}]')
                else:
                    print('Error')
                customData[id] = []

    customThread(target=interval, cfgId=id, name='aggregatorNested', args=(id)).start()
    # Trzeba potem zamknąć ten wątek w pliku wyżej
    app.run(port=port)

