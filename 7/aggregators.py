from flask import Flask, request
import threading

from custom.cfg import Aggregator
from custom.parse import parse
from custom.customThread import customThread
from devices.aggregator import startAggregator
import requests
import socket
import custom.logging

ports = []

def getFreePort(ports, firstPort=8002, append=False):
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

@app.route('/threads')
def threads():
    for thread in threading.enumerate():
        print(thread)
    return 'OK'

@app.route('/start/<id>', methods=['POST'])
def start(id):
    global ports

    cfg = Aggregator.getCfgById(id)
    port = getFreePort(ports, append=True)
    cfg.insertPort(id, port)

    thread = customThread(target=startAggregator, cfgId=id, name='aggregator', args=(id, cfg, port))
    thread.start()
    print(f'Thread started [{cfg.title}]')

    return 'OK'

@app.route('/stop/<id>', methods=['POST'])
def stop(id):
    global ports
    cfg = Aggregator.getCfgById(id)
    port = cfg.port
    cfg.deletePort(id)

    for thread in threading.enumerate():
        if thread.name == 'aggregator' and thread.cfgId == id:
            requests.post(f'http://127.0.0.1:{port}/stop', timeout=10)
            thread.kill()

            print(f'Thread stopped [{cfg.title}]')
        elif thread.name == 'aggregatorNested' and thread.cfgId == id:
            thread.kill()
            cfg = Aggregator.getCfgById(thread.cfgId)
            print(f'Nested thread stopped [{cfg.title}]')

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
