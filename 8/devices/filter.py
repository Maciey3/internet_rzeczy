from flask import Flask, request
from datetime import datetime
import json
import threading
import colorama
colorama.init(autoreset=True)

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
                cfg.addElementToHistory(message['content'])
                print(f"{colorama.Fore.LIGHTGREEN_EX}({message['date']}) Data sent [{cfg.title}]")
            else:
                print(f"{colorama.Fore.LIGHTRED_EX}({message['date']}) Error")
        else:
            print(f"{colorama.Fore.LIGHTRED_EX}({datetime.now().strftime('%d.%m.%Y %H:%M:%S')}) Message didnt pass requirements of filter [{cfg.title}]")

        return 'OK'

    @app.route('/history', methods=['GET'])
    def sendHistory():
        return json.dumps(cfg.history)

    app.run(port=port)

