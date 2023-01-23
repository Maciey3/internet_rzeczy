from flask import Flask, request
import threading

from custom.cfg import Generator
from custom.parse import parse
from custom.customThread import customThread
from devices.generator import publish

app = Flask(__name__)

@app.route('/threads')
def threads():
    for thread in threading.enumerate():
        print(thread)
        if thread.name == 'generator':
            print(thread.killed)
    return 'OK'

@app.route('/start/<id>', methods=['POST'])
def start(id):
    cfg = Generator.getCfgById(id)

    thread = customThread(target=publish, cfgId=id, name='generator', args=(id, cfg))
    thread.start()
    print(f'Thread started [{cfg.title}]')
    return 'OK'

@app.route('/stop/<id>', methods=['POST'])
def stop(id):
    for thread in threading.enumerate():
        if thread.name == 'generator' and thread.cfgId == id:
            thread.kill()
            cfg = Generator.getCfgById(thread.cfgId)
            print(f'Thread stopped [{cfg.title}]')

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

app.run(port=8000)