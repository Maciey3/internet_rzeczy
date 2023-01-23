import threading
import requests

from custom.cfg import Generator, Aggregator
from custom.parse import parse
from custom.customThread import customThread

from flask import Flask, request, render_template, url_for, redirect, Blueprint


app = Flask(__name__)


@app.route('/')
def index():
    generators = Generator.getDatabase()
    agregators = Aggregator.getDatabase()

    return render_template('index.html', generators=generators, agregators=agregators)

# GENERATORS
@app.route('/generator/show/<id>')
def genShow(id):
    # cfg = Generator(parse(True))
    cfg = Generator.getCfgById(id)
    print(cfg)
    return render_template('generator/show.html', cfg=cfg, id=id)

@app.route('/generator/activate/<id>', methods=['GET'])
def genActivate(id):
    cfg = Generator.getCfgById(id)
    cfg.update(id, updateStatus=True)

    print(cfg)
    if cfg.status:
        requests.post(f'http://127.0.0.1:8000/start/{id}')
    else:
        requests.post(f'http://127.0.0.1:8000/stop/{id}')

    return redirect(url_for('index'))

@app.route('/generator/receive', methods=['POST'])
def genReceive():
    print('Data received')
    return 'Data received'

@app.route('/generator/delete', methods=['POST'])
def genDelete():
    id = request.form['id']
    cfg = Generator.getCfgById(id)
    cfg.delete(id)

    return redirect(url_for('index'))

@app.route('/generator/register')
def genRegister():
    return render_template('generator/register.html')

@app.route('/generator/edit/<id>')
def genEdit(id):
    cfg = Generator.getCfgById(id)

    datasets = [
        'temperatures.csv',
        'beach-water-quality-automated-sensors-1.csv',
        'Dollar-billionaires-per-million-people.csv',
        'earnings.csv',
        'surnames_en.csv',
        'zip-code-breakdowns-1.csv'
    ]

    return render_template('generator/edit.html', cfg=cfg.__dict__, datasets=datasets, id=id)

@app.route('/generator/update/', methods=['POST'])
def genUpdate():
    id = request.form['id']
    args = {
        'request': request.form['request'],
        'title': request.form['title'],
        'address': request.form['address'],
        'send_frequency': request.form['send_frequency'],
        'MQTT_topic': request.form['MQTT_topic'],
        'dataset': request.form['dataset']
    }


    cfg = Generator.getCfgById(id)

    if cfg.status:
        requests.post(f'http://127.0.0.1:8000/stop/{id}')

    cfg.update(id, updateArgs=args)

    if cfg.status:
        requests.post(f'http://127.0.0.1:8000/start/{id}')

    return redirect(url_for('index'))

@app.route('/generator/addObject', methods=["POST"])
def genAddObject():
    args = {
        'request': request.form['request'],
        'title': request.form['title'],
        'address': request.form['address'],
        'send_frequency': request.form['send_frequency'],
        'MQTT_topic': request.form['MQTT_topic'],
        'dataset': request.form['dataset']
    }

    Generator.save(args)

    return redirect(url_for('index'))

@app.route('/addAggr', methods=["GET"])
def addAggr():
    args = {
        'title': 'Aggregator1',
        'address': 'test'
    }

    cfg = Aggregator(args=args)
    print(cfg)
    cfg.save()

    # return redirect(url_for('index'))
    return 'OK'
# AGGREGATORS
@app.route('/aggregator/addObject', methods=["POST"])
def aggrCreate():
    args = {
        'title': request.form['title'],
        'address': request.form['address'],
        'send_frequency': request.form['send_frequency'],
        'destination_form': request.form['destination_form']
    }
    Aggregator.save(args)
    return redirect(url_for('index'))

@app.route('/aggregator/show/<id>')
def aggrShow(id):
    cfg = Aggregator.getCfgById(id)
    return render_template('aggregator/show.html', cfg=cfg, id=id)

@app.route('/aggregator/update/', methods=['POST'])
def aggrUpdate():
    id = request.form['id']
    args = {
        'title': request.form['title'],
        'address': request.form['address'],
        'send_frequency': request.form['send_frequency'],
        'destination_form': request.form['destination_form']
    }
    cfg = Aggregator.getCfgById(id)

    if cfg.status:
        requests.post(f'http://127.0.0.1:8001/stop/{id}')
    cfg.update(id, updateArgs=args)
    if cfg.status:
        requests.post(f'http://127.0.0.1:8001/start/{id}')
    return redirect(url_for('index'))

@app.route('/aggregator/delete', methods=['POST'])
def aggrDelete():
    id = request.form['id']
    cfg = Aggregator.getCfgById(id)
    cfg.delete(id)
    return redirect(url_for('index'))

@app.route('/aggregator/register')
def aggrRegister():
    return render_template('aggregator/register.html')

@app.route('/aggregator/edit/<id>')
def aggrEdit(id):
    cfg = Aggregator.getCfgById(id)
    return render_template('aggregator/edit.html', cfg=cfg.__dict__, id=id)

@app.route('/aggregator/activate/<id>', methods=['GET'])
def aggrActivate(id):
    cfg = Aggregator.getCfgById(id)
    cfg.update(id, updateStatus=True)
    # print(cfg)
    if cfg.status:
        requests.post(f'http://127.0.0.1:8001/start/{id}')
    else:
        requests.post(f'http://127.0.0.1:8001/stop/{id}')

    return redirect(url_for('index'))

@app.route('/aggregator/receive', methods=['POST'])
def aggrReceive():
    print('Data received')
    print(request.form['customData'])
    return 'Data received'

@app.route('/test')
def shutdown():
    cfg = Aggregator.getCfgById(1)
    print(cfg.getLastPort())

    return 'OK'

app.run(debug=True)