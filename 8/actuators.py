from flask import Flask, request
import threading
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
    port = getFreePort(ports)
    cfg.insertPort(id, port)

    thread = customThread(target=startActuator, cfgId=id, name='actuator', args=(id, cfg, port))
    thread.start()
    print(f'{colorama.Fore.CYAN}Thread started [{cfg.title}]')
    return 'OK'

@app.route('/stop/<id>', methods=['POST'])
def stop(id):
    cfg = Actuator.getCfgById(id)
    cfg.deletePort(id)

    for thread in threading.enumerate():
        if thread.name == 'actuator' and thread.cfgId == id:
            thread.kill()
            print(f'{colorama.Fore.YELLOW}Thread stopped [{cfg.title}]')
        elif thread.name == 'generatorNested' and thread.cfgId == id:
            thread.kill()
            print(f'{colorama.Fore.YELLOW}Nested thread stopped [{cfg.title}]')

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