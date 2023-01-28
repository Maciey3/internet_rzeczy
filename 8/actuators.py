from flask import Flask, request
import threading
from datetime import datetime
import requests
import json
import custom.logging
from custom.cfg import Actuator
from custom.customThread import customThread
from devices.actuator import startActuator
import colorama
colorama.init(autoreset=True)

ports = []

def getFreePort(ports, firstPort=6002, append=True):
    if ports:
        result = ports[-1]
    else:
        result = firstPort

    if append:
        if len(ports):
            result = ports[-1] + 1
            ports.append(result)
        else:
            ports.append(firstPort)
    return result


app = Flask(__name__)

@app.route('/start/<id>', methods=['POST'])
def start(id):
    global ports
    cfg = Actuator.getCfgById(id)
    if not cfg.port:
        port = getFreePort(ports)
        cfg.insertPort(id, port)

        thread = customThread(target=startActuator, cfgId=id, name='actuator', args=(id, cfg, port))
        thread.start()
        print(f'{colorama.Fore.CYAN}Thread started [{cfg.title}]')
        # message = {
        #     'status': 1,
        #     'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        #     'from': 'main'
        # }
        # if requests.get(f'http://127.0.0.1:{cfg.port}/status/1', json=json.dumps(message), timeout=10):
        #     # print(f"{colorama.Fore.LIGHTGREEN_EX}({message['date']}) Data sent [{cfg.title}]")
        #     pass
        # else:
        #     print(f"{colorama.Fore.LIGHTRED_EX}({message['date']}) Error")
    else:
        message = {
            'status': 1,
            'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'from': 'main'
        }
        if requests.get(f'http://127.0.0.1:{cfg.port}/status/1', json=json.dumps(message), timeout=10):
            # print(f"{colorama.Fore.LIGHTGREEN_EX}({message['date']}) Data sent [{cfg.title}]")
            pass
        else:
            print(f"{colorama.Fore.LIGHTRED_EX}({message['date']}) Error")
    return 'OK'

@app.route('/stop/<id>', methods=['POST'])
def stop(id):
    cfg = Actuator.getCfgById(id)
    message = {
        'status': 0,
        'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        'from': 'main'
    }
    if requests.get(f'http://127.0.0.1:{cfg.port}/status/0', json=json.dumps(message), timeout=10):
        # print(f"{colorama.Fore.LIGHTGREEN_EX}({message['date']}) Data sent [{cfg.title}]")
        pass
    else:
        print(f"{colorama.Fore.LIGHTRED_EX}({message['date']}) Error")

    # cfg = Actuator.getCfgById(id)
    # cfg.deletePort(id)
    #
    # for thread in threading.enumerate():
    #     if thread.name == 'actuator' and thread.cfgId == id:
    #         thread.kill()
    #         print(f'{colorama.Fore.YELLOW}Thread stopped [{cfg.title}]')
    #     elif thread.name == 'generatorNested' and thread.cfgId == id:
    #         thread.kill()
    #         print(f'{colorama.Fore.YELLOW}Nested thread stopped [{cfg.title}]')

    return 'OK'

@app.route('/status/<id>', methods=['GET'])
def status(id):
    flag = False

    for thread in threading.enumerate():
        if thread.name == 'generator' and thread.cfgId == id:
            flag = True

    if flag:
        return '1'
    else:
        return '0'

app.run(port=6001)