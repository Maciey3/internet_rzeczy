from flask import Flask, request
import threading
import json
from datetime import datetime

from custom.cfg import Aggregator
from custom.parse import parse
from custom.customThread import customThread

import requests
from time import sleep

def startFilter(id, cfg, port):
    app = Flask(__name__)
    @app.route('/receive', methods=['POST'])
    def receive():
        receive = json.loads(request.json)
        date = receive['date']
        content = receive['content']

        if not int(date[-1]) % 2:
            message = {
                'content': content,
                'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                'from': cfg.title
            }

            if requests.post(cfg.address, json=json.dumps(message), timeout=10):
                print(f'Data sent [{cfg.title}]')
            else:
                print(f'Error [{cfg.title}]')
        else:
            print(f'Message didnt pass requirements of filter [{cfg.title}]')

        return 'OK'
    print(port)
    app.run(port=port)

