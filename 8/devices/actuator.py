from flask import Flask, request
from datetime import datetime
import json
import threading
import colorama
colorama.init(autoreset=True)

from custom.cfg import Actuator
from custom.customThread import customThread

import requests
from time import sleep

status = {}
def startActuator(id, cfg, port):
    app = Flask(__name__)

    @app.route('/status/<changedStatus>', methods=['GET'])
    def changeStatus(changedStatus):
        global status
        # if request.json:
        #     message = json.loads(request.json)
        print(f"{colorama.Fore.LIGHTGREEN_EX}Data received")
        if port not in status:
            status[port] = 1
        else:
            if status[port] == 1:
                status[port] = 0
            else:
                status[port] = 1

        print(status)
        return 'OK'

    @app.route('/history', methods=['GET'])
    def sendHistory():
        return json.dumps(cfg.history)

    def interval(id, cfg, port):
        global status
        starting = 20
        temp = starting
        while True:
            global status
            print(temp)
            cfg.addElementToHistory(data=temp, seconds=True)
            if temp < starting:
                return True
            sleep(1)
            if status[port]:
                if temp < int(cfg.temp_target):
                    temp += 2
                else:
                    temp -= 1
            else:
                temp -= 1

    changeStatus(1)
    customThread(target=interval, cfgId=id, name='actuatorNested', args=(id, cfg, port)).start()
    print(f'{colorama.Fore.CYAN}Nested thread started [{cfg.title}]')
    app.run(port=port)


