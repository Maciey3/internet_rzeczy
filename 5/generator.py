from flask import Flask, request
import threading

from custom.cfg import Configuration
from custom.parse import parse
from custom.customThread import customThread
from device import publish

app = Flask(__name__)

@app.route('/start/<id>', methods=['POST'])
def start(id):
    cfg = Configuration(parse(True))
    cfg.getCfgById(id)

    thread = customThread(target=publish, cfgId=id, name='generator', args=(id, cfg))
    thread.start()

    return 'OK'

@app.route('/stop/<id>', methods=['POST'])
def stop(id):
    for thread in threading.enumerate():
        if thread.name == 'generator' and thread.cfgId == id:
            thread.kill()
            cfg = Configuration(parse(True))
            cfg.getCfgById(thread.cfgId)
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

app.run(debug=True, port=8000)