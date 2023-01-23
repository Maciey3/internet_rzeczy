from flask import Flask, request
from custom.cfg import Aggregator
from custom.customThread import customThread
from devices.aggregator import startAggregator
import threading
import requests
import custom.logging
import colorama
colorama.init(autoreset=True)

ports = []

def getFreePort(ports, firstPort=8002, append=True):
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
    cfg = Aggregator.getCfgById(id)
    port = getFreePort(ports)
    cfg.insertPort(id, port)

    thread = customThread(target=startAggregator, cfgId=id, name='aggregator', args=(id, cfg, port))
    thread.start()
    print(f'{colorama.Fore.CYAN}Thread started [{cfg.title}]')

    return 'OK'

@app.route('/stop/<id>', methods=['POST'])
def stop(id):
    global ports
    cfg = Aggregator.getCfgById(id)
    cfg.deletePort(id)

    for thread in threading.enumerate():
        if thread.name == 'aggregator' and thread.cfgId == id:
            thread.kill()
            print(f'{colorama.Fore.YELLOW}Thread stopped [{cfg.title}]')
        elif thread.name == 'aggregatorNested' and thread.cfgId == id:
            thread.kill()
            print(f'{colorama.Fore.YELLOW}Nested thread stopped [{cfg.title}]')

    return 'OK'

@app.route('/status/<id>', methods=['GET'])
def status(id):
    flag = False

    for thread in threading.enumerate():
        if thread.name == 'aggregator' and thread.cfgId == id:
            flag = True

    if flag:
        return '1'
    else:
        return '0'

app.run(port=8001)
