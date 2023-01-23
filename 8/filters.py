from flask import Flask, request
from custom.cfg import Filter
from custom.customThread import customThread
from devices.filter import startFilter
import threading
import requests
import custom.logging
import colorama
colorama.init(autoreset=True)


ports = []

def getFreePort(ports, firstPort=9002, append=True):
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

    cfg = Filter.getCfgById(id)
    port = getFreePort(ports)
    cfg.insertPort(id, port)
    thread = customThread(target=startFilter, cfgId=id, name='filter', args=(id, cfg, port))
    thread.start()
    print(f'{colorama.Fore.CYAN}Thread started [{cfg.title}]')

    return 'OK'

@app.route('/stop/<id>', methods=['POST'])
def stop(id):
    cfg = Filter.getCfgById(id)
    cfg.deletePort(id)

    for thread in threading.enumerate():
        if thread.name == 'filter' and thread.cfgId == id:
            thread.kill()
            print(f'{colorama.Fore.YELLOW}Thread stopped [{cfg.title}]')

    return 'OK'

@app.route('/status/<id>', methods=['GET'])
def status(id):
    flag = False

    for thread in threading.enumerate():
        if thread.name == 'filter' and thread.cfgId == id:
            flag = True

    if flag:
        return '1'
    else:
        return '0'

app.run(port=9001)
# 121 C6